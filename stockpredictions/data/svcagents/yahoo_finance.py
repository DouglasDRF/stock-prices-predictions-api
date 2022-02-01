import http.client
import json
import datetime as dt
from stockpredictions.models import StockPrice


class YahooFinanceApiSvcAgent:
    def __init__(self):
        self.__connection = http.client.HTTPSConnection(
            "query1.finance.yahoo.com")

    def get_last_updated_value(self, ticker) -> StockPrice:
        payload = ''
        headers = {}
        self.__connection.request(
            "GET", f"/v8/finance/chart/{ticker}.SA?region=US&lang=en-US&includePrePost=false&interval=1d&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance", payload, headers)
        res = self.__connection.getresponse()
        data = json.loads(res.read().decode('utf-8'))

        x_dt = dt.datetime.fromtimestamp(
            data['chart']['result'][0]['timestamp'][0])
        x_indicators = data['chart']['result'][0]['indicators']['quote'][0]
        return StockPrice(ticker, x_dt, x_indicators['open'][0], x_indicators['close'][0], x_indicators['high'][0], x_indicators['low'][0], x_indicators['volume'][0])

    def get_history_values(self, ticker) -> list:
        payload = ''
        headers = {}
        self.__connection.request(
            "GET", f"/v8/finance/chart/{ticker}.SA?region=US&lang=en-US&includePrePost=false&interval=1d&range=3mo&corsDomain=finance.yahoo.com&.tsrc=finance", payload, headers)
        res = self.__connection.getresponse()
        data = json.loads(res.read().decode('utf-8'))

        indicators = data['chart']['result'][0]['indicators']['quote'][0]

        datetime_list = []
        for x in data['chart']['result'][0]['timestamp']:
            datetime_list.append(dt.datetime.fromtimestamp(x))

        open_list = []
        for x in indicators['open']:
            open_list.append(x)

        close_list = []
        for x in indicators['close']:
            close_list.append(x)

        high_list = []
        for x in indicators['high']:
            high_list.append(x)

        low_list = []
        for x in indicators['low']:
            low_list.append(x)

        volume_list = []
        for x in indicators['volume']:
            volume_list.append(x)

        result_list = []
        for i in range(0, len(datetime_list)):
            if(open_list[i] is not None and close_list[i] is not None and high_list[i] is not None and low_list[i] is not None and volume_list is not None):
                result_list.append(StockPrice(
                    ticker, datetime_list[i], open_list[i], close_list[i], high_list[i], low_list[i], volume_list[i]))

        return result_list
