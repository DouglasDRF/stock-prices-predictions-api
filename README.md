
# StockPricesPredictions

[![License](https://img.shields.io/github/license/douglasdrf/StockPricesPredictions?style=plastic)](https://github.com/DouglasDRF/StockPricesPredictions/blob/master/LICENSE)
[![Build Status](https://img.shields.io/travis/DouglasDRF/StockPricesPredictions?style=plastic)](https://www.travis-ci.com/DouglasDRF/StockPricesPredictions)


Disclaimer: This is not an investment suggestion. This is and experimental tool with reseach purposes.

API with Stock Prices Predictions 1d for helping on Swing Trade using LSTM Deep Learning Algorithm.
Currently, it only supports few Bovespa stocks. There's a crawler instead an API that most of them are paid


This application requires a MySQL database that should be provided before the application startup. The script for the schemas model it's on file database_mode.sql

It also depends of firefox and an selenium web driver. For Linux users, there's a shell to install it all. On windows, it should be installed manually and it can be found at:
https://github.com/mozilla/geckodriver
