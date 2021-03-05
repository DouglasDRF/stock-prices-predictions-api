import numpy as np
import matplotlib.pyplot as plt

from core.model import StocksPredictionModel
from data import StocksCrawler, CoreDataRepository


class PredictionService:

    def __init__(self):
        self.__model = StocksPredictionModel()
        self.__repository = CoreDataRepository()

    def predict_next_day(self, ticker: str):
        history = self.__repository.get_history(ticker)
        df_history = self.__repository.get_history_dataframe(history)

        ochlv_normalized = self.__model.normalize_ochlv_history(df_history)
        price_predicted = self.__model.predict(ochlv_normalized)
        return price_predicted.item(0)