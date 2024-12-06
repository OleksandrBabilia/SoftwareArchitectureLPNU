import pika
import json
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Payment
from users.models import Profile


# RabbitMQ connection settings
rabbitmq_host = settings.RABBITMQ_HOST  # E.g., 'localhost'
queue_name = settings.RABBITMQ_QUEUE  # E.g., 'stripe_payments'
secret_key = settings.SECRET_KEY  # Secret key for Django (can also be used for JWT)

# Connect to RabbitMQ
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    return channel


# Decode JWT token to extract user information using Simple JWT
def get_user_from_jwt(jwt_token):
    try:
        # Decode the JWT token using Simple JWT's AccessToken class
        token = AccessToken(jwt_token)
        user_id = token['user_id']  # Assuming the user ID is stored in the 'user_id' claim
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        print(f"Error decoding JWT token: {str(e)}")
        return None


# Callback to handle incoming messages from RabbitMQ
def callback(ch, method, properties, body):
    str_body = body.decode('utf-8')

    message = json.loads(str_body.replace("'", '"'))

    print(f"Received message: {message}")

    # Process the message (e.g., save to the database)
    try:
        # Extract the JWT token from the message
        jwt_token = message.get('jwt_token')
        if not jwt_token:
            print("JWT token missing in message")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        # Get the user from the JWT token
        user = get_user_from_jwt(jwt_token)
        if not user:
            print("User not found based on the JWT token")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        # Create a payment with status=False (initial state)
        payment = Payment.objects.create(
            uuid=message['transaction_id'],
            success=False,
            payment_method=message['payment_method'],
            transaction_id=message['transaction_id'],
            amount=message['amount'],
            payment_date=message['date'],
            user=user  # Link the user
        )
        print(f"Payment created with status=False: {payment}")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def handle_success_message(ch, method, properties, body):
    str_body = body.decode('utf-8')
    message = json.loads(str_body.replace("'", '"'))

    print(f"Received success message: {message}")

    try:
        # Get the payment by UUID
        payment = Payment.objects.get(uuid=message['transaction_id'])
        user = payment.user

        # Update the payment to success=True
        payment.success = True
        payment.save()
        print(f"Payment updated to success=True: {payment}")

        # Check if the user has a related profile, if not, create one
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            print(f"Profile for user {user.username} created.")

        # Update the user's premium status
        profile.premium = True  # Set premium status to True
        profile.save()
        print(f"User {user.username} updated to premium.")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Payment.DoesNotExist:
        print(f"Payment with UUID {message['transaction_id']} not found.")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error updating payment: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


# Start consuming messages
def start_consuming():
    channel = connect_to_rabbitmq()

    # First consumer for initial payment creation (with status False)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    # Another consumer for success messages (to update payment status)
    channel.basic_consume(queue=queue_name, on_message_callback=handle_success_message, auto_ack=False)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
