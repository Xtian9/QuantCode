from core.stack import *
from datahandler import DataHandler
import statsmodels.tsa.stattools as ts


##___________________________________________________________________________||
## Config

#symbols    = ['SPY']#,'IWM']
symbols    = ['AREX','WLL']
#qcodes     = ['GOOG/NYSEARCA_'+s for s in symbols]
qcodes     = ['GOOG/NASDAQ_AREX','GOOG/NYSE_WLL']
date_start = "2012-01-01"
date_end   = "2013-01-01"
frequency  = "daily"
datas      = ['Close']
trade_time = 'Close'

TEST = 'adf'


##___________________________________________________________________________||
## Main

def main():
    
    data_handler = DataHandler(symbols, qcodes, date_start, date_end, frequency, datas)
    datas_symbols = data_handler.generate_data()
    
    #prices = datas_symbols['Close'].iloc[:,0]
    prices = datas_symbols[trade_time]

    plot_time_series(prices)
    plot_scatter(prices)
    plot_residuals(prices)
    print cadf(prices)

    #prices = pd.Series(np.log(np.cumsum(np.random.randn(100000)+100)))
    #plt.plot(prices);plt.show()

    #adf(prices)
    #prices = np.log(prices)
    #hurst(prices)


##___________________________________________________________________________||
## Statistical tools

def adf(prices, nlags=None):
    """
    Augmented Dickey Fuller test
    """
    adf_res = ts.adfuller(prices, 1)

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


def hurst(prices):
    """
    Hurst exponent test
    """
    prices = np.log(prices)
    lags = range(1,100)
    means = [((prices.shift(-lag) - prices)**2).mean() for lag in lags]
    plt.scatter(np.log(lags), np.log(means)); plt.show()
    linfit = np.polyfit(np.log(lags), np.log(means), 1)
    hurst = linfit[0] / 2
    return hurst


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


##___________________________________________________________________________||
## Plotting tools

def plot_time_series(prices, *names):
    if names: 
        assert len(prices.columns) == len(names), "AH"
    else:
        names = prices.columns

    # add axes labels, title, etc
    prices.plot()
    plt.show()
        

def plot_scatter(prices, *names):
    plt.scatter(prices.iloc[:,0], prices.iloc[:,1])
    plt.show()


def plot_residuals(prices):
    residuals(prices).plot()
    plt.show()


##___________________________________________________________________________||
if __name__ == "__main__":
    main()

