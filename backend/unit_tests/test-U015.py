import unittest
from State import State
from StateMetrics import StateMetrics

class StateTest(unittest.TestCase):
    def test_get_name(self):
        obj = StateMetrics([100, 110, 120], 50, 0.99, 0.01)
        s = State('Bob Ross', obj)
        self.assertEqual(s.get_name(), 'Bob Ross', "Should be 'Bob Ross'")

    def test_get_metrics(self):
        obj = StateMetrics([100, 110, 120], 50, 0.99, 0.01)
        s = State('Bob Ross', obj)
        self.assertEqual(s.get_metrics, obj, "Should store object of StateMetrics")


if __name__ == '__main__':
    unittest.main()
    
