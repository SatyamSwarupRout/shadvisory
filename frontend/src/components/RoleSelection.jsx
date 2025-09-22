import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Leaf, User, Shield, Settings } from 'lucide-react';

export function RoleSelection({ onRoleSelect }) {
  const roles = [
    {
      id: 'farmer',
      title: 'Farmer',
      description: 'View land parcels, test results, and soil health advisory',
      icon: User,
      color: 'bg-green-100 text-green-800 hover:bg-green-200',
      bgGradient: 'from-green-500 to-green-600'
    },
    {
      id: 'coordinator',
      title: 'Coordinator',
      description: 'Manage farmers, land parcels, and soil test results',
      icon: Shield,
      color: 'bg-blue-100 text-blue-800 hover:bg-blue-200',
      bgGradient: 'from-blue-500 to-blue-600'
    },
    {
      id: 'admin',
      title: 'Admin',
      description: 'Bulk upload test results, manage users, and view analytics',
      icon: Settings,
      color: 'bg-purple-100 text-purple-800 hover:bg-purple-200',
      bgGradient: 'from-purple-500 to-purple-600'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center space-x-2">
            <Leaf className="h-8 w-8 text-green-600" />
            <h1 className="text-2xl font-bold">Soil Health Advisory</h1>
          </div>
          <p className="text-gray-600">Better care for your farm's soil health</p>
        </div>

        <Card>
          <CardHeader className="text-center">
            <CardTitle>Select Your Role</CardTitle>
            <CardDescription>
              Choose how you want to access the application
            </CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {roles.map(({ id, title, description, icon: Icon, color, bgGradient }) => (
              <Button
                key={id}
                variant="outline"
                className="h-auto p-6 flex flex-col items-center space-y-3 hover:shadow-md transition-all"
                onClick={() => onRoleSelect(id)}
              >
                <div className={`p-3 rounded-full bg-gradient-to-r ${bgGradient}`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="text-center">
                  <h3 className="font-semibold">{title}</h3>
                </div>
              </Button>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}