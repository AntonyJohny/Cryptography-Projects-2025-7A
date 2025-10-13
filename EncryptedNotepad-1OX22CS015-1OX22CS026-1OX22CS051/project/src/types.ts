export interface EncryptedNote {
  id: string;
  title: string;
  data: string;
  iv: string;
  colorSequence?: string[];
  algorithm?: string;
  createdAt: string;
  updatedAt: string;
}

export interface StoredNote {
  id: string;
  title: string;
  encryptedData: string;
  createdAt: string;
  updatedAt: string;
}