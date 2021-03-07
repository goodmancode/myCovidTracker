import numpy as np

class StateMetrics:
    predictions = None
    avg_cases_per_day = None
    model_accuracy = None
    percent_change = None
    days_out = None
    last_historical_data = None

    def __init__(self, predictions, avg_cases_per_day, model_accuracy, percent_change, last_historical_data):
        self.predictions = predictions
        self.avg_cases_per_day = avg_cases_per_day
        self.model_accuracy = model_accuracy
        self.percent_change = percent_change
        self.last_historical_data = last_historical_data

    def get_predictions(self):
        return self.predictions

    def get_percent_change(self):
        return self.percent_change

    def get_model_accuracy(self):
        return self.model_accuracy

    def avg_cases_per_day(self):
        return self.avg_cases_per_day

    def get_last_historical_data(self):
        return self.last_historical_data

    def predict_days_out(self, days):
        self.days_out = days
        return self.predictions[:days]

    

