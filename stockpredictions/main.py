
from fastapi import FastAPI
from routers import prediction_router
from routers import data_router

app = FastAPI()
app.description = 'Stock Prices Predcition API'
app.include_router(prediction_router)
app.include_router(data_router)


@app.get("/")
async def root():
    return {"status": "Application is running. Check /docs"}
