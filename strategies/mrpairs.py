from core.stack import *
from core.baseclasses import Strategy

class MeanReversionPairsStrategy(Strategy):
    """
    Pairs trading mean reversion strategy using Bollinger Bands.
    Compute hedge ratio on a rolling basis with lookback window.
    Go long/short the spread when it's below/above the entry threshold,
    exit position when spread is less than exit threshold.
    """
    def __init__(self, window=None, zentry=None, zexit=None):
        super(MeanReversionPairsStrategy, self).__init__()

        if window is None:
            raise ValueError, "Need to choose a lookback window"
        if zentry is None or zexit is None:
            raise ValueError, "Need to choose an entry/exit z-score"
        if window == -1:
            print "\nWARNING: Performing regression over entire time frame", \
                  "- lookahead bias!\n"

        self.window = window
        self.zentry = zentry
        self.zexit = zexit

        print "\nRunning strategy with parameters:", \
              "\n\tWindow:", self.window, \
              "\n\tEntry z:", self.zentry, \
              "\n\tExit z:", self.zexit, \
              "\n"

    def begin(self):
        super(MeanReversionPairsStrategy, self).begin()

        if len(self.symbols) != 2:
            raise ValueError, "Can only handle two assets"

    def generate_signals(self):
        super(MeanReversionPairsStrategy, self).generate_signals()

        self.x_prices = self.prices.iloc[:, 0]
        self.y_prices = self.prices.iloc[:, 1]

        # Perform linear regression
        ols_arg = dict(x=self.x_prices, y=self.y_prices)
        if self.window != -1: ols_arg['window'] = self.window
        ols_res = pd.ols(**ols_arg)

        # Regression coefficients
        self.beta  = ols_res.beta.x
        alpha = ols_res.beta.intercept

        # Residuals (absorb intercept)
        #spread = y_prices - beta * x_prices - alpha
        spread = self.y_prices - self.beta * self.x_prices
       
        # Mean and standard deviation of residuals
        if self.window == -1:
            spread_mean = spread.mean() 
            spread_std  = spread.std()
        else:
            spread_mean = pd.rolling_mean(spread, self.window)
            spread_std  = pd.rolling_std (spread, self.window)

        # Deviation of residuals from mean
        z_score = (spread - spread_mean) / spread_std

        longs  = z_score < -self.zentry
        shorts = z_score > self.zentry
        exits  = abs(z_score) < self.zexit

        self.signals.loc[longs , :] = np.array( ([-1, 1],)*len(self.signals[longs])  )
        self.signals.loc[shorts, :] = np.array( ([ 1,-1],)*len(self.signals[shorts]) )
        self.signals.loc[exits , :] = np.array( ([ 0, 0],)*len(self.signals[exits])  )

        if self.options.debug:
            #self.debug_output()
            plt.scatter(self.x_prices,self.y_prices); plt.show()
            if self.window != -1:
                self.beta.plot(); plt.show()
            spread.plot(); plt.show()
            z_score.plot(); plt.show()
        
    def debug_output(self):
        pass
