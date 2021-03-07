from fastapi import APIRouter
from stockpredictions.services import TrainingService

training_router = APIRouter()
training_service = TrainingService()

@training_router.post('/train/{ticker}', tags=['Training'])
async def train(ticker: str):
    return { 'schedule_train': training_service.train(ticker) }

@training_router.get('/train/status', tags=['Training'])
async def get_status():
    return training_service.get_status() 