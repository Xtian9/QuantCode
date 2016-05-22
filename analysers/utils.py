import pandas as pd
import math

def sharpe_ratio(returns, nperiods, rfrate):
    """
    Calculate annualised Sharpe ratio
        returns = series of returns
        nperiods = number of returns in a year
        rfrate = risk free rate
    """
    # Annualised mean return and volatility
    mu = nperiods * returns.mean()
    sigma = math.sqrt(nperiods) * returns.std()

    return (mu - rfrate) / sigma


def information_ratio(returns, bmreturns, nperiods):
    """
    Calculate annualised information ratio
        returns = series of portfolio returns
        bmreturns = series of benchmark returns
        nperiods = number of returns in a year
    """
    # Excess returns over benchmark
    excreturns = returns - bmreturns

    # Annualised mean excess return and volatility
    mu = nperiods * excreturns.mean()
    sigma = math.sqrt(nperiods) * excreturns.std()

    return mu / sigma


def alpha_beta(returns, bmreturns):
    """
    Calculate porfolio alpha and beta
        returns = series of portfolio returns
        bmreturns = series of benchmark returns
    """
    # Regress portfolio returns against market returns
    ols_res = pd.ols(y=returns, x=bmreturns)

    # alpha is intercept, beta is gradient
    beta, alpha = ols_res.beta

    return alpha, beta


def drawdown(cumrets):
    """
    Calculate max drawdown and max drawdown duration
        cumrets = series of cumulative returns
    """
    #hwm = cumrets.cummax()
    #dd = (1 + hwm) / (1 + cumrets) - 1
    #isdd = dd > 0

    highwatermark = [0]
    drawdown = [0]
    drawdownduration = [0]

    for t in range(1, len(cumrets.index)):

        # High water mark
        hwm = max(cumrets[t], highwatermark[t-1])
        highwatermark.append(hwm)

        # Drawdown
        dd = ( (1+highwatermark[t]) / (1+cumrets[t]) ) - 1
        drawdown.append(dd)

        # Drawdown duration
        ddd = drawdownduration[t-1] + 1 if dd > 0 else 0
        drawdownduration.append(ddd)

    return max(drawdown), max(drawdownduration)

