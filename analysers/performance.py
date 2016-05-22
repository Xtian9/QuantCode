from core.stack import *
from math import sqrt
from collections import OrderedDict as odict
import os

class PerformanceAnalyser(object):

    # Number of periods in a year
    freq_nperiods = {'hourly': 252*6.5, 'daily': 252, 'weekly': 52, 'monthly': 12, 'annually': 1}
    prec = '.2f'
    
    def __init__(self, **kwargs):#symbols, returns, frequency, cls_benchmark, rfrate=0.04, save=False, outdir="output"):#, benchmark='SPY'):
        self.__dict__.update(kwargs)
        #self.symbols = symbols
        #self.returns = returns
        ##self.nperiods = PerformanceAnalyser.freq_nperiods[self.frequency]
        self.rfrate = 0.04#rfrate
        #self.benchmark = benchmark
        #self.cls_benchmark = cls_benchmark
        #self.save = self.options.save
        #self.outdir = self.options.outdir#'output'#outdir
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
        self.excess_return = self.returns - (self.rfrate / self.nperiods)
        self.cumulative_return = (1 + self.returns).cumprod() - 1

        # annual percentage return, approximation only
        self.mean_annual_return = self.nperiods * self.returns.mean()
        self.results['APR'] = self.format_string(self.mean_annual_return, '.2f', True)

        self.mean_annual_excess_return = self.nperiods * self.excess_return.mean()
        self.results['Excess APR'] = self.format_string(self.mean_annual_excess_return, '.2f', True)

        self.mean_annual_std = sqrt(self.nperiods) * self.returns.std()
        self.results['APSTD'] = self.format_string(self.mean_annual_std, '.2f', True)

        self.mean_annual_excess_std = sqrt(self.nperiods) * self.excess_return.std()

        self.total_return = self.cumulative_return[-1]
        self.results['Total return'] = self.format_string(self.total_return, '.2f', True)

    def benchmark_returns(self):
        self.benchmark_return = self.prices_bm.pct_change().iloc[:,0]
        self.benchmark_excess_return = self.benchmark_return - (self.rfrate / self.nperiods)
        self.benchmark_cumulative_return = ((1 + self.benchmark_return).cumprod() - 1)

        self.total_return_benchmark = self.benchmark_cumulative_return[-1]
        self.results['Total return bmark'] = self.format_string(self.total_return_benchmark, '.2f', True)

    def alpha_beta(self):
        # Regress portfolio returns against market returns
        ols_res = pd.ols(y=self.excess_return, x=self.benchmark_excess_return)

        # Alpha is intercept
        self.alpha = ols_res.beta[1]
        self.results['Alpha'] = self.format_string(self.alpha, '.2f')

        # Beta is gradient
        self.beta = ols_res.beta[0]
        self.results['Beta'] = self.format_string(self.beta, '.2f')

    #def total_return(self):
    #   try: 
    #       self.total_return = self.cumulative_return[-1]
    #   except NameError:
    #       pass
    #       #self.total_return = final holdings - initial holdings
    #   self.results['Total return'] = 100 * self.total_return

    def sharpe_ratio(self):
        self.sharpe = self.mean_annual_excess_return / self.mean_annual_excess_std
        self.results['Sharpe ratio'] = self.format_string(self.sharpe, '.2f')

    def information_ratio(self):
        self.excess_returns_bm = self.returns - self.benchmark_return
        self.mean_annual_excess_returns_bm = self.nperiods * self.excess_returns_bm.mean()
        self.mean_annual_excess_std_bm = sqrt(self.nperiods) * self.excess_returns_bm.std()
        self.information_ratio = self.mean_annual_excess_returns_bm / self.mean_annual_excess_std_bm
        self.results['Information ratio'] = self.format_string(self.information_ratio, '.2f')

    def drawdown(self):
        highwatermark = [0]
        drawdown = [0]
        drawdownduration = [0]

        for t in range(1, len(self.returns.index)):

            # high water mark
            hwm = max(self.cumulative_return[t], highwatermark[t-1])
            highwatermark.append(hwm)

            # drawdown
            dd = ((1+highwatermark[t]) / (1+self.cumulative_return[t])) - 1
            drawdown.append(dd)

            # drawdown duration
            ddd = drawdownduration[t-1] + 1 if dd>0 else 0
            drawdownduration.append(ddd)
        
        self.max_drawdown = max(drawdown)
        self.max_drawdown_duration = max(drawdownduration)

        self.results['Max DD'] = self.format_string(self.max_drawdown, '.2f', True)
        self.results['Max DD duration'] = self.format_string(self.max_drawdown_duration, 'd')

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
        self.cumulative_return.plot(ax=ax, label='Equity')
        self.benchmark_cumulative_return.plot(ax=ax, label='Benchmark')
        ax.legend(loc='best')

        #df.plot()
        #if self.full:
        #   print "save to output"
        #else:
        plt.show()

    def log_results(self):
        #if self.save
        fout = open(os.path.join(self.options.outdir, 'log.txt'), 'w')
        print "\n\nPerformance:"
        for metric, value in self.results.iteritems():
            #s = "%-20s %.2f" % (metric, value)
            s = '{:20} {}'.format(metric, value)
            print s
            fout.write(s+"\n")

    def format_string(self, value, fmt, pct=False):
        return '{:{}}'.format(value*(100 if pct else 1), fmt) + '%'*pct

