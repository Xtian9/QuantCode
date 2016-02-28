from core.backtest import Backtest
from strategies.macross import MovingAverageCrossoverStrategy
from portfolios.equalweights import EqualWeightsPortfolio
from analysers.performance import PerformanceAnalyser

from core.parser import parser


options = parser.parse_args()

#____________________________________________________________________________||

symbols = ['AAPL']
qcodes = ['GOOG/NASDAQ_'+s for s in symbols]
date_start, date_end = "2010-01-01", "2015-12-31"
frequency = "daily"
datas = ['Close']
trade_time = ['Close','Open'][0]

short_window = 9
long_window = 200

#____________________________________________________________________________||

strategy = MovingAverageCrossoverStrategy(short_window,long_window)

portfolio = EqualWeightsPortfolio()

analyser = [PerformanceAnalyser()]#,MovingAverageCrossoverAnalyser()]

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

