import yfinance as yf


def load_data(ticker1: str, ticker2: str):
    df = yf.download(tickers=[ticker1, ticker2],
                       start="2015-01-01",
                       end="2025-01-01")["Adj Close"]
    df.columns = [ticker1, ticker2]
    df.dropna(inplace=True)
    df.to_csv(f"../data/{ticker1}&{ticker2}.csv")
    return df
