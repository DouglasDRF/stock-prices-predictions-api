from datetime import datetime
import re


class StockPrice():

    def __init__(self, ticker='', timestamp=datetime.now(), opn=0, close=0, high=0, low=0, volume=''):
        self.ticker = ticker
        self.date = timestamp.strftime(
            '%Y-%m-%d') if type(timestamp) is datetime else timestamp
        self.open = round(float(opn), 2)
        self.close = round(float(close), 2)
        self.high = round(float(high), 2)
        self.low = round(float(low), 2)
        self.volume = volume
        return

    def to_dict(self):
        return {'ticker': self.ticker, 'timestamp': self.date, 'open': self.open, 'close': self.close, 'high': self.high, 'low': self.close, 'volume': self.volume}