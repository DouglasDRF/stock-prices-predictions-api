DROP DATABASE IF EXISTS StockPricesPrediction;
CREATE DATABASE StockPricesPrediction;
USE StockPricesPrediction;

DROP TABLE IF EXISTS SupportedCompaniesToCrawler;
CREATE TABLE SupportedCompaniesToCrawler(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    B3Code CHAR(6) NOT NULL,
    SourceEndpoint VARCHAR(1024)
);

DROP TABLE IF EXISTS StockPrice;
CREATE TABLE StockPrice(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
	Ticker CHAR(6) NOT NULL,
	`Date` DATE NOT NULL,
	`Open` DOUBLE NOT NULL,
	`Close` DOUBLE NOT NULL,
	High DOUBLE NOT NULL, 
	Low DOUBLE NOT NULL,
	Volume DOUBLE NOT NULL
);

DROP TABLE IF EXISTS PredictionHistories;
CREATE TABLE PredictionHistories(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	Ticker CHAR(6) NOT NULL, 
	`Open` DOUBLE NOT NULL,
	RealOpen DOUBLE NOT NULL,
	PredictionType INT NULL,
	`Timestamp` TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX idx_b3code ON SupportedCompaniesToCrawler (B3Code);

CREATE INDEX idx_b3code ON StockPrice (Ticker);
CREATE INDEX idx_timestamp ON StockPrice (`Date`);
CREATE UNIQUE INDEX uk_ticker_timestamp ON StockPrice (Ticker, `Date`);

CREATE INDEX idx_ticker ON PredictionHistories (Ticker);
CREATE INDEX idx_timestamp ON PredictionHistories (`Timestamp`);
