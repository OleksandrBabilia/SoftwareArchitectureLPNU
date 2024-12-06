import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import './StripeCheckout.css'; // Add custom CSS for styling

const stripePromise = loadStripe('pk_test_51QLYRgFovu7WKbeEPK2MR1ggwY9R7vv3F6iSQyHrx3iCFSO36TRQlphDbqpQmKhU8FCmsTmbnlAKV50KJC7hp0At00hA9cNfTP'); // Replace with your Stripe public key

const StripeCheckout = () => {
    const [loading, setLoading] = useState(false);

    const handleCheckout = async () => {
        setLoading(true);
        const jwtToken = localStorage.getItem('token');
        try {
            // Request a session from your backend to create the checkout session
            const response = await fetch('http://localhost:5000/create-checkout-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${jwtToken}`  // Pass JWT in Authorization header
                },
            });
            const sessionId = await response.json();

            const stripe = await stripePromise;

            // Redirect to Stripe Checkout
            const result = await stripe.redirectToCheckout({ sessionId: sessionId.id });

            if (result.error) {
                alert(result.error.message);
            }
        } catch (error) {
            console.error('Error during checkout:', error);
            alert('An error occurred while processing your checkout.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="stripe-checkout-container">
            <div className="stripe-checkout-content">
                <h1>Lifetime Subscription</h1>
                <p className="benefits-description">
                    Unlock unlimited access to more books, priority in order processing, and support the growth of our book world.
                    With your lifetime subscription, you will enjoy:
                </p>
                <ul className="benefits-list">
                    <li>Access to a wider catalog of books</li>
                    <li>Priority processing for your orders</li>
                    <li>Support our community and the growth of the library world</li>
                </ul>
                <p className="price-info">
                    <strong>Only $20.00 for a lifetime subscription!</strong>
                </p>
                <div className="checkout-button-container">
                    <button
                        id="checkout-button"
                        onClick={handleCheckout}
                        disabled={loading}
                        className="checkout-button"
                    >
                        {loading ? 'Loading...' : 'Start Your Lifetime Subscription'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default StripeCheckout;
