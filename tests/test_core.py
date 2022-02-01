from stockpredictions.core import get_model_instance, StocksPredictionModel

def test_get_model_instance():
    model = get_model_instance()
    assert model is not None
    assert type(model) is StocksPredictionModel
    
       
