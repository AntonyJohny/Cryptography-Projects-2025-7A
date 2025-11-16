📘 Steganography Message Encryption – Web Application

This project demonstrates the integration of cryptography and steganography to achieve secure and concealed communication. The system encrypts messages using the classical Caesar cipher and hides the encrypted data inside images using LSB (Least Significant Bit) steganography.
The project is implemented as a simple and user-friendly web application using HTML, CSS, and JavaScript.

🚀 Project Overview

In traditional encryption, the content of a message is hidden, but the existence of the message is still visible. In contrast, steganography hides the message inside another medium but often lacks encryption.
This project combines both techniques, ensuring:

Confidentiality

Concealment

Ease of use

Users can:

Enter a secret message

Encrypt it with Caesar cipher

Embed the encrypted data into an image

Download the stego image

Later extract and decrypt the hidden message

🔐 Key Features
1. Caesar Cipher Encryption

Shifts each character based on a user-defined key (1–25)

Supports encryption and decryption

Ensures the message is unreadable even if discovered

2. LSB Image Steganography

Embeds encrypted message bits into the least significant bits of the red pixel channel

Does not visually affect the image

First 32 bits store message length for accurate extraction

3. Image-Based Communication

Image upload and preview

Embedding and extraction using HTML5 Canvas API

Downloadable stego image

4. User-Friendly Interface

Clear two-panel layout:
Embed Message | Extract Message

Real-time validation for input correctness

Error alerts for invalid keys, unsupported images, or oversized messages

📂 System Workflow
Encryption & Embedding

User enters secret message

User enters Caesar cipher shift key

System encrypts the message

Encrypted text → converted into binary

User uploads a cover image

System embeds binary data into LSBs

Stego image generated and downloadable

Extraction & Decryption

User uploads the stego image

System reads message length

System extracts LSB bit-stream

Bits → encrypted text

Decrypted using Caesar cipher key

Original message displayed

🧰 Technologies Used

HTML5 – UI structure

CSS3 – Styling

JavaScript (ES6) – Logic for encryption, embedding, extraction

Canvas API – Pixel-level manipulation for steganography

📊 Use Cases

Secure personal communication

Data hiding for privacy

Educational demonstration of cryptography & steganography

Research and academic projects

🧪 Project Results

Encrypted messages successfully hidden inside images

Stego images maintain original visual quality

Accurate extraction and decryption of messages

Simple and smooth user experience for embedding and retrieving messages

🔮 Future Enhancements

Add more encryption schemes (Playfair, Vigenère, Hill cipher)

Support for audio and video steganography

Add compression and error-correction

Improve UI with drag-and-drop and dark mode

Implement user authentication for secure multi-user usage

📚 References

William Stallings – Cryptography and Network Security

Katzenbeisser & Petitcolas – Information Hiding Techniques for Steganography

MDN Docs – Canvas API

Academic tutorials on Caesar cipher and digital steganography