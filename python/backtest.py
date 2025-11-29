import numpy as np


def PnL(df, A, B):
    df['pnl'] = df['position'] * (df[f"{A}_ret"] - df[f"{B}_ret"])
    df['pnl_cum'] = df['pnl'].cumsum()
    return df


def PnL_compound(df, A, B):
    df['pnl_frac'] = df['position'] * (df[f"{A}_ret"] - df[f"{B}_ret"])
    df['capital'] = (1 + df['pnl_frac']).cumprod()
    df['pnl'] = df['capital'].diff().fillna(df['capital'])
    return df


def sharpe_ratio(returns, risk_free_rate=0.0, freq=252):
    excess = returns - risk_free_rate / freq
    if returns.std() == 0:
        return np.nan
    return np.sqrt(freq) * excess.mean() / excess.std()


def sortino_ratio(returns, risk_free_rate=0.0, freq=252):
    excess = returns - risk_free_rate / freq
    downside_std = excess[excess < 0].std()

    if downside_std == 0 or np.isnan(downside_std):
        return np.nan

    return np.sqrt(freq) * excess.mean() / downside_std


def max_drawdown(capital):
    roll_max = capital.cummax()
    drawdown = (capital - roll_max) / roll_max
    return drawdown.min()


def CAGR(capital, freq=252):
    total_periods = len(capital)
    if total_periods == 0:
        return np.nan
    return (capital.iloc[-1])**(freq / total_periods) - 1


def calmar_ratio(capital, freq=252):
    cagr = CAGR(capital, freq)
    mdd = abs(max_drawdown(capital))
    if mdd == 0:
        return np.nan
    return cagr / mdd


def performance_report(returns, capital, risk_free_rate=0.0, freq=252) ->\
        dict:

    report = {
        "Sharpe Ratio": sharpe_ratio(returns, risk_free_rate, freq),
        "Sortino Ratio": sortino_ratio(returns, risk_free_rate, freq),
        "Max Drawdown (%)": 100 * max_drawdown(capital),
        "CAGR (%)": 100 * CAGR(capital, freq),
        "Calmar Ratio": calmar_ratio(capital, freq),
        "Volatility (%)": 100 * returns.std() * np.sqrt(freq),
        "Annualized Return (%)": 100 * returns.mean() * freq,
        "Maximum capital": capital.max(),
        "Minimum capital": capital.min(),
        "Final capital": capital.iloc[-1]
    }

    return report
