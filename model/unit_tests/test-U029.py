import os, unittest
from State import State
from model import regression

states = ['Alaska','Alabama','Arkansas', 'Arizona','California','Colorado',
  'Connecticut','Delaware','Florida','Georgia','Hawaii','Iowa','Idaho',
  'Illinois','Indiana','Kansas','Kentucky','Louisiana','Massachusetts','Maryland',
  'Maine','Michigan','Minnesota','Missouri','Mississippi','Montana',
  'North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
  'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania',
  'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
  'Virginia','Vermont','Washington','Wisconsin','West Virginia']

class TestModel(unittest.TestCase):
    state_data = regression()

    def test_accuracy(self):
        avg_accuracy = sum([state.metrics.model_accuracy for state in self.__class__.state_data]) / 50
        self.assertTrue(avg_accuracy >= 0.95, 'Should be True')

    def test_forecast_length(self):
        forecasts_thirty_days = True

        for state in self.__class__.state_data:
            forecasts_thirty_days = forecasts_thirty_days and len(state.metrics.predictions) == 30

        self.assertTrue(forecasts_thirty_days, 'Should be True')

    def test_each_state_has_own_object(self):
        all_states_have_data = True

        for i, state in enumerate(states):
            all_states_have_data = all_states_have_data and self.__class__.state_data[i].name == state

        self.assertTrue(all_states_have_data, 'Should be True')

    def test_each_state_has_pickle(self):
        all_states_have_pickle = True
        dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))

        for state in states:
            pickle_path = dir_path + '/pickle_files/' + state + '_model.pickle'
            all_states_have_pickle = all_states_have_pickle and os.path.exists(pickle_path)

        self.assertTrue(all_states_have_pickle)

    def test_existence_of_json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_to_json = dir_path + '/forecast_data.json'
        self.assertTrue(os.path.exists(path_to_json), 'Should be True')




if __name__ == '__main__':
    unittest.main()
