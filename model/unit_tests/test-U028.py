import unittest
from request import make_request

class TestAPI(unittest.TestCase):
    def test_response(self):
        url = 'https://api.covidtracking.com/v1/states/daily.csv'
        self.assertEqual(make_request(url), 200, 'Should be 200')

if __name__ == '__main__':
    unittest.main()
