from fastapi import APIRouter
from services import DataService

data_router = APIRouter()
data_service = DataService()

@data_router.put('/data/fill-history/{ticker}', tags=['Data'])
async def update_database(ticker: str):
    return data_service.fill_history(ticker)

@data_router.put('/data/update-last/{ticker}', tags=['Data'])
async def update_database(ticker: str):
    return data_service.update(ticker)
