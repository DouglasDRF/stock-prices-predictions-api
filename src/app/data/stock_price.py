from datetime import datetime


class StockPrice():

    def __init__(self, ticker='', timestamp=datetime.now(), opn=0, close=0, high=0, low=0, volume=0):
        self.ticker = ticker
        self.timestamp = timestamp
        self.open = opn
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume

        return
