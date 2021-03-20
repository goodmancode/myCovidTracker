import StateMetrics
import numpy as np

class RiskAssessment:
    risk_value = None
    risk_string = None
    age = None
    sex = None
    loss_of_smell_and_taste = None
    persistent_cough = None
    severe_fatigue = None
    skipped_meals = None
    level_of_contact = None
    immuno_compromised = None
    vaccinated = None
    stateInfo = None


    def __init__(self, age, sex, loss_of_smell_and_taste, persistent_cough, severe_fatigue, skipped_meals, level_of_contact, immuno_compromised, vaccinated, StateMetrics):
        self.age = age
        self.sex = sex
        self.loss_of_smell_and_taste = loss_of_smell_and_taste
        self.persistent_cough = persistent_cough
        self.severe_fatigue = severe_fatigue
        self.ss = skipped_meals
        self.level_of_contact = level_of_contact
        self.immuno_compromised = immuno_compromised
        self.vaccinated = vaccinated
        self.stateInfo = StateMetrics

    def set_riskAssessment(self):
        self.risk_value, self.risk_string = self.risk_assessment()
        return

    def risk_from_predicted_cases(self):
        days_out = self.stateInfo.days_out
        pct_change = np.array(self.stateInfo.get_percent_change())
        forecast_pct_change = (np.array(self.stateInfo.predictions[days_out]) - np.array(self.stateInfo.predictions[0])) / np.array(self.stateInfo.predictions[0]) * 100.0
        avg_pct_change = (sum(pct_change / len(self.stateInfo.get_percent_change()))) * 100.0

        if ((avg_pct_change - forecast_pct_change) > 0):
            return 0 # less risk
        elif (avg_pct_change - forecast_pct_change < 0):
            return 1 # more risk

    def bool_to_num(self, bool_data):
        if type(bool_data) != bool:
            raise Exception("input should be a boolean")

        if (bool_data == True):
            return 1
        else:
            return 0

    def set_age(self, age):
        if type(age) != int:
            raise Exception("input should be an integer")
        self.age = age

    def set_sex(self, sex):
        if type(sex) != bool:
            raise Exception("input should be a boolean")
        self.sex = sex

    def set_loss_of_smell_and_taste(self, loss_of_smell_and_taste):
        if type(loss_of_smell_and_taste) != bool:
            raise Exception("input should be a boolean")
        self.loss_of_smell_and_taste = loss_of_smell_and_taste

    def set_presistent_cough(self, persistent_cough):
        if type(persistent_cough) != bool:
            raise Exception("input should be a boolean")
        self.persistent_cough = persistent_cough

    def set_skipped_meals(self, skipped_meals):
        if type(skipped_meals) != bool:
            raise Exception("input should be a boolean")
        self.skipped_meals = skipped_meals

    def set_severe_fatigue(self, severe_fatigue):
        if type(severe_fatigue) != bool:
            raise Exception("input should be a boolean")
        self.severe_fatigue = severe_fatigue

    def set_immuno_compromised(self, immuno_compromised):
        if type(immuno_compromised) != bool:
            raise Exception("input should be a boolean")
        self.immuno_compromised = immuno_compromised

    def set_level_of_contact(self, level_of_contact):
        #0=non-active 1=semi-active 2=very-active
        if type(level_of_contact) != int:
            raise Exception("input should be an integer")
        self.level_of_contact = level_of_contact

    def set_vaccinated(self, vaccinated):
        if type(vaccinated) != bool:
            raise Exception("input should be a boolean")
        self.vaccinated = vaccinated

    def sigmoid(self, x):
        return (np.exp(x) / (1 + np.exp(x)))

    def risk_assessment(self):
        age_over_55 = 1 if (self.age >= 55) else 0

        sex = self.bool_to_num(self.sex) #1=male 0=female
        loss_of_smell_and_taste = self.bool_to_num(self.loss_of_smell_and_taste)
        persistent_cough = self.bool_to_num(self.persistent_cough)
        severe_fatigue = self.bool_to_num(self.severe_fatigue)
        skipped_meals = self.bool_to_num(self.skipped_meals)
        immuno_compromised = self.bool_to_num(self.immuno_compromised)
        vaccinated = self.bool_to_num(self.vaccinated)

        predicted_risk = (-1.32 - (-0.25 * age_over_55) + (0.44 * sex) + (1.75 * loss_of_smell_and_taste)
        + (0.31 * persistent_cough) + (0.49 * severe_fatigue) + (0.39 * skipped_meals)
        + (0.5 * self.risk_from_predicted_cases()) + (self.level_of_contact) + (1.25 * immuno_compromised)
        + (-0.25 * vaccinated))
        risk_value = self.sigmoid(predicted_risk)
        risk_string = ''

        if risk_value > 0.0 and risk_value <= .20:
            risk_string = 'Low - Travel is reccommended'
        if risk_value > 0.20 and risk_value <= .40:
            risk_string = 'Low - Travel with low exposure'
        if risk_value > 0.40 and risk_value <= .60:
            risk_string = 'Medium - Travel with caution'
        if risk_value > 0.60 and risk_value <= .80:
            risk_string = 'Medium - Travel with high caution'
        if risk_value > 0.80 and risk_value <= 1.0:
            risk_string = 'High - Travel not reccommended'

        return risk_value, risk_string
