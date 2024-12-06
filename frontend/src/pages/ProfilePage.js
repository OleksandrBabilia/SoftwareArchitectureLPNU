// src/pages/UserProfile.js

import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form } from 'react-bootstrap';
import axios from 'axios';

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Example: User token stored in localStorage or via context
    const token = localStorage.getItem('access_token');

    useEffect(() => {
        // Fetch user data when the component mounts
        const fetchUserData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/users/me/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setUser(response.data);
                setLoading(false);
            } catch (error) {
                setError('Error fetching user data');
                setLoading(false);
            }
        };

        if (token) {
            fetchUserData();
        } else {
            setLoading(false);
            setError('No authentication token found');
        }
    }, [token]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <Container>
            <Row className="mt-5">
                <Col md={8}>
                    <Card>
                        <Card.Body>
                            <Card.Title>User Profile</Card.Title>
                            <Form>
                                <Form.Group controlId="formUsername">
                                    <Form.Label>Username</Form.Label>
                                    <Form.Control type="text" placeholder="Enter username" value={user.username} readOnly />
                                </Form.Group>

                                <Form.Group controlId="formEmail">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control type="email" placeholder="Enter email" value={user.email} readOnly />
                                </Form.Group>

                                <Form.Group controlId="formFirstName">
                                    <Form.Label>First Name</Form.Label>
                                    <Form.Control type="text" placeholder="Enter first name" value={user.first_name} readOnly />
                                </Form.Group>

                                <Form.Group controlId="formLastName">
                                    <Form.Label>Last Name</Form.Label>
                                    <Form.Control type="text" placeholder="Enter last name" value={user.last_name} readOnly />
                                </Form.Group>

                                <Button variant="primary" type="submit" disabled>
                                    Edit Profile
                                </Button>
                            </Form>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default UserProfile;
