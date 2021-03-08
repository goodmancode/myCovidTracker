import pandas as pd
import numpy as np
import datetime, json, math, os, pickle, requests

from StateMetrics import StateMetrics
from State import State

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib import style

# List of states
states = ['Alaska','Alabama','Arkansas', 'Arizona','California','Colorado',
  'Connecticut','Delaware','Florida','Georgia','Hawaii','Iowa','Idaho',
  'Illinois','Indiana','Kansas','Kentucky','Louisiana','Massachusetts','Maryland',
  'Maine','Michigan','Minnesota','Missouri','Mississippi','Montana',
  'North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
  'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania',
  'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
  'Virginia','Vermont','Washington','Wisconsin','West Virginia']

def pickle_model(state_name, model):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/pickle_files/' + state_name + '_model.pickle'

    with open(file_path, 'wb') as f:
        pickle.dump(model, f) # dumps the regressor
        f.close()

    return

def create_state_dict(states, state_acronyms):
    state_dict = {}

    for state, state_acronym in zip(states, state_acronyms):
        state_dict[state] = state_acronym

    return state_dict

# Create json file for front end to use
def create_json(state_data, dates):
    data = {}

    for i, state in enumerate(state_data):
        data[state.name] = []

        for j in range(len(dates[i])):
            forecast = {'date': str(dates[i][j]), 'value': state.metrics.predictions[j]}
            data[state.name].append(forecast)

    # Dumping data onto new json file
    with open('forecast_data.json', 'w') as f:
        json.dump(data, f, indent = 2, sort_keys = True)
        f.close()

    return

def convert_dates_to_datetime(data):
    for id, date in zip(data.index, data['submission_date']):
        date = date.split('T')[0]
        data.at[id, 'submission_date'] = datetime.datetime.strptime(date, '%Y-%m-%d')

    return data

# If missing values are detected in a column, that column's
# value will be the value to replace missing values with
def check_missing_values(data):
    col_missing_vals = []

    for column in data.columns:
        num_missing_values = sum(pd.isnull(data[column]))

        if (num_missing_values > 0):
            col_missing_vals.append(column)

    return col_missing_vals

def find_first_non_nan(data, col_missing_values):
    indices = {}
    for col in col_missing_values:
        i = 0

        for val in data[col]:
            if not np.isnan(val):
                break
            else:
                i += 1
        indices[col] = i

    return indices

def handle_inf_values(data):
    for column in data.columns:
        data.loc[data[column] == np.inf] = 0

    return data

# Data passes any day with no cases recorded as NaN values
# Those specific dates are filled with zeroes
def set_initial_zeroes(data, col_missing_vals, indices):
    for col in col_missing_vals:
        last_non_nan = indices[col]
        data.fillna(value = 0, limit = last_non_nan, inplace = True)

    return data

def regression():

    api_endpoint = 'https://data.cdc.gov/resource/9mfq-cb36.csv'
    limit = '?$limit=50000'

    response = requests.get(api_endpoint)

########################################################

    # seconds per day
    one_day = 86400

    # Dataset should be stored locally only if the request was successful
    if response.status_code == requests.codes.ok:
        df = pd.read_csv(api_endpoint + limit)
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/dataset.csv'
        df.to_csv(dir_path)

    # Getting rid of anything that's not any of the 50 states
    df = df[(df.state != 'DC') & (df.state != 'FSM') & (df.state != 'GU') &
            (df.state != 'MP') & (df.state != 'NYC') & (df.state != 'PR') &
            (df.state != 'AS') & (df.state != 'PW') & (df.state != 'RMI') & (df.state != 'VI')]

    # Creating dictionary with state name : state_acronym
    # key value pairs
    state_dict = create_state_dict(states, df['state'].sort_values().unique())

    # Store all 50 states worth of metrics
    all_metrics = []

    # 30 days out
    forecast_dates = []

    # Only saving relevant featutes
    df = df[['submission_date', 'state', 'tot_death', 'new_death', 'tot_cases', 'new_case']]

    # Adding new features to assist with prediction
    df['prev_day'] = df['tot_cases'] - df['new_case']
    df['PCT_change'] = (df['new_case'] / df['prev_day']) * 100.0

    for i, state in enumerate(states):
        # Getting the specified state
        chosen_state = state_dict[state]

        # Creating a new dataframe to only hold data
        # from a specific state to avoid slicing issues
        df_filtered = pd.DataFrame(df.loc[:,][df.state == chosen_state])
        df_filtered.drop(['state'], 1, inplace = True)

        # Using the date as the index as a way to organize the data
        df_filtered = convert_dates_to_datetime(df_filtered)
        df_filtered.set_index('submission_date', drop = True, inplace = True)
        df_filtered.sort_index(inplace = True)

        # Missing values are located, and replaced as most nan values are dates
        # with no cases reported
        col_missing_vals = check_missing_values(df_filtered)
        indices = find_first_non_nan(df_filtered, col_missing_vals)
        df_filtered = set_initial_zeroes(df_filtered, col_missing_vals, indices)

        # How many days in the future to predict out
        pred_out = 30

        # Creating the label column with pred_out rows to hold truth values
        pred_column = 'tot_cases' # target
        df_filtered['label'] = df_filtered[pred_column].shift(-pred_out)

        df_filtered = handle_inf_values(df_filtered) # Final cleanup

        X = np.array(df_filtered.drop('label', 1).values)

        # Adjusting data to only include historical data
        X = X[:-pred_out]

        # Standardizing the data to get all data on the same scale
        X = StandardScaler().fit_transform(X)

        # Creating unseen values
        X_new = X[-pred_out:]

        df_filtered.dropna(inplace = True)
        y = np.array(df_filtered['label'].values)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

        # Using GridSearchCV to search for the best alpha to implement into the model
        ridge = Ridge()
        alphas = np.logspace(-4, 0, 50)
        param_grid = {'alpha': alphas, 'normalize': [True, False]}
        ridge_cv = GridSearchCV(ridge, param_grid, cv = 10)
        ridge_cv.fit(X_train, y_train)
        best_ridge = ridge_cv.best_estimator_

        # Model training and prediction
        best_ridge.fit(X_train, y_train)

        # Storing model so it can be reused in the future
        pickle_model(state, best_ridge)

        # Getting the score and forecast set
        score = best_ridge.score(X_test, y_test)
        forecast_set = best_ridge.predict(X_new)

        # Getting the dates to predict and setting up the forecast column to receive
        # prediction values
        df_filtered['Forecast'] = np.nan
        last_date = df_filtered.iloc[-1].name
        last_unix = last_date.timestamp()
        next_unix = last_unix + one_day

        # List of dates for specified state
        dates = []

        # Setting up data for the forecast
        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            dates.append(next_date)
            next_unix += one_day
            df_filtered.loc[next_date] = [np.nan for _ in range(len(df_filtered.columns) - 1)] + [i]

        # Prepping fields for StateMetrics
        avg_cases_per_day = df_filtered['tot_cases'].mean()
        daily_pct_change = np.array(df_filtered['PCT_change'].values)

        # Create new instantiation of StateMetrics class
        all_metrics.append(StateMetrics(forecast_set, avg_cases_per_day, score, daily_pct_change))
        forecast_dates.append(dates)


    state_objects = []

    for i, state in enumerate(states):
        state_objects.append(State(state, all_metrics[i]))

    create_json(state_objects, forecast_dates)

    return state_objects

if __name__ == '__main__':
    regression()
