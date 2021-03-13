import json, schedule, os, requests, time
from urllib.error import HTTPError

from datetime import datetime, timedelta

from get_retrain_days import get_retrain_time, post_new_retrain_time
from model import regression
from State import State
from StateMetrics import StateMetrics

import numpy as np
import pandas as pd


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

def make_request(url):
    try:
        response = requests.get(url)
    except HTTPError as err:
        if err.code == 404:
            print('Error: GET request unsuccessful')
            return None
        else:
            raise

    print('Status: ' + str(response.status_code))
    return response


def api_call():
    url = 'https://data.cdc.gov/resource/9mfq-cb36.csv'

    # api does not return full dataset. Limit has to be
    # specified to get all data
    limit = '?$limit=50000'

    response = make_request(url)
    success = requests.codes.ok

    while (response == None or response.status_code != success):
        response = make_request(url)
        print('Trying again...')

    df = pd.read_csv(url + limit)
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/dataset.csv'
    df.to_csv(dir_path)

    return


def refresh_data():

    days_since_last_retrain = get_retrain_time()

    # Model training and prediction
    state_data, forecast_dates = regression(days_since_last_retrain)

    # At this point a day will have passed
    days_since_last_retrain += 1

    if (days_since_last_retrain == 15):
        days_since_last_refresh = 1

    post_new_retrain_time(days_since_last_retrain)

    # JSON is created for front end use
    create_json(state_data, forecast_dates)

    return

if __name__ == '__main__':
    schedule.every().day.at(datetime.today()).do(refresh_data)

    schedule.every().day.at('19:30').do(api_call)
    schedule.every(1).seconds.do(api_call)

    while True:
        schedule.run_pending()
        time.sleep(1)
