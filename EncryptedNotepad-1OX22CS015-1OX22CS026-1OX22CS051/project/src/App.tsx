import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import Header from './components/Header';
import WritePage from './components/WritePage';
import NotesPage from './components/NotesPage';
import { EncryptedNote } from './types';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState('');
  const [currentPage, setCurrentPage] = useState<'write' | 'notes'>('write');
  const [selectedNote, setSelectedNote] = useState<EncryptedNote | undefined>();
  const [notification, setNotification] = useState('');

  const showNotification = (message: string) => {
    setNotification(message);
    setTimeout(() => setNotification(''), 3000);
  };

  const handleLogin = (username: string) => {
    setIsLoggedIn(true);
    setCurrentUser(username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentUser('');
    setCurrentPage('write');
  };

  const handleNoteSelect = (note: EncryptedNote) => {
    setSelectedNote(note);
  };

  const handlePageChange = (page: 'write' | 'notes') => {
    setCurrentPage(page);
    setSelectedNote(undefined);
  };

  const handleNoteSaved = () => {
    // Optionally switch to notes page after saving
    // setCurrentPage('notes');
  };

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen scribble-bg">
      <Header 
        currentPage={currentPage} 
        onPageChange={handlePageChange}
        currentUser={currentUser}
        onLogout={handleLogout}
      />
      
      {/* Notification */}
      {notification && (
        <div className="fixed top-4 right-4 bg-gradient-to-r from-green-400 to-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in handwritten text-lg border-2 border-dashed border-green-600">
          {notification}
        </div>
      )}

      <div className="px-4 pb-8">
        {currentPage === 'write' && (
          <WritePage 
            onNoteSaved={handleNoteSaved}
            showNotification={showNotification}
          />
        )}
        
        {currentPage === 'notes' && (
          <NotesPage
            onNoteSelect={handleNoteSelect}
            showNotification={showNotification}
          />
        )}
      </div>
    </div>
  );
}

export default App;