from abc import ABCMeta, abstractmethod
import pandas as pd

class Strategy():
    """
    Base class for strategies.
    Need to implement generate_signals in derived classes.
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    def begin(self):
        pass

    @abstractmethod
    def generate_signals(self):
        """
        Initialise signals to empty dataframe.
        Needs to filled in derived class.
        """
        self.signals = pd.DataFrame(index=self.prices.index, columns=self.prices.columns)


class Portfolio():
    """
    Base class for portfolios.
    Need to implement generate_positions and generate_returns in derived classes.
    """
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    def begin(self):
        self._carry_forward_signals()
        self.generate_positions()

    def _carry_forward_signals(self):
        self.signals.fillna(method='ffill', inplace=True)

    def generate_returns(self):
        """
        Default return calculation
        = weighted average of asset returns
        """
        self.asset_returns = self.prices.pct_change()
        self.returns = (self.weights.shift(1) * self.asset_returns * self.signals.shift(1)).sum(1)

    @abstractmethod
    def generate_positions(self):
        """
        Initialise positions to empty dataframe.
        Needs to be filled in derived class
        """
        self.weights = pd.DataFrame(index=self.signals.index, columns=self.signals.columns)


class Analyser():
    """
    Base class for analysers
    Need to implement generate_analysis in derived classes
    """
    def __init__(self):
        pass

    def begin(self):
        pass

    @abstractmethod
    def generate_analysis(self):
        pass

