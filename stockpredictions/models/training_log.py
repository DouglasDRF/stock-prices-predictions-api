class TrainingLog:
    def __init__(self, samples_count, accuracy, model_file_name, tickers_on_trainning):
        self.samples_count = samples_count,
        self.accuracy = accuracy,
        self.model_file_name = model_file_name,
        self.tickers_on_trainning = tickers_on_trainning

    def to_dict(self):
        result = {"date": self.date, "samples_count": self.samples_count, "accuracy": self.accuracy, "prediction_type":
                  self.prediction_type, "model_file_name": self.model_file_name, "tickers_on_trainning": self.tickers_on_trainning}
        return result
