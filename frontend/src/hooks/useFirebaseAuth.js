import { useState } from 'react';
import { 
  signInWithPhoneNumber, 
  RecaptchaVerifier, 
  PhoneAuthProvider,
  signInWithCredential
} from 'firebase/auth';
import { auth } from '../config/firebase';

export function useFirebaseAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recaptchaVerifier, setRecaptchaVerifier] = useState(null);
  const [confirmationResult, setConfirmationResult] = useState(null);

  const initializeRecaptcha = (containerId) => {
    if (recaptchaVerifier) {
      recaptchaVerifier.clear();
    }

    const verifier = new RecaptchaVerifier(auth, containerId, {
      size: 'invisible',
      callback: () => {
        // reCAPTCHA solved, allow signInWithPhoneNumber
        console.log('reCAPTCHA solved');
      },
      'expired-callback': () => {
        setError('reCAPTCHA expired. Please try again.');
      }
    });

    setRecaptchaVerifier(verifier);
    return verifier;
  };

  const sendOTP = async (phoneNumber, containerId) => {
    setIsLoading(true);
    setError(null);

    try {
      // Format phone number to include country code if not present
      const formattedPhone = phoneNumber.startsWith('+') ? phoneNumber : `+91${phoneNumber.replace(/\D/g, '')}`;
      
      const verifier = initializeRecaptcha(containerId);
      const confirmationResult = await signInWithPhoneNumber(auth, formattedPhone, verifier);
      
      setConfirmationResult(confirmationResult);
      setIsLoading(false);
      return true;
    } catch (error) {
      console.error('Error sending OTP:', error);
      setError(error.message || 'Failed to send OTP. Please try again.');
      setIsLoading(false);
      return false;
    }
  };

  const verifyOTP = async (otp) => {
    if (!confirmationResult) {
      setError('No OTP request found. Please request OTP first.');
      return false;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await confirmationResult.confirm(otp);
      console.log('Phone verification successful:', result.user);
      setIsLoading(false);
      return true;
    } catch (error) {
      console.error('Error verifying OTP:', error);
      setError('Invalid OTP. Please check and try again.');
      setIsLoading(false);
      return false;
    }
  };

  const clearError = () => setError(null);

  const cleanup = () => {
    if (recaptchaVerifier) {
      recaptchaVerifier.clear();
      setRecaptchaVerifier(null);
    }
    setConfirmationResult(null);
    setError(null);
  };

  return {
    isLoading,
    error,
    sendOTP,
    verifyOTP,
    clearError,
    cleanup,
    hasConfirmationResult: !!confirmationResult
  };
}