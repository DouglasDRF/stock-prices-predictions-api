from fastapi import APIRouter
from stockpredictions.services import PredictionService

prediction_router = APIRouter()
prediction_service = PredictionService()

@prediction_router.get('/predict/nextday/{ticker}', tags=['Prediction'])
async def predic_next_day(ticker: str):
    return prediction_service.predict_next_day(ticker)

@prediction_router.get('/predict/nextweek/{ticker}', tags=['Prediction'])
async def predic_next_day(ticker: str):
    return prediction_service.predict_next_day(ticker)

@prediction_router.get('/predict/nextmonth/{ticker}', tags=['Prediction'])
async def predic_next_day(ticker: str):
    return prediction_service.predict_next_day(ticker) 