import unittest
from StateMetrics import StateMetrics
from RiskAssessment import RiskAssessment

class RiskAssessmentTest(unittest.TestCase):

    def test_set_age(self):
        test = RiskAssessment(20, True, True, True, 25)
        self.assertEqual(test.age, 20, 'Should be 20')
        test.set_age(50)
        self.assertEqual(test.age, 50, 'Should be 50')
        with self.assertRaises(Exception):
            test.set_age('thirty')

    def test_set_immuno_compromised(self):
        test = RiskAssessment(20, True, True, True, 25)
        self.assertEqual(test.immuno_compromised, True, 'Should be True')
        test.set_immuno_compromised(False)
        self.assertEqual(test.immuno_compromised, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_immuno_compromised(55)

    def test_calculate_risk(self):
        s = StateMetrics([100, 120], 1, 150, 0.99, [0.25], 150)
        calcRisk = RiskAssessment(20, True, True, True, 1)
        self.assertEqual(calcRisk.calculate_risk(s), 1, "Should be 1")
    
    def test_set_environment(self):
        test = RiskAssessment(20, True, True, True, 25)
        self.assertEqual(test.environment, True, 'Should be True')
        test.set_environment(False)
        self.assertEqual(test.environment, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_environment(55)

    def test_set_vaccinated(self):
        test = RiskAssessment(20, True, True, True, 25)
        self.assertEqual(test.vaccinated, True, 'Should be True')
        test.set_vaccinated(False)
        self.assertEqual(test.vaccinated, False, 'Should be False')
        with self.assertRaises(Exception):
            test.set_vaccinated(55)

if __name__ == '__main__':
    unittest.main()
