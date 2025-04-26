# Pi-Scanner Demo

| file | role | one-liner |
|------|------|-----------|
| `pi_api.py` | **server/api** | Tiny Flask REST endpoint that returns simple JSON for now. |
| `PiScannerGUI.py` | **Desktop client** | Tkinter window with a **Ping Pi** button that shows the server’s reply. |

---

## GUI

**Requirements**

* Python 3.13.3  
* A virtual-env  
* `tkinter` (should be bundled with Python on macOS/Windows)  
* `requests` &nbsp;→ inside your .venv run  
  ```bash
  pip3 install requests
