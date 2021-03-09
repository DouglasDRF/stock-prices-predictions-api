
from fastapi import FastAPI
import uvicorn
from stockpredictions.routers import prediction_router, data_router, training_router
import gc

app=FastAPI()
app.description='Stock Prices Predcition API'
app.include_router(prediction_router)
app.include_router(data_router)
app.include_router(training_router)

if not gc.isenabled():
    gc.enable()
    print('GC has been enabled')

@app.get("/")
async def root():
    return {"status": "Application is running. Check /docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)