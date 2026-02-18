import yfinance as yf
import pandas as pd
import numpy as np

def analyze_eurusd():

    try:

        m15 = yf.download("EURUSD=X", period="3d", interval="15m", progress=False)

        if m15.empty:
            return safe_return("No data")

        price = m15["Close"].iloc[-1].item()

        highs = m15["High"]
        lows = m15["Low"]
        closes = m15["Close"]

        # =========================
        # STRUCTURE BREAK (BOS)
        # =========================

        recent_high = highs.iloc[-4]
        previous_high = highs.iloc[-6]

        recent_low = lows.iloc[-4]
        previous_low = lows.iloc[-6]

        bos_up = recent_high > previous_high
        bos_down = recent_low < previous_low

        # =========================
        # LIQUIDITY SWEEP
        # =========================

        sweep_low = lows.iloc[-2] < lows.iloc[-5]
        sweep_high = highs.iloc[-2] > highs.iloc[-5]

        # =========================
        # FAIR VALUE GAP (FVG)
        # =========================

        fvg_bull = lows.iloc[-2] > highs.iloc[-4]
        fvg_bear = highs.iloc[-2] < lows.iloc[-4]

        # =========================
        # ATR for dynamic stop
        # =========================

        high_low = highs - lows
        high_close = (highs - closes.shift()).abs()
        low_close = (lows - closes.shift()).abs()

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]

        # =========================
        # DEMAND / SUPPLY ZONES
        # =========================

        demand_zone = lows.rolling(10).min().iloc[-1]
        supply_zone = highs.rolling(10).max().iloc[-1]

        signal = "WAIT"
        sl = price
        tp = price

        # =========================
        # BUY CONDITIONS
        # =========================

        if bos_up and sweep_low and fvg_bull:

            signal = "BUY"
            sl = price - atr
            risk = atr
            tp = price + (risk * 2)

        # =========================
        # SELL CONDITIONS
        # =========================

        elif bos_down and sweep_high and fvg_bear:

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
            "bos_up": bool(bos_up),
            "bos_down": bool(bos_down),
            "fvg_bull": bool(fvg_bull),
            "fvg_bear": bool(fvg_bear),
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