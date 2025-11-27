Secure Notes Application Using Hybrid Substitution Cryptography
Caesar Cipher + Vigenère Cipher + Playfair Cipher
📝 Project Overview

The Secure Notes Application is a Flask-based web platform designed to protect sensitive text using a hybrid multi-layer cryptography model.
It combines three classical substitution ciphers:

Caesar Cipher – character shifting

Vigenère Cipher – key-based polyalphabetic encryption

Playfair Cipher – digraph-based grid substitution

Each layer increases security, making the encrypted note significantly harder to break compared to using any single classical cipher. 
Why Hybrid Cryptography?

Instead of relying on one cipher, this project applies a pipeline of three encryption layers:

Plaintext
 → Caesar Shift
 → Vigenère Encryption
 → Playfair Encryption
 → Final Ciphertext (stored in database)


Decryption follows the exact reverse order:

Ciphertext
 → Playfair Decryption
 → Vigenère Decryption
 → Caesar Reverse Shift
 → Original Plaintext


This multi-stage approach:
✔ Enhances security
✔ Makes brute-force attacks highly impractical
✔ Ensures that no plaintext is ever stored
Key Features

✔ Triple-layer hybrid encryption (Caesar + Vigenère + Playfair)

✔ Only encrypted text stored (no plaintext saved anywhere)

✔ Flask-based user-friendly interface

✔ Decryption possible only with correct keys

✔ Preserves formatting, spacing, and punctuation

✔ Automatically stores metadata for accurate decryption
Project Structure
secure_notes_hybrid/
├── app.py                 # Flask web application
├── ciphers.py             # Caesar, Vigenère, Playfair hybrid pipeline
├── requirements.txt       # Flask dependencies
│
├── data/
│   └── notes.json         # Encrypted notes generated at runtime
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── new.html
│   └── view.html
│
└── static/
    └── style.css          # UI styling
Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/secure_notes_hybrid.git
cd secure_notes_hybrid

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py

4️⃣ Open in browser

Visit:
👉 http://127.0.0.1:5000

🖥️ How to Use
✏️ Encrypt a Note

Click Create New Secure Note

Enter:

Title

Plaintext note

Caesar shift value

Vigenère passphrase

Playfair keyword

Click Encrypt & Save

Your note is saved safely as encrypted text.

🔓 Decrypt a Note

Open your saved note

Enter the same three keys:

Caesar shift

Vigenère key

Playfair keyword

Click Decrypt

✔ Correct keys → Original plaintext restored
✖ Wrong keys → Output remains unreadable

⭐ Real-World Applications

Secure private notes

Safe record keeping

Confidential text storage

Cryptography education tool

Encrypted journaling system

🧠 Tech Stack

Python 3

Flask

HTML / CSS

Classical Cryptography Algorithms
Future Enhancements

Add authentication/login

Integrate AES for modern encryption

Mobile-responsive UI

Encrypted note exporting

Cloud sync functionality

🤝 Contributors

Eshwari N R

Biradar Gururaj

📄 License

This project is developed for academic and educational purposes.