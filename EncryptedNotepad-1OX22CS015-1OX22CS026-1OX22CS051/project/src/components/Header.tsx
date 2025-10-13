import React from 'react';
import { FileText, List, LogOut, User } from 'lucide-react';

interface HeaderProps {
  currentPage: 'write' | 'notes';
  onPageChange: (page: 'write' | 'notes') => void;
  currentUser: string;
  onLogout: () => void;
}

export default function Header({ currentPage, onPageChange, currentUser, onLogout }: HeaderProps) {
  return (
    <header className="paper-texture shadow-lg border-b-4 border-dashed border-purple-300 mb-8">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <FileText className="w-10 h-10 text-purple-600 animate-wiggle" />
              <svg className="absolute -top-1 -right-1 w-6 h-6 text-pink-400" viewBox="0 0 20 20">
                <path d="M2,10 Q10,2 18,10" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="2,2" />
              </svg>
            </div>
            <h1 className="handwritten text-3xl font-bold text-gray-800 transform -rotate-1">
              Scribble Notes
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            {/* User Info */}
            <div className="flex items-center gap-2 bg-yellow-100 px-3 py-2 rounded-lg border-2 border-dashed border-yellow-300">
              <User className="w-4 h-4 text-yellow-700" />
              <span className="handwritten text-yellow-800 font-medium">{currentUser}</span>
            </div>

            {/* Navigation */}
            <nav className="flex gap-2">
              <button
                onClick={() => onPageChange('write')}
                className={`handwritten flex items-center gap-2 px-4 py-2 rounded-lg transition-all transform hover:scale-105 border-2 border-dashed ${
                  currentPage === 'write'
                    ? 'bg-blue-100 text-blue-700 border-blue-300 shadow-md'
                    : 'text-gray-600 hover:bg-pink-50 border-gray-300 hover:border-pink-300'
                }`}
              >
                <FileText className="w-4 h-4" />
                Write Note
              </button>
              
              <button
                onClick={() => onPageChange('notes')}
                className={`handwritten flex items-center gap-2 px-4 py-2 rounded-lg transition-all transform hover:scale-105 border-2 border-dashed ${
                  currentPage === 'notes'
                    ? 'bg-green-100 text-green-700 border-green-300 shadow-md'
                    : 'text-gray-600 hover:bg-pink-50 border-gray-300 hover:border-pink-300'
                }`}
              >
                <List className="w-4 h-4" />
                My Notes
              </button>
            </nav>

            {/* Logout Button */}
            <button
              onClick={onLogout}
              className="handwritten flex items-center gap-2 px-3 py-2 rounded-lg text-red-600 hover:bg-red-50 border-2 border-dashed border-red-300 hover:border-red-400 transition-all transform hover:scale-105"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}