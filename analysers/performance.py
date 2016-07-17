from core.stack import *
from core.baseclasses import Analyser
from collections import OrderedDict as odict
from utils import timeseries, plotting
import matplotlib.gridspec as gridspec
import os

def format_string(value, fmt, pct=False):
    return '{:{}}'.format(value*(100 if pct else 1), fmt) + '%'*pct


class PerformanceAnalyser(Analyser):
    """
    Compute performance measures like Sharpe ratio,
    drawdown, etc. and make performance plots like 
    equity curve, etc.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.rfrate = 0.04
        self.results = odict()

    def begin(self):
        pass

    def generate_analysis(self):
        # Calculations
        self.portfolio_returns()
        self.benchmark_returns()

        # Measures
        self.alpha_beta()
        self.sharpe_ratio()
        self.information_ratio()
        self.drawdown()
        self.log_results()

        # Plots
        self.create_tearsheet()

    #________________________________________________________________________||
    # Input/Calculations

    def portfolio_returns(self):
        self.cumreturns = timeseries.cumulate_returns(self.returns)

        self.annual_return = timeseries.annualised_return(
                                 self.returns, self.frequency)
        self.results['APR'] = format_string(self.annual_return, 
                                            '.2f', True)

        self.annual_std = timeseries.annualised_volatility(
                              self.returns, self.frequency)
        self.results['Volatility'] = format_string(self.annual_std, 
                                                   '.2f', True)

        self.total_return = timeseries.total_return(self.returns)
        self.results['Total return'] = format_string(self.total_return,
                                                     '.2f', True)

    def benchmark_returns(self):
        self.returns_bm = self.prices_bm.pct_change().iloc[:,0]
        self.cumreturns_bm = timeseries.cumulate_returns(self.returns_bm)

        self.results['Total return bmark'] = format_string(
                                                self.cumreturns_bm[-1],
                                                '.2f', True)

    #________________________________________________________________________||
    # Measures

    def alpha_beta(self):
        self.alpha, self.beta = timeseries.alpha_beta(
                                    self.returns, self.returns_bm)
        self.results['Alpha'] = format_string(self.alpha, '.2f')
        self.results['Beta'] = format_string(self.beta, '.2f')

    def sharpe_ratio(self):
        self.sharpe = timeseries.sharpe_ratio(
                          self.returns, self.frequency, self.rfrate)
        self.results['Sharpe ratio'] = format_string(self.sharpe, '.2f')

    def information_ratio(self):
        self.information_ratio = timeseries.information_ratio(self.returns, 
                                     self.returns_bm, self.frequency)
        self.results['Information ratio'] = format_string(
                                                self.information_ratio, '.2f')

    def drawdown(self):
        self.max_dd = timeseries.max_drawdown(self.cumreturns)
        self.max_ddd = timeseries.max_drawdown_duration(self.cumreturns)
        self.results['Max DD'] = format_string(self.max_dd, '.2f', True)
        self.results['Max DD duration'] = format_string(self.max_ddd, '.0f')

    #________________________________________________________________________||
    # Plots

    def create_tearsheet(self):
        vertical_sections = 7
        fig = plt.figure(figsize=(14, 5 * vertical_sections), facecolor='w')
        gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.5, hspace=0.5)

        # Equity curve
        ax_ref = plt.subplot(gs[:2, :])
        plotting.plot_equity_curve(
            self.cumreturns, self.cumreturns_bm, ax=ax_ref)

        # Rolling Sharpe
        i = 2
        ax = plt.subplot(gs[i, :], sharex=ax_ref)
        plotting.plot_rolling_sharpe(
            self.returns, self.frequency, self.rfrate, window=6, ax=ax)

        # Rolling drawdown
        i += 1
        ax = plt.subplot(gs[i, :], sharex=ax_ref)
        plotting.plot_drawdown(self.cumreturns, ax=ax)

        # Top drawdowns by magnitude
        i += 1
        ax = plt.subplot(gs[i, :], sharex=ax_ref)
        plotting.plot_top_drawdowns(
            self.cumreturns, ntop=5, ddtype='magnitude', ax=ax)

        # Top drawdowns by duration
        i += 1
        ax = plt.subplot(gs[i, :], sharex=ax_ref)
        plotting.plot_top_drawdowns(
            self.cumreturns, ntop=5, ddtype='duration', ax=ax)

        i += 1

        # Returns distribution
        ax = plt.subplot(gs[i, 1])
        plotting.plot_returns_distr(self.returns, 'monthly', ax=ax)

        for ax in fig.axes:
            plt.setp(ax.get_xticklabels(), visible=True)

        self.save_fig(fig, 'tearsheet', ['.png', '.pdf'], bbox_inches='tight')

    #________________________________________________________________________||
    # Output

    def log_results(self):
        fout = open(os.path.join(self.outdir, 'log.txt'), 'w')
        fout.write("Start date: {}\n".format(self.date_start))
        fout.write("End date: {}\n\n".format(self.date_end))
        fout.write("Symbols: {}\n\n".format(self.symbols))
        print "\n\nPerformance:"
        for metric, value in self.results.iteritems():
            s = '{:20} {}'.format(metric, value)
            print s
            fout.write(s+"\n")

    def save_fig(self, fig, name, exts=['.png'], **kwargs):
        if not isinstance(exts, list):
            exts = [exts]
        for ext in exts:
            fig.savefig(os.path.join(self.outdir, name+ext), **kwargs)

