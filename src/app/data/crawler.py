import requests
import os

from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.firefox.options import Options
from stock_price import StockPrice

from bs4 import BeautifulSoup

class StocksCrawler():
    def __init__(self, ticker='PETR4', source='https://br.investing.com/equities/'):
        opts = Options()
        opts.headless = True
        driver = Firefox(options=opts)
        url = source

        driver.get(url)

        html_content = driver.page_source
        self.__ticker = ticker
        self.__soup = BeautifulSoup(html_content, 'html.parser')

    def get_last_daily_price(self):
        table = self.__soup.find(id='curr_table').find('tbody')
        results = table.find_all('tr')
        last_daily_price = results[0]

        result = StockPrice(
            self.__ticker,
            last_daily_price.find_all('td')[0].get_text(),
            last_daily_price.find_all('td')[2].get_text(),
            last_daily_price.find_all('td')[1].get_text(),
            last_daily_price.find_all('td')[3].get_text(),
            last_daily_price.find_all('td')[4].get_text(),
            last_daily_price.find_all('td')[5].get_text())
        
        return result

crawler = StocksCrawler(ticker='AZUL4', source='https://br.investing.com/equities/azul-sa-pref-historical-data')
crawler.get_last_daily_price()
