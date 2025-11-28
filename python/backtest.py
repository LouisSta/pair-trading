def PnL(df, A, B):
    df['pnl'] = df['position'] * (df[f"{A}_ret"] - df[f"{B}_ret"])
    df['pnl_cum'] = df['pnl'].cumsum()
    return df


def PnL_compound(df, A, B):
    df['pnl_frac'] = df['position'] * (df[f"{A}_ret"] - df[f"{B}_ret"])
    df['capital'] = (1 + df['pnl_frac']).cumprod()
    df['pnl'] = df['capital'].diff().fillna(df['capital'])
    return df


def max_drawdown(df, col='capital'):
    series = df[col]
    roll_max = series.cummax()
    dd = series / roll_max - 1
    return dd.min()


def sharpe_ratio(df, freq=252):  # 252 days per year]
    return (df['pnl'].mean() / df['pnl'].std()) * (freq ** 0.5)


def sortino_ratio(df, freq=252):
    ret = df['pnl']
    downside = ret[ret < 0]
    return (ret.mean() / downside.std()) * (freq ** 0.5)
