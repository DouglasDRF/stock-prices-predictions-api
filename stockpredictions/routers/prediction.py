from fastapi import APIRouter
from stockpredictions.services import PredictionService


prediction_router = APIRouter()
prediction_service = PredictionService()


@prediction_router.get('/predict/nextday/{ticker}', tags=['Prediction'])
async def predic_next_day(ticker: str, save_log: bool = False):
    return {'ticker': ticker, 'next_day_value': prediction_service.predict_next_day(ticker, save_log)}

# @prediction_router.get('/predict/nextweek/{ticker}', tags=['Prediction'])
# async def predic_next_week(ticker: str):
#     return { "Message" : "Not implemented"}
#     # return prediction_service.predict_next_day(ticker)

# @prediction_router.get('/predict/nextmonth/{ticker}', tags=['Prediction'])
# async def predic_next_month(ticker: str):
#     return { "Message" : "Not implemented"}
#     # return prediction_service.predict_next_day(ticker)
