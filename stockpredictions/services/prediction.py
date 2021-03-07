import numpy as np
import matplotlib.pyplot as plt

from stockpredictions.core.consts import PredictionType, Direction
from stockpredictions.models import Predicted
from stockpredictions.core.model import get_model_instance
from stockpredictions.data import StocksCrawler, CoreDataRepository, StatisticsRepository
import datetime as dt


class PredictionService:

    def __init__(self):
        self.__model = get_model_instance()
        self.__core_repository = CoreDataRepository()
        self.__stats_repository = StatisticsRepository()

    def predict_next_day(self, ticker: str):
        history = self.__core_repository.get_history(ticker)
        df_history = self.__core_repository.get_history_dataframe(history)

        ochlv_normalized = self.__model.normalize_ochlv_history(df_history)
        price_predicted = self.__model.predict(ochlv_normalized).item(0)

        direction = Direction.up if price_predicted > history[0].open else Direction.down
        try:
            self.__stats_repository.save_prediction(Predicted(ticker, price_predicted, PredictionType.opn, direction, dt.datetime.now().isoformat()))
        finally:
            return price_predicted

    