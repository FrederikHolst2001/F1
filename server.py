from flask import Flask, jsonify
from institutional_core import analyze
from eurusd_core import analyze_eurusd

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "running"
    })

@app.route("/signal")
def signal():

    data = analyze()

    return jsonify(data)
    
@app.route("/eurusd")
def eurusd():

    data = analyze_eurusd()

    return jsonify(data)