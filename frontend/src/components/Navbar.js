import React from 'react';
import { Link } from 'react-router-dom'; // For navigation, if you're using react-router
import { FaHome, FaInfoCircle, FaEnvelope, FaCreditCard, FaSignInAlt, FaSignOutAlt } from 'react-icons/fa'; // Icons for beautification
import './NavBar.css'; // Adjust the path if necessary
const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark custom-navbar shadow-lg">
            <div className="container-fluid">
                <a className="navbar-brand fw-bold fs-2" href="#">
                    <span className="text-light">Online</span> <span className="text-warning">Library</span>
                </a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/">
                                <FaHome className="me-2" /> Home
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/about">
                                <FaInfoCircle className="me-2" /> About
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/contact">
                                <FaEnvelope className="me-2" /> Contact
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/login">
                                <FaSignInAlt className="me-2" /> Login
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/signup">
                                <FaSignOutAlt className="me-2" /> Sign Up
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link custom-link" to="/payment">
                                <FaCreditCard className="me-2" /> Premium                             </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
