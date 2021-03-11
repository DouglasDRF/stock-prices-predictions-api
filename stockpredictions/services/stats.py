import numpy as np
import matplotlib.pyplot as plt

from stockpredictions.core.consts import PredictionType, Direction
from stockpredictions.data.repositories import StatisticsRepository
from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent
import datetime as dt
import asyncio

class StatisticsService:

    def __init__(self, stats_repository=StatisticsRepository(), svc=YahooFinanceApiSvcAgent()):
        self.__stats = StatisticsRepository()
        self.__svc_agent = svc

    def update_stats(self, ticker):
        last_real = self.__svc_agent.get_last_updated_value(ticker)
        last_predicted_price = self.__stats.get_last_predicted_price(ticker)
        direction = Direction.up if last_real.close > last_predicted_price else Direction.down
        self.__stats.update_logs_with_real_values(ticker, last_real.close, direction)
