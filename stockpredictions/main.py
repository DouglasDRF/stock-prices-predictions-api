from fastapi import FastAPI
from stockpredictions.routers import prediction_router
from stockpredictions.routers import data_router

app = FastAPI()
app.description = 'Stock Prices Predcition API'
app.include_router(prediction_router)
app.include_router(data_router)