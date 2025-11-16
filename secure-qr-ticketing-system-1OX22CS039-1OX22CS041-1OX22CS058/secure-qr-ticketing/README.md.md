SECURE QR TICKETING SYSTEM



Bhuvaneshwari L Kinagi(1OX22CS039)

Brunda P(1OX22CS041)

Gaganasruti R Naidu(1OX22CS058)



Secure QR Ticketing System is a web-based application that securely generates and validates digital tickets using QR codes.

It combines AES-256-GCM encryption (for confidentiality) and RSA-PSS digital signatures (for authenticity) to prevent forgery, duplication, and misuse.

Each ticket is single-use, stored in an SQLite database, and automatically marked as “used” once validated — ensuring secure access for events or transport systems.


How to Run Secure QR Ticketing in VS Code 
Step 1: Open VS Code with PowerShell
1. Open VS Code
2. Open Terminal → Press Ctrl + (backtick) or go to Terminal → New Terminal
3. Ensure PowerShell is selected→ Check bottom-right corner of terminal should say "PowerShell"

---

Step 2: Navigate to Project Directory
```powershell
# Navigate to your project folder
cd "C:\Users\Dell\OneDrive\Desktop\_MINI_ PROJECT\CNS PROJECT\secure-qr-ticketing"
```

---

Step 3: Create Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# If 'python' doesn't work, try:
py -m venv venv
```

---

Step 4: Activate Virtual Environment
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**⚠️ If you get an error about execution policy:**
```powershell
# Fix execution policy (run as Administrator or use this)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

**✅ You'll know it's activated when you see `(venv)` at the start of your prompt:**
```powershell
(venv) PS C:\Users\Dell\OneDrive\Desktop\_MINI_ PROJECT\CNS PROJECT\secure-qr-ticketing>
```

---

Step 5: Install Dependencies
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install cryptography qrcode[pil] flask pillow
```

**Wait for installation to complete...**

---

Step 6: Verify Files Exist
```powershell
# List files in directory
dir

# You should see:
# - Main.py (or main.py)
# - requirements.txt (optional)
```

---

Step 7: Run the Application
```powershell
# Run the application
python Main.py

# If that doesn't work, try:
python main.py
# or
py Main.py
```

---

Step 8: Expected Output
You should see:
```
🎫 Secure QR Ticketing System Starting...
📋 Features:
   ✅ AES-256-GCM Encryption
   ✅ RSA-PSS Digital Signatures
   ✅ Single-use Validation
   ✅ Tamper Detection
   ✅ Expiry Management

🌐 Web interface: http://localhost:5000
📁 QR codes saved in current directory
🗃️ Database: tickets.db
 * Serving Flask app 'Main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```
---

Step 9: Access Web Interface
1. **Open your browser** (Chrome, Firefox, Edge)
2. **Go to:** `http://localhost:5000`
3. You should see the ticketing interface

---

Step 10: Test the System
**Create a Ticket:**
1. Fill in the form:
   - Event Name: `Concert 2024`
   - Holder Name: `John Doe`
   - Seat Number: `A-15`
   - Valid Hours: `24`
2. Click "Create Ticket"
3. Check your project folder for `ticket_[uuid].png`

Validate a Ticket:
1. Scan the QR code or open it in an app
2. Copy the JSON data from the QR code
3. Paste into validation form
4. Click "Validate Ticket"

---

 🛠️ Common Issues & Solutions
Issue 1: "python is not recognized"
```powershell
# Try these alternatives:
py Main.py
python3 Main.py
py -3 Main.py
```

Issue 2: Virtual Environment Won't Activate
```powershell
# Solution 1: Fix execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Solution 2: Use activate.bat instead
.\venv\Scripts\activate.bat

# Solution 3: Activate using full path
& "C:\Users\Dell\OneDrive\Desktop\_MINI_ PROJECT\CNS PROJECT\secure-qr-ticketing\venv\Scripts\Activate.ps1"
```

Issue 3: Module Not Found
```powershell
# Ensure virtual environment is activated (look for (venv))
# Then reinstall:
pip install cryptography qrcode[pil] flask pillow
```

Issue 4: Port 5000 Already in Used
```powershell
# Option 1: Find and kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Option 2: Change port in Main.py (last line)
# Change: app.run(debug=True, host='0.0.0.0', port=5000)
# To: app.run(debug=True, host='0.0.0.0', port=5001)
```

Issue 5: Can't Open Main.py
```powershell
# Check if file exists
Test-Path Main.py

# If False, create it:
code Main.py
# Then copy and paste the code
```

---

🎯 Quick Command Reference

```powershell
# Navigate to project
cd "C:\Users\Dell\OneDrive\Desktop\_MINI_ PROJECT\CNS PROJECT\secure-qr-ticketing"

# Create virtual environment (once)
python -m venv venv

# Activate virtual environment (every time)
.\venv\Scripts\Activate.ps1

# Install dependencies (once)
pip install cryptography qrcode[pil] flask pillow

# Run application
python Main.py

# Stop application
# Press Ctrl+C in terminal

# Deactivate virtual environment
deactivate
```

---

 📁 Project Structure After Running

```
secure-qr-ticketing/
├── venv/                          # Virtual environment folder
├── Main.py                        # Your main application file
├── tickets.db                     # SQLite database (created automatically)
├── private_key.pem               # RSA private key (created automatically)
├── public_key.pem                # RSA public key (created automatically)
└── ticket_[uuid].png             # Generated QR codes
```

---

 ✅ Success Checklist

- [ ] Virtual environment activated `(venv)` visible
- [ ] All packages installed without errors
- [ ] Main.py file exists in directory
- [ ] Application runs without syntax errors
- [ ] Web interface accessible at localhost:5000
- [ ] Can create tickets successfully
- [ ] QR code PNG files generated
- [ ] Can validate tickets successfully

---

🎬 Full Workflow in VS Code

powershell
# 1. Open VS Code and terminal
# 2. Navigate
cd "C:\Users\Dell\OneDrive\Desktop\_MINI_ PROJECT\CNS PROJECT\secure-qr-ticketing"

# 3. Activate environment
.\venv\Scripts\Activate.ps1

# 4. Run
python Main.py

# 5. Open browser → http://localhost:5000

# 6. Stop with Ctrl+C when done

🎉 Your Secure QR Ticketing System is now running!