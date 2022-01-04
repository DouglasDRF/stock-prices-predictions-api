from fastapi import APIRouter, Depends
from .basic_security import get_basic_auth
from stockpredictions.services import StatisticsService

stats_router = APIRouter()
stats_service = StatisticsService()

@stats_router.put('/stats/{ticker}', tags=['Stats'])
async def update_with_real_values(ticker: str, credentials=Depends(get_basic_auth)):
    return { 'schedule_train': stats_service.update_stats(ticker) }
