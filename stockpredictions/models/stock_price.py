from datetime import datetime
import re

class StockPrice():

    def __init__(self, ticker='', timestamp=datetime.now(), opn=0, close=0, high=0, low=0, volume=0):
        self.ticker = ticker
        self.timestamp = timestamp
        self.open = opn
        self.close = close
        self.high = high
        self.low = low
        self.volume = self.__parse_and_format_volume_value(volume)

        return

    def __parse_and_format_volume_value(self, value):
        volume_regex =  re.compile(r'(\d+|,)|(K|M|B)')
        m = volume_regex.match(value)
        value = float(m.group(0))
        sufix = str(m.group(1))
        
        if(sufix == 'K' or sufix == 'k'):
            return value * 1000
        elif(sufix == 'M' or sufix == 'm'):
            return value * 1000000
        elif(sufix == 'B' or sufix == 'b'):
            return value * 1000000000
        
