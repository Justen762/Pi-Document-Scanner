import io
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import requests

class PiScannerGUI(tk.Tk):
    PI_HOST = "192.168.137.32"   # ← your Pi’s IP
    # interval between frames in milliseconds (lower = higher fps)
    STREAM_INTERVAL_MS = 60  # ~20 fps

    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Document Scanner")
        self.geometry("400x600")
        self.last_image = None
        self.streaming = False
        self._build_widgets()
        # start the live viewfinder
        self.start_stream()

    def _build_widgets(self):
        preview_container = tk.Frame(
            self, width=360, height=480, relief="groove", bd=2, bg="black"
        )
        preview_container.pack(pady=10)
        preview_container.pack_propagate(False)

        self.preview = tk.Label(preview_container, bg="black")
        self.preview.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        for label, cmd in [("Ping Pi", self.ping_pi),
                           ("📸 Capture", self.capture),
                           ("💾 Download", self.download),
                           ("Quit", self.quit_app)]:
            btn = tk.Button(btn_frame, text=label, command=cmd)
            btn.pack(side="left", padx=4)

        self.status = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status).pack(pady=6)

    def start_stream(self):
        if not self.streaming:
            self.streaming = True
            self.stream_preview()

    def stop_stream(self):
        self.streaming = False

    def stream_preview(self):
        if not self.streaming:
            return
        try:
            # use the faster preview endpoint
            url = f"http://{self.PI_HOST}:5000/preview"
            r = requests.get(url, timeout=1)
            r.raise_for_status()
            img = Image.open(io.BytesIO(r.content))

            # scale to fit container
            container = self.preview.master
            container.update_idletasks()
            max_w = container.winfo_width()
            max_h = container.winfo_height()
            img.thumbnail((max_w, max_h), Image.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            self.preview.config(image=photo)
            self.preview.image = photo
            self.status.set("Streaming")
        except Exception:
            # ignore occasional errors silently or show minimal status
            self.status.set("Streaming...")
        finally:
            # schedule next frame for high fps
            self.after(self.STREAM_INTERVAL_MS, self.stream_preview)

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
        # pause streaming to avoid conflict
        self.stop_stream()
        try:
            r = requests.get(f"http://{self.PI_HOST}:5000/capture", timeout=5)
            r.raise_for_status()

            orig = Image.open(io.BytesIO(r.content))
            self.last_image = orig.copy()

            # display thumbnail of the captured still
            container = self.preview.master
            container.update_idletasks()
            max_w = container.winfo_width()
            max_h = container.winfo_height()
            thumb = orig.copy()
            thumb.thumbnail((max_w, max_h), Image.LANCZOS)

            photo = ImageTk.PhotoImage(thumb)
            self.preview.config(image=photo)
            self.preview.image = photo
            self.status.set("Captured ✔️")
        except Exception as e:
            self.status.set("Capture failed")
            messagebox.showerror("Capture", str(e))

    def download(self):
        if self.last_image is None:
            messagebox.showerror(
                "Download", "No image to save. Please capture first."
            )
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG Image", "*.jpg"),
                ("PNG Image", "*.png"),
                ("All Files", "*.*"),
            ],
            initialdir=os.path.expanduser("~/Desktop"),
            title="Save Image As",
        )
        if file_path:
            try:
                self.last_image.save(file_path)
                self.status.set(f"Saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))
        # resume viewfinder
        self.start_stream()

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Close the scanner UI?" ):
            self.destroy()

if __name__ == "__main__":
    PiScannerGUI().mainloop()
