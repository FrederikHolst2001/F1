from flask import Flask, jsonify
from institutional import institutional_signal
from eurusd_core import analyze_eurusd
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

last_trade = None  # gemmer sidste signal

@app.route("/eurusd")
def eurusd():

    global last_trade

    data = analyze_eurusd()

    price = data["entry"]
    signal = data["signal"]

    # Hvis ingen aktiv trade endnu
    if last_trade is None and signal != "WAIT":
        last_trade = data
        return jsonify(data)

    # Hvis vi har en tidligere trade
    if last_trade:

        old_signal = last_trade["signal"]
        old_entry = last_trade["entry"]
        old_tp = last_trade["tp"]

        # ===== 90% TP reached =====
        if old_signal == "BUY":
            progress = (price - old_entry) / (old_tp - old_entry)

        elif old_signal == "SELL":
            progress = (old_entry - price) / (old_entry - old_tp)

        else:
            progress = 0

        # ===== CONDITION =====
        if progress >= 0.9 and signal != old_signal and signal != "WAIT":

            msg = f"""
EURUSD REVERSAL ALERT 🔥

Previous Signal: {old_signal}
Price reached: {round(progress*100,1)}% of TP

New Signal: {signal}
Entry: {data['entry']}
SL: {data['sl']}
TP: {data['tp']}

Expected reversal zone.
"""

            send_alert(msg)

            last_trade = data  # opdater

    return jsonify(data)