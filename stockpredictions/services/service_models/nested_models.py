
from pydantic import BaseModel

class StockPrice(BaseModel):
    ticker: str
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: int

class Predicted(BaseModel):
    ticker: str
    previous: str
    predicted_value: float
    real_value: float
    prediction_type: str
    direction: str
    real_direction: str
    date: str