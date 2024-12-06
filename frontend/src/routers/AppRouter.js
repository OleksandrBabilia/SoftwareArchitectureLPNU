import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SignUpPage from '../pages/SignUpPage';
import BookPage from '../pages/BookPage';
import LoginPage from '../pages/LoginPage';
import PaymentPage from '../pages/PaymentPage';
import About from '../components/About'; // Import the About component
import Contact from '../components/Contact';
// Utility function to check if the user is authenticated
const isAuthenticated = () => {
    const token = localStorage.getItem('token'); // Retrieve token from localStorage
    if (!token) return false;

    try {
        const decodedToken = JSON.parse(atob(token.split('.')[1])); // Decode JWT token
        console.log(decodedToken);
        const currentTime = Date.now() / 1000; // Get current time in seconds
        if (decodedToken.exp < currentTime) {
            localStorage.removeItem('token'); // Remove expired token
            return false;
        }
        return true; // Token is valid
    } catch (error) {
        console.error('Invalid token', error);
        return false;
    }
};

// Protected Route Component
const ProtectedRoute = ({ element, ...rest }) => {
    return isAuthenticated() ? element : <Navigate to="/login" />;
};

const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path="/signup" element={<SignUpPage />} />
                <Route path="/" element={<BookPage />} />
                <Route path="/login" element={<LoginPage />} />

                {/* Protected Payment Route */}
                <Route path="/payment" element={<ProtectedRoute element={<PaymentPage />} />} />
                <Route path="/about" element={<About />} /> {/* Add the About route */}
                <Route path="/contact" element={<Contact />} />
            </Routes>
        </Router>
    );
};

export default AppRouter;
