from flask import Flask, render_template, request, send_file
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

# Initialize RSA keys
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

        # Encrypt file using Vigenère
        data = filepath.read_bytes()
        keylen = int(request.form.get("keylen", 32))
        vkey = generate_vigenere_key_bytes(keylen)
        cipher_data = vigenere_encrypt_bytes(data, vkey)

        # Encrypt Vigenère key using RSA
        pub_key = rsa_utils.load_public_key(KEY_DIR / "public.pem")
        encrypted_vkey = rsa_utils.rsa_encrypt_bytes(vkey, pub_key)

        # Save outputs
        enc_file = OUTPUT_DIR / (uploaded_file.filename + "_encrypted.bin")
        enc_key_file = OUTPUT_DIR / (uploaded_file.filename + "_key_encrypted.bin")
        enc_file.write_bytes(cipher_data)
        enc_key_file.write_bytes(encrypted_vkey)

        return f"""
        <h4>File encrypted successfully!</h4>
        <a href='/download/{enc_file.name}'>Download Encrypted Report</a><br>
        <a href='/download/{enc_key_file.name}'>Download Encrypted Key</a><br>
        <a href='/'>Encrypt Another File</a>
        """
    return render_template("index.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        enc_file = request.files["enc_file"]
        enc_key_file = request.files["enc_key_file"]
        if not enc_file or not enc_key_file:
            return "Please upload both files"

        enc_file_path = UPLOAD_DIR / enc_file.filename
        enc_key_path = UPLOAD_DIR / enc_key_file.filename
        enc_file.save(enc_file_path)
        enc_key_file.save(enc_key_path)

        priv_key = rsa_utils.load_private_key(KEY_DIR / "private.pem")
        vkey = rsa_utils.rsa_decrypt_bytes(enc_key_path.read_bytes(), priv_key)

        decrypted_data = vigenere_decrypt_bytes(enc_file_path.read_bytes(), vkey)

        # keep original filename (remove "_encrypted.bin")
        original_name = enc_file.filename.replace("_encrypted.bin", "")
        out_file = OUTPUT_DIR / ("decrypted_" + original_name)

        out_file.write_bytes(decrypted_data)

        return f"""
        <h4>File decrypted successfully!</h4>
        <a href='/download/{out_file.name}'>Download Decrypted Report</a><br>
        <a href='/decrypt'>Decrypt Another File</a>
        """
    return render_template("decrypt.html")

@app.route("/download/<filename>")
def download(filename):
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    return "File not found"

if __name__ == "__main__":
    app.run(debug=True)
