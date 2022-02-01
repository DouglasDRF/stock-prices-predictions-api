import sys
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from decimal import Decimal
from stockpredictions.data.svcagents.yahoo_finance import YahooFinanceApiSvcAgent
from stockpredictions.models import StockPrice

dynamodb = boto3.resource('dynamodb')


class CoreDataRepository:
    def __init__(self, api_data=YahooFinanceApiSvcAgent()):
        self.__api_data = api_data
        pass

    def get_supported_stocks(self):
        table = dynamodb.Table('SupportedCompanies')
        response = table.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            print(response['LastEvaluatedKey'])
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        for x in items:
            yield x['B3Code']

    def save_to_history(self, stock_prices: list):
        table = dynamodb.Table('StockPrices')
        with table.batch_writer() as batch:
            for s in stock_prices:
                batch.put_item(Item={
                    'ticker': s.ticker,
                    'date': s.date,
                    'open': Decimal(str(s.open)),
                    'close': Decimal(str(s.close)),
                    'high': Decimal(str(s.high)),
                    'low': Decimal(str(s.low)),
                    'volume': s.volume
                })

    def save_last(self, stock_price: StockPrice):
        table = dynamodb.Table('StockPrices')
        try:
            table.put_item(Item={
                'ticker': stock_price.ticker,
                'date': stock_price.date,
                'open': Decimal(str(stock_price.open)),
                'close': Decimal(str(stock_price.close)),
                'high': Decimal(str(stock_price.high)),
                'low': Decimal(str(stock_price.low)),
                'volume': stock_price.volume
            })
        except Exception as e:
            print(sys.exc_info()[0])
            raise

    def update_last(self, stock_price: StockPrice):
        table = dynamodb.Table('StockPrices')
        response = table.update_item(
            Key={
                'ticker': stock_price.ticker,
                'date': stock_price.date
            },
            UpdateExpression='SET #opn = :o, #cls = :c, high = :h, low = :l, volume = :v ',
            ExpressionAttributeValues={
                ':o': Decimal(str(stock_price.open)),
                ':c': Decimal(str(stock_price.close)),
                ':h': Decimal(str(stock_price.high)),
                ':l': Decimal(str(stock_price.low)),
                ':v': stock_price.volume
            },
            ExpressionAttributeNames={
                '#opn': 'open',
                '#cls': 'close'
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def get_history(self, ticker, limit=40) -> list:
        table = dynamodb.Table('StockPrices')
        date = datetime.today() - timedelta(days=limit * 3)
        date = date.strftime('%Y-%m-%d')
        response = table.query(
            KeyConditionExpression=Key('ticker').eq(
                ticker) & Key('date').gt(date)
        )
        typedDataList = []

        for x in response['Items']:
            typedDataList.append(StockPrice(x['ticker'],
                                            datetime.fromisoformat(x['date']),
                                            x['open'],
                                            x['close'],
                                            x['high'],
                                            x['low'],
                                            x['volume']))

        sorted_list = sorted(typedDataList, key=lambda t: datetime.strptime(
            t.date, '%Y-%m-%d'), reverse=False)
        return sorted_list[-limit:]

    def get_history_dataframe(self, history, limit=40):
        df = pd.DataFrame([x.to_dict() for x in history])
        data = df.drop(columns=['ticker', 'timestamp'])
        return data[:limit]

    def get_non_past_days_compliant(self, count=40):
        supported = self.get_supported_stocks()
        non_compliant = []

        for x in supported:
            res = self.get_history(x)
            last = self.__api_data.get_last_updated_value(x)
            if len(res) < count or res[-1].date != last.date:
                non_compliant.append(x)

        return non_compliant
