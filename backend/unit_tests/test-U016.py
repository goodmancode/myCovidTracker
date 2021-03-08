import unittest
from StateMetrics import StateMetrics
import numpy as np

class StateMetricsTest(unittest.TestCase):

    def test_get_percent_change(self):
        s = StateMetrics([110, 100, 90], 100, 0.99, 0.5)
        self.assertEqual(s.get_percent_change(), 0.5, 'Should be 0.5')

    def test_get_model_accuracy(self):
        s = StateMetrics([110, 100, 90], 100, 0.99, 0.5)
        self.assertEqual(s.get_model_accuracy(), 0.99, 'Should be 0.99')

    def test_get_avg_cases_per_day(self):
        s = StateMetrics([110, 100, 90], 100, 0.99, 0.5)
        self.assertEqual(s.get_avg_cases_per_day(), 100, 'Should be 100')

    def test_get_predictions(self):
        s = StateMetrics(np.array([110, 100, 90]), 100, 0.99, 0.5)
        array_test = np.array([110, 100, 90])
        self.assertTrue(np.array_equal(s.predictions, array_test), 'Should be True')

    def test_predict_days_out(self):
        s = StateMetrics([110, 100, 90], 100, 0.99, 0.5)
        self.assertEqual(s.predictions[1], 100, 'Should be 100')

if __name__ == '__main__':
    unittest.main()
