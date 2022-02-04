from datetime import datetime
import re

from pydantic import validate_model


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
        self.validate()
        
    def to_dict(self):
        return {'ticker': self.ticker, 'timestamp': self.date, 'open': self.open, 'close': self.close, 'high': self.high, 'low': self.close, 'volume': self.volume}

    def validate(self):
        if self.ticker == '' or None:
            raise('Ticker cannot be empty or null')
        if self.date == '' or None:
            raise('date cannot be empty or null')
        if self.open == 0 or None:
            raise('open cannot be empty or null')
        if self.close == 0 or None:
            raise('close cannot be empty or null')
        if self.high == 0 or None:
            raise('high cannot be empty or null')
        if self.low == 0 or None:
            raise('low cannot be empty or null')
        if self.volume == 0 or None:
            raise('volume cannot be empty or null')
        
