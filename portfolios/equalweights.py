from core.stack import *
from core.coreclasses import Portfolio

class EqualWeightsPortfolio(Portfolio):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def generate_positions(self):
        self.weights = pd.DataFrame(index=self.signals.index, columns=self.signals.columns)
        nassets = len(self.weights.columns)
        #FIXME: should only assign weights to assets which have signals
        self.weights.loc[:,:] = 1. / nassets
        self.carry_forward_positions()

    def carry_forward_positions(self):
        #self.weights.fillna(method='ffill', inplace=True)
        self.signals.fillna(method='ffill', inplace=True)

    def backtest_portfolio(self):
        self.generate_positions()
        self.asset_returns = self.prices.pct_change()
        self.returns = (self.weights * self.asset_returns * self.signals.shift(1)).sum(1)
        return self.returns

    #carry_forward_posiions and backtest_portfolio could go in base class

