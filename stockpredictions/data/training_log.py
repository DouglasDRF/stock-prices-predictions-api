import os
import mysql.connector
from stockpredictions.models import TrainingLog
from stockpredictions.models import StockPrice

class TrainingLogRepository:
    def __init__(self):
        self.__dbConnection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )

    def save_training_log(self, training_log):
        query = """INSERT INTO TrainingLog (TrainingDate, DatasetSamplesCount, Accuracy, ModelFileName) VALUES (%s, %s, %s, %s);"""
        params = (training_log.date[0], training_log.samples_count[0], round(training_log.accuracy[0], 4), training_log.model_file_name[0])
        cursor = self.__dbConnection.cursor()
        cursor.execute(query, params)
        self.__dbConnection.commit()
        cursor.close()
    
    def get_last_log(self):
        query = """SELECT TrainingDate, DatasetSamplesCount, Accuracy, ModelFileName FROM TrainingLog ORDER BY TrainingDate DESC"""
        cursor = self.__dbConnection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return TrainingLog(result[0], result[1], result[2], result[3])