from State import State
import numpy as np

class RiskAssessment:
    age = None
    immuno_compromised = None
    environment = None
    vaccinated = None
    days_traveling = None

    def __init__(self, age, immuno_compromised, environment, vaccinated, days_traveling):
        self.age = age
        self.immuno_compromised = immuno_compromised
        self.environment = environment
        self.vaccinated = vaccinated
        self.days_traveling = days_traveling

    def calculate_risk(self, state):
        days_out = state.metrics.days_out
        pct_change = np.array(state.metrics.get_percent_change())

        forecast_pct_change = (np.array(state.metrics.predictions[days_out]) -
        np.array(state.metrics.predictions[0])) / np.array(state.metrics.predictions[0]) * 100.0

        avg_pct_change = np.sum(pct_change) / len(pct_change)

        if ((avg_pct_change - forecast_pct_change) > 0):
            return 0 # less risk
        elif (avg_pct_change - forecast_pct_change < 0):
            return 1 # more risk

    def set_age(self, age):
        if type(age) != int:
            raise Exception("input should be an integer")
        self.age = age

    def set_immuno_compromised(self, immuno_compromised):
        if type(immuno_compromised) != bool:
            raise Exception("input should be a boolean")
        self.immuno_compromised = immuno_compromised

    def set_environment(self, environment):
        if type(environment) != bool:
            raise Exception("input should be a boolean")
        self.environment = environment

    def set_vaccinated(self, vaccinated):
        if type(vaccinated) != bool:
            raise Exception("input should be a boolean")
        self.vaccinated = vaccinated
