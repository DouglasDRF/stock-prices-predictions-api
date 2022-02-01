from fastapi import APIRouter, Depends
from .basic_security import get_basic_auth
from stockpredictions.services import DataService

data_router = APIRouter()
data_service = DataService()

@data_router.get('/data/predictions', tags=['Data'])
async def get_last_predictions(): 
    return data_service.get_last_predictions()

@data_router.get('/data/supported-stocks', tags=['Data'])
async def get_supported_stocks():
    return data_service.get_supported_stocks()

@data_router.get('/data/supported-stocks/non-compliant/{count}', tags=['Data'])
async def get_non_past_days_compliant(count:int=40):
    return data_service.get_non_past_days_compliant(count)

@data_router.put('/data/stock-prices/{ticker}', tags=['Data'])
async def update_last_price(ticker: str, credentials=Depends(get_basic_auth)):
    return data_service.update_last(ticker)

@data_router.post('/data/stock-prices/{ticker}', tags=['Data'])
async def save_last_price(ticker: str, credentials=Depends(get_basic_auth)):
    return data_service.save_last(ticker)

@data_router.post('/data/stock-prices/history/{ticker}', tags=['Data'])
async def fill_history(ticker: str, credentials=Depends(get_basic_auth)):
    return data_service.fill_history(ticker)