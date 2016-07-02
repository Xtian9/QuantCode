from core.stack import *
from core.baseclasses import Analyser
from math import sqrt
from collections import OrderedDict as odict
import plotting
import utils
import os

# Number of periods in a year
freq_nperiods = {'hourly': 252*6.5, 'daily': 252, 
                 'weekly': 52, 'monthly': 12, 'annually': 1}

def format_string(value, fmt, pct=False):
    return '{:{}}'.format(value*(100 if pct else 1), fmt) + '%'*pct


class PerformanceAnalyser(Analyser):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.rfrate = 0.04
        self.results = odict()
        self.figures = []

    def begin(self):
        pass

    def generate_analysis(self):
        self.nperiods = freq_nperiods[self.frequency]

        self.portfolio_returns()
        self.benchmark_returns()

        # Measures
        self.alpha_beta()
        self.sharpe_ratio()
        self.information_ratio()
        self.drawdown()
        self.log_results()

        # Plots
        self.plot_equity_curve()
        self.plot_rolling_sharpe()
        self.plot_drawdown()
        self.plot_top_drawdowns()

    #____________________________________________________________________________||
    # Input

    def portfolio_returns(self):
        self.cumreturns = (1 + self.returns).cumprod() - 1

        # annual percentage return, approximation only
        self.annual_return = self.nperiods * self.returns.mean()
        self.results['APR'] = format_string(self.annual_return, 
                                            '.2f', True)

        self.annual_std = sqrt(self.nperiods) * self.returns.std()
        self.results['Volatility'] = format_string(self.annual_std, 
                                                   '.2f', True)

        self.results['Total return'] = format_string(self.cumreturns[-1],
                                                     '.2f', True)

    def benchmark_returns(self):
        self.returns_bm = self.prices_bm.pct_change().iloc[:,0]
        self.cumreturns_bm = (1 + self.returns_bm).cumprod() - 1

        self.results['Total return bmark'] = format_string(
                                                self.cumreturns_bm[-1],
                                                '.2f', True)

    #____________________________________________________________________________||
    # Measures

    def alpha_beta(self):
        self.alpha, self.beta = utils.alpha_beta(self.returns, 
                                                 self.returns_bm)
        self.results['Alpha'] = format_string(self.alpha, '.2f')
        self.results['Beta'] = format_string(self.beta, '.2f')

    def sharpe_ratio(self):
        self.sharpe = utils.sharpe_ratio(self.returns, self.nperiods, 
                                         self.rfrate)
        self.results['Sharpe ratio'] = format_string(self.sharpe, '.2f')

    def information_ratio(self):
        self.information_ratio = utils.information_ratio(self.returns, 
                                               self.returns_bm, self.nperiods)
        self.results['Information ratio'] = format_string(
                                                self.information_ratio, '.2f')

    def drawdown(self):
        self.max_dd = utils.max_drawdown(self.cumreturns)
        self.max_ddd = utils.max_drawdown_duration(self.cumreturns)
        self.results['Max DD'] = format_string(self.max_dd, '.2f', True)
        self.results['Max DD duration'] = format_string(self.max_ddd, '.0f')

    #____________________________________________________________________________||
    # Plots

    def plot_equity_curve(self):
        fig, ax = plotting.plot_equity_curve(self.cumreturns, 
                                             self.cumreturns_bm)
        self.save_fig(fig, 'equitycurve')

    def plot_rolling_sharpe(self, window=6):
        fig, ax = plotting.plot_rolling_sharpe(self.returns, self.nperiods, 
                                               self.rfrate, window)
        self.save_fig(fig, 'rollingsharpe')

    def plot_drawdown(self):
        fig, ax = plotting.plot_drawdown(self.cumreturns)
        self.save_fig(fig, 'drawdown')

    def plot_top_drawdowns(self, ntop=5):
        for ddtype, (fig, ax) in plotting.plot_top_drawdowns(
                                    self.cumreturns, ntop).iteritems():
            self.save_fig(fig, 'drawdown_top{}_{}'.format(ntop, ddtype))

    #____________________________________________________________________________||
    # Output

    def log_results(self):
        fout = open(os.path.join(self.outdir, 'log.txt'), 'w')
        fout.write("Start date: {}\n".format(self.date_start))
        fout.write("End date: {}\n\n".format(self.date_end))
        fout.write("Symbols: {}\n\n".format(self.symbols))
        print "\n\nPerformance:"
        for metric, value in self.results.iteritems():
            #s = "%-20s %.2f" % (metric, value)
            s = '{:20} {}'.format(metric, value)
            print s
            fout.write(s+"\n")

    def save_fig(self, fig, name, ext='.png'):
        fig.savefig(os.path.join(self.outdir, name+ext))
        self.figures.append(fig)

