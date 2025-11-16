import React, { useState, useEffect } from 'react';
import { FileText, Trash2, Calendar, Search, Unlock, Eye, EyeOff, Copy, Palette, Shield } from 'lucide-react';
import { EncryptedNote } from '../types';

interface NotesPageProps {
  onNoteSelect: (note: EncryptedNote) => void;
  showNotification: (message: string) => void;
}

export default function NotesPage({ onNoteSelect, showNotification }: NotesPageProps) {
  const [notes, setNotes] = useState<EncryptedNote[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNote, setSelectedNote] = useState<EncryptedNote | null>(null);
  const [decryptionKey, setDecryptionKey] = useState('');
  const [decryptedContent, setDecryptedContent] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [isDecrypting, setIsDecrypting] = useState(false);
  const [selectedColors, setSelectedColors] = useState<string[]>([]);

  const rainbowColors = [
    '#FF0000', '#FF4500', '#FF8C00', '#FFD700', '#ADFF2F', 
    '#00FF00', '#00CED1', '#0000FF', '#4169E1', '#8A2BE2',
    '#FF1493', '#FF69B4', '#FFC0CB', '#F0E68C', '#DDA0DD'
  ];

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = () => {
    const savedNotes = JSON.parse(localStorage.getItem('encryptedNotes') || '[]');
    setNotes(savedNotes.sort((a: EncryptedNote, b: EncryptedNote) => 
      new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    ));
  };

  const deleteNote = (noteId: string) => {
    const updatedNotes = notes.filter(note => note.id !== noteId);
    setNotes(updatedNotes);
    localStorage.setItem('encryptedNotes', JSON.stringify(updatedNotes));
    showNotification('Note deleted successfully');
  };

  const handleNoteClick = (note: EncryptedNote) => {
    setSelectedNote(note);
    setDecryptedContent('');
    setDecryptionKey('');
    setSelectedColors([]);
  };

  const handleColorSelect = (colorValue: string) => {
    if (selectedColors.includes(colorValue)) {
      setSelectedColors(selectedColors.filter(c => c !== colorValue));
    } else if (selectedColors.length < 3) {
      setSelectedColors([...selectedColors, colorValue]);
    }
  };

  const handleDecrypt = async () => {
    if (!decryptionKey.trim()) {
      showNotification('Please enter the decryption key');
      return;
    }
    if (selectedColors.length !== 3) {
      showNotification('Please select exactly 3 colors in the correct order');
      return;
    }
    if (!selectedNote) return;

    setIsDecrypting(true);
    try {
      const { generateKey, decryptText } = await import('../utils/crypto');
      const combinedKey = decryptionKey + selectedColors.join('');
      const key = await generateKey(combinedKey);
      const dataToDecrypt = {
        data: selectedNote.data,
        iv: selectedNote.iv
      };
      const decrypted = await decryptText(dataToDecrypt, key);
      setDecryptedContent(decrypted);
      showNotification('Note decrypted successfully!');
    } catch (error) {
      showNotification('Decryption failed. Please check your key.');
      setDecryptedContent('');
    }
    setIsDecrypting(false);
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showNotification('Copied to clipboard!');
    } catch (error) {
      showNotification('Failed to copy to clipboard');
    }
  };

  const closeDecryption = () => {
    setSelectedNote(null);
    setDecryptedContent('');
    setDecryptionKey('');
    setSelectedColors([]);
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Decorative Elements */}
      <div className="absolute top-32 left-10 pointer-events-none">
        <svg className="w-16 h-16 text-yellow-300 opacity-50" viewBox="0 0 100 100">
          <path d="M10,10 L90,10 L90,90 L10,90 Z M20,30 L80,30 M20,50 L80,50 M20,70 L80,70" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="3,3" />
        </svg>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Notes List */}
        <div className="paper-texture rounded-2xl shadow-2xl border-4 border-dashed border-green-300 overflow-hidden transform hover:scale-[1.02] transition-transform duration-300">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 px-6 py-4 border-b-4 border-dashed border-green-200 relative">
            <svg className="absolute top-2 right-4 w-8 h-8 text-green-300 opacity-60" viewBox="0 0 20 20">
              <path d="M5,5 Q10,2 15,5 Q18,10 15,15 Q10,18 5,15 Q2,10 5,5" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
            <h2 className="handwritten text-2xl font-bold text-green-900 transform rotate-1">My Encrypted Notes</h2>
            <p className="handwritten text-green-700 mt-1">
              {notes.length} {notes.length === 1 ? 'note' : 'notes'} stored securely
            </p>
          </div>

          <div className="p-6">
            {/* Search Bar */}
            <div className="relative mb-6">
              <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search notes by title..."
                className="handwritten w-full pl-10 pr-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:ring-2 focus:ring-green-400 focus:border-green-400 transition-all bg-white transform hover:scale-[1.02]"
              />
            </div>

            {/* Notes List */}
            {filteredNotes.length === 0 ? (
              <div className="text-center py-12">
                <div className="relative inline-block mb-4">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto" />
                  <svg className="absolute -top-2 -right-2 w-8 h-8 text-pink-300" viewBox="0 0 20 20">
                    <path d="M2,10 Q10,2 18,10" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="2,2" />
                  </svg>
                </div>
                <h3 className="handwritten text-xl font-bold text-gray-900 mb-2">
                  {searchTerm ? 'No notes found' : 'No notes yet'}
                </h3>
                <p className="handwritten text-gray-500">
                  {searchTerm 
                    ? 'Try adjusting your search terms'
                    : 'Create your first encrypted note to get started'
                  }
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredNotes.map((note) => (
                  <div
                    key={note.id}
                    className={`border-2 border-dashed rounded-lg p-4 transition-all cursor-pointer group transform hover:scale-105 hover:shadow-lg ${
                      selectedNote?.id === note.id
                        ? 'border-blue-400 bg-blue-50 shadow-md'
                        : 'border-gray-300 hover:border-green-400 hover:bg-green-50'
                    }`}
                    onClick={() => handleNoteClick(note)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <h3 className={`handwritten text-xl font-bold truncate transform -rotate-1 ${
                          selectedNote?.id === note.id
                            ? 'text-blue-800'
                            : 'text-gray-900 group-hover:text-green-800'
                        }`}>
                          {note.title}
                        </h3>
                        <div className="flex items-center gap-2 mt-1">
                          <Shield className="w-4 h-4 text-gray-500" />
                          <span className="handwritten text-sm text-gray-600">
                            {note.algorithm || 'AES-GCM'}
                          </span>
                        </div>
                        <div className="handwritten flex items-center gap-4 mt-2 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            Created: {formatDate(note.createdAt)}
                          </div>
                          {note.updatedAt !== note.createdAt && (
                            <div className="flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              Updated: {formatDate(note.updatedAt)}
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteNote(note.id);
                        }}
                        className="opacity-0 group-hover:opacity-100 p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-all transform hover:scale-110 border-2 border-dashed border-transparent hover:border-red-300"
                        title="Delete note"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Decryption Panel */}
        {selectedNote && (
          <div className="paper-texture rounded-2xl shadow-2xl border-4 border-dashed border-amber-300 overflow-hidden transform hover:scale-[1.02] transition-transform duration-300">
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 px-6 py-4 border-b-4 border-dashed border-amber-200 relative">
              <svg className="absolute top-2 right-12 w-8 h-8 text-amber-300 opacity-60" viewBox="0 0 20 20">
                <path d="M5,10 Q10,5 15,10 Q10,15 5,10" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="2,2" />
              </svg>
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="handwritten text-2xl font-bold text-amber-900 transform rotate-1">
                    Decrypt: {selectedNote.title}
                  </h2>
                  <p className="handwritten text-amber-700 mt-1">
                    Enter your decryption key to view the content
                  </p>
                </div>
                <button
                  onClick={closeDecryption}
                  className="handwritten text-2xl text-amber-600 hover:text-amber-800 transition-colors transform hover:scale-110 hover:rotate-12"
                >
                  ✕
                </button>
              </div>
              </div>

            <div className="p-6 space-y-6">
              {/* Algorithm Display */}
              <div className="mb-4">
                <div className="bg-blue-50 border-2 border-dashed border-blue-300 rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-blue-600" />
                    <span className="handwritten text-blue-800 font-semibold">
                      Algorithm: {selectedNote.algorithm || 'AES-GCM'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Decryption Key */}
              <div>
                <label htmlFor="decrypt-key" className="handwritten block text-lg font-medium text-gray-700 mb-2">
                  Decryption Key
                </label>
                <div className="relative">
                  <input
                    id="decrypt-key"
                    type={showKey ? 'text' : 'password'}
                    value={decryptionKey}
                    onChange={(e) => setDecryptionKey(e.target.value)}
                    placeholder="Enter your decryption key..."
                    className="handwritten w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-400 pr-12 transition-all bg-white transform hover:scale-[1.02]"
                    onKeyPress={(e) => e.key === 'Enter' && handleDecrypt()}
                  />
                  <button
                    type="button"
                    onClick={() => setShowKey(!showKey)}
                    className="absolute right-3 top-3.5 text-gray-500 hover:text-amber-600 transition-colors transform hover:scale-110"
                  >
                    {showKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Color Palette Selection */}
              <div>
                <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
                  <Palette className="inline w-5 h-5 mr-2" />
                  Rainbow Security Colors (Select 3 in order)
                </label>
                <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-dashed border-amber-300 rounded-lg p-4">
                  <div className="grid grid-cols-5 gap-2 mb-4">
                    {rainbowColors.map((color, index) => (
                      <button
                        key={color}
                        type="button"
                        onClick={() => handleColorSelect(color)}
                        className={`relative w-12 h-12 rounded-lg border-2 border-dashed transition-all transform hover:scale-110 ${
                          selectedColors.includes(color)
                            ? 'border-gray-800 shadow-lg scale-105'
                            : 'border-gray-300 hover:border-gray-500'
                        }`}
                        style={{ backgroundColor: color }}
                      >
                        {selectedColors.includes(color) && (
                          <div className="absolute -top-2 -right-2 bg-white text-gray-800 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold border-2 border-gray-800">
                            {selectedColors.indexOf(color) + 1}
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                  
                  {/* Selected Colors Display */}
                  <div className="flex items-center gap-2">
                    <span className="handwritten text-sm font-medium text-gray-700">Selected sequence:</span>
                    <div className="flex gap-1">
                      {[0, 1, 2].map((index) => (
                        <div
                          key={index}
                          className="w-8 h-8 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center text-xs font-bold"
                          style={{ 
                            backgroundColor: selectedColors[index] || '#f3f4f6'
                          }}
                        >
                          {index + 1}
                        </div>
                      ))}
                    </div>
                    <span className="handwritten text-xs text-gray-500">
                      ({selectedColors.length}/3 selected)
                    </span>
                  </div>
                </div>
                <p className="handwritten text-sm text-gray-500 mt-1">
                  Select the same 3 rainbow colors in the exact same order used during encryption.
                </p>
              </div>

              {/* Decrypt Button */}
              <button
                onClick={handleDecrypt}
                disabled={isDecrypting}
                className="handwritten w-full bg-gradient-to-r from-amber-500 to-orange-500 text-white py-3 px-6 rounded-lg hover:from-amber-600 hover:to-orange-600 disabled:opacity-50 transition-all flex items-center justify-center gap-2 font-semibold text-lg transform hover:scale-105 active:scale-95 shadow-lg border-2 border-dashed border-amber-600"
              >
                {isDecrypting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Decrypting...
                  </>
                ) : (
                  <>
                    <Unlock className="w-5 h-5" />
                    Decrypt Note
                  </>
                )}
              </button>

              {/* Decrypted Content */}
              {decryptedContent && (
                <div>
                  <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
                    Decrypted Content
                  </label>
                  <div className="bg-green-50 border-2 border-dashed border-green-300 rounded-lg p-4 min-h-[200px] overflow-auto">
                    <div className="handwritten text-green-800 whitespace-pre-wrap leading-relaxed text-lg">
                      {decryptedContent}
                    </div>
                  </div>
                  <button
                    onClick={() => copyToClipboard(decryptedContent)}
                    className="handwritten w-full mt-3 bg-gradient-to-r from-green-500 to-teal-500 text-white py-3 px-4 rounded-lg hover:from-green-600 hover:to-teal-600 transition-all flex items-center justify-center gap-2 font-semibold transform hover:scale-105 active:scale-95 shadow-lg border-2 border-dashed border-green-600"
                  >
                    <Copy className="w-4 h-4" />
                    Copy Decrypted Text
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}