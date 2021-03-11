import os
import mysql.connector
from datetime import datetime

from stockpredictions.models import StockPrice


class StatisticsRepository:
    def __init__(self):
        self.__dbConnection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )

    def get_last_predicted_price(self, ticker):
        query = """SELECT NextPredictedValue FROM PredictionHistories WHERE Ticker = %s ORDER BY `Date` DESC LIMIT 1"""
        params = (ticker,)
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    
    def save_prediction(self, prediction):
        query = """INSERT INTO PredictionHistories (Ticker, PreviousReference, NextPredictedValue, PredictionType, Direction, `Date`) VALUES (%s, %s, %s, %s, %s, %s);"""
        params = (prediction.ticker[0], prediction.previous[0], prediction.next_predicted_value[0], prediction.prediction_type[0], prediction.direction[0], prediction.date)
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        self.__dbConnection.commit()
        cursor.close()
    
    def update_logs_with_real_values(self, ticker, real_val, real_dir):
        query = """SELECT Id FROM PredictionHistories WHERE Ticker = %s ORDER BY `Date` DESC LIMIT 1"""
        params = (ticker, )
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        result_id = cursor.fetchone()
        
        query = """UPDATE PredictionHistories SET RealValue = %s, RealDirection = %s WHERE Id = %s"""
        params = (real_val, real_dir, result_id[0])
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        self.__dbConnection.commit()
        cursor.close()
    

