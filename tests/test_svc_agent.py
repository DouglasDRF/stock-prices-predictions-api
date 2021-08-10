from stockpredictions.data.svcagents.yahoo_finance import YahooFinanceApiSvcAgent
import datetime

class TestSvcAgent:

    def test_get_last_updated_value(self):

        svc = YahooFinanceApiSvcAgent()
        result = svc.get_last_updated_value('PETR4')    
     
        assert result.ticker == 'PETR4'
        assert result.close != 0.0
        
        now = datetime.datetime.now()
        hour = int('{:02d}'.format(now.hour))

        if(hour < 17 and hour > 9):
            assert result.open != 0.0
            assert result.high != 0.0
            assert result.low != 0.0
            assert result.low != 0
        else:
            assert result.open == 0.0
            assert result.high == 0.0
            assert result.low == 0.0
            assert result.low == 0

    def test_get_history_values(self):

        svc = YahooFinanceApiSvcAgent()
        result = svc.get_history_values('PETR4')    
     
        assert len(result) > 1
        assert result[0].ticker == 'PETR4'
        assert result[0].open != 0.0
        assert result[0].close != 0.0
        assert result[0].high != 0.0
        assert result[0].low != 0.0
        assert result[0].low != 0          

