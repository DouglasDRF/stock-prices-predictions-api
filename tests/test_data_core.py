from stockpredictions.data.repositories.core_data import CoreDataRepository
from stockpredictions.data.svcagents.yahoo_finance import YahooFinanceApiSvcAgent


def test_get_last_predictions():
    repo = CoreDataRepository(YahooFinanceApiSvcAgent())
    result = repo.get_last_predictions()
    assert len(result) > 0

