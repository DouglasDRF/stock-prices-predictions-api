from stockpredictions.data.svcagents import YahooFinanceApiSvcAgent
from unittest.mock import MagicMock

class TestSvcAgent:

    def test_get_last_updated_value(self):

        svc = YahooFinanceApiSvcAgent()
        result = svc.get_last_updated_value('BBDC4')    
     
        assert result.ticker == 'BBDC4'
        assert result.open != 0.0
        assert result.close != 0.0
        assert result.high != 0.0
        assert result.low != 0.0
        assert result.low != 0

    def test_get_history_values(self):

        svc = YahooFinanceApiSvcAgent()
        result = svc.get_history_values('BBDC4')    
     
        assert len(result) > 1
        assert result[0].ticker == 'BBDC4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0          
