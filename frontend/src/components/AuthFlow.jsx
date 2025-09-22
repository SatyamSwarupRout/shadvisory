import React, { useState } from 'react';
import { RoleSelection } from './RoleSelection';
import { FarmerLoginForm } from './FarmerLoginForm';
import { CoordinatorLoginForm } from './CoordinatorLoginForm';
import { AdminLoginForm } from './AdminLoginForm';

export function AuthFlow() {
  const [currentStep, setCurrentStep] = useState('role-selection');

  const handleRoleSelect = (role) => {
    switch (role) {
      case 'farmer':
        setCurrentStep('farmer-login');
        break;
      case 'coordinator':
        setCurrentStep('coordinator-login');
        break;
      case 'admin':
        setCurrentStep('admin-login');
        break;
    }
  };

  const handleBack = () => {
    setCurrentStep('role-selection');
  };

  switch (currentStep) {
    case 'farmer-login':
      return <FarmerLoginForm onBack={handleBack} />;
    case 'coordinator-login':
      return <CoordinatorLoginForm onBack={handleBack} />;
    case 'admin-login':
      return <AdminLoginForm onBack={handleBack} />;
    default:
      return <RoleSelection onRoleSelect={handleRoleSelect} />;
  }
}