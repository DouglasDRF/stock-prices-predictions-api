class Predicted:
    def __init__(self, ticker:str, previous, predicted_value, prediction_type:str, direction:str, date:str, real_value=None, real_direction=None):
        self.ticker = ticker,
        self.previous = previous,
        self.predicted_value = predicted_value,
        self.real_value = real_value,
        self.prediction_type = prediction_type,
        self.direction = direction,
        self.real_direction = real_direction,
        self.date = date

    def to_dict(self):
        result = {"ticker": self.ticker, "previous": self.previous, "next_predicted_value": self.predicted_value, "real_value": self.real_value, "prediction_type": self.prediction_type, "direction": self.direction, "real_direction": self.real_direction, "date": self.date}
        return result
