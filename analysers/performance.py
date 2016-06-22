from core.stack import *
from core.baseclasses import Analyser
from math import sqrt
from collections import OrderedDict as odict
import utils
import os

def format_string(value, fmt, pct=False):
    return '{:{}}'.format(value*(100 if pct else 1), fmt) + '%'*pct


class PerformanceAnalyser(Analyser):

    # Number of periods in a year
    freq_nperiods = {'hourly': 252*6.5, 'daily': 252, 'weekly': 52, 'monthly': 12, 'annually': 1}
    prec = '.2f'
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.rfrate = 0.04
        self.results = odict()

    def begin(self):
        pass

    def generate_analysis(self):
        self.nperiods = PerformanceAnalyser.freq_nperiods[self.frequency]

        self.portfolio_returns()
        self.benchmark_returns()
        self.alpha_beta()
        self.sharpe_ratio()
        self.information_ratio()
        self.drawdown()
        self.log_results()
        self.plot_equity_curve()

    def portfolio_returns(self):
        self.cumreturns = (1 + self.returns).cumprod() - 1

        # annual percentage return, approximation only
        self.annual_return = self.nperiods * self.returns.mean()
        self.results['APR'] = format_string(self.annual_return, '.2f', True)

        self.annual_std = sqrt(self.nperiods) * self.returns.std()
        self.results['Volatility'] = format_string(self.annual_std, '.2f', True)

        self.results['Total return'] = format_string(self.cumreturns[-1], '.2f', True)

    def benchmark_returns(self):
        self.returns_bm = self.prices_bm.pct_change().iloc[:,0]
        self.cumreturns_bm = (1 + self.returns_bm).cumprod() - 1

        self.results['Total return bmark'] = format_string(self.cumreturns_bm[-1], '.2f', True)

    def alpha_beta(self):
        self.alpha, self.beta = utils.alpha_beta(self.returns, self.returns_bm)
        self.results['Alpha'] = format_string(self.alpha, '.2f')
        self.results['Beta'] = format_string(self.beta, '.2f')

    def sharpe_ratio(self):
        self.sharpe = utils.sharpe_ratio(self.returns, self.nperiods, self.rfrate)
        self.results['Sharpe ratio'] = format_string(self.sharpe, '.2f')

    def information_ratio(self):
        self.information_ratio = utils.information_ratio(self.returns, self.returns_bm, self.nperiods)
        self.results['Information ratio'] = format_string(self.information_ratio, '.2f')

    def drawdown(self):
        self.max_dd, self.max_ddd = utils.drawdown(self.cumreturns)
        self.results['Max DD'] = format_string(self.max_dd, '.2f', True)
        self.results['Max DD duration'] = format_string(self.max_ddd, 'd')

    def plot_equity_curve(self):
        #df = pd.DataFrame(index=self.cumulative_return.index)
        #df['Equity'] = self.cumulative_return
        #df['Benchmark'] = self.benchmark_cumulative_return
        #df = pd.DataFrame(dict(Equity=self.cumulative_return, 
        #                       Benchmark=self.benchmark_cumulative_return))

        fig = plt.figure()
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(111, ylabel='Portfolio value growth (%)')
        ax.set_title('Equity curve')
        self.cumreturns.plot(ax=ax, label='Equity')
        self.cumreturns_bm.plot(ax=ax, label='Benchmark')
        ax.legend(loc='best')

        #df.plot()
        #if self.full:
        #   print "save to output"
        #else:
        plt.show()

    def log_results(self):
        #if self.save
        fout = open(os.path.join(self.outdir, 'log.txt'), 'w')
        print "\n\nPerformance:"
        for metric, value in self.results.iteritems():
            #s = "%-20s %.2f" % (metric, value)
            s = '{:20} {}'.format(metric, value)
            print s
            fout.write(s+"\n")

