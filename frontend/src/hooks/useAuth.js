import { useState } from 'react';
import axios from 'axios';
import { saveTokens } from '../helpers/authHelper';

const useAuth = () => {
  const [error, setError] = useState(null);

  const handleSignup = async (username, password, email, first_name, last_name) => {
    try {
      const response = await axios.post('http://localhost:8000/api/v1/signup/', {
        username,
        password,
        email,
        first_name,
        last_name,
      });

      // Save tokens in localStorage
      saveTokens(response.data);

      console.log("User signed up and authenticated:", response.data);
      alert("Signup successful!");
    } catch (error) {
      console.error("Error signing up:", error);
      setError("Signup failed. Please try again.");
    }
  };

  return { handleSignup, error };
};

export default useAuth;
