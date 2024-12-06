import React from 'react';
import SignUpForm from '../components/SignUpForm';
import useAuth from '../hooks/useAuth';

const SignUpPage = () => {
  const { handleSignup, error } = useAuth();

  return (
    <div>
      <SignUpForm onSubmit={handleSignup} error={error} />
    </div>
  );
};

export default SignUpPage;
