import requests
import os
import datetime

from models.stock_price import StockPrice
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


class StocksCrawler():
    def __init__(self, ticker='PETR4', source='https://br.investing.com/equities/petrobras-pn-historical-data'):

        self.__source = source
        self.__ticker = ticker
        self.__expected_data = None
        self.__soup = None

        self.__init_webdrive()

    def get_last_daily_price(self):

        if 'br.investing' in self.__source:
            return self.__extract_data_from_brinvesting(True)
        else:
            return self.__extract_data_from_infomoney(True)

    def get_history(self):

        if 'br.investing' in self.__source:
            return self.__extract_data_from_brinvesting()
        else:
            return self.__extract_data_from_infomoney()

    def __extract_data_from_infomoney(self, lastOnly=False):
        lines = self.__expected_data.split('\n')
        results = []

        if lastOnly == True:
            lines = lines[:1]

        for l in lines:
            columns = l.split(' ')
            results.append(StockPrice(
                self.__ticker,
                datetime.datetime.strptime(columns[0], '%d/%m/%Y'),
                columns[1].replace(',', '.'),
                columns[2].replace(',', '.'),
                columns[4].replace(',', '.'),
                columns[5].replace(',', '.'),
                columns[6]))

        return results

    def __extract_data_from_brinvesting(self, lastOnly=False):
        table = self.__soup.find(id='curr_table').find('tbody')
        data = table.find_all('tr')
        results = []

        if lastOnly == True:
            data = data[:1]

        for r in data:
            results.append(StockPrice(
                self.__ticker,
                r.find_all('td')[0].get_text(),
                r.find_all('td')[2].get_text().replace(',', '.'),
                r.find_all('td')[1].get_text().replace(',', '.'),
                r.find_all('td')[3].get_text().replace(',', '.'),
                r.find_all('td')[4].get_text().replace(',', '.'),
                r.find_all('td')[5].get_text()))

        return results

    def __init_webdrive(self):
        opts = Options()
        opts.headless = True
        driver = Firefox(options=opts)

        driver.get(self.__source)

        if 'br.investing' in self.__source:
            html_content = driver.page_source
            self.__soup = BeautifulSoup(html_content, 'html.parser')

        elif 'infomoney' in self.__source:
            max_retries = 100
            retry = 0
            while(True):
                waiting_time = 10
                expected_data = WebDriverWait(driver, waiting_time).until(
                    EC.presence_of_element_located((By.ID, 'quotes_history')))
                self.__expected_data = expected_data.find_element_by_tag_name(
                    'tbody').text
                if('Carregando...' not in self.__expected_data or retry > max_retries):
                    break
        else:
            raise('Data source not supported')

        driver.close()
