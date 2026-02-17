import yfinance as yf
import numpy as np

def get_orderflow():

    df = yf.download("GC=F", period="30d", interval="1h")

    df["buy_pressure"] = df["Close"] > df["Open"]
    df["sell_pressure"] = df["Close"] < df["Open"]

    buy_volume = df[df["buy_pressure"]]["Volume"].sum()
    sell_volume = df[df["sell_pressure"]]["Volume"].sum()

    imbalance = buy_volume - sell_volume

    return {

        "buy_volume": float(buy_volume),
        "sell_volume": float(sell_volume),
        "imbalance": float(imbalance)

    }