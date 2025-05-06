# PiScannerGUI.py
import io
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

class PiScannerGUI(tk.Tk):
    PI_HOST = "192.168.137.145"   # ← your Pi’s IP

    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Document Scanner")
        self.geometry("400x600")
        self._build_widgets()

    def _build_widgets(self):
        # Create a fixed-size container for the viewfinder (360×480 px)
        preview_container = tk.Frame(self,
                                     width=360,
                                     height=480,
                                     relief="groove",
                                     bd=2,
                                     bg="black")
        preview_container.pack(pady=10)
        # Prevent the container from resizing to its contents
        preview_container.pack_propagate(False)

        # This Label will hold the live thumbnail
        self.preview = tk.Label(preview_container, bg="black")
        self.preview.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Ping Pi",
                  command=self.ping_pi).grid(row=0, column=0, padx=4)
        tk.Button(btn_frame, text="📸 Capture",
                  command=self.capture).grid(row=0, column=1, padx=4)
        tk.Button(btn_frame, text="Quit",
                  command=self.quit_app).grid(row=0, column=2, padx=4)

        self.status = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status).pack(pady=6)

    def ping_pi(self):
        try:
            r = requests.get(f"http://{self.PI_HOST}:5000/hello", timeout=3)
            r.raise_for_status()
            msg = r.json().get("message", "")
            self.status.set(f"Pi says: {msg}")
        except Exception as e:
            self.status.set("Ping failed")
            messagebox.showerror("Ping Pi", str(e))

    def capture(self):
        try:
            r = requests.get(f"http://{self.PI_HOST}:5000/capture", timeout=5)
            r.raise_for_status()

            # load JPEG bytes
            img = Image.open(io.BytesIO(r.content))

            # Figure out our container size (360×480)
            container = self.preview.master
            container.update_idletasks()
            max_w = container.winfo_width()
            max_h = container.winfo_height()

            # Scale down with aspect‐ratio preserved
            img.thumbnail((max_w, max_h), Image.LANCZOS)

            photo = ImageTk.PhotoImage(img)

            # swap into the label
            self.preview.config(image=photo, text="")
            self.preview.image = photo

            self.status.set("Captured ✔️")
        except Exception as e:
            self.status.set("Capture failed")
            messagebox.showerror("Capture", str(e))

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Close the scanner UI?"):
            self.destroy()

if __name__ == "__main__":
    PiScannerGUI().mainloop()
