import unittest
import pandas as pd

class TestDataFrame(unittest.TestCase):
    df = pd.read_csv('https://data.cdc.gov/resource/9mfq-cb36.csv?$limit=50000')

    def test_date_and_state(self):
        contains_date_and_state = ('submission_date' in self.__class__.df.columns and
        'state' in self.__class__.df.columns)

        self.assertTrue(contains_date_and_state, 'Should be True')

    def test_pct_change(self):
        contains_positive_cases = 'tot_cases' in self.__class__.df.columns

        self.assertTrue(contains_positive_cases, 'Should be True')

if __name__ == '__main__':
    unittest.main()
