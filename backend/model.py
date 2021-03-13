import pandas as pd
import numpy as np
import datetime, json, math, os, pickle, requests, time

from get_retrain_days import get_retrain_time, post_new_retrain_time
from StateMetrics import StateMetrics
from State import State

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
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
    json_file = []

    for i, state in enumerate(state_data):
        state_info = {}
        data = []
        state_info['state'] = state.name

        for j in range(len(dates[i])):
            data.append({'date': str(dates[i][j]), 'value': state.metrics.predictions[j]})

        state_info['data'] = data
        json_file.append(state_info)

    # Dumping data onto new json file
    with open('forecast_data.json', 'w') as f:
        json.dump(json_file, f, indent = 4, sort_keys = False)
        f.close()

    return


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

def regression(days_since_last_retrain):
    response = requests.get(url)

    if (response.status_code == 200):
        df = pd.read_csv(url + limit)
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/dataset.csv'
        df.to_csv(dir_path)

    # seconds per day
    one_day = 86400

    time_to_retrain = (days_since_last_retrain == 14)

    # Dataset should be stored locally only if the request was successful
    df = pd.read_csv('dataset.csv')

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

    # Changing index to dates as datetime objects
    df['submission_date'] = pd.to_datetime(df.submission_date, format = '%Y-%m-%d')
    df.set_index('submission_date', inplace = True)
    df.sort_index(inplace = True)

    for i, state in enumerate(states):
        # Getting the specified state
        chosen_state = state_dict[state]

        # Creating a new dataframe to only hold data
        # from a specific state to avoid slicing issues
        df_filtered = pd.DataFrame(df.loc[:,][df.state == chosen_state])

        df_filtered.drop(['state'], 1, inplace = True)

        # Missing values are located, and replaced as most nan values are dates
        # with no cases reported
        col_missing_vals = check_missing_values(df_filtered)
        indices = find_first_non_nan(df_filtered, col_missing_vals)
        df_filtered = set_initial_zeroes(df_filtered, col_missing_vals, indices)

        # How many days in the future to predict out
        pred_out = 30

        # Creating the label column with pred_out rows to hold truth values
        pred_column = 'tot_cases' # target
        df_filtered['label'] = df_filtered[pred_column]

        df_filtered = handle_inf_values(df_filtered) # Final cleanup

        X = np.array(df_filtered.drop('label', 1).values)

        # Normalizing data as data is all on same scale
        X = StandardScaler().fit_transform(X)

        # Using last 30 values to predict 30 days into the future
        X_new = X[-pred_out:]

        df_filtered.dropna(inplace = True)
        y = np.array(df_filtered['label'].values)

        # Only using data up to last 60 entries for training and validation
        X_split = X[:-2 * pred_out]
        y_split = y[pred_out:-pred_out]

        X_train, X_val, y_train, y_val = train_test_split(X_split, y_split, test_size = 0.2)

        # Path to pickle_file
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/pickle_files/'
        pickle_file = dir_path + state + '_model.pickle'

        # Will retrain model after 14 days have passed or the pickle file doesn't exist
        if time_to_retrain or not os.path.exists(pickle_file):
            # Using GridSearchCV to search for the best alpha to implement into the model
            ridge = Ridge()
            alphas = np.logspace(-4, 0, 50)
            param_grid = {'alpha': alphas, 'normalize': [True, False]}
            ridge_cv = GridSearchCV(ridge, param_grid, cv = 10, scoring = 'neg_root_mean_squared_error')
            ridge_cv.fit(X_train, y_train)
            best_ridge = ridge_cv.best_estimator_

            # Model training
            best_ridge.fit(X_train, y_train)

            # Storing model so it can be reused in the future
            pickle_model(state, best_ridge)
        else:
            pickle_in = open(pickle_file, 'rb')
            best_ridge = pickle.load(pickle_in)

        # Getting the score and forecast set
        score = best_ridge.score(X_val, y_val)

        # Testing on last thirty days of data
        X_pred_prev = X[-2 * pred_out:-pred_out]

        y_pred_prev = best_ridge.predict(X_pred_prev)

        # Making a prediction 30 days into the future
        forecast_set = best_ridge.predict(X_new)

        df_filtered['Forecast'] = np.nan # Forecast Column

        # Getting next 30 days
        last_date = df_filtered.iloc[-1].name
        last_unix = last_date.timestamp()
        next_unix = last_unix + (2 * one_day)

        # Setting Forecast values for previous 30 days
        prev_thirty_days = len(y_pred_prev)
        for j, y_pred in enumerate(y_pred_prev):
            prev_unix = last_unix - (one_day * (prev_thirty_days - j))
            prev_date = datetime.datetime.fromtimestamp(prev_unix)
            df_filtered.at[prev_date, 'Forecast'] = y_pred

        # List of dates for specified state
        dates = []

        # Setting up data for the forecast
        for j in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            dates.append(next_date)
            next_unix += one_day
            df_filtered.loc[next_date] = [np.nan for _ in range(len(df_filtered.columns) - 1)] + [j]

        # Prepping fields for StateMetrics
        avg_cases_per_day = df_filtered['tot_cases'].mean()
        daily_pct_change = np.array(df_filtered['PCT_change'].values)

        # Create new instantiation of StateMetrics class
        all_metrics.append(StateMetrics(forecast_set, avg_cases_per_day, score, daily_pct_change))
        forecast_dates.append(dates)
        print(state + ' predictions complete...')


    state_objects = []

    for i, state in enumerate(states):
        state_objects.append(State(state, all_metrics[i]))


    return state_objects, forecast_dates
