from stockpredictions.core.consts import PredictionType, Direction
from stockpredictions.models import TrainingLog
from stockpredictions.core.model import get_model_instance
from stockpredictions.core.data_helper import load_dataset
from stockpredictions.data.repositories import TrainingLogRepository
import datetime as dt

class TrainingService:

    def __init__(self):
        self.__training_log = TrainingLogRepository()
        self.__model = get_model_instance()

    def train(self, ticker: str):
        try:
            dataset = load_dataset(ticker)
            
            model_saved = self.__model.train(dataset, True)
            
            self.__model.tickers_on_trainning.append(ticker)
            tickers_text_list = ''
            
            for x in self.__model.tickers_on_trainning:
                tickers_text_list = tickers_text_list + str(x) + ','

            self.__training_log.save_training_log(TrainingLog(len(dataset), float(self.__model.current_accuracy), model_saved, tickers_text_list))
            print("Train task ran sucessfully")
        except Exception as e:
            print("Train task ran with error: \n" + str(e))

    def get_status(self):
        return {"is_model_trained": self.__model.is_trained,
                "current_accuracy": self.__model.current_accuracy,
                "tickers_on_trainning": self.__model.tickers_on_trainning
                }