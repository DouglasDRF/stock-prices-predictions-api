
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn
from stockpredictions.routers import prediction_router, data_router, training_router, stats_router

app = FastAPI()
app.include_router(prediction_router)
app.include_router(data_router)
app.include_router(training_router)
app.include_router(stats_router)


@app.get("/")
async def root():
    return {"status": "Application is running. Check /docs or /redoc"}

def init_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stock Prices Prediction",
        version="v0.2.3",
        description='This is not an investiment sugestion. ' + 
        'This an API with research purposes only using LSTM (Long Short Term Memory) Deep Learning model to predict next day stocks prices (1d)',
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://cdn.iconscout.com/icon/free/png-256/stocks-72-1100762.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = init_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    print('Application is running without a web proxy...')
