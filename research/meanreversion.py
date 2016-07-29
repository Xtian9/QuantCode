from core.stack import *
from datahandler import DataHandler
from utils import plotting
import statsmodels.tsa.stattools as ts
#import statsmodels.formula.api as sm
import math


## __________________________________________________________________________||
## Config

#symbols = ['GOOG']
#qcodes = ['GOOG/NASDAQ_GOOG']
#date_start = "2000-01-01"
#date_end   = "2013-01-01"

symbols    = ['AREX','WLL']
qcodes     = ['GOOG/NASDAQ_AREX','GOOG/NYSE_WLL']
date_start = "2012-01-01"
date_end   = "2013-01-01"

frequency  = "daily"
datas      = ['Close']
trade_time = 'Close'

#TEST = 'adf'


## __________________________________________________________________________||
## Main

def main():
    
    data_handler = DataHandler(symbols, qcodes, date_start, date_end, 
                               frequency, datas)
    datas_symbols = data_handler.generate_data()
    
    if len(symbols) == 1:
        prices = datas_symbols[trade_time].iloc[:,0]
    else:
        prices = datas_symbols[trade_time]

    #plot_time_series(prices)
    
    #___ Single asset ___#
    #print adf(prices)
    #print hurst(prices, True)

    #___ Multiple assets ___#
    #plot_scatter(prices)
    plot_residuals(prices)
    #print cadf(prices)
    print halflife(residuals(prices))


## __________________________________________________________________________||
## Statistical tools

def adf(prices, nlags=1):
    """
    Augmented Dickey Fuller test
    """
    adf_res = ts.adfuller(prices, nlags)

    ret = {}
    ret['Test statistic'] = adf_res[0]
    ret['p-value'] = adf_res[1]
    #ret['No. lags'] = adf_res[2]
    #ret['No. observations'] = adf_res[3]
    ret['Critical values'] = adf_res[4]

    return ret


def cadf(prices):
    """
    Cointegrating Augmented Dickey Fuller test
    """
    return adf(residuals(prices))


def hurst(prices, plot=False):
    """
    Hurst exponent test
    """
    prices = np.log(prices)

    lags = range(1, 100)

    # Variance of differences for each lag tau
    variances = [((prices.shift(-lag) - prices)**2).mean() for lag in lags]

    loglags = np.log(lags)
    logvars = np.log(variances)

    # Fit a straight line
    b, a = np.polyfit(loglags, logvars, 1)

    if plot:
        fig, ax = plt.subplots()

        plt.scatter(loglags, logvars)
        plt.plot(loglags, a + b * loglags, lw=2, color='orange')

        plotting.style_default(ax, fig,
                               xlabel='log(Lag)', ylabel='log(Variance)')
        plt.show()

    # Gradient is 2H
    hurst = b / 2

    return hurst


def vratiotest():
    """
    Variance ratio test
    """
    raise NotImplementedError, "See EPChan2 p.45"


def halflife(prices):
    """
    Half life of mean reversion
    using Ornstein-Uhlenbeck
    """
    prices_lag1 = prices.shift(1)
    delta_prices = prices - prices_lag1
    
    # EPChan2 Eq. (2.5)
    lamda = pd.ols(x=prices_lag1, y=delta_prices).beta.x

    return -math.log(2) / lamda


def ols(prices):
    """
    Ordinary Least Squares
    """
    return pd.ols(x=prices.iloc[:,0], y=prices.iloc[:,1])


def beta(prices):
    """
    Slope of linear regression
    """
    return ols(prices).beta.x


def residuals(prices, beta=None):
    """
    Residuals of linear regression
    residual = y - beta * x
    """
    if beta is None:
        beta = globals()['beta'](prices)

    return prices.iloc[:,1] - beta * prices.iloc[:,0]


## __________________________________________________________________________||
## Plotting tools

def plot_time_series(prices, *names):
    fig, ax = plt.subplots()

    prices.plot(ax=ax)
    plotting.style_default(ax, fig, ylabel='Price')

    plt.show()
        

def plot_scatter(prices):
    assert len(prices.columns) == 2

    xprices = prices.iloc[:, 0]
    yprices = prices.iloc[:, 1]

    fig, ax = plt.subplots()
    ax.scatter(xprices, yprices, label=None)

    b, a = ols(prices).beta
    #print sm.ols(formula='{} ~ {}'.format(*reversed(prices.columns)),
    #             data=prices).fit().summary()

    xmin, xmax = xprices.min(), xprices.max()
    axrange = np.arange(xmin, xmax, 0.01 * (xmax - xmin))

    ax.plot(axrange, a + b * axrange, 
            lw=4, color='orange', 
            label='y = {:.2f}x + {:.2f}'.format(b, a))

    axlabel = 'Price of {}'
    plotting.style_default(ax, fig,
                           xlabel=axlabel.format(prices.columns[0]), 
                           ylabel=axlabel.format(prices.columns[1]))
    
    plt.show()


def plot_residuals(prices):
    fig, ax = plt.subplots()

    #residuals(prices).plot()
    ax.plot(residuals(prices))

    plotting.style_default(ax, fig, ylabel='Residual')                           

    plt.show()


## __________________________________________________________________________||
if __name__ == "__main__":
    main()

