import mysql.connector
from stockpredictions.models import StockPrice
from datetime import datetime

class CoreDataRepository:
    def __init__(self):
        self.__dbConnection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='StockPricesPrediction'
        )

    def get_ticker_source(self, ticker) -> str:
        query = """SELECT SourceEndpoint FROM SupportedCompaniesToCrawler WHERE B3Code = %s;"""
        params = (ticker,)
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result[0]

    def save_to_history(self, stock_prices: list):
        query = """INSERT INTO StockPrice (Ticker, `Date`, `Open`, `Close`, High, Low, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        params = []
        for s in stock_prices:
            params.append((s.ticker, s.timestamp, s.open, s.close, s.high, s.low, s.volume))

        cursor = self.__dbConnection.cursor()
        cursor.executemany(query, params)
        self.__dbConnection.commit()

    def get_history(self, ticker, limit=40) -> list:
        query = """SELECT * FROM StockPrice WHERE Ticker = %s ORDER BY `Date` DESC LIMIT %s;"""
        params = (ticker, limit)

        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        
        final_result = []

        for r in result:
            final_result.append(StockPrice(r[1], r[2], r[3], r[4], r[5], r[6], str(r[7])))
        
        return final_result