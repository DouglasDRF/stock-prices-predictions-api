from fastapi import APIRouter
from stockpredictions.services import TrainingService

training_router = APIRouter()
training_service = TrainingService()

@training_router.post('/train/{ticker}', tags=['Training'])
async def predic_next_day(ticker: str):
    return { 'schedule_train': training_service.train(ticker) }

@training_router.get('/train/status', tags=['Training'])
async def predic_next_day():
    return { 'IsLSTMModelTrained': training_service.get_status() }