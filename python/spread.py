import statsmodels.api as sm


def compute_spread(df, A, B):
    # regression (OLS)
    x = sm.add_constant(df[B])
    y = df[A]
    model = sm.OLS(y, x).fit()
    beta = model.params[B]
    # spread
    df[f"spread_{A}_{B}"] = df[A] - beta * df[B]
    return df, beta
