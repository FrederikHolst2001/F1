import yfinance as yf
import numpy as np
from orderflow import get_orderflow
from cot import get_institutional_bias

def analyze():

    df = yf.download("GC=F", period="6mo", interval="1d")

    price = float(df["Close"].iloc[-1])

    # liquidity zones
    liquidity_high = df["High"].rolling(40).max().iloc[-1]
    liquidity_low = df["Low"].rolling(40).min().iloc[-1]

    # institutional trend
    ema50 = df["Close"].ewm(span=50).mean().iloc[-1]
    ema200 = df["Close"].ewm(span=200).mean().iloc[-1]

    # orderflow
    flow = get_orderflow()

    bias = get_institutional_bias()

    signal = "WAIT"

    entry = price
    sl = price
    tp = price

    # Institutional buy logic
    if ema50 > ema200 and flow["imbalance"] > 0 and bias == "BULLISH":

        signal = "BUY"

        sl = liquidity_low

        risk = entry - sl

        tp = entry + (risk * 3)

    # Institutional sell logic
    elif ema50 < ema200 and flow["imbalance"] < 0 and bias == "BEARISH":

        signal = "SELL"

        sl = liquidity_high

        risk = sl - entry

        tp = entry - (risk * 3)

    return {

        "signal": signal,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "price": price,
        "institutional_bias": bias,
        "orderflow_imbalance": flow["imbalance"],
        "liquidity_high": liquidity_high,
        "liquidity_low": liquidity_low

    }