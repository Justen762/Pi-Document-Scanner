from picamera2 import Picamera2
import threading
import numpy as np
import io
from PIL import Image
import time

# serialize all camera access
_camera_lock = threading.Lock()

def capture_still(output_path: str, size=(2480, 3508), quality=80):
    """
    Grabs a preview‐sized JPEG (RGB888) and write it to output_path
    """
    with _camera_lock:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"size": size, "format": "RGB888"}
        )
        picam2.configure(config)
        picam2.start()
        # warm up AE/AWB
        time.sleep(1)
        # grab the frame
        array = picam2.capture_array("main")
        picam2.stop()
        picam2.close()
    # ensure the numpy array is C-contiguous
    array = np.ascontiguousarray(array)
    img = Image.fromarray(array)
    #convert to greyscale to reduce filesize
    img = img.convert("L")
    img.save(output_path,format="JPEG", quality=85, optimize=True)
    print(f"[capture.py] Wrote preview to {output_path}")

def quick_capture(size=(620, 877), quality=60):
    with _camera_lock:
        picam2 = Picamera2()
        # low-res preview configuration
        config = picam2.create_preview_configuration(
            main={"size": size, "format": "RGB888"}
        )
        picam2.configure(config)
        picam2.start()
        # minimal frame delay
        time.sleep(0.1)
        array = picam2.capture_array("main")
        picam2.stop()
        picam2.close()
    array = np.ascontiguousarray(array)
    img = Image.fromarray(array)
    img = img.convert("L")                # single-channel grayscale
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()
