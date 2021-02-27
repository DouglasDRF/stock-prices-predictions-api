from stockpredictions.core.model import StocksPredictionModel
from stockpredictions.core.data_helper import load_dataset

class TestLstmModel:

    def test_create_model_from_saved(self):

        model = StocksPredictionModel()
        
        dataset = load_dataset('BBDC4')
        ochlv_history_normalized = model.normalize_ochlv_history(dataset)

        y_predicted = model.predict(ochlv_history_normalized)

        assert y_predicted[0] > 0
    
    def test_train_model(self):

        model = StocksPredictionModel()

        dataset = load_dataset('BBDC4')
        model.train(dataset)

        ochlv_history_normalized = model.normalize_ochlv_history(dataset)
        y_predicted = model.predict(ochlv_history_normalized)

        assert y_predicted[0] > 0
        assert model.current_accuracy > 0.9