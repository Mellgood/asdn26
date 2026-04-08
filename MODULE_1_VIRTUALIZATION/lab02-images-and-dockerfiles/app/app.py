from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Return information about the container."""
    hostname = socket.gethostname()

    # Try to get the container's IP address
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "unknown"

    return jsonify({
        "message": "Hello from ASDN Lab!",
        "hostname": hostname,
        "ip_address": ip_address,
        "platform": os.uname().sysname,
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
