from core.backtest import Backtest
from strategies.mrpairs import MeanReversionPairsStrategy
from portfolios.equalweights import EqualWeightsPortfolio
from analysers.performance import PerformanceAnalyser
from core.parser import parser

parser.add_argument('-w', '--window', action='store', dest='window', default=None, help='lookback window')
parser.add_argument('--zentry', action='store', dest='zentry', default=None, help='z entry threshold')
parser.add_argument('--zexit',  action='store', dest='zexit',  default=None, help='z exit threshold')
options = parser.parse_args()

#____________________________________________________________________________||

symbols    = ['GLD','GDX'][::-1] # x,y
#symbols    = ['SPY','IWM']
qcodes     = ['GOOG/NYSEARCA_'+s for s in symbols]
date_start = "2006-05-23"
date_end   = "2007-11-30"
#date_end   = "2007-05-23"
frequency  = "daily"
datas      = ['Close']
trade_time = 'Close'

window = -1
zentry, zexit = 1, 0.5

if options.window is not None: window = options.window
if options.zentry is not None: zentry = options.zentry
if options.zexit  is not None: zexit  = options.zexit

#____________________________________________________________________________||

strategy = MeanReversionPairsStrategy(window, zentry, zexit)

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

