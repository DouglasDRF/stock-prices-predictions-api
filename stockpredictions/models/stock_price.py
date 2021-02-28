from datetime import datetime
import re
class StockPrice():

    def __init__(self, ticker='', timestamp=datetime.now(), opn=0, close=0, high=0, low=0, volume=''):
        self.ticker = ticker
        self.timestamp = timestamp.isoformat()
        self.open = float(opn)
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.volume = self.__parse_and_format_volume_value(volume)

        return

    def __parse_and_format_volume_value(self, value):
        volume_regex =  re.compile(r'(\d+.\d+)|(K|k|M|m|B|b)')
    
        rgxResult = []
        for m in volume_regex.finditer(value.replace(',', '.')):
            rgxResult.append(m.group(0))
        
        val = float(rgxResult[0])
        sufix = str(rgxResult[1])
                
        if(sufix == 'K' or sufix == 'k'):
            return val * pow(10, 3)
        elif(sufix == 'M' or sufix == 'm'):
            return val * pow(10, 6)
        elif(sufix == 'B' or sufix == 'b'):
            return val * pow(10, 9)
        else: 
            return val

