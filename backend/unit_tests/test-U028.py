import unittest
from backend import make_request

class TestAPI(unittest.TestCase):
    def test_response(self):
        url = 'https://data.cdc.gov/resource/9mfq-cb36.csv'
        self.assertEqual(make_request(url).status_code, 200, 'Should be 200')

if __name__ == '__main__':
    unittest.main()
