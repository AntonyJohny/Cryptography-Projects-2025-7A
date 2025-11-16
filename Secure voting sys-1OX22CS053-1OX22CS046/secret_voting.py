import os
import base64
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# ======================== KEY MANAGEMENT ========================
KEY_DIR = "server/keys"
PRIV_KEY_FILE = os.path.join(KEY_DIR, "election_priv.pem")
PUB_KEY_FILE = os.path.join(KEY_DIR, "election_pub.pem")

def generate_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    if not os.path.exists(PRIV_KEY_FILE) or not os.path.exists(PUB_KEY_FILE):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open(PRIV_KEY_FILE, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(PUB_KEY_FILE, "wb") as f:
            f.write(private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

def load_rsa_public():
    with open(PUB_KEY_FILE, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def load_rsa_private():
    with open(PRIV_KEY_FILE, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# ==================== ENCRYPTION / DECRYPTION ====================
def hybrid_encrypt(plaintext_bytes, rsa_public):
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)

    enc_key = rsa_public.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return {
        "enc_key": base64.b64encode(enc_key).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

def hybrid_decrypt(encrypted_dict, rsa_private):
    try:
        enc_key = base64.b64decode(encrypted_dict["enc_key"])
        nonce = base64.b64decode(encrypted_dict["nonce"])
        ciphertext = base64.b64decode(encrypted_dict["ciphertext"])

        aes_key = rsa_private.decrypt(
            enc_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        aesgcm = AESGCM(aes_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
    except Exception as e:
        return f"❌ Decryption Error: {str(e)}"

# ========================== VOTING PAGE ==========================
class VotingPage(tk.Frame):
    def __init__(self, parent, controller, rsa_public):
        super().__init__(parent, bg="#e6f2ff")
        self.controller = controller
        self.rsa_public = rsa_public
        self.encrypted = None  # Store last encrypted vote for passing to decrypt page

        tk.Label(self, text="🗳️ Secure Voting System using Hybrid Cryptography",
                 font=("Helvetica", 18, "bold"), bg="#003366", fg="white", pady=10).pack(fill="x")

        tk.Label(self, text="🔐 Vote Submission", font=("Arial", 14, "bold"), bg="#e6f2ff").pack(pady=5)

        tk.Label(self, text="Enter Voter ID:", font=("Arial", 12), bg="#e6f2ff").pack()
        self.voter_id_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.voter_id_entry.pack(pady=3)

        tk.Label(self, text="Select your candidate:", font=("Arial", 12), bg="#e6f2ff").pack(pady=3)
        self.choice_var = tk.StringVar(value="")
        for candidate in ["Alice", "Bob", "Charlie", "NOTA"]:
            tk.Radiobutton(self, text=candidate, variable=self.choice_var, value=candidate,
                           font=("Arial", 11), bg="#e6f2ff", padx=10).pack(anchor="w", padx=80)

        tk.Button(self, text="Submit Vote", command=self.submit_vote,
                  bg="#28a745", fg="white", font=("Arial", 12), padx=8, pady=3).pack(pady=8)

        tk.Label(self, text="Encrypted Vote Output:", font=("Arial", 12, "bold"), bg="#e6f2ff").pack()
        self.encrypted_output = tk.Text(self, height=6, width=80, font=("Courier", 9), state="disabled", bg="#fff8dc")
        self.encrypted_output.pack(pady=5)

        tk.Button(self, text="Go to Decrypt Page", command=self.go_to_decrypt,
                  bg="#6f42c1", fg="white", font=("Arial", 11), padx=8, pady=3).pack(pady=10)

    def submit_vote(self):
        voter_id = self.voter_id_entry.get().strip()
        candidate = self.choice_var.get()

        if not voter_id:
            messagebox.showwarning("Input Error", "Please enter your Voter ID.")
            return
        if not candidate:
            messagebox.showwarning("Input Error", "Please select a candidate.")
            return

        vote_data = f"VoterID: {voter_id} -> Vote: {candidate}"
        encrypted = hybrid_encrypt(vote_data.encode(), self.rsa_public)
        self.encrypted = encrypted  # Save encrypted vote

        self.encrypted_output.config(state="normal")
        self.encrypted_output.delete(1.0, tk.END)
        self.encrypted_output.insert(tk.END, f"enc_key: {encrypted['enc_key']}\n")
        self.encrypted_output.insert(tk.END, f"nonce: {encrypted['nonce']}\n")
        self.encrypted_output.insert(tk.END, f"ciphertext: {encrypted['ciphertext']}\n")
        self.encrypted_output.config(state="disabled")

    def go_to_decrypt(self):
        if self.encrypted is None:
            if not messagebox.askyesno("No Vote Submitted", "No encrypted vote found. Continue to decrypt page?"):
                return
        self.controller.show_frame("DecryptPage")

# ========================== DECRYPT PAGE ==========================
class DecryptPage(tk.Frame):
    def __init__(self, parent, controller, rsa_private):
        super().__init__(parent, bg="#e6f2ff")
        self.controller = controller
        self.rsa_private = rsa_private

        tk.Label(self, text="🔓 Decrypt Encrypted Vote", font=("Arial", 14, "bold"), bg="#e6f2ff").pack(pady=(10, 5))

        self.enc_key_entry = self.create_labeled_entry("Encrypted AES Key (base64):")
        self.nonce_entry = self.create_labeled_entry("Nonce (base64):")
        self.ciphertext_entry = self.create_labeled_entry("Ciphertext (base64):")

        tk.Button(self, text="Decrypt", command=self.decrypt_input,
                  bg="#007bff", fg="white", font=("Arial", 12), padx=8, pady=3).pack(pady=6)

        tk.Label(self, text="Decrypted Plaintext:", font=("Arial", 12, "bold"), bg="#e6f2ff").pack(pady=4)

        self.decrypted_output = tk.Text(self, height=5, width=80, font=("Courier", 10), state="disabled", bg="#e8f5e9")
        self.decrypted_output.pack(pady=5)

        tk.Button(self, text="Back to Vote Page", command=lambda: controller.show_frame("VotingPage"),
                  bg="#6f42c1", fg="white", font=("Arial", 11), padx=8, pady=3).pack(pady=10)

    def create_labeled_entry(self, label):
        tk.Label(self, text=label, font=("Arial", 10), bg="#e6f2ff").pack()
        entry = tk.Entry(self, font=("Courier", 9), width=80)
        entry.pack(pady=2)
        return entry

    def clear_inputs(self):
        self.enc_key_entry.delete(0, tk.END)
        self.nonce_entry.delete(0, tk.END)
        self.ciphertext_entry.delete(0, tk.END)
        self.decrypted_output.config(state="normal")
        self.decrypted_output.delete(1.0, tk.END)
        self.decrypted_output.config(state="disabled")

    def decrypt_input(self):
        enc_key = self.enc_key_entry.get().strip()
        nonce = self.nonce_entry.get().strip()
        ciphertext = self.ciphertext_entry.get().strip()

        if not enc_key or not nonce or not ciphertext:
            messagebox.showwarning("Input Error", "Please fill in all encryption fields.")
            return

        encrypted_data = {
            "enc_key": enc_key,
            "nonce": nonce,
            "ciphertext": ciphertext
        }

        decrypted = hybrid_decrypt(encrypted_data, self.rsa_private)

        self.decrypted_output.config(state="normal")
        self.decrypted_output.delete(1.0, tk.END)
        self.decrypted_output.insert(tk.END, "✅ Decrypted Plaintext Vote:\n\n")
        self.decrypted_output.insert(tk.END, decrypted)
        self.decrypted_output.config(state="disabled")

# ========================== CONTROLLER APP ===========================
class VotingApp(tk.Tk):
    def __init__(self, rsa_public, rsa_private):
        super().__init__()
        self.title("🗳️ Secret Voting System - Hybrid Encryption")
        self.geometry("720x620")
        self.configure(bg="#e6f2ff")

        self.frames = {}

        container = tk.Frame(self, bg="#e6f2ff")
        container.pack(fill="both", expand=True)

        self.frames["VotingPage"] = VotingPage(container, self, rsa_public)
        self.frames["DecryptPage"] = DecryptPage(container, self, rsa_private)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("VotingPage")

    def show_frame(self, page_name, encrypted_data=None):
        frame = self.frames[page_name]
        frame.tkraise()
        # Removed clear_inputs on decrypt page to keep data persistent

if __name__ == "__main__":
    generate_keys()
    rsa_pub = load_rsa_public()
    rsa_priv = load_rsa_private()

    app = VotingApp(rsa_pub, rsa_priv)
    app.mainloop()
