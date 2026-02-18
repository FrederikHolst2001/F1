import yfinance as yf

def analyze_eurusd():

    try:

        # Trend filter (H1)
        h1 = yf.download("EURUSD=X", period="7d", interval="1h", progress=False)

        # Entry precision (M15)
        m15 = yf.download("EURUSD=X", period="2d", interval="15m", progress=False)

        if h1.empty or m15.empty:
            return safe_return("No data")

        price = m15["Close"].iloc[-1].item()

        # H1 Trend
        ema20 = h1["Close"].ewm(span=20).mean().iloc[-1].item()
        ema50 = h1["Close"].ewm(span=50).mean().iloc[-1].item()

        # Recent swing structure (last 8 M15 candles)
        swing_low = m15["Low"].rolling(8).min().iloc[-1].item()
        swing_high = m15["High"].rolling(8).max().iloc[-1].item()

        signal = "WAIT"
        sl = price
        tp = price

        # BUY condition
        if ema20 > ema50:

            signal = "BUY"
            sl = swing_low
            risk = price - sl
            tp = price + (risk * 1.8)

        # SELL condition
        elif ema20 < ema50:

            signal = "SELL"
            sl = swing_high
            risk = sl - price
            tp = price - (risk * 1.8)

        return {
            "pair": "EURUSD",
            "signal": signal,
            "entry": round(price,5),
            "sl": round(sl,5),
            "tp": round(tp,5),
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