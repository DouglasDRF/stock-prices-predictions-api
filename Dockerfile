FROM python:3.8-slim-buster

EXPOSE 8000

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./datasets ./datasets
COPY ./stockpredictions ./stockpredictions

ENV AWS_DEFAULT_REGION=sa-east-1
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=

CMD ["uvicorn", "stockpredictions.main:app", "--host", "0.0.0.0", "--port", "8000"]
