from pathlib import Path


def save_df(df, filename=None):
    if filename is None:
        filename = Path.cwd() / "data/pair.csv"
    df.to_csv(filename, index=False)
