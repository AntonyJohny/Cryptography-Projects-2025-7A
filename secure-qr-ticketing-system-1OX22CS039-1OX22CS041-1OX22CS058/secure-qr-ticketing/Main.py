# Secure QR Ticketing System
# Dependencies: pip install cryptography qrcode[pil] flask pillow

import json
import base64
import time
import uuid
import hashlib
import re
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import qrcode
from PIL import Image
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

class SecureTicketingSystem:
    def __init__(self):
        self.backend = default_backend()
        self.db_path = "tickets.db"
        self.init_database()
        
        # Generate or load RSA key pair
        if not os.path.exists("private_key.pem"):
            self.generate_keys()
        else:
            self.load_keys()
    
    def init_database(self):
        """Initialize SQLite database for ticket tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                event_name TEXT,
                issue_time TEXT,
                expiry_time TEXT,
                used BOOLEAN DEFAULT FALSE,
                use_time TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def generate_keys(self):
        """Generate RSA key pair for digital signatures"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=self.backend
        )
        self.public_key = self.private_key.public_key()
        
        # Save keys to files
        with open("private_key.pem", "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open("public_key.pem", "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def load_keys(self):
        """Load existing RSA key pair"""
        with open("private_key.pem", "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=self.backend
            )
        
        with open("public_key.pem", "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(), backend=self.backend
            )
    
    def parse_datetime_string(self, datetime_str):
        """Parse datetime string - compatible with Python < 3.7"""
        try:
            # Simple approach: just take the first 19 characters
            clean_str = datetime_str[:19]
            return datetime.strptime(clean_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Fallback: try with microseconds
            try:
                clean_str = datetime_str[:26]
                return datetime.strptime(clean_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                raise ValueError(f"Unable to parse datetime: {datetime_str}")
    
    def generate_aes_key(self):
        """Generate AES-256 key and IV"""
        key = os.urandom(32)  # 256-bit key
        iv = os.urandom(12)   # 96-bit IV for GCM
        return key, iv
    
    def encrypt_data(self, data, key, iv):
        """Encrypt data using AES-256-GCM"""
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
        return ciphertext, encryptor.tag
    
    def decrypt_data(self, ciphertext, tag, key, iv):
        """Decrypt data using AES-256-GCM"""
        try:
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext.decode()
        except Exception:
            return None
    
    def sign_data(self, data):
        """Sign data using RSA-PSS with SHA-256"""
        signature = self.private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify_signature(self, data, signature):
        """Verify RSA-PSS signature"""
        try:
            self.public_key.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def create_ticket(self, event_name, holder_name, seat_number, valid_hours=24):
        """Create a secure ticket"""
        # Generate unique ticket ID
        ticket_id = str(uuid.uuid4())
        
        # Create ticket data
        issue_time = datetime.now()
        expiry_time = issue_time + timedelta(hours=valid_hours)
        
        ticket_data = {
            "ticket_id": ticket_id,
            "event_name": event_name,
            "holder_name": holder_name,
            "seat_number": seat_number,
            "issue_time": issue_time.isoformat(),
            "expiry_time": expiry_time.isoformat(),
            "nonce": os.urandom(16).hex()  # Additional uniqueness
        }
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (ticket_id, event_name, issue_time, expiry_time, used)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticket_id, event_name, issue_time.isoformat(), expiry_time.isoformat(), False))
        conn.commit()
        conn.close()
        
        # Convert to JSON and encrypt
        ticket_json = json.dumps(ticket_data)
        aes_key, iv = self.generate_aes_key()
        ciphertext, tag = self.encrypt_data(ticket_json, aes_key, iv)
        
        # Create signature of the original data
        signature = self.sign_data(ticket_json)
        
        # Combine everything for QR code
        qr_payload = {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "tag": base64.b64encode(tag).decode(),
            "iv": base64.b64encode(iv).decode(),
            "key": base64.b64encode(aes_key).decode(),
            "signature": base64.b64encode(signature).decode()
        }
        
        # Generate QR code
        qr_data = json.dumps(qr_payload)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"ticket_{ticket_id}.png"
        qr_image.save(qr_filename)
        
        return {
            "ticket_id": ticket_id,
            "qr_filename": qr_filename,
            "ticket_data": ticket_data
        }
    
    def validate_ticket(self, qr_data):
        """Validate a ticket from QR code data"""
        try:
            # Parse QR payload
            qr_payload = json.loads(qr_data)
            
            # Extract components
            ciphertext = base64.b64decode(qr_payload["ciphertext"])
            tag = base64.b64decode(qr_payload["tag"])
            iv = base64.b64decode(qr_payload["iv"])
            key = base64.b64decode(qr_payload["key"])
            signature = base64.b64decode(qr_payload["signature"])
            
            # Decrypt ticket data
            decrypted_data = self.decrypt_data(ciphertext, tag, key, iv)
            if not decrypted_data:
                return {"valid": False, "reason": "Decryption failed - Invalid or tampered ticket"}
            
            # Verify signature
            if not self.verify_signature(decrypted_data, signature):
                return {"valid": False, "reason": "Signature verification failed - Ticket not authentic"}
            
            # Parse decrypted data
            ticket_data = json.loads(decrypted_data)
            ticket_id = ticket_data["ticket_id"]
            
            # Check database for ticket existence and usage
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
            db_ticket = cursor.fetchone()
            
            if not db_ticket:
                conn.close()
                return {"valid": False, "reason": "Ticket not found in database"}
            
            if db_ticket[5]:  # used column
                conn.close()
                return {"valid": False, "reason": "Ticket already used"}
            
            # Check expiry using our compatible method
            expiry_time = self.parse_datetime_string(ticket_data["expiry_time"])
            if datetime.now() > expiry_time:
                conn.close()
                return {"valid": False, "reason": "Ticket expired"}
            
            # Mark ticket as used
            cursor.execute('''
                    UPDATE tickets SET used = 1, use_time = ?
                        WHERE ticket_id = ?
                ''',(datetime.now().isoformat(), ticket_id))

            conn.commit()
            conn.close()
            
            return {
                "valid": True,
                "ticket_data": ticket_data,
                "message": "Ticket validated successfully"
            }
            
        except Exception as e:
            return {"valid": False, "reason": f"Validation error: {str(e)}"}

# Flask Web Application
app = Flask(__name__)
ticketing_system = SecureTicketingSystem()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Secure QR Ticketing System</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; border-radius: 4px; }
            .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🎫 Secure QR Ticketing System</h1>
        
        <div class="section">
            <h2>Create Ticket</h2>
            <form id="createForm">
                <div class="form-group">
                    <label>Event Name:</label>
                    <input type="text" id="eventName" required>
                </div>
                <div class="form-group">
                    <label>Holder Name:</label>
                    <input type="text" id="holderName" required>
                </div>
                <div class="form-group">
                    <label>Seat Number:</label>
                    <input type="text" id="seatNumber" required>
                </div>
                <div class="form-group">
                    <label>Valid Hours:</label>
                    <input type="number" id="validHours" value="24" min="1" max="168">
                </div>
                <button type="submit">Create Ticket</button>
            </form>
            <div id="createResult"></div>
        </div>
        
        <div class="section">
            <h2>Validate Ticket</h2>
            <form id="validateForm">
                <div class="form-group">
                    <label>QR Code Data (paste JSON):</label>
                    <textarea id="qrData" rows="5" style="width: 100%; font-family: monospace;"></textarea>
                </div>
                <button type="submit">Validate Ticket</button>
            </form>
            <div id="validateResult"></div>
        </div>
        
        <script>
            document.getElementById('createForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = new FormData();
                formData.append('event_name', document.getElementById('eventName').value);
                formData.append('holder_name', document.getElementById('holderName').value);
                formData.append('seat_number', document.getElementById('seatNumber').value);
                formData.append('valid_hours', document.getElementById('validHours').value);
                
                try {
                    const response = await fetch('/create_ticket', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    
                    const resultDiv = document.getElementById('createResult');
                    if (result.success) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <h3>Ticket Created Successfully!</h3>
                                <p><strong>Ticket ID:</strong> ${result.ticket_id}</p>
                                <p><strong>QR Code saved as:</strong> ${result.qr_filename}</p>
                                <p><strong>Event:</strong> ${result.ticket_data.event_name}</p>
                                <p><strong>Holder:</strong> ${result.ticket_data.holder_name}</p>
                                <p><strong>Seat:</strong> ${result.ticket_data.seat_number}</p>
                                <p><strong>Valid until:</strong> ${result.ticket_data.expiry_time}</p>
                            </div>`;
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${result.error}</div>`;
                    }
                } catch (error) {
                    document.getElementById('createResult').innerHTML = `<div class="result error">Network error: ${error}</div>`;
                }
            });
            
            document.getElementById('validateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const qrData = document.getElementById('qrData').value;
                
                try {
                    const response = await fetch('/validate_ticket', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({qr_data: qrData})
                    });
                    const result = await response.json();
                    
                    const resultDiv = document.getElementById('validateResult');
                    if (result.valid) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <h3>✅ Ticket Valid!</h3>
                                <p><strong>Message:</strong> ${result.message}</p>
                                <p><strong>Event:</strong> ${result.ticket_data.event_name}</p>
                                <p><strong>Holder:</strong> ${result.ticket_data.holder_name}</p>
                                <p><strong>Seat:</strong> ${result.ticket_data.seat_number}</p>
                                <p><strong>Issued:</strong> ${result.ticket_data.issue_time}</p>
                            </div>`;
                    } else {
                        resultDiv.innerHTML = `
                            <div class="result error">
                                <h3>❌ Ticket Invalid!</h3>
                                <p><strong>Reason:</strong> ${result.reason}</p>
                            </div>`;
                    }
                } catch (error) {
                    document.getElementById('validateResult').innerHTML = `<div class="result error">Error: ${error}</div>`;
                }
            });
        </script>
    </body>
    </html>
    ''')

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    try:
        event_name = request.form['event_name']
        holder_name = request.form['holder_name']
        seat_number = request.form['seat_number']
        valid_hours = int(request.form['valid_hours'])
        
        result = ticketing_system.create_ticket(event_name, holder_name, seat_number, valid_hours)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/validate_ticket', methods=['POST'])
def validate_ticket():
    try:
        qr_data = request.json['qr_data']
        result = ticketing_system.validate_ticket(qr_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"valid": False, "reason": str(e)})

if __name__ == '__main__':
    print("🎫 Secure QR Ticketing System Starting...")
    print("📋 Features:")
    print("   ✅ AES-256-GCM Encryption")
    print("   ✅ RSA-PSS Digital Signatures") 
    print("   ✅ Single-use Validation")
    print("   ✅ Tamper Detection")
    print("   ✅ Expiry Management")
    print("\n🌐 Web interface: http://localhost:5000")
    print("📁 QR codes saved in current directory")
    print("🗃️ Database: tickets.db")
    app.run(debug=True, host='0.0.0.0', port=5000)