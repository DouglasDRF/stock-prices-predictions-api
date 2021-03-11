FROM python:3.8-slim-buster

EXPOSE 8000

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./trained_models ./trained_models
COPY ./datasets ./datasets
COPY ./stockpredictions ./stockpredictions

ENV MYSQL_HOST=""
ENV MYSQL_USER=""
ENV MYSQL_PASSWORD=""
ENV MYSQL_DATABASE=""

CMD ["uvicorn", "stockpredictions.main:app", "--host", "0.0.0.0", "--port", "8000"]