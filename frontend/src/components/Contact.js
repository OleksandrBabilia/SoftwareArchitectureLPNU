import React from 'react';
import { Link } from 'react-router-dom'; // Import Link to redirect users to home
import Navbar from './Navbar'; // Import the Navbar component
import './Contact.css'; // Import the styled Contact page

const Contact = () => {
    return (
        <div>
            {/* Navbar Component */}
            <Navbar />

            <div className="contact-container">
                <h1>Contact Us</h1>
                <p className="contact-description">
                    Feel free to reach out to us! Whether you have a question, suggestion, or just want to get in touch, we are happy to help.
                </p>

                <div className="contact-details">
                    <p><strong>Phone Number:</strong> +1 (123) 456-7890</p>
                    <p><strong>Telegram:</strong> @ourTelegramHandle</p>
                    <p><strong>Email:</strong> contact@ourlibrary.com</p>
                </div>

                {/* Return to Home Button */}
                <Link to="/" className="home-btn">Return to Home</Link>
            </div>
        </div>
    );
};

export default Contact;
