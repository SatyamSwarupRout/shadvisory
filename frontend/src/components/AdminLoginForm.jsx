import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Leaf, ArrowLeft, Settings } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export function AdminLoginForm({ onBack }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login, switchRole } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const success = await login(email, password);
      if (success) {
        switchRole('admin'); // ✅ explicitly set role as admin
      } else {
        setError('Invalid email or password');
      }
    } catch (err) {
      console.error(err);
      setError('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setEmail('admin@example.com');
    setPassword('password');

    // Auto login in demo mode
    setIsLoading(true);
    try {
      const success = await login('admin@example.com', 'password');
      if (success) {
        switchRole('admin');
      } else {
        setError('Demo login failed');
      }
    } catch (err) {
      console.error(err);
      setError('Demo login error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center space-x-2">
            <Leaf className="h-8 w-8 text-green-600" />
            <h1 className="text-2xl font-bold">Soil Health Advisory</h1>
          </div>
          <p className="text-gray-600">Better care for your farm's soil health</p>
        </div>

        {/* Admin Login Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" onClick={onBack}>
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div className="flex items-center space-x-2">
                <Settings className="h-5 w-5 text-purple-600" />
                <CardTitle>Admin Login</CardTitle>
              </div>
            </div>
            <CardDescription>
              Enter your admin credentials to access the system
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="admin@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              {/* Password */}
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              
              {/* Error */}
              {error && <div className="text-red-600 text-sm">{error}</div>}

              {/* Submit */}
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Demo Account */}
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
              disabled={isLoading}
            >
              <Settings className="h-4 w-4 mr-2" />
              Use Demo Admin Account
            </Button>
            <div className="text-xs text-gray-500 mt-2">
              Email: <span className="font-mono">admin@example.com</span> | 
              Password: <span className="font-mono">password</span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
