from core.stack import *
from core.coreclasses import Portfolio
#from copy import deepcopy

class EqualWeightsPortfolio(Portfolio):

    def __init__(self, **kwargs):#, symbols, data, signals):
        #self.symbols = symbols
        #self.cls = data
        #self.signals = signals

        #self.generate_positions()
        self.__dict__.update(kwargs)

    def generate_positions(self):
        self.weights = pd.DataFrame(index=self.signals.index, columns=self.signals.columns)
        nassets = len(self.weights.columns)
        #FIXME: should only assign weights to assets which have signals
        for symbol in self.weights.columns:
            self.weights[symbol] = 1. / nassets
        self.carry_forward_positions()#self.weights)

    def carry_forward_positions(self):
        self.weights.fillna(method='ffill', inplace=True)

    def backtest_portfolio(self):
        self.generate_positions()
        #self.asset_returns = self.cls.pct_change()
        self.asset_returns = self.prices.pct_change()
        self.returns = (self.weights * self.asset_returns).sum(1)
        #FIXME: check need to lag positions??
        return self.returns

    #carry_forward_posiions and backtest_portfolio could go in base class

