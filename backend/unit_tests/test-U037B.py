import time, unittest

from model import regression
from State import State
from StateMetrics import StateMetrics

# This will test the creation of retraining of models when 14 days has passed
class TestModelRetraining(unittest.TestCase):

    def test_retrain(self):
        days = 14 # two weeks

        start_time = time.time()
        state_data, forecast_dates = regression(days)
        end_time = time.time() - start_time

        self.assertTrue(end_time >= 60.0, 'Should be True')



if __name__ == '__main__':
    unittest.main()
