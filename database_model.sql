CREATE TABLE SupportedCompaniesToCrawler(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
    B3Code CHAR(6) NOT NULL,
    BrInvestingEndpoint VARCHAR(1024)
);

CREATE UNIQUE INDEX idx_b3code ON SupportedCompaniesToCrawler (B3Code);

CREATE TABLE StockPrice(
	Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
	Ticker CHAR(6) NOT NULL,
	`Timestamp` TIMESTAMP NOT NULL,
	`Open` DOUBLE NOT NULL,
	`Close` DOUBLE NOT NULL,
	High DOUBLE NOT NULL, 
	Low DOUBLE NOT NULL,
	Volume DOUBLE NOT NULL
);

CREATE INDEX idx_b3code ON StockPrice (Ticker);
CREATE INDEX idx_timestamp ON StockPrice (`Timestamp`);
CREATE INDEX uk_ticker_timestamp ON StockPrice (Ticker, `Timestamp`);