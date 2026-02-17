from flask import Flask, jsonify
from institutional_core import analyze
from telegram import send_alert

app = Flask(__name__)

last_signal = None

@app.route("/")
def home():
    return "Institutional system running"

@app.route("/signal")
def signal():

    global last_signal

    data = analyze()

    if data["signal"] != last_signal and data["signal"] != "WAIT":

        msg = f"""
XAUUSD INSTITUTIONAL SIGNAL

Signal: {data['signal']}

Entry: {data['entry']:.2f}
Stop Loss: {data['sl']:.2f}
Take Profit: {data['tp']:.2f}

Bias: {data['institutional_bias']}
Orderflow imbalance: {data['orderflow_imbalance']}

Hold time: 3–10 days
"""

        send_alert(msg)

        last_signal = data["signal"]

    return jsonify(data)