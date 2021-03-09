from stockpredictions.data import CoreDataRepository
from stockpredictions.data import StocksCrawler
import asyncio

class DataService:

    def __init__(self):
        self.__repository = CoreDataRepository()

    def get_supported_stocks(self):
        return  self.__repository.get_supported_stocks() 
    
    def update(self, ticker):
        t = asyncio.create_task(self.__update(ticker))
        return { "status_message": "Update database task has been scheduled"}

    def fill_history(self, ticker):
        t = asyncio.create_task(self.__fillTask(ticker))
        return { "status_message": "Fill history task has been scheduled"}

    async def __update(self, ticker):
        try:
            with StocksCrawler(ticker, self.__repository.get_ticker_source(ticker)) as crawler:
                last = crawler.get_last_daily_price()
                self.__repository.save_last(last)
                print("Scheduler update task ran sucessfully")
        except Exception as e:
            print("Scheduled update task ran with error: \n" + str(e))

    async def __fillTask(self, ticker):
        try:
            print('Initiating fiiling task')
            with StocksCrawler(ticker, self.__repository.get_ticker_source(ticker)) as crawler:
                history = crawler.get_history()
                self.__repository.save_to_history(history)
                print("Scheduler fill history task ran sucessfully")
        except Exception as e:
            print("Scheduled fill history task ran with error: \n" + str(e))
        
