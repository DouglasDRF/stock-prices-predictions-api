import mysql.connector
import os
from stockpredictions.models import StockPrice
from datetime import datetime
import pandas as pd


class CoreDataRepository:
    def __init__(self):
        self.__dbConnection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )

    def get_ticker_source(self, ticker) -> str:
        query = """SELECT SourceEndpoint FROM SupportedCompaniesToCrawler WHERE B3Code = %s;"""
        params = (ticker,)
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def get_supported_stocks(self):
        query = """SELECT B3Code FROM SupportedCompaniesToCrawler;"""
        cursor = self.__dbConnection.cursor()
        cursor.execute(query)
        fetch = cursor.fetchall()
        cursor.close()
        for s in fetch:
            yield s[0]

    def save_to_history(self, stock_prices: list):
        query = """INSERT INTO StockPrice (Ticker, `Date`, `Open`, `Close`, High, Low, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        params = []
        for s in stock_prices:
            params.append((s.ticker, s.timestamp, s.open,s.close, s.high, s.low, s.volume))

        cursor = self.__dbConnection.cursor()
        cursor.executemany(query, params)
        self.__dbConnection.commit()
        cursor.close()

    def save_last(self, stock_price: StockPrice):
        query = """INSERT INTO StockPrice (Ticker, `Date`, `Open`, `Close`, High, Low, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        params = (stock_price.ticker, stock_price.timestamp, stock_price.open, stock_price.close, stock_price.high, stock_price.low, stock_price.volume)

        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        self.__dbConnection.commit()
        cursor.close()

    def get_history(self, ticker, limit=40) -> list:
        query = """SELECT * FROM StockPrice WHERE Ticker = %s ORDER BY `Date` DESC LIMIT %s;"""
        params = (ticker, limit)

        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()

        final_result = []

        for r in result:
            final_result.append(StockPrice(r[1], r[2], r[3], r[4], r[5], r[6], str(r[7])))

        final_result.reverse()
        return final_result

    def get_history_dataframe(self, history):
        df = pd.DataFrame([x.to_dict() for x in history])
        data = df.drop(columns=['ticker', 'timestamp'])
        return data
