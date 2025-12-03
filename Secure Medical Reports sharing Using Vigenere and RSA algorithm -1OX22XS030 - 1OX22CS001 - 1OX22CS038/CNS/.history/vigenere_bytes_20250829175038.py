# vigenere_bytes.py
# Byte-wise Vigenere: works for any file (text, pdf, image) by operating on bytes.

import os
import secrets

def generate_vigenere_key_bytes(length: int = 32) -> bytes:
    """Generate a random key of given byte length."""
    return secrets.token_bytes(length)

def vigenere_encrypt_bytes(data: bytes, key: bytes) -> bytes:
    """Encrypt data using byte-wise Vigenere (add key bytes mod 256)."""
    out = bytearray(len(data))
    klen = len(key)
    for i, b in enumerate(data):
        out[i] = (b + key[i % klen]) % 256
    return bytes(out)

def vigenere_decrypt_bytes(cipher: bytes, key: bytes) -> bytes:
    """Decrypt data encrypted by vigenere_encrypt_bytes."""
    out = bytearray(len(cipher))
    klen = len(key)
    for i, c in enumerate(cipher):
        out[i] = (c - key[i % klen]) % 256
    return bytes(out)
