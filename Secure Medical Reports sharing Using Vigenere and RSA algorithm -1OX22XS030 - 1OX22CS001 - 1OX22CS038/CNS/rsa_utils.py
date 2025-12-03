from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_keypair(bits: int = 2048):
    key = RSA.generate(bits)
    private_pem = key.export_key()          # PEM format
    public_pem = key.publickey().export_key()
    return private_pem, public_pem

def save_key(pem_bytes: bytes, filename: str):
    with open(filename, "wb") as f:
        f.write(pem_bytes)                  # write bytes to file

def load_public_key(pem_file: str):
    from Crypto.PublicKey import RSA
    with open(pem_file, "rb") as f:
        return RSA.import_key(f.read())

def load_private_key(pem_file: str):
    from Crypto.PublicKey import RSA
    with open(pem_file, "rb") as f:
        return RSA.import_key(f.read())

def rsa_encrypt_bytes(message: bytes, public_key: RSA) -> bytes:
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message)

def rsa_decrypt_bytes(ciphertext: bytes, private_key: RSA) -> bytes:
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)
