from stockpredictions.core.consts import Direction
from stockpredictions.data.repositories import StatisticsRepository
from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent


class StatisticsService:

    def __init__(self, stats_repository=StatisticsRepository(), svc=YahooFinanceApiSvcAgent()):
        self.__stats = stats_repository
        self.__svc_agent = svc

    def update_stats(self, ticker) -> bool:
        try:
            last_real = self.__svc_agent.get_last_updated_value(ticker)
            last_predicted_price = self.__stats.get_last_predicted_price(
                ticker)
            direction = Direction.up if last_real.close > last_predicted_price.predicted_value[
                0] else Direction.down
            self.__stats.update_logs_with_real_values(
                ticker, last_predicted_price.date, last_real.close, direction)
            return True
        except Exception as e:
            print(e)
            return False
