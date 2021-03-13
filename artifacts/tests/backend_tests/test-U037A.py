import json, random, time, unittest

from datetime import datetime, timedelta

from backend import create_json
from model import regression
from State import State
from StateMetrics import StateMetrics

# This will test the reading of pickle files when not enough days have passed
# for retrain
class TestPickleReadingAndForecast(unittest.TestCase):
    # Simulating backend
    days = random.randint(1, 13)

    start_time = time.time()
    state_data, forecast_dates = regression(days)
    end_time = time.time() - start_time

    create_json(state_data, forecast_dates)

    f = open('forecast_data.json')
    data = json.load(f)
    f.close()

    def test_forecast(self):
        # 29 days from the last submission date which is a day less
        # then the current date
        thirty_days_out = datetime.today() + timedelta(29)
        thirty_days_out_str = datetime.strftime(thirty_days_out, '%Y-%m-%d')
        all_dates_thirty_out = True

        for i, state in enumerate(self.__class__.state_data):
            date = self.__class__.data[i]['data'][29]['date'].split(' ')[0]
            all_dates_thirty_out = all_dates_thirty_out and (date == thirty_days_out_str)

        self.assertTrue(all_dates_thirty_out, 'Should be True')

    def test_pickle_loading(self):
        self.assertTrue(self.__class__.end_time < 60.0, 'Should be True')


if __name__ == '__main__':
    unittest.main()
