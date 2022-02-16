from stockpredictions.core.consts import Direction
from stockpredictions.data.repositories import StatisticsRepository
from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent
from stockpredictions.models.predicted import Predicted
import pandas as pd


class StatisticsService:

    def __init__(self, stats_repository=StatisticsRepository(), svc=YahooFinanceApiSvcAgent()):
        self.__stats = stats_repository
        self.__svc_agent = svc

    def update_stats(self, ticker) -> Predicted:
        try:
            last_real = self.__svc_agent.get_last_updated_value(ticker)
            last_predicted_price = self.__stats.get_last_predicted_price(
                ticker)
            direction = Direction.up if last_real.close > last_predicted_price.previous else Direction.down
            result = self.__stats.update_logs_with_real_values(
                ticker, last_predicted_price.date, last_real.close, direction)
            last_predicted_price.real_direction = result['real_direction']
            last_predicted_price.real_value = result['real_value']
            return last_predicted_price
        except Exception as e:
            print(e)
            return None

    def get_real_current_overall_accuracy(self):
        predictions = self.__stats.get_all_predictions_updated()
        df = pd.DataFrame(vars(p) for p in predictions)

        correct_predictions = len(df[df.real_direction == df.direction])
        percentage = correct_predictions / len(predictions) * 100

        return {'overall_current_predictions_percentage': percentage}

    def get_real_current_accuracy_by_ticker(self, ticker: str):
        predictions = self.__stats.get_all_predictions_updated()
        df = pd.DataFrame(vars(p) for p in predictions)
        df = df.drop(df[df.ticker != ticker].index)

        correct_predictions = len(df[df.real_direction == df.direction])
        percentage = correct_predictions / len(df) * 100

        return {'current_predictions_percentage': percentage}
