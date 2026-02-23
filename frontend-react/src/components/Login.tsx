import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../context/AuthContext';
import { GraduationCap } from 'lucide-react';

const Login: React.FC = () => {
  const { login } = useAuth();
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  const handleSuccess = async (response: any) => {
    if (response.credential) {
      try {
        setLoading(true);
        setError(null);
        console.log('Login: Starting Google authentication...');
        console.log('Login: Credential length:', response.credential.length);
        console.log('Login: API Base URL:', (window as any).location.origin);
        await login(response.credential);
        console.log('Login: Authentication successful!');
      } catch (err: any) {
        console.error('Login error:', err);
        const errorMsg = err?.response?.data?.detail || err?.message || 'Login failed. Please try again.';
        setError(`Authentication failed: ${errorMsg}`);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleError = () => {
    console.error('Google Login Failed');
    setError('Google authentication failed. Please try again.');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background p-4">
      <div className="w-full max-w-md bg-secondary/10 border border-border/50 rounded-3xl p-8 shadow-2xl backdrop-blur-sm flex flex-col items-center text-center">
        <div className="w-16 h-16 bg-primary/20 rounded-2xl flex items-center justify-center mb-6">
          <GraduationCap className="w-10 h-10 text-primary" />
        </div>
        
        <h1 className="text-3xl font-bold mb-2 text-foreground">MathPilot</h1>
        <p className="text-muted-foreground mb-8">
          Your personal JEE Math Tutor. Log in to save your sessions and track your progress.
        </p>

        {error && (
          <div className="w-full mb-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-500 text-sm">
            {error}
          </div>
        )}

        <div className="w-full flex justify-center">
          {loading ? (
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
          ) : (
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={handleError}
              useOneTap
              theme="filled_black"
              shape="pill"
            />
          )}
        </div>

        <p className="mt-8 text-xs text-muted-foreground">
          By logging in, you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
};

export default Login;
