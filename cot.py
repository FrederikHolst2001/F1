import yfinance as yf

def get_institutional_bias():

    df = yf.download("GC=F", period="90d", interval="1d")

    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()

    if df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:

        return "BULLISH"

    else:

        return "BEARISH"