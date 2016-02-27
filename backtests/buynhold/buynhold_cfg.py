from core.backtest import Backtest
from strategies.buynhold import BuyAndHoldStrategy
from portfolios.equalweights import EqualWeightsPortfolio
from analysers.performance import PerformanceAnalyser

from core.parser import parser


options = parser.parse_args()

#____________________________________________________________________________||

symbols = ['SPY','DIA'][:]
qcodes = ['GOOG/NYSE_'+s for s in symbols]
date_start, date_end = "2010-01-01", "2015-12-31"
frequency = "daily"
datas = ['Close']
trade_time = ['Close','Open'][0]

#____________________________________________________________________________||

strategy = BuyAndHoldStrategy()#mykwargs

portfolio = EqualWeightsPortfolio()

analyser = PerformanceAnalyser()

backtest = Backtest(strategy = strategy,
                    portfolio = portfolio,
                    analyser = analyser,
                    symbols = symbols,
                    qcodes = qcodes,
                    date_start = date_start,
                    date_end = date_end,
                    frequency = frequency,
                    datas = datas,
                    trade_time = trade_time,
                    options = options)

backtest.run()

