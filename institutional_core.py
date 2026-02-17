import yfinance as yf

def analyze():

    try:

        df = yf.download("GC=F", period="6mo", interval="1d", progress=False)

        if df.empty:
            return safe_return("No data")

        price = df["Close"].iloc[-1].item()

        liquidity_high = df["High"].rolling(40).max().iloc[-1].item()

        liquidity_low = df["Low"].rolling(40).min().iloc[-1].item()

        ema50 = df["Close"].ewm(span=50).mean().iloc[-1].item()

        ema200 = df["Close"].ewm(span=200).mean().iloc[-1].item()

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