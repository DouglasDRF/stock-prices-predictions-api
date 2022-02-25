from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class StockPriceViewModel(BaseModel):
    ticker: str
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: int

class PredictedViewModel(BaseModel):
    ticker: Optional[str]
    previous: Optional[float]
    predicted_value: Optional[float]
    real_value: Optional[float]
    prediction_type: Optional[str]
    direction: Optional[str]
    real_direction: Optional[str]
    date: Optional[Any]