import React from 'react';
import { Link } from 'react-router-dom';  // Import Link to redirect users to home
import Navbar from './Navbar'; // Import the Navbar component
import './About.css'; // Import the styled About page


const About = () => {
    return (
        <div>
            {/* Navbar Component */}
            <Navbar />

            <div className="about-container">
                <h1>About Us</h1>
                <p>Welcome to our online library! We are passionate about books and aim to provide easy access to a vast collection for all book lovers. Our mission is to bring knowledge, entertainment, and education to everyone.</p>

                <h2>What We Offer</h2>
                <ul>
                    <li>A diverse catalog of books across multiple genres</li>
                    <li>Exclusive premium subscriptions with additional benefits</li>
                    <li>Fast approval for book requests and high-priority customer support</li>
                </ul>

                <h2>Our Vision</h2>
                <p>To create a world where everyone has access to the books they need and foster a culture of learning and growth.</p>

                {/* Return to Home Button */}
                <Link to="/" className="home-btn">Return to Home</Link>
            </div>
        </div>
    );
};

export default About;
