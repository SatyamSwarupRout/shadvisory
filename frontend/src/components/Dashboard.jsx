import React from "react";
import { Button } from "./ui/button";
import { LogOut, Leaf, User } from 'lucide-react';
import { useAuth } from "../contexts/AuthContext";


function Dashboard() {
      const { user, logout } = useAuth();

  return (
    <div>
      Dashboard
      <div>
        <Button
          variant="outline"
          size="sm"
          onClick={logout}
          className="flex items-center space-x-1"
        >
          <LogOut className="h-4 w-4" />
          <span>Sign Out</span>
        </Button>
      </div>
    </div>
  );
}

export default Dashboard;
