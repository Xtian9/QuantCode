import pandas as pd
import numpy as np
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


def rolling_sharpe(returns, nperiods, rfrate, window):
    """
    Calculate rolling Sharpe ratio
        returns = series of returns
        nperiods = number of returns in a year
        rfrate = risk free rate
        window = number of periods in rolling window
    """
    mu = nperiods * pd.rolling_mean(returns, window)
    sigma = math.sqrt(nperiods) * pd.rolling_std(returns, window)

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


def rolling_max(series):
    """
    Calculate rolling maximum of a series
    """
    return series.cummax()


def rolling_drawdown(cumrets):
    """
    Calculate rolling drawdown
        cumrets = series of cumulative returns
        dd = series of drawdowns (positive)
    """
    cummax = rolling_max(cumrets)
    dd = (1 + cummax) / (1 + cumrets) - 1

    return dd


def rolling_drawdown_duration(cumrets):
    """
    Calculate rolling drawdown duration
        cumrets = series of cumulative returns
        dd = series of drawdown durations
    """
    drawdown = rolling_drawdown(cumrets)
    drawdownduration = pd.Series(index=cumrets.index)

    prev_date = None
    for i, (date, ret) in enumerate(cumrets.iteritems()):

        if i == 0:
            drawdownduration[date] = 0
            continue

        else:
            dd = drawdown[date]
            ddd = drawdownduration[prev_date] + 1 if dd > 0 else 0
            drawdownduration[date] = ddd

        prev_date = date

    return drawdownduration


def max_drawdown(cumrets):
    """
    Calculate maximum drawdown size
        cumrets = series of cumulative returns
    """
    return rolling_drawdown(cumrets).max()


def max_drawdown_duration(cumrets):
    """
    Calculate maximum drawdown duration
        cumrets = series of cumulative returns
    """
    return rolling_drawdown_duration(cumrets).max()


def sort_drawdowns(cumrets):
    """
    Return drawdown periods ordered by
    drawdown size and drawdown duration
        cumrets = series of cumulative returns
        dd_info = list of tuples
                  (start_date, end_date, dd)
                  ordered by drawdown size
        ddd_info = list of tuples
                   (start_date, end_date, ddd)
                   ordered by drawdown duration
    """
    dd_info, ddd_info = [], []

    dd  = rolling_drawdown(cumrets)
    ddd = rolling_drawdown_duration(cumrets)

    # Holders
    start_date, end_date = None, None
    dd_vec, ddd_vec = [], []

    for t, date in enumerate(cumrets.index):
        if np.isnan(cumrets[date]):
            continue

        # No drawdown
        if ddd[date] == 0:
            # End of drawdown
            if start_date is not None:
                end_date = date
                dd_info.append((start_date, end_date, max(dd_vec)))
                ddd_info.append((start_date, end_date, max(ddd_vec)))

                start_date, end_date = None, None
                dd_vec, ddd_vec = [], []

        # Continuation or start of drawdown
        else:
            # Start of drawdown
            if start_date is None:
                start_date = date

            dd_vec.append(dd[date])
            ddd_vec.append(ddd[date])

    for info in (dd_info, ddd_info):
        info.sort(key=lambda tup: tup[2], reverse=True)

    return dd_info, ddd_info


#def drawdown_DEPRECATED(cumrets):
#    """
#    Calculate high water mark, drawdown and 
#    drawdown duration series
#        cumrets = series of cumulative returns
#    """
#    highwatermark = [0]
#    drawdown = [0]
#    drawdownduration = [0]
#
#    for t in range(1, len(cumrets.index)):
#
#        # High water mark
#        hwm = max(cumrets[t], highwatermark[t-1])
#        highwatermark.append(hwm)
#
#        # Drawdown
#        dd = ( (1+highwatermark[t]) / (1+cumrets[t]) ) - 1
#        drawdown.append(dd)
#
#        # Drawdown duration
#        ddd = drawdownduration[t-1] + 1 if dd > 0 else 0
#        drawdownduration.append(ddd)
#
#    return max(drawdown), max(drawdownduration)

