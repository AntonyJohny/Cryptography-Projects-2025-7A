import React, { useState } from 'react';
import { Lock, Eye, EyeOff, Save, Palette, Shield } from 'lucide-react';
import { EncryptedNote } from '../types';
import { generateKey, encryptText, generateRSAKeyPair } from '../utils/crypto';

interface WritePageProps {
  onNoteSaved: () => void;
  showNotification: (message: string) => void;
}

export default function WritePage({ onNoteSaved, showNotification }: WritePageProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [encryptionKey, setEncryptionKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [isEncrypting, setIsEncrypting] = useState(false);
  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<'AES-GCM' | 'RSA-OAEP' | 'ECC'>('AES-GCM');

  const rainbowColors = [
    '#FF0000', '#FF4500', '#FF8C00', '#FFD700', '#ADFF2F', 
    '#00FF00', '#00CED1', '#0000FF', '#4169E1', '#8A2BE2',
    '#FF1493', '#FF69B4', '#FFC0CB', '#F0E68C', '#DDA0DD'
  ];

  const handleColorSelect = (colorValue: string) => {
    if (selectedColors.includes(colorValue)) {
      setSelectedColors(selectedColors.filter(c => c !== colorValue));
    } else if (selectedColors.length < 3) {
      setSelectedColors([...selectedColors, colorValue]);
    }
  };

  const handleEncryptAndSave = async () => {
    if (!title.trim()) {
      showNotification('Please enter a title for your note');
      return;
    }
    if (!content.trim()) {
      showNotification('Please enter some content');
      return;
    }
    if (!encryptionKey.trim()) {
      showNotification('Please enter an encryption key');
      return;
    }
    if (selectedColors.length !== 3) {
      showNotification('Please select exactly 3 colors in order');
      return;
    }

    setIsEncrypting(true);
    try {
      let encrypted: any;
      let key: CryptoKey;
      
      if (selectedAlgorithm === 'RSA-OAEP') {
        const keyPair = await generateRSAKeyPair();
        encrypted = await encryptText(content, keyPair.publicKey, 'RSA-OAEP');
        // Store private key for decryption (in real app, this would be handled differently)
        localStorage.setItem(`rsa-private-${Date.now()}`, JSON.stringify(await crypto.subtle.exportKey('jwk', keyPair.privateKey)));
      } else {
        const combinedKey = encryptionKey + selectedColors.join('');
        key = await generateKey(combinedKey);
        encrypted = await encryptText(content, key, selectedAlgorithm);
      }
      
      const note: EncryptedNote = {
        id: Date.now().toString(),
        title: title.trim(),
        data: encrypted.data,
        iv: encrypted.iv,
        colorSequence: selectedColors,
        algorithm: selectedAlgorithm,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      // Save to localStorage
      const existingNotes = JSON.parse(localStorage.getItem('encryptedNotes') || '[]');
      existingNotes.push(note);
      localStorage.setItem('encryptedNotes', JSON.stringify(existingNotes));

      showNotification('Note encrypted and saved successfully!');
      setTitle('');
      setContent('');
      setEncryptionKey('');
      setSelectedColors([]);
      setSelectedAlgorithm('AES-GCM');
      onNoteSaved();
    } catch (error) {
      showNotification('Encryption failed. Please try again.');
    }
    setIsEncrypting(false);
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Decorative Elements */}
      <div className="absolute top-20 right-10 pointer-events-none">
        <svg className="w-20 h-20 text-pink-300 opacity-50 animate-wiggle" viewBox="0 0 100 100">
          <path d="M20,50 Q50,20 80,50 Q50,80 20,50" stroke="currentColor" strokeWidth="3" fill="none" strokeDasharray="4,4" />
        </svg>
      </div>

      <div className="paper-texture rounded-2xl shadow-2xl border-4 border-dashed border-blue-300 overflow-hidden transform hover:scale-[1.02] transition-transform duration-300">
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-4 border-b-4 border-dashed border-blue-200 relative">
          <svg className="absolute top-2 right-4 w-8 h-8 text-blue-300 opacity-60" viewBox="0 0 20 20">
            <circle cx="10" cy="10" r="6" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="2,2" />
          </svg>
          <h2 className="handwritten text-2xl font-bold text-blue-900 transform -rotate-1">Create New Note</h2>
          <p className="handwritten text-blue-700 mt-1">Write your note and encrypt it with a secure key</p>
        </div>
        
        <div className="p-6 space-y-6">
          {/* Title Input */}
          <div>
            <label htmlFor="title" className="handwritten block text-lg font-medium text-gray-700 mb-2">
              Note Title
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter a title for your note..."
              className="handwritten w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all text-lg bg-white transform hover:scale-[1.02]"
            />
          </div>

          {/* Content Textarea */}
          <div>
            <label htmlFor="content" className="handwritten block text-lg font-medium text-gray-700 mb-2">
              Note Content
            </label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your private note here..."
              rows={12}
              className="handwritten w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all bg-white transform hover:scale-[1.01]"
            />
          </div>

          {/* Encryption Key */}
          <div>
            <label htmlFor="key" className="handwritten block text-lg font-medium text-gray-700 mb-2">
              Encryption Key
            </label>
            <div className="relative">
              <input
                id="key"
                type={showKey ? 'text' : 'password'}
                value={encryptionKey}
                onChange={(e) => setEncryptionKey(e.target.value)}
                placeholder="Enter a strong encryption key..."
                className="handwritten w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-400 focus:border-purple-400 pr-12 transition-all bg-white transform hover:scale-[1.02]"
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-3.5 text-gray-500 hover:text-purple-600 transition-colors transform hover:scale-110"
              >
                {showKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            <p className="handwritten text-sm text-gray-500 mt-1">
              Use a strong, memorable key. You'll need this exact key to decrypt your note later.
            </p>
          </div>

          {/* Algorithm Selection */}
          <div>
            <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
              <Shield className="inline w-5 h-5 mr-2" />
              Encryption Algorithm
            </label>
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-dashed border-blue-300 rounded-lg p-4">
              <div className="grid grid-cols-3 gap-3">
                {(['AES-GCM', 'RSA-OAEP', 'ECC'] as const).map((algorithm) => (
                  <button
                    key={algorithm}
                    type="button"
                    onClick={() => setSelectedAlgorithm(algorithm)}
                    className={`handwritten p-3 rounded-lg border-2 border-dashed transition-all transform hover:scale-105 ${
                      selectedAlgorithm === algorithm
                        ? 'border-blue-600 bg-blue-100 text-blue-800 shadow-md'
                        : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
                    }`}
                  >
                    <div className="text-center">
                      <div className="font-bold text-sm">{algorithm}</div>
                      <div className="text-xs mt-1 opacity-75">
                        {algorithm === 'AES-GCM' && 'Symmetric'}
                        {algorithm === 'RSA-OAEP' && 'Asymmetric'}
                        {algorithm === 'ECC' && 'Elliptic Curve'}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
            <p className="handwritten text-sm text-gray-500 mt-1">
              Choose your preferred encryption algorithm for securing the note.
            </p>
          </div>

          {/* Color Palette Selection */}
          <div>
            <label className="handwritten block text-lg font-medium text-gray-700 mb-2">
              <Palette className="inline w-5 h-5 mr-2" />
              Rainbow Security Colors (Select 3 in order)
            </label>
            <div className="bg-gradient-to-r from-pink-50 to-purple-50 border-2 border-dashed border-pink-300 rounded-lg p-4">
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
              Choose 3 rainbow colors in a specific order. You'll need the same colors in the same order to decrypt.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleEncryptAndSave}
              disabled={isEncrypting}
              className="handwritten flex-1 bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 transition-all flex items-center justify-center gap-2 font-semibold text-lg transform hover:scale-105 active:scale-95 shadow-lg border-2 border-dashed border-blue-600"
            >
              {isEncrypting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Encrypting...
                </>
              ) : (
                <>
                  <Lock className="w-5 h-5" />
                  Encrypt & Save Note
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}