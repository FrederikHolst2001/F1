import yfinance as yf
import pandas as pd

def analyze_eurusd():

    try:

        # Trend (H1)
        h1 = yf.download("EURUSD=X", period="7d", interval="1h", progress=False)

        # Entry precision (M15)
        m15 = yf.download("EURUSD=X", period="2d", interval="15m", progress=False)

        if h1.empty or m15.empty:
            return safe_return("No data")

        price = m15["Close"].iloc[-1].item()

        # ===== TREND FILTER =====
        ema20 = h1["Close"].ewm(span=20).mean().iloc[-1].item()
        ema50 = h1["Close"].ewm(span=50).mean().iloc[-1].item()

        bullish_trend = ema20 > ema50
        bearish_trend = ema20 < ema50

        # ===== STRUCTURE BREAK =====
        last_high = m15["High"].iloc[-2]
        prev_high = m15["High"].iloc[-3]

        last_low = m15["Low"].iloc[-2]
        prev_low = m15["Low"].iloc[-3]

        structure_break_up = last_high > prev_high
        structure_break_down = last_low < prev_low

        # ===== VOLUME SPIKE =====
        avg_volume = m15["Volume"].rolling(10).mean().iloc[-1]
        current_volume = m15["Volume"].iloc[-1]

        volume_spike = current_volume > avg_volume * 1.5

        # ===== ATR STOP =====
        high_low = m15["High"] - m15["Low"]
        high_close = (m15["High"] - m15["Close"].shift()).abs()
        low_close = (m15["Low"] - m15["Close"].shift()).abs()

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)

        atr = true_range.rolling(14).mean().iloc[-1]

        signal = "WAIT"
        sl = price
        tp = price

        # ===== BUY SNIPER =====
        if bullish_trend and structure_break_up and volume_spike:

            signal = "BUY"
            sl = price - atr
            risk = atr
            tp = price + (risk * 2)

        # ===== SELL SNIPER =====
        elif bearish_trend and structure_break_down and volume_spike:

            signal = "SELL"
            sl = price + atr
            risk = atr
            tp = price - (risk * 2)

        return {
            "pair": "EURUSD",
            "signal": signal,
            "entry": round(price,5),
            "sl": round(sl,5),
            "tp": round(tp,5),
            "atr": round(atr,5),
            "max_hold": "4 hours"
        }

    except Exception as e:
        return safe_return(str(e))


def safe_return(error):
    return {
        "pair": "EURUSD",
        "signal": "WAIT",
        "entry": 0,
        "sl": 0,
        "tp": 0,
        "error": error
    }