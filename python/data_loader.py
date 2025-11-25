import yfinance as yf
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def load(ticker1: str, ticker2: str, start="2015-01-01", end="2025-01-01", clean=False):
    df = yf.download([ticker1, ticker2], start=start, end=end)["Adj Close"]
    df.columns = [ticker1, ticker2]
    if clean:
        df = df.dropna()
        filename = f"{ticker1}&{ticker2}_clean.csv"
    else:
        filename = f"{ticker1}&{ticker2}"
    df.to_csv(filename)
    return df
