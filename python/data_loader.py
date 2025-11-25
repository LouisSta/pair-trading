import yfinance as yf
from pathlib import Path
import pandas as pd


def load(ticker1: str, ticker2: str, start="2015-01-01", end="2025-01-01",
         clean=True, data_dir=None):
    if data_dir is None:
        data_dir = Path.cwd() / "data"
    data_dir.mkdir(exist_ok=True)
    df = yf.download([ticker1, ticker2], start=start, end=end, auto_adjust=True)
    df = df["Close"]
    df.columns = [ticker1, ticker2]
    if clean:
        df = df.dropna()
        filename = data_dir / f"{ticker1}&{ticker2}_clean.csv"
    else:
        filename = data_dir / f"{ticker1}&{ticker2}.csv"
    df.to_csv(filename)
    return df


def load_prices_and_returns(ticker1: str, ticker2: str,
                            start="2015-01-01", end="2025-01-01",
                            data_dir=None):
    if data_dir is None:
        data_dir = Path.cwd() / "data"
    data_dir.mkdir(exist_ok=True)
    df = yf.download([ticker1, ticker2], start=start, end=end, auto_adjust=True)
    df = df["Close"]
    returns = df.pct_change()
    df = pd.concat([df, returns], axis=1)
    df.dropna(inplace=True)
    filename = data_dir / f"P&R_{ticker1}&{ticker2}.csv"
    df.columns = [ticker1, ticker2, f"{ticker1}_ret", f"{ticker2}_ret"]
    df.to_csv(filename)
    return df
