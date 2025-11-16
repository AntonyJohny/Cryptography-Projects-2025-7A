import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from pyzbar import pyzbar
import requests
import json

# =========================
# App Configuration
# =========================
class TicketDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Ticket Manager")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.api_base = "http://localhost:5000"
        self.dark_mode = False

        # Colors
        self.light_bg = "#f0f0f0"
        self.dark_bg = "#2c2c2c"
        self.primary_color = "#4a90e2"
        self.text_color = "#000000"
        self.text_color_dark = "#ffffff"

        self.root.configure(bg=self.light_bg)

        # Sidebar
        self.sidebar = tk.Frame(root, width=180, bg=self.primary_color)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = tk.Frame(root, bg=self.light_bg)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.create_main_ui()

    # =========================
    # Sidebar
    # =========================
    def create_sidebar(self):
        tk.Label(self.sidebar, text="MENU", bg=self.primary_color, fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        
        buttons = [
            ("Scan QR", self.scan_qr),
            ("Upload Ticket", self.upload_ticket),
            ("Toggle Theme", self.toggle_theme),
            ("Exit", self.root.quit)
        ]
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, command=command,
                            bg="#ffffff", fg="#000000", relief="flat", bd=0, font=("Arial", 12),
                            activebackground="#d9d9d9", cursor="hand2")
            btn.pack(pady=10, padx=10, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#d9d9d9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff"))

    # =========================
    # Main UI
    # =========================
    def create_main_ui(self):
        self.title_label = tk.Label(self.main_frame, text="Secure Ticket Manager", font=("Arial", 20, "bold"),
                                    bg=self.light_bg, fg=self.text_color)
        self.title_label.pack(pady=30)

        self.info_label = tk.Label(self.main_frame, text="Ready to scan or upload tickets", font=("Arial", 14),
                                   bg=self.light_bg, fg=self.text_color)
        self.info_label.pack(pady=20)

        # Placeholder for QR image preview
        self.img_label = tk.Label(self.main_frame, bg=self.light_bg)
        self.img_label.pack(pady=10)

    # =========================
    # Functions
    # =========================
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = self.dark_bg if self.dark_mode else self.light_bg
        fg = self.text_color_dark if self.dark_mode else self.text_color
        self.main_frame.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=fg)
        self.info_label.configure(bg=bg, fg=fg)

    def scan_qr(self):
        cap = cv2.VideoCapture(0)
        self.info_label.config(text="Scanning QR code... Press 'q' to exit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            decoded_objs = pyzbar.decode(frame)
            for obj in decoded_objs:
                qr_data = obj.data.decode("utf-8")
                self.info_label.config(text=f"QR Data: {qr_data}")
                cap.release()
                cv2.destroyAllWindows()
                return
            cv2.imshow("QR Scanner - Press q to exit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.info_label.config(text="Scan cancelled or no QR found.")

    def upload_ticket(self):
        file_path = filedialog.askopenfilename(title="Select Ticket Image")
        if file_path:
            self.info_label.config(text=f"Uploading: {file_path}")
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            self.img_label.config(image=img)
            self.img_label.image = img
        else:
            self.info_label.config(text="No file selected.")

# =========================
# Run App
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = TicketDesktopApp(root)
    root.mainloop()
