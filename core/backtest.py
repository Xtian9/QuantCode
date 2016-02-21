from datahandler import DataHandler

class Backtest(object):

	def __init__(self, strategy, portfolio, analyser, **kwargs):
		self.strategy = strategy
		self.portfolio = portfolio
		self.analyser = analyser
		self.backtest_modules = [self, self.strategy, self.portfolio, self.analyser]

		self.symbols = None
		self.date_start = None
		self.date_end = None
		self.frequency = None
		self.datas = None
		self.trade_time = None
		self.benchmark = None

		for module in self.backtest_modules:
			module.__dict__.update(kwargs)
		#self.__dict__.update(kwargs)

		self.validate_input()

		self.data_handler = DataHandler(self.symbols, self.date_start, self.date_end, self.frequency, self.datas)
		self.benchmark_handler = DataHandler([self.benchmark], self.date_start, self.date_end, self.frequency, self.datas)

	def validate_input(self):
		if self.symbols is None:
			raise ValueError, "Need to choose symbols to trade"

		if self.benchmark is None:
			print "WARNING: No benchmark chosen. Default is SPY"
			self.benchmark = 'SPY'

	def run(self):
		print "\n\nHandling data"
		datas_symbols = self.data_handler.generate_data()
		datas_benchmark = self.benchmark_handler.generate_data()
		for module in self.backtest_modules:
			module.datas_symbols = datas_symbols
			module.datas_benchmark = datas_benchmark
			module.prices = datas_symbols[self.trade_time]
			module.prices_bm = datas_benchmark[self.trade_time]
		
		print "\n\nGenerating signals"
		signals = self.strategy.generate_signals()
		for module in self.backtest_modules:
			module.signals = signals
		
		print "\n\nBacktesting portfolio"
		returns = self.portfolio.backtest_portfolio()
		for module in self.backtest_modules:
			module.returns = returns

		print "\n\nAnalysing results"
		self.analyser.analyse_performance()