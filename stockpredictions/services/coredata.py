from data import CoreDataRepository
from data import StocksCrawler
import threading

class DataService:

    def __init__(self):
        self.__repository = CoreDataRepository()

    
    def update(self, ticker):
        t = threading.Thread(target=self.__update, args=(ticker,))
        t.start()
        return { "status_message": "Update database task has been scheduled"}

    def __update(self, ticker):
        try:
            crawler = StocksCrawler(ticker, self.__repository.get_ticker_source(ticker))
            last = crawler.get_last_daily_price()
            self.__repository.save_last(last)
            print("Scheduler update task ran sucessfully")
        except Exception as e:
            print("Scheduled update task ran with error: \n" + e)
        
    
    def fill_history(self, ticker):
        t = threading.Thread(target=self.__fillTask, args=(ticker,))
        t.start()
        return { "status_message": "Fill history task has been scheduled"}

    def __fillTask(self, ticker):
        try:
            crawler = StocksCrawler(ticker, self.__repository.get_ticker_source(ticker))
            history = crawler.get_history()
            self.__repository.save_to_history(history)
            print("Scheduler fill history task ran sucessfully")
        except Exception as e:
            print("Scheduled fill history task ran with error: \n" + str(e))
        
