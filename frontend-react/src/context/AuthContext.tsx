import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { api } from '../lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  picture: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credential: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('auth_user');
    
    if (savedToken && savedUser) {
      try {
        const decoded: any = jwtDecode(savedToken);
        const currentTime = Date.now() / 1000;
        
        if (decoded.exp > currentTime) {
          setToken(savedToken);
          setUser(JSON.parse(savedUser));
        } else {
          logout();
        }
      } catch (e) {
        logout();
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (credential: string) => {
    try {
      console.log('AuthContext: Calling backend auth...');
      const response = await api.authGoogle(credential);
      console.log('AuthContext: Backend responded:', {
        hasToken: !!response.access_token,
        hasUser: !!response.user,
        userId: response.user?.id
      });
      
      if (!response.access_token || !response.user) {
        throw new Error('Invalid response from server');
      }
      
      // Update state
      setToken(response.access_token);
      setUser(response.user);
      
      // Persist to localStorage
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('auth_user', JSON.stringify(response.user));
      
      console.log('AuthContext: Login complete, token saved');
    } catch (error: any) {
      console.error('AuthContext: Login failed:', error);
      // Clear any partial state
      setToken(null);
      setUser(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
