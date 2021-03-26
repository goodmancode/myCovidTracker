import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime, json, math, os, pickle, requests, time, sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mycovidtracker.get_retrain_days import get_retrain_time, post_new_retrain_time
from mycovidtracker.StateMetrics import StateMetrics
from mycovidtracker.State import State

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso, LinearRegression, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from matplotlib import style

# List of states
states = ['Alaska','Alabama','Arkansas', 'Arizona','California','Colorado',
  'Connecticut','Delaware','Florida','Georgia','Hawaii','Iowa','Idaho',
  'Illinois','Indiana','Kansas','Kentucky','Louisiana','Massachusetts','Maryland',
  'Maine','Michigan','Minnesota','Missouri','Mississippi','Montana',
  'North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
  'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania',
  'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
  'Virginia','Vermont','Washington','Wisconsin','West Virginia', 'Wyoming']

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
    data.replace([np.inf, -np.inf], 1.0, inplace = True)

    return data

# Data passes any day with no cases recorded as NaN values
# Those specific dates are filled with zeroes
def set_initial_zeroes(data, col_missing_vals, indices):
    data.replace([np.nan], 0, limit = find_first_non_nan(data, col_missing_vals), inplace = True)
    return data

def regression(days_since_last_retrain):
    # seconds per day
    one_day = 86400

    pred_column = 'tot_cases' # target

    # How many days in the future to predict out
    pred_out = 30

    time_to_retrain = (days_since_last_retrain == 14)

    # Path to pickle_files
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/pickle_files/'

    # Dataset should be stored locally only if the request was successful
    dataset_path = os.path.dirname(os.path.realpath(__file__)) + '/dataset.csv'
    df = pd.read_csv(dataset_path)

    # Getting rid of anything that's not any of the 50 states
    df = df[(df.state != 'DC') & (df.state != 'FSM') & (df.state != 'GU') &
            (df.state != 'MP') & (df.state != 'NYC') & (df.state != 'PR') &
            (df.state != 'AS') & (df.state != 'PW') & (df.state != 'RMI') & (df.state != 'VI')]

    # Creating dictionary with state name : state_acronym
    # key value pairs
    state_dict = create_state_dict(states, df['state'].sort_values().unique())

    # Store all 50 states worth of information
    state_objects = []

    forecast_dates = []

    # Only saving relevant features
    df = df[['submission_date', 'state', 'tot_death', 'new_death', 'tot_cases', 'new_case']]

    # Changing index to dates as datetime objects
    df['submission_date'] = pd.to_datetime(df.submission_date, format = '%Y-%m-%d')
    df.set_index('submission_date', drop = True, inplace = True)
    df.sort_index(inplace = True)

    for i, state in enumerate(states):
        # Getting the specified state
        chosen_state = state_dict[state]

        # Creating a new dataframe to only hold data
        # from the current state to avoid slicing issues
        df_filtered = pd.DataFrame(df.loc[:,][df.state == chosen_state])
        df_filtered.drop(['state'], 1, inplace = True)

        # Adding new features to assist with prediction
        df_filtered['prev_day'] = df_filtered['tot_cases'] - df_filtered['new_case']
        df_filtered['PCT_change'] = (df_filtered['new_case'] / df_filtered['prev_day']) * 100.0
        df_filtered['AVG_cases'] = df_filtered['tot_cases'] // len(df_filtered)

        # Missing values are located, and replaced as most nan values are dates
        # with no cases reported
        col_missing_vals = check_missing_values(df_filtered)
        indices = find_first_non_nan(df_filtered, col_missing_vals)
        df_filtered = set_initial_zeroes(df_filtered, col_missing_vals, indices)

        # Creating the label column with pred_out rows to hold truth values
        df_filtered['label'] = df_filtered[pred_column]

        df_filtered = handle_inf_values(df_filtered) # Final cleanup

        X = np.array(df_filtered.drop('label', 1).values)

        # Using last 30 values to predict 30 days into the future
        X_new = X[-pred_out:]

        # Creating label data
        df_filtered.dropna(inplace = True)
        y = np.array(df_filtered['label'].values)

        # Only using data up to last 30 entries for training and validation
        X_split = X[:-1 * pred_out]
        y_split = y[pred_out // 2: -pred_out // 2]

        # Creating a pipeline for the model
        pipe = make_pipeline(Ridge())

        X_train, X_val, y_train, y_val = train_test_split(X_split, y_split, test_size = 0.2)

        # Location of state pickle file
        pickle_file = dir_path + state + '_model.pickle'

        # Will retrain model after 14 days have passed or the pickle file doesn't exist
        if time_to_retrain or not os.path.exists(pickle_file):
            # Using GridSearchCV to search for the best alpha and normalization office
            # to implement into the model
            print('Retraining ' + state + ' model...')
            alphas = np.logspace(-4, 0, 50)

            # Using grid search to find the best params
            param_grid = {'ridge__alpha': alphas, 'ridge__normalize': [True]}
            ridge_cv = GridSearchCV(pipe, param_grid = param_grid, cv = 10)
            ridge_cv.fit(X_train, y_train)
            pipe = ridge_cv.best_estimator_

            # Storing model so it can be reused in the future
            pickle_model(state, pipe)
        else:
            print('Loading model from ' + pickle_file + '...')
            pickle_in = open(pickle_file, 'rb')
            pipe = pickle.load(pickle_in)

        # Getting the score and forecast set
        score = pipe.score(X_val, y_val)

        # Making a prediction 30 days into the future
        forecast_set = pipe.predict(X_new)

        df_filtered['Forecast'] = np.nan # Forecast Column

        # Prepping fields for StateMetrics
        avg_cases_per_day = df_filtered['tot_cases'].mean()
        daily_pct_change = np.array(df_filtered['PCT_change'].values)

        # Getting next 30 days
        last_date = df_filtered.iloc[-1].name
        last_unix = last_date.timestamp()
        next_unix = last_unix + (2 * one_day)

        # List of dates for specified state
        dates = []

        # Setting up dates for the forecast
        for j in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            dates.append(next_date)
            next_unix += one_day
            df_filtered.loc[next_date] = [np.nan for _ in range(len(df_filtered.columns) - 1)] + [j]

        # Create new instantiation of StateMetrics class
        metrics = StateMetrics(forecast_set, avg_cases_per_day, score, daily_pct_change, None)

        # Create new instantiation of State class
        state_objects.append(State(state, metrics))

        forecast_dates.append(dates)

        # Packaging everything into State objects
        print(state + ' predictions complete...')
        print()


    return state_objects, forecast_dates
