import yfinance as yf

def analyze():

    try:

        df = yf.download("GC=F", period="6mo", interval="1d", progress=False)

        if df.empty:
            return safe_return("No data")

        price = float(df["Close"].iloc[-1])

        liquidity_high = float(df["High"].rolling(40).max().iloc[-1])
        liquidity_low = float(df["Low"].rolling(40).min().iloc[-1])

        ema50 = float(df["Close"].ewm(span=50).mean().iloc[-1])
        ema200 = float(df["Close"].ewm(span=200).mean().iloc[-1])

        signal = "WAIT"
        sl = price
        tp = price

        if ema50 > ema200:

            signal = "BUY"

            sl = liquidity_low

            risk = price - sl

            tp = price + (risk * 3)

        elif ema50 < ema200:

            signal = "SELL"

            sl = liquidity_high

            risk = sl - price

            tp = price - (risk * 3)

        return {

            "signal": signal,
            "entry": price,
            "sl": sl,
            "tp": tp,
            "price": price

        }

    except Exception as e:

        return safe_return(str(e))


def safe_return(error):

    return {

        "signal": "WAIT",
        "entry": 0,
        "sl": 0,
        "tp": 0,
        "price": 0,
        "error": error

    }