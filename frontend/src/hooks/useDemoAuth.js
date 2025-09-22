import { useState } from 'react';

export function useDemoAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showOtp, setShowOtp] = useState(false);

  const sendOTP = async (phoneNumber) => {
    setIsLoading(true);
    setError(null);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    if (phoneNumber.length >= 10) {
      setShowOtp(true);
      setIsLoading(false);
      return true;
    } else {
      setError('Please enter a valid phone number');
      setIsLoading(false);
      return false;
    }
  };

  const verifyOTP = async (otp) => {
    setIsLoading(true);
    setError(null);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (otp === '123456') {
      setIsLoading(false);
      return true;
    } else {
      setError('Invalid OTP. Please use 123456 for demo.');
      setIsLoading(false);
      return false;
    }
  };

  const clearError = () => setError(null);

  const cleanup = () => {
    setError(null);
    setShowOtp(false);
  };

  return {
    isLoading,
    error,
    showOtp,
    sendOTP,
    verifyOTP,
    clearError,
    cleanup,
    hasConfirmationResult: showOtp
  };
}