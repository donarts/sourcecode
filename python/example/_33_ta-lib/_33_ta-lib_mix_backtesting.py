import numpy
import talib

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

class SmaCross(Strategy):
	def init(self):
		price = self.data.Close
		self.ma1 = self.I(SMA, price, 10)
		self.ma2 = self.I(SMA, price, 20)
		
		#https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
		#macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
		self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9)
		
		#https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
		#integer = CDLBELTHOLD(open, high, low, close)
		self.CDLBELTHOLD = self.I(talib.CDLBELTHOLD, self.data.Open, self.data.High, self.data.Low, self.data.Close)

	def next(self):
		if crossover(self.ma1, self.ma2):
			self.buy()
		elif crossover(self.ma2, self.ma1):
			self.sell()


bt = Backtest(GOOG, SmaCross, commission=.002,
			  exclusive_orders=True)
stats = bt.run()
bt.plot()

print(stats)


    def I(self,  # noqa: E741, E743
          func: Callable, *args,
          name=None, plot=True, overlay=None, color=None, scatter=False,
          **kwargs) -> np.ndarray: