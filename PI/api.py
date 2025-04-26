# pi_api.py  ── a tiny Flask REST server
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")                      # GET http://<pi-ip>:5000/
def root():
    return jsonify(message="👋  Hi from your Raspberry Pi!"), 200

@app.route("/hello")
def hello():
    return jsonify(message="Hello there!"), 200

@app.route("/echo/<msg>")
def echo(msg):
    """Repeat whatever the caller puts after /echo/…"""
    return jsonify(echo=msg), 200

@app.route("/health")
def health():
    """Simple liveness probe for scripts or load-balancers."""
    return {"ok": True}, 200


if __name__ == "__main__":
    # 0.0.0.0 makes it reachable from other machines.
    # Change port if 5000 is already taken.
    app.run(host="0.0.0.0", port=5000, debug=False)