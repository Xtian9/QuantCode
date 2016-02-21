import pandas as pd
import Quandl
#import time

AUTHTOKEN = 'HpLYEUhzrjV84uXkT9wu'

class DataHandler(object):

	def __init__(self, symbols, 
					   date_start, 
					   date_end,#=time.strftime("%Y-%m-%d"), 
					   collapse, 
					   datas): ##sampling_rate
		self.symbols = symbols
		self.date_start = date_start
		self.date_end = date_end
		self.collapse = collapse
		self.datas = datas

	def fetch_data(self):

		self.symbols_datas = {}
		for symbol in self.symbols:
			datas = Quandl.get("GOOG/NYSE_%s" % symbol, 
								trim_start = self.date_start, 
								trim_end = self.date_end, 
								collapse = self.collapse,
								authtoken = AUTHTOKEN)
			self.symbols_datas[symbol] = datas

	def generate_data(self):

		print "Fetching data..."
		self.fetch_data()
		print "Generating data..."
		self.datas_symbols = {}
		for data in self.datas:
			df = pd.DataFrame()
			for symbol in self.symbols:
				df_tojoin = self.symbols_datas[symbol][data].to_frame()
				df_tojoin.rename(columns={data:symbol}, inplace=True)
				if df.empty:
					df = df_tojoin
				else:
					df = df.join(df_tojoin, how='outer')
			self.datas_symbols[data] = df
		return self.datas_symbols


	def resample(self):
		pass
			
		
