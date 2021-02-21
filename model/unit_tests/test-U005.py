import os.path
from os import path
import unittest
import pandas as pd

class TestRefresher(unittest.TestCase):

    # Test to make sure the file is created
    def test_refresher(self):
        path_to_data = './dataset.csv'
        refresh_data()
        self.assertTrue(path.exists(path_to_data), 'Should be True')

    # Test to make sure the data has data up to the previous day
    def test_file_time(self):
        path_to_data = './dataset.csv'
        refresh_data()
        df = pd.read_csv(path_to_data)
        # Set this value to yesterday's date
        # date column in dataset is an int value
        current_date = 20210220
        self.assertEqual(max(df['date']), current_date, 'Should be 20210220')

if __name__ == '__main__':
    unittest.main()
