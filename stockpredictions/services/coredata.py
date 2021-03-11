from stockpredictions.data.repositories import CoreDataRepository
from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent

class DataService:

    def __init__(self, repository=CoreDataRepository(), apiData=YahooFinanceApiSvcAgent()):
        self.__repository = repository
        self.__apiData = apiData

    def get_supported_stocks(self):
        return self.__repository.get_supported_stocks()

    def save_last(self, ticker):
        last = self.__apiData.get_last_updated_value(ticker)
        self.__repository.save_last(last)
        return {"status_message": "Last StockPrice has been inserted to database", "last_stock_price": last}

    def update_last(self, ticker):
        last = self.__apiData.get_last_updated_value(ticker)
        self.__repository.update_last(last)
        return {"status_message": "Last StockPrice has been updated in database", "last_stock_price": last}

    def fill_history(self, ticker):
        history = self.__apiData.get_history_values(ticker)
        self.__repository.save_to_history(history)
        return {"status_message": "History has been filled"}
