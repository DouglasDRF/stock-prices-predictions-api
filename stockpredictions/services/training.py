from stockpredictions.models import TrainingLog
from stockpredictions.core.model import get_model_instance
from stockpredictions.core.data_helper import load_dataset
from stockpredictions.data.repositories import TrainingLogRepository


class TrainingService:

    def __init__(self):
        self.__training_log = TrainingLogRepository()
        self.__model = get_model_instance()

    def train(self, ticker: str):
        status = self.get_status()
        if(len(self.__model.tickers_on_training) == 0 and self.__model.is_trained):
            self.__model.tickers_on_training.append(
                status['tickers_on_training'])
        try:
            dataset = load_dataset(ticker)
            SAVE = True
            model_saved = self.__model.train(dataset, SAVE)

            self.__model.tickers_on_training.append(ticker)
            tickers_text_list = ''

            for x in self.__model.tickers_on_training:
                tickers_text_list = tickers_text_list + str(x) + ','

            tickers_text_list = tickers_text_list.rstrip(',')
            if(SAVE):
                self.__training_log.save_training_log(TrainingLog(self.__model.total_samples_trained + len(dataset), float(
                    self.__model.current_accuracy), model_saved, tickers_text_list))
            print("Train task ran sucessfully")
        except Exception as e:
            print("Train task ran with error: \n" + str(e))

    def get_status(self):
        if(self.__model.is_trained and len(self.__model.tickers_on_training) == 0):
            log = self.__training_log.get_last_log()
            self.__model.tickers_on_training = log.tickers_on_training
            self.__model.current_accuracy = log.accuracy
            self.__model.total_samples_trained = log.samples_count

        return {
            "is_model_trained": self.__model.is_trained,
            "current_accuracy": float(self.__model.current_accuracy),
            "tickers_on_training": self.__model.tickers_on_training
        }
