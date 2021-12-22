
# StockPricesPredictions

[![License](https://img.shields.io/github/license/douglasdrf/StockPricesPredictions?style=plastic)](https://github.com/DouglasDRF/StockPricesPredictions/blob/master/LICENSE)
[![Build Status](https://app.travis-ci.com/DouglasDRF/stock-prices-predictions-api.svg?branch=master)](https://app.travis-ci.com/DouglasDRF/stock-prices-predictions-api.svg?branch=master)


Disclaimer: This is not an investment suggestion. This is and experimental tool with reseach purposes.

API with Stock Prices Predictions 1d for helping on Swing Trade using LSTM Deep Learning Algorithm.
You should insert on table `SupportedCompanies` the ticker symbol to get its being on list to be processed.

This application requires a AWS DynamoDB resource to store the date and if you're ruinnin in a cointainer, the AWS Credentials must be provided by enviroment variables.

The daily automation for running this API should be found at the repo below: </br>
https://github.com/DouglasDRF/StockPredictionsCronJob

