"""
web api for haipproxy
"""
import os

from flask import Flask, jsonify

from haipproxy.client import ProxyClient

pc = ProxyClient()
app = Flask(__name__)
app.debug = bool(os.environ.get("DEBUG"))
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.errorhandler(404)
def not_found(e):
    return jsonify({'reason': 'resource not found', 'status_code': 404})


@app.errorhandler(500)
def not_found(e):
    return jsonify({'reason': 'internal server error', 'status_code': 500})


@app.route("/pool/get/<protocol>")
def get_proxies(protocol):
    return jsonify({
        'pool': [p for p in pc.next_proxy(protocol)],
        'resource': protocol,
        'status_code': 200
    })
