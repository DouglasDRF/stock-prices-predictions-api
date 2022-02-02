class Predicted:
    def __init__(self, ticker:str, previous:float, predicted_value:float, prediction_type:str, direction:str, date:str, real_value=None, real_direction=None):
        self.ticker = ticker
        self.previous = previous
        self.predicted_value = predicted_value
        self.real_value = real_value
        self.prediction_type = prediction_type
        self.direction = direction
        self.real_direction = real_direction
        self.date = date