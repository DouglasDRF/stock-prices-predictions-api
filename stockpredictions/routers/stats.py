from fastapi import APIRouter, Depends
from .basic_security import get_basic_auth
from stockpredictions.services import StatisticsService

stats_router = APIRouter()
stats_service = StatisticsService()

@stats_router.get('/stats/accuracy', tags=['Stats'])
async def get_real_current_overall_accuracy():
    response = stats_service.get_real_current_overall_accuracy()
    if response is not None:
        return response
@stats_router.get('/stats/accuracy/{ticker}', tags=['Stats'])
async def get_real_current_accuracy_by_ticker(ticker: str):
    response = stats_service.get_real_current_accuracy_by_ticker(ticker)
    if response is not None:
        return response

@stats_router.put('/stats/predictions/{ticker}', tags=['Stats'])
async def update_with_real_values(ticker: str, credentials=Depends(get_basic_auth)):
    response = stats_service.update_stats(ticker)
    if response is not None:
        return response
    