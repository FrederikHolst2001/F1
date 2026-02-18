import yfinance as yf
import pandas as pd

def analyze_eurusd():

    try:

        # Første forsøg (M15)
        m15 = yf.download("EURUSD=X", period="5d", interval="15m", progress=False)

        if isinstance(m15.columns, pd.MultiIndex):
            m15.columns = m15.columns.get_level_values(0)

        if m15.empty:
            return safe_return("Feed unavailable")

        price = float(m15["Close"].iloc[-1])

        highs = m15["High"]
        lows = m15["Low"]
        closes = m15["Close"]

        # Simple structure
        bos_up = highs.iloc[-2] > highs.iloc[-4]
        bos_down = lows.iloc[-2] < lows.iloc[-4]

        # ATR
        high_low = highs - lows
        high_close = (highs - closes.shift()).abs()
        low_close = (lows - closes.shift()).abs()

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]

        signal = "WAIT"
        sl = price
        tp = price

        if bos_up:
            signal = "BUY"
            sl = price - atr
            tp = price + (atr * 2)

        elif bos_down:
            signal = "SELL"
            sl = price + atr
            tp = price - (atr * 2)

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