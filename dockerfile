FROM python:3.8-slim-buster

EXPOSE 8000

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get update 
RUN apt-get install software-properties-common -y
RUN apt-get install gnupg2 -y
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 3B4FE6ACC0B21F32
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 871920D1991BC93C
RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu/ focal main restricted"
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install firefox -y
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/

RUN pip3 install -r requirements.txt

COPY ./stockpredictions ./stockpredictions

ENV MYSQL_HOST=""
ENV MYSQL_USER=""
ENV MYSQL_PASSWORD=""
ENV MYSQL_DATABASE=""

CMD [ "python3", "-m" , "uvicorn", "stockpredictions.main:app"]