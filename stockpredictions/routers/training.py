from fastapi import APIRouter, BackgroundTasks, Depends
from stockpredictions.services import TrainingService
from .basic_security import get_basic_auth

training_router = APIRouter()
training_service = TrainingService()

@training_router.post('/train/{ticker}', tags=['Training'])
async def train(ticker: str, background_tasks: BackgroundTasks, credentials=Depends(get_basic_auth)):
    background_tasks.add_task(training_service.train, ticker)
    return { 'schedule_train': "Train has been scheduled sucessfully" }

@training_router.get('/train/status', tags=['Training'])
async def get_status():
    return training_service.get_status() 