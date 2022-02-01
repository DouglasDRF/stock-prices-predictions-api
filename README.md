# StockPricesPredictions

[![License](https://img.shields.io/github/license/douglasdrf/StockPricesPredictions?style=plastic)](https://github.com/DouglasDRF/StockPricesPredictions/blob/master/LICENSE)
![Lines of code](https://img.shields.io/tokei/lines/github/DouglasDRF/stock-prices-predictions-api?style=plastic)
[![Build Status](https://img.shields.io/travis/com/DouglasDRF/stock-prices-predictions-api/master?style=plastic)](https://app.travis-ci.com/github/DouglasDRF/stock-prices-predictions-api)
[![Code Quality](https://img.shields.io/codacy/grade/0d099f9713954c929336ea0e453403a8/master?style=plastic)](https://www.codacy.com/gh/DouglasDRF/stock-prices-predictions-api/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DouglasDRF/stock-prices-predictions-api&amp;utm_campaign=Badge_Grade)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/DouglasDRF/stock-prices-predictions-api?style=plastic)](https://codeclimate.com/github/DouglasDRF/stock-prices-predictions-api/maintainability)

Disclaimer: This is not an investment suggestion. This is and experimental tool with reseach purposes.

API with Stock Prices Predictions 1d for helping on Swing Trade using LSTM Deep Learning Algorithm.
You should insert on table `SupportedCompanies` the ticker symbol to get its being on list to be processed.

This application requires a AWS DynamoDB resource to store the date and if you're ruinnin in a cointainer, the AWS Credentials must be provided by enviroment variables.

The daily automation for running this API should be found at the repo below: </br>
https://github.com/DouglasDRF/StockPredictionsCronJob
