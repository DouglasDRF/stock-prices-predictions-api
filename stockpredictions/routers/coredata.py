from fastapi import APIRouter
from stockpredictions.services import DataService

data_router = APIRouter()
data_service = DataService()

@data_router.get('/data/update/{ticker}', tags=['Data'])
async def update_database(ticker: str):
    return data_service.update(ticker)
