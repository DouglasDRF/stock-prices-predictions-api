DROP DATABASE IF EXISTS StockPricesPrediction;
CREATE DATABASE StockPricesPrediction;
USE StockPricesPrediction;

DROP TABLE IF EXISTS SupportedCompaniesToCrawler;
CREATE TABLE SupportedCompaniesToCrawler(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    B3Code CHAR(6) NOT NULL,
    SourceEndpoint VARCHAR(1024)
);

CREATE UNIQUE INDEX idx_b3code ON SupportedCompaniesToCrawler (B3Code);

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


CREATE INDEX idx_b3code ON StockPrice (Ticker);
CREATE INDEX idx_timestamp ON StockPrice (`Date`);
CREATE UNIQUE INDEX uk_ticker_timestamp ON StockPrice (Ticker, `Date`);

DROP TABLE IF EXISTS PredictionHistories;
CREATE TABLE PredictionHistories(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	Ticker CHAR(6) NOT NULL, 
	PreviousReference DOUBLE NOT NULL,
	NextPredictedValue DOUBLE NOT NULL,
	RealValue DOUBLE,
	PredictionType VARCHAR(5) NULL,
	Direction VARCHAR(4) NOT NULL,
	RealDirection VARCHAR(4),
	`Date` DATE NOT NULL
);

CREATE INDEX idx_ticker ON PredictionHistories (Ticker);
CREATE INDEX idx_date ON PredictionHistories (`Date`);
CREATE UNIQUE INDEX uk_date_ticker ON PredictionHistories (`Date`, Ticker);

DROP TABLE IF EXISTS TrainingLog;
CREATE TABLE TrainingLog(
	Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    PreviousTrainingId INT,
    TrainingDate TIMESTAMP NOT NULL,
    DatasetSamplesCount INT NOT NULL,
    Accuracy DOUBLE NOT NULL,
    ModelFileName VARCHAR(64) NOT NULL
);

