import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Leaf, ArrowLeft, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useDemoAuth } from '../hooks/useDemoAuth';

export function FarmerLoginForm({ onBack }) {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');

  const { switchRole } = useAuth();
  const demoAuth = useDemoAuth();

  const {
    isLoading,
    error,
    sendOTP,
    verifyOTP,
    clearError,
    cleanup,
    showOtp,
  } = demoAuth;

  const handleSendOtp = async (e) => {
    e.preventDefault();
    clearError();

    if (phoneNumber.length < 10) return;

    await sendOTP(phoneNumber);
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    clearError();

    if (otp.length !== 6) return;

    const success = await verifyOTP(otp);
    if (success) {
      // For demo mode, directly log in
      switchRole('farmer');
    }
  };

  const handleDemoLogin = async () => {
    setPhoneNumber('+91 9876543210');
    await demoAuth.sendOTP('+91 9876543210');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center space-x-2">
            <Leaf className="h-8 w-8 text-green-600" />
            <h1 className="text-2xl font-bold">Soil Health Advisory</h1>
          </div>
          <p className="text-gray-600">Better care for your farm's soil health</p>
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" onClick={onBack}>
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-green-600" />
                <CardTitle>Farmer Login</CardTitle>
              </div>
            </div>
            <CardDescription>
              {showOtp ? 'Enter the OTP sent to your phone' : 'Enter your phone number to receive OTP'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!showOtp ? (
              <form onSubmit={handleSendOtp} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+91 9876543210"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    required
                  />
                </div>

                {error && (
                  <div className="text-red-600 text-sm">{error}</div>
                )}

                <Button
                  type="submit"
                  className="w-full"
                  disabled={isLoading || phoneNumber.length < 10}
                >
                  {isLoading ? 'Sending OTP...' : 'Send OTP'}
                </Button>
              </form>
            ) : (
              <form onSubmit={handleVerifyOtp} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="otp">Enter OTP</Label>
                  <Input
                    id="otp"
                    type="text"
                    placeholder="123456"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    maxLength={6}
                    required
                  />
                  <p className="text-sm text-gray-500">
                    OTP sent to {phoneNumber}
                  </p>
                </div>

                {error && (
                  <div className="text-red-600 text-sm">{error}</div>
                )}

                <div className="space-y-2">
                  <Button
                    type="submit"
                    className="w-full"
                    disabled={isLoading || otp.length !== 6}
                  >
                    {isLoading ? 'Verifying...' : 'Verify OTP'}
                  </Button>

                  <Button
                    type="button"
                    variant="outline"
                    className="w-full"
                    onClick={() => {
                      cleanup();
                      setOtp('');
                    }}
                  >
                    Change Phone Number
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Demo Account</CardTitle>
            <CardDescription>
              Use demo credentials for testing
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={handleDemoLogin}
            >
              <User className="h-4 w-4 mr-2" />
              Use Demo Farmer Account
            </Button>
            <div className="text-xs text-gray-500 mt-2">
              Phone: +91 9876543210 | OTP: 123456
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
