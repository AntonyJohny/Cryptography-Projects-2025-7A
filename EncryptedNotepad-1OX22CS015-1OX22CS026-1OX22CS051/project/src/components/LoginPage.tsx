import React, { useState } from 'react';
import { User, Lock, BookDown as Doodle } from 'lucide-react';

interface LoginPageProps {
  onLogin: (username: string) => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Demo credentials
  const validCredentials = {
    username: 'cns',
    password: 'cns@123'
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Simulate loading
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (username === validCredentials.username && password === validCredentials.password) {
      onLogin(username);
    } else {
      setError('Invalid credentials! Try demo/password123');
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen scribble-bg flex items-center justify-center p-4">
      {/* Decorative Scribbles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <svg className="absolute top-10 left-10 w-32 h-32 text-pink-300 opacity-60 animate-wiggle" viewBox="0 0 100 100">
          <path d="M10,50 Q30,10 50,50 T90,50" stroke="currentColor" strokeWidth="3" fill="none" strokeDasharray="5,5" />
        </svg>
        <svg className="absolute top-20 right-20 w-24 h-24 text-blue-300 opacity-60" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="30" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="3,3" />
        </svg>
        <svg className="absolute bottom-20 left-20 w-28 h-28 text-yellow-300 opacity-60" viewBox="0 0 100 100">
          <path d="M20,20 L80,20 L80,80 L20,80 Z" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="4,4" />
        </svg>
      </div>

      <div className="w-full max-w-md">
        {/* Login Card */}
        <div className="paper-texture rounded-2xl shadow-2xl border-4 border-dashed border-purple-300 p-8 transform hover:scale-105 transition-transform duration-300">
          {/* Header with Scribble */}
          <div className="text-center mb-8">
            <div className="relative inline-block">
              <Doodle className="w-16 h-16 text-purple-600 mx-auto mb-4 animate-wiggle" />
              <svg className="absolute -top-2 -right-2 w-8 h-8 text-pink-400" viewBox="0 0 20 20">
                <path d="M2,10 Q10,2 18,10 Q10,18 2,10" stroke="currentColor" strokeWidth="2" fill="none" />
              </svg>
            </div>
            <h1 className="handwritten text-4xl font-bold text-gray-800 mb-2">
              Scribble Notes
            </h1>
            <p className="handwritten text-lg text-gray-600">
              Your creative encrypted notepad
            </p>
          </div>

          {/* Demo Credentials Box */}
          <div className="bg-yellow-50 border-2 border-dashed border-yellow-300 rounded-lg p-4 mb-6">
            <h3 className="handwritten text-lg font-semibold text-yellow-800 mb-2">Demo Credentials</h3>
            <div className="space-y-1 text-sm">
              <p className="handwritten text-yellow-700">
                <strong>Username:</strong> cns
              </p>
              <p className="handwritten text-yellow-700">
                <strong>Password:</strong> cns@123
              </p>
            </div>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-6">
            {error && (
              <div className="bg-red-50 border-2 border-dashed border-red-300 rounded-lg p-3">
                <p className="handwritten text-red-700 text-center">{error}</p>
              </div>
            )}

            <div>
              <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
                Username
              </label>
              <div className="relative">
                <User className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="handwritten w-full pl-10 pr-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition-all text-lg bg-white"
                  placeholder="Enter your username..."
                  required
                />
              </div>
            </div>

            <div>
              <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="handwritten w-full pl-10 pr-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:border-purple-400 focus:ring-2 focus:ring-purple-200 transition-all text-lg bg-white"
                  placeholder="Enter your password..."
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 px-6 rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 transition-all transform hover:scale-105 active:scale-95 shadow-lg handwritten text-lg font-semibold"
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Logging in...
                </div>
              ) : (
                'Login to Scribble Notes'
              )}
            </button>
          </form>

          {/* Decorative Footer */}
          <div className="mt-8 text-center">
            <svg className="w-full h-4 text-gray-300" viewBox="0 0 200 20">
              <path d="M10,10 Q50,5 100,10 T190,10" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="2,3" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}