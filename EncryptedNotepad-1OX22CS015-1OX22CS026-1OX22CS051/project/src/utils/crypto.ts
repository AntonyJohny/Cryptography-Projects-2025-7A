export interface EncryptedData {
  data: string;
  iv: string;
  algorithm?: string;
}

// Generate ECC key pair
export const generateECCKeyPair = async (): Promise<CryptoKeyPair> => {
  return await crypto.subtle.generateKey(
    {
      name: 'ECDH',
      namedCurve: 'P-256'
    },
    true,
    ['deriveKey']
  );
};

// Generate RSA key pair
export const generateRSAKeyPair = async (): Promise<CryptoKeyPair> => {
  return await crypto.subtle.generateKey(
    {
      name: 'RSA-OAEP',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256'
    },
    true,
    ['encrypt', 'decrypt']
  );
};

export const generateKey = async (password: string): Promise<CryptoKey> => {
  const encoder = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    { name: 'PBKDF2' },
    false,
    ['deriveKey']
  );

  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt: encoder.encode('secure-notepad-salt'),
      iterations: 100000,
      hash: 'SHA-256'
    },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
};

export const encryptText = async (text: string, key: CryptoKey, algorithm: string = 'AES-GCM'): Promise<EncryptedData> => {
  const encoder = new TextEncoder();
  
  if (algorithm === 'RSA-OAEP') {
    const encrypted = await crypto.subtle.encrypt(
      { name: 'RSA-OAEP' },
      key,
      encoder.encode(text)
    );
    
    return {
      data: Array.from(new Uint8Array(encrypted)).map(b => b.toString(16).padStart(2, '0')).join(''),
      iv: '',
      algorithm: 'RSA-OAEP'
    };
  } else {
    // Default AES-GCM
    const iv = crypto.getRandomValues(new Uint8Array(12));
    
    const encrypted = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      key,
      encoder.encode(text)
    );

    return {
      data: Array.from(new Uint8Array(encrypted)).map(b => b.toString(16).padStart(2, '0')).join(''),
      iv: Array.from(iv).map(b => b.toString(16).padStart(2, '0')).join(''),
      algorithm: 'AES-GCM'
    };
  }
};

export const decryptText = async (encryptedData: EncryptedData, key: CryptoKey): Promise<string> => {
  const encryptedBytes = new Uint8Array(
    encryptedData.data.match(/.{2}/g)!.map(byte => parseInt(byte, 16))
  );

  let decrypted: ArrayBuffer;
  
  if (encryptedData.algorithm === 'RSA-OAEP') {
    decrypted = await crypto.subtle.decrypt(
      { name: 'RSA-OAEP' },
      key,
      encryptedBytes
    );
  } else {
    // Default AES-GCM
    const iv = new Uint8Array(
      encryptedData.iv.match(/.{2}/g)!.map(byte => parseInt(byte, 16))
    );
    
    decrypted = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      key,
      encryptedBytes
    );
  }

  const decoder = new TextDecoder();
  return decoder.decode(decrypted);
};