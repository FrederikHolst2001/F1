from flask import Flask, jsonify
from institutional_core import analyze

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