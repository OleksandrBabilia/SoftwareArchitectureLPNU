import os
import json
import pika
import stripe
import uuid  # Import uuid module
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
from werkzeug.exceptions import Unauthorized  # To raise unauthorized error

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for specific origin (localhost:3000)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Set Stripe API keys
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')

# RabbitMQ connection parameters
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
queue_name = os.getenv('RABBITMQ_QUEUE', 'stripe_payments')


# Connect to RabbitMQ
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return connection, channel


# Route to render the checkout page
@app.route('/')
def index():
    return render_template('checkout.html', stripe_public_key=stripe_public_key)


# Route to handle the creation of a Stripe payment intent (JWT protected)
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Retrieve the JWT token from request headers
        jwt_token = request.headers.get('Authorization')
        if not jwt_token:
            raise Unauthorized("JWT token is required.")

        # Extract the token from "Bearer <token>"
        if jwt_token.startswith("Bearer "):
            jwt_token = jwt_token[7:]
        else:
            raise Unauthorized("Invalid token format.")

        # Generate a unique UUID for the transaction
        transaction_uuid = str(uuid.uuid4())

        # Create a new checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Premium Subscription',
                        },
                        'unit_amount': 2000,  # Amount in cents ($20.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.host_url + 'success?uuid=' + transaction_uuid,  # Include UUID in success URL
            cancel_url=request.host_url + 'cancel?uuid=' + transaction_uuid,    # Include UUID in cancel URL
        )

        # Connect to RabbitMQ and send initial message with JWT token
        connection, channel = get_rabbitmq_channel()

        # Construct the payment message with 'success: false' and JWT token
        payment_message = {
            'status': 'false',  # Initial status before payment
            'payment_method': 'stripe',
            'transaction_id': transaction_uuid,  # Use the transaction UUID here
            'amount': 2000,  # Amount in cents ($20.00)
            'date': datetime.now().strftime('%Y-%m-%d'),
            'jwt_token': jwt_token  # Include the JWT token in the message
        }

        # Convert the message to a JSON string
        message_body = json.dumps(payment_message)

        # Send the message to RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        # Close the RabbitMQ connection
        connection.close()

        # Return the session ID to the client
        return jsonify({'id': checkout_session.id})

    except Exception as e:
        return str(e), 400


# Success route
@app.route('/success')
def success():
    try:
        # Retrieve the UUID from the URL
        transaction_uuid = request.args.get('uuid')

        # Connect to RabbitMQ
        connection, channel = get_rabbitmq_channel()

        # Construct the payment message with success status
        payment_message = {
            'status': 'success',
            'payment_method': 'stripe',
            'transaction_id': transaction_uuid,  # Use the transaction UUID here
            'amount': 2000,  # Amount in cents ($20.00)
            'date': datetime.now().strftime('%Y-%m-%d'),
        }

        # Convert the message to a JSON string
        message_body = json.dumps(payment_message)

        # Send the message to RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        connection.close()

        # Render the success page with the transaction UUID
        return render_template('success.html', transaction_uuid=transaction_uuid)

    except Exception as e:
        return f"Error sending message to RabbitMQ: {str(e)}", 500

# Cancel route
@app.route('/cancel')
def cancel():
    # Retrieve the UUID from the URL
    transaction_uuid = request.args.get('uuid')
    return f"Payment Cancelled for transaction {transaction_uuid}."


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
