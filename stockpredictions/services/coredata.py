from stockpredictions.data.repositories import CoreDataRepository
from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent
from stockpredictions.services.service_models.model_responses import FillHistoryResponse, StockPriceResponse
from stockpredictions.services.service_models.nested_models import PredictedViewModel, StockPriceViewModel


class DataService:

    def __init__(self, repository=CoreDataRepository(), apiData=YahooFinanceApiSvcAgent()):
        self.__repository = repository
        self.__apiData = apiData

    def get_last_predictions(self):
        result = self.__repository.get_last_predictions()
        for x in result:
            yield PredictedViewModel(
                ticker=x.ticker, previous=x.previous, predicted_value=x.predicted_value, real_value=x.real_value,
                prediction_type=x.prediction_type, direction=x.direction, real_direction=x.direction, date=x.date)

    def get_supported_stocks(self):
        return self.__repository.get_supported_stocks()

    def get_non_past_days_compliant(self, count):
        return self.__repository.get_non_past_days_compliant(count)

    def save_last(self, ticker):
        last = self.__apiData.get_last_updated_value(ticker)
        result = self.__repository.save_last(last)
        return StockPriceResponse(
            status_message="Last StockPrice has been inserted to database",
            last_stock_price=StockPriceViewModel(ticker=result.ticker, date=result.date, open=result.open,
                                                 close=result.close, high=result.high, low=result.low, volume=result.volume))

    def update_last(self, ticker):
        last = self.__apiData.get_last_updated_value(ticker)
        result = self.__repository.update_last(last)
        return StockPriceResponse(
            status_message="Last StockPrice has been updated in database",
            last_stock_price=StockPriceViewModel(ticker=result.ticker, date=result.date, open=result.open,
                                                 close=result.close, high=result.high, low=result.low, volume=result.volume))

    def fill_history(self, ticker):
        history = self.__apiData.get_history_values(ticker)
        self.__repository.save_to_history(history)
        return FillHistoryResponse(status_message="History has been filled")
