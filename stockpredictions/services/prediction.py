from stockpredictions.core.consts import PredictionType, Direction
from stockpredictions.models import Predicted
from stockpredictions.core.model import get_model_instance
from stockpredictions.data.repositories import CoreDataRepository, StatisticsRepository
import datetime as dt

from stockpredictions.services.service_models.model_responses import PredictNextDayResponse


class PredictionService:

    def __init__(self, core_repository=CoreDataRepository(), stats_repository=StatisticsRepository()):
        self.__model = get_model_instance()
        self.__core_repository = core_repository
        self.__stats_repository = stats_repository

    def predict_next_day(self, ticker: str, save_log: bool = False):
        history = self.__core_repository.get_history(ticker)
        df_history = self.__core_repository.get_history_dataframe(history)

        ochlv_normalized = self.__model.normalize_ochlv_history(df_history)
        price_predicted = round(self.__model.predict(ochlv_normalized).item(0), 2)

        direction = Direction.up if price_predicted > history[-1].close else Direction.down
        try:
            if(save_log):
                self.__stats_repository.save_prediction(Predicted(ticker, history[-1].close, price_predicted, PredictionType.close, direction,
                                                                  dt.date.today().isoformat()))
        except Exception as e:
            print(str(e))
        finally:
            return PredictNextDayResponse(ticker=ticker, next_day_value=float(price_predicted))