# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os, json, uuid
from ciphers import encrypt_note, decrypt_note

app = Flask(__name__)
app.secret_key = "dev-secret"  # for demo only. Change in real deployments.

DATA_DIR = "data"
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

@app.route("/")
def index():
    notes = load_notes()
    return render_template("index.html", notes=notes)

@app.route("/new", methods=["GET", "POST"])
def new_note():
    if request.method == "POST":
        title = request.form.get("title", "Untitled")
        plaintext = request.form.get("plaintext", "")
        try:
            caesar_shift = int(request.form.get("caesar_shift", "3")) % 26
        except:
            caesar_shift = 3
        vkey = request.form.get("vkey", "").strip()
        pkey = request.form.get("pkey", "").strip()
        if not vkey or not pkey:
            flash("Vigenere key and Playfair keyword are required.", "danger")
            return redirect(url_for("new_note"))
        cipher, metadata = encrypt_note(plaintext, caesar_shift, vkey, pkey)
        note = {
            "id": str(uuid.uuid4()),
            "title": title,
            "ciphertext": cipher,
            "metadata": metadata
        }
        notes = load_notes()
        notes.append(note)
        save_notes(notes)
        flash("Note encrypted and saved (ciphertext stored).", "success")
        return redirect(url_for("index"))
    return render_template("new.html")

@app.route("/view/<note_id>", methods=["GET","POST"])
def view_note(note_id):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    if not note:
        flash("Note not found.", "danger")
        return redirect(url_for("index"))
    decrypted_text = None
    if request.method == "POST":
        try:
            caesar_shift = int(request.form.get("caesar_shift", "3")) % 26
        except:
            caesar_shift = 3
        vkey = request.form.get("vkey", "").strip()
        pkey = request.form.get("pkey", "").strip()
        if not vkey or not pkey:
            flash("Vigenere key and Playfair keyword are required to decrypt.", "danger")
        else:
            try:
                decrypted_text = decrypt_note(note["ciphertext"], caesar_shift, vkey, pkey, note["metadata"])
            except Exception as e:
                decrypted_text = None
                flash("Decryption failed (wrong keys or corrupted data).", "danger")
    return render_template("view.html", note=note, decrypted=decrypted_text)

if __name__ == "__main__":
    app.run(debug=True)
