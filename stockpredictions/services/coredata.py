from stockpredictions.data import StocksCrawler, CoreDataRepository
import threading


class DataService:

    def __init__(self):
        self.__repository = CoreDataRepository()

    def update(self, ticker):
        t = threading.Thread(target=self.__updateTask, args=(ticker,))
        t.start()
        return { "status_message": "Update database task has been scheduled"}

    def __updateTask(self, ticker):
        try:
            crawler = StocksCrawler(ticker, self.__repository.get_ticker_source(ticker))
            history = crawler.get_history()
            self.__repository.save_to_history(history)
            print("Scheduler update task ran sucessfully")
        except:
            print("Scheduled update task ran with error")
        
