import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(undefined);

// Mock users for demo
const mockUsers = [
  {
    id: '1',
    name: 'Ram Sharma',
    email: 'farmer@example.com',
    phone: '+91 9876543210',
    role: 'farmer',
    shahayakId: '2',
    createdAt: '2024-01-15T00:00:00Z'
  },
  {
    id: '2',
    name: 'Priya Patel',
    email: 'shahayak@example.com',
    phone: '+91 9876543211',
    role: 'shahayak',
    createdAt: '2024-01-10T00:00:00Z'
  },
  {
    id: '3',
    name: 'Dr. Amit Kumar',
    email: 'admin@example.com',
    phone: '+91 9876543212',
    role: 'admin',
    createdAt: '2024-01-01T00:00:00Z'
  }
];

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('soil_app_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  // Mock login with email/password
  const login = async (email, password) => {
    setIsLoading(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    const foundUser = mockUsers.find(u => u.email === email);
    if (foundUser && password === 'password') {
      setUser(foundUser);
      localStorage.setItem('soil_app_user', JSON.stringify(foundUser));
      setIsLoading(false);
      return true;
    }

    setIsLoading(false);
    return false;
  };

  // Mock login with phone number + role (used for farmer/shahayak)
  const loginWithPhone = async (phoneNumber, role) => {
    setIsLoading(true);

    try {
      let appUser = mockUsers.find(
        u => u.phone === phoneNumber && u.role === role
      );

      if (!appUser) {
        // Create new user if not found
        appUser = {
          id: Date.now().toString(),
          name: role === 'farmer' ? 'Farmer User' : 'Coordinator User',
          email: '',
          phone: phoneNumber,
          role,
          shahayakId: role === 'farmer' ? '2' : undefined,
          createdAt: new Date().toISOString()
        };
      }

      setUser(appUser);
      localStorage.setItem('soil_app_user', JSON.stringify(appUser));
      setIsLoading(false);
      return true;
    } catch (error) {
      console.error('Error in loginWithPhone:', error);
      setIsLoading(false);
      return false;
    }
  };

  const logout = async () => {
    setUser(null);
    localStorage.removeItem('soil_app_user');
  };

  const switchRole = (role) => {
    const newUser = mockUsers.find(u => u.role === role);
    if (newUser) {
      setUser(newUser);
      localStorage.setItem('soil_app_user', JSON.stringify(newUser));
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, loginWithPhone, logout, switchRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
