from core.stack import *
from core.baseclasses import Strategy

class MovingAverageCrossoverStrategy(Strategy):

    def __init__(self, short_window=None, long_window=None):
        super(MovingAverageCrossoverStrategy, self).__init__()

        if short_window is None or long_window is None:
            raise ValueError, "Need to choose a MA window"
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        super(MovingAverageCrossoverStrategy, self).generate_signals()

        mavg_short = pd.rolling_mean(self.prices, self.short_window, min_periods=1)
        mavg_long  = pd.rolling_mean(self.prices, self.long_window,  min_periods=1)

        self.signals[mavg_short > mavg_long] = 1
        self.signals[mavg_long > mavg_short] = -1
        
        #signals = 1 * (mavg_short > mavg_long) - 1 * (mavg_long > mavg_short)
        #signals.iloc[:, :] = np.where(mavg_short > mavg_long, 1, -1)

        self.signals.iloc[:self.long_window-1, :] = np.nan

