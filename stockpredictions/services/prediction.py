import numpy as np
import matplotlib.pyplot as plt

from stockpredictions.core.model import StocksPredictionModel
from stockpredictions.core.data_helper import load_dataset

class PredictionService:

    def __init__(self):
        self.__model = StocksPredictionModel()

    def predict_next_day(self, ticker:str):
        ochlv_normalized = self.__model.normalize_ochlv_history()
        price_predicted = self.__model.predict()
