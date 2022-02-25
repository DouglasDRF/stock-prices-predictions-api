from typing import List
from pydantic import BaseModel

from stockpredictions.services.service_models.nested_models import StockPriceViewModel


class StockPriceResponse(BaseModel):
    status_message: str
    last_stock_price: StockPriceViewModel


class FillHistoryResponse(BaseModel):
    status_message: str


class PredictNextDayResponse(BaseModel):
    ticker: str
    next_day_value: float

class TrainingStatusResponse(BaseModel):
    is_model_trained: bool
    current_accuracy: float
    tickers_on_training: List[str]
