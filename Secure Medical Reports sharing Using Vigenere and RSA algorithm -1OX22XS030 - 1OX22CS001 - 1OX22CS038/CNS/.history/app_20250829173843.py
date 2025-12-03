from flask import Flask, render_template, request, send_file, redirect, url_for
from pathlib import Path
import os
from vigenere_bytes import generate_vigenere_key_bytes, vigenere_encrypt_bytes, vigenere_decrypt_bytes
import rsa_utils

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
KEY_DIR = BASE_DIR / "keys"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
KEY_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

# Generate RSA keys if not exist
def init_keys():
    priv_file = KEY_DIR / "private.pem"
    pub_file = KEY_DIR / "public.pem"
    if not priv_file.exists() or not pub_file.exists():
        priv, pub = rsa_utils.generate_rsa_keypair()
        rsa_utils.save_key(priv, priv_file)
        rsa_utils.save_key(pub, pub_file)

@app.route("/", methods=["GET", "POST"])
def index():
    init_keys()
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return "No file selected"
        filepath = UPLOAD_DIR / uploaded_file.filename
        uploaded_file.save(filepath)

        # Encrypt
        data = filepath.read_bytes()
        vkey = generate_vigenere_key_bytes(32)
        cipher_data = vigenere_encrypt_bytes(data, vkey)

        # Encrypt Vigenère key with RSA public key
        pub_pem = rsa_utils.load_public_key(KEY_DIR / "public.pem")
        encrypted_vkey = rsa_utils.rsa_encrypt_bytes(vkey, pub_pem)

        # Save outputs
        enc_file = OUTPUT_DIR / (uploaded_file.filename + "_encrypted.bin")
        enc_key_file = OUTPUT_DIR / (uploaded_file.filename + "_key_encrypted.bin")
        enc_file.write_bytes(cipher_data)
        enc_key_file.write_bytes(encrypted_vkey)

        return f"File encrypted successfully! Download:<br>" \
               f"<a href='/download/{enc_file.name}'>Encrypted Report</a><br>" \
               f"<a href='/download/{enc_key_file.name}'>Encrypted Key</a>"

    return render_template("index.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        enc_file = request.files["enc_file"]
        enc_key_file = request.files["enc_key_file"]
        if not enc_file or not enc_key_file:
            return "Please upload both files"

        enc_file_path = UPLOAD_DIR / enc_file.filename
        enc_key_file_path = UPLOAD_DIR / enc_key_file.filename
        enc_file.save(enc_file_path)
        enc_key_file.save(enc_key_file_path)

        # Decrypt Vigenère key
        priv_pem = rsa_utils.load_private_key(KEY_DIR / "private.pem")
        vkey = rsa_utils.rsa_decrypt_bytes(enc_key_file_path.read_bytes(), priv_pem)

        # Decrypt file
        decrypted_data = vigenere_decrypt_bytes(enc_file_path.read_bytes(), vkey)
        out_file = OUTPUT_DIR / (enc_file.filename + "_decrypted" + ".txt")
        out_file.write_bytes(decrypted_data)

        return f"File decrypted successfully! Download:<br>" \
               f"<a href='/download/{out_file.name}'>Decrypted Report</a>"

    return render_template("decrypt.html")

@app.route("/download/<filename>")
def download(filename):
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    return "File not found"

if __name__ == "__main__":
    app.run(debug=True,port=5001)
