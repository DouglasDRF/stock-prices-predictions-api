import os
import mysql.connector

from stockpredictions.models import StockPrice


class StatisticsRepository:
    def __init__(self):
        self.__dbConnection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )

    def save_prediction(self, prediction):
        query = """INSERT INTO PredictionHistories (Ticker, NextPredictedValue, PredictionType, Direction, `Date`) VALUES (%s, %s, %s, %s, %s);"""
        params = (prediction.ticker[0], prediction.next_predicted_value[0], prediction.prediction_type[0], prediction.direction[0], prediction.date)
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        self.__dbConnection.commit()
        cursor.close()
