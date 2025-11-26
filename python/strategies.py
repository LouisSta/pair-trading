from python.spread import compute_spread


def pairs_z_score(df, A: str, B: str, entry, tp, sl, window=None):
    """
    tp<entry<sl
    """
    df["position"] = 0
    position = 0

    for i in range(len(df)):
        if window is None:
            start_idx = 0
        else:
            start_idx = max(0, i - window + 1)

        df_window = df.iloc[start_idx:i+1].copy()

        df_window, beta = compute_spread(df_window, A, B)
        spread_window = df_window[f"spread_{A}_{B}"]

        spr_mean = spread_window.mean()
        spr_std = spread_window.std()
        
        if spr_std == 0:
            z = 0
        else:
            z = (spread_window.iloc[-1] - spr_mean) / spr_std

        if abs(z) < tp or abs(z) > sl:
            position = 0

        elif z > entry:
            position = -1  # short spread

        elif z < -entry:
            position = 1  # long spread

        df.loc[i, "position"] = position

    df["position"] = df["position"].shift(1)  # trade the next day

    return df
