# api.py
from flask import Flask, send_file, current_app, make_response
import os
from capture import capture_still

app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "👋 Pi is connected"}, 200

@app.route("/hello")
def hello():
    return {"message": "Hello endpoint works"}, 200

@app.route("/health")
def health():
    return {"ok": True}, 200

@app.route("/capture", methods=["GET"])
def capture():
    dst = "/tmp/preview.jpg"
    try:
        capture_still(dst)
    except Exception as e:
        current_app.logger.error(f"Capture failed: {e}", exc_info=True)
        return {"error": "Capture failed"}, 500

    if not os.path.exists(dst):
        return {"error": "File missing"}, 500

    # send_file without cache_timeout, then override headers
    response = send_file(dst, mimetype="image/jpeg", conditional=False)
    # disable all caching
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    # debug=False ensures a single-threaded server (avoids camera lock issues)
    app.run(host="0.0.0.0", port=5000, debug=False)