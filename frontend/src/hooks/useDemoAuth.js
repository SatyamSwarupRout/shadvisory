import { useState } from "react";

export function useDemoAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showOtp, setShowOtp] = useState(false);

  const API_BASE = "http://localhost:8000";

  const sendOTP = async (phoneNumber) => {
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: phoneNumber }),
      });

      const data = await res.json();
      if (data.success) {
        setShowOtp(true);
        setIsLoading(false);
        return true;
      } else {
        setError(data.error || "Failed to send OTP");
        setIsLoading(false);
        return false;
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
      setIsLoading(false);
      return false;
    }
  };

  const verifyOTP = async (otp, phoneNumber) => {
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone: phoneNumber, code: otp }),
      });

      const data = await res.json();
      if (data.success) {
        setIsLoading(false);
        return true;
      } else {
        setError(data.error || "Invalid OTP");
        setIsLoading(false);
        return false;
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
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
    hasConfirmationResult: showOtp,
  };
}
