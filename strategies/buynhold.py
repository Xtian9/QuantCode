from core.stack import *
from core.coreclasses import Strategy

class BuyAndHoldStrategy(Strategy):
    
    def __init__(self, **kwargs):#, symbols, datas_symbols):
        #self.symbols = symbols
        #self.datas_symbols = datas_symbols
        ## make abovehis block super().__init__()
        #self.datas_symbols = None
        #self.cls = self.datas_symbols['Close']
        self.__dict__.update(kwargs)
    
    def generate_signals(self):
        #self.cls = self.datas_symbols[self.trade_time]
        #signals = pd.DataFrame(index=self.cls.index, columns=self.cls.columns)
        signals = pd.DataFrame(index=self.prices.index, columns=self.prices.columns)
        signals.loc[:,:] = 1
        return signals

