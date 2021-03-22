import unittest
from StateMetrics import StateMetrics
from RiskAssessment import RiskAssessment

class RiskAssessmentTest(unittest.TestCase):

    def test_set_age(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.age, 20, 'Should be 20')
        test.set_age(50)
        self.assertEqual(test.age, 50, 'Should be 50')
        with self.assertRaises(Exception):
            test.set_age('thirty')

    def test_set_sex(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.sex, True, 'Should be True')
        test.set_sex(False)
        self.assertEqual(test.sex, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_sex(55)

    def test_set_loss_of_smell_and_taste(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.loss_of_smell_and_taste, True, 'Should be True')
        test.set_loss_of_smell_and_taste(False)
        self.assertEqual(test.loss_of_smell_and_taste, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_loss_of_smell_and_taste(55)
    
    def test_persistent_cough(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.persistent_cough, True, 'Should be True')
        test.set_presistent_cough(False)
        self.assertEqual(test.persistent_cough, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_presistent_cough(55)

    def test_set_skipped_meals(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.skipped_meals, True, 'Should be True')
        test.set_skipped_meals(False)
        self.assertEqual(test.skipped_meals, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_skipped_meals(55)

    def test_set_severe_fatigue(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.severe_fatigue, True, 'Should be True')
        test.set_severe_fatigue(False)
        self.assertEqual(test.severe_fatigue, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_severe_fatigue(55)

    def test_set_immuno_compromised(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.immuno_compromised, True, 'Should be True')
        test.set_immuno_compromised(False)
        self.assertEqual(test.immuno_compromised, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_immuno_compromised(55)
    
    def test_set_level_of_contact(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.level_of_contact, 2, 'Should be 2')
        test.set_level_of_contact(1)
        self.assertEqual(test.level_of_contact, 1, 'Should be 1')
        with self.assertRaises(Exception):
            test.set_level_of_contact(True)

    def test_set_vaccinated(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.vaccinated, True, 'Should be True')
        test.set_vaccinated(False)
        self.assertEqual(test.vaccinated, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_vaccinated(55)

    def test_risk_from_predicted_cases(self):
        calcRisk = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(calcRisk.risk_from_predicted_cases(), 1, "Should be 1")
        calcRisk.stateInfo.percent_change = [0.75]
        self.assertEqual(calcRisk.risk_from_predicted_cases(), 0, "Should be 0")

    def test_bool_to_num(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        self.assertEqual(test.bool_to_num(True), 1, 'Should be 1')
        self.assertEqual(test.bool_to_num(False), 0, 'Should be 0')
        with self.assertRaises(Exception):
            test.bool_to_num(55)

    def test_risk_assessment(self):
        test = RiskAssessment(20, True, True, True, True, True, 2, True, True, StateMetrics([100, 120], 1, 150, 0.99, [0.15], 150))
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )
       
        test.set_vaccinated(False)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )
        
        test.set_level_of_contact(1)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )

        test.set_level_of_contact(0)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )

        test.set_immuno_compromised(False)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )

        test.set_severe_fatigue(False)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value > 0.85, 'Should be greater than 0.5' )

        test.set_skipped_meals(False)
        test.set_riskAssessment()
        self.assertTrue((test.risk_value < 0.85) and (test.risk_value > 0.5), 'Should be greater than 0.5' )

        test.set_presistent_cough(False)
        test.set_riskAssessment()
        self.assertTrue((test.risk_value < 0.85) and (test.risk_value > 0.5), 'Should be greater than 0.5' )
       
        test.set_loss_of_smell_and_taste(False)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value < 0.5, 'Should be greater than 0.5' )

        test.set_sex(False)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value < 0.5, 'Should be greater than 0.5' )

        test.set_age(55)
        test.set_riskAssessment()
        self.assertTrue(test.risk_value < 0.5, 'Should be greater than 0.5' )
        '''
        self.assertEqual(test.bool_to_num(True), 1, 'Should be 1')
        self.assertEqual(test.bool_to_num(False), 0, 'Should be 0')
        '''
if __name__ == '__main__':
    unittest.main()
