Secure Medical Report Encryption System using Vigenère Cipher + RSA Hybrid Encryption
------------------------------------------------------------------------------------
This project implements a secure file-sharing system for medical reports, using a hybrid encryption model that combines:

Vigenère Cipher → for encrypting the actual report (symmetric encryption)

RSA → for encrypting the Vigenère key (asymmetric encryption)

This ensures fast file encryption and secure key transfer, suitable for a medical data–sharing workflow.
--------------------------------------------------------------------------------
🚀 Features

🔐 Upload medical report files (PDF, TXT, etc.)

🔑 Upload/enter a Vigenère key to encrypt the file

🛡️ Encrypt the Vigenère key using RSA public key

📄 Download encrypted file + encrypted key

🔓 Use RSA private key to decrypt the key on receiver side

📥 Decrypt the file using the recovered Vigenère key

✔️ Ensures confidentiality for sensitive medical reports
-------------------------------------------------------------------------------------
🧠 How the Hybrid Encryption Works

This system uses the standard hybrid-encryption approach:

1. Encryption (Sender Side)

    User uploads a medical report file

    User provides a Vigenère key

    Application encrypts the file using Vigenère Cipher

    The Vigenère key is encrypted using RSA Public Key

    Output:

    encrypted_report.txt

    encrypted_vigenere_key.bin

2. Decryption (Receiver Side)

    Receiver uses their RSA Private Key to decrypt the key

    The recovered Vigenère key is used to decrypt the report

    Output:

    The original medical report
-------------------------------------------------------------------------
🚀 How to Run the Project (Important Section)

Follow these steps to run the application on your machine:

1️⃣ Clone the Repository
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2️⃣ Install Required Libraries
pip install -r requirements.txt


If you don’t have a requirements.txt, create one (optional):

flask
pycryptodome

3️⃣ Generate RSA Keys (One-Time Setup)

Run the following Python script OR use the built-in function in rsa_utils.py:

from Crypto.PublicKey import RSA

key = RSA.generate(2048)
open("keys/private.pem", "wb").write(key.export_key())
open("keys/public.pem", "wb").write(key.publickey().export_key())


This will generate:

keys/public.pem → used for encryption

keys/private.pem → used for decryption

4️⃣ Run the Application

Execute:

python app.py


Then open your browser and go to:

http://127.0.0.1:5000/

5️⃣ Encrypting a Medical Report

Open Encrypt Page

Upload the medical report (PDF/text)

Enter a Vigenère key

The system:

Encrypts the file using Vigenère

Encrypts the Vigenère key using RSA public key

Download:

encrypted_report.txt

encrypted_key.bin

6️⃣ Decrypting a Medical Report

Open Decrypt Page

Upload:

encrypted_report.txt

encrypted_key.bin

Upload your RSA private key

System will:

Decrypt the Vigenère key

Decrypt the medical report

Download the original medical report.
-----------------------------------------------------------------------------
🧪 Tech Stack

Python

Flask (optional, if using web UI)

PyCryptodome for RSA functionality

Custom Vigenère implementation
-----------------------------------------------------------------------------------
🤝 Contributing

Pull requests and suggestions are welcome!