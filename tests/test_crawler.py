from stockpredictions.data.crawler import StocksCrawler
from unittest.mock import MagicMock

class TestCrawler:

    def test_get_last_price_infomoney(self):

        crawler = StocksCrawler(ticker='BBDC4', source='https://www.infomoney.com.br/cotacoes/bradesco-bbdc4/historico/')
        result = crawler.get_last_daily_price()    
        
        assert len(result) == 1
        
        assert result[0].ticker == 'BBDC4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0 
        

    def test_get_history_infomoney(self):

        crawler = StocksCrawler(ticker='BBDC4', source='https://www.infomoney.com.br/cotacoes/bradesco-bbdc4/historico/')
        result = crawler.get_history()    

        assert len(result) > 1
        
        assert result[0].ticker == 'BBDC4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0 
    
    def test_get_last_price_brinvesting(self):

        crawler = StocksCrawler(ticker='BBDC4', source='https://br.investing.com/equities/bradesco-pn-n1-historical-data')
        result = crawler.get_last_daily_price()    
        
        assert len(result) == 1
        
        assert result[0].ticker == 'BBDC4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0 
        

    def test_get_history_brinvesting(self):

        crawler = StocksCrawler(ticker='BBDC4', source='https://br.investing.com/equities/bradesco-pn-n1-historical-data')
        result = crawler.get_history()    

        assert len(result) > 1
        
        assert result[0].ticker == 'BBDC4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0         
