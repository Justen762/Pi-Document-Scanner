import tkinter as tk
from tkinter import messagebox
import requests

class PiScannerGUI(tk.Tk):
    PI_HOST = "192.168.137.145"     # address Flask printed

    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Document Scanner")
        self.geometry("400x340")
        self._build_widgets()

    def _build_widgets(self):
        self.preview = tk.Label(self, text="View-finder\n(placeholder)",
                                width=40, height=10, relief="groove")
        self.preview.pack(pady=10)

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
        url = f"http://{self.PI_HOST}:5000/"
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()                     # 4xx / 5xx -> exception
            # /hello returns {"message": "Hello there!"}
            msg = r.json().get("message", r.text)
            self.status.set(f"Pi says: {msg}")
        except Exception as e:
            self.status.set("Ping failed")
            messagebox.showerror("Ping Pi", str(e))

    # stubs that we’ll fill in later
    def capture(self):
        self.status.set("Capturing… (stub)")

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Close the scanner UI?"):
            self.destroy()

if __name__ == "__main__":
    PiScannerGUI().mainloop()
