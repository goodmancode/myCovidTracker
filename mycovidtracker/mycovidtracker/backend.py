import json, os, requests, time, firebase_admin, sys, firebase_admin
from urllib.error import HTTPError
from datetime import datetime, timedelta
from firebase_admin import credentials, initialize_app, storage, firestore

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mycovidtracker.get_retrain_days import get_retrain_time, post_new_retrain_time
from mycovidtracker.model import regression
from mycovidtracker.State import State
from mycovidtracker.StateMetrics import StateMetrics
from mycovidtracker.RiskAssessment import RiskAssessment

import numpy as np
import pandas as pd

def send_state_info_to_database(state_data):
    # Getting credentials to access database
    cred = credentials.Certificate('/root/mycovidtracker/mycovidtracker/service.json')

    # Ensures that firebase has not already been started
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    for state in state_data:
        doc_ref = db.collection(u'states').document(state.name)
        doc_ref.set({
            u'predictions': state.metrics.predictions.tolist(),
            u'avg_cases_per_day': state.metrics.avg_cases_per_day,
            u'model_accuracy': state.metrics.model_accuracy,
            u'percent_change': state.metrics.percent_change.tolist(),
            u'predicted_percent_change': state.metrics.calculate_prediction_percent_change()
        }, merge = True)

def send_risk_to_database(uid):
    # Getting credentials to access database
    cred = credentials.Certificate('/root/mycovidtracker/mycovidtracker/service.json')

    # Ensures that firebase has not already been started
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # Getting access to the database
    db = firestore.client()

    # Getting the users information
    user_inputs = db.collection(u'users').document(uid)

    # Putting database fields into python readable format
    fields = user_inputs.get().to_dict()

    state = str(fields['state'])

    # Setting fields for risk assessment
    days_out = fields['days_out']
    age = fields['age']
    sex = fields['sex']
    loss_of_smell_and_taste = fields['loss_of_smell_and_taste']
    persistent_cough = fields['persistent_cough']
    severe_fatigue = fields['severe_fatigue']
    skipped_meals = fields['skipped_meals']
    level_of_contact = fields['level_of_contact']
    immuno_compromised = fields['immuno_compromised']
    vaccinated = fields['vaccinated']
    state_info = db.collection(u'states').document(state)

    state_metrics = state_info.get().to_dict()

    metrics = StateMetrics(state_metrics['predictions'], state_metrics['avg_cases_per_day'], state_metrics['model_accuracy'], state_metrics['percent_change'], days_out)

    risk = RiskAssessment(age, sex, loss_of_smell_and_taste, persistent_cough, severe_fatigue, skipped_meals, level_of_contact, immuno_compromised, vaccinated, metrics)
    risk_value, risk_string = risk.risk_assessment()

    user_inputs.set({
        u'age': age,
        u'sex': sex,
        u'loss_of_smell_and_taste': loss_of_smell_and_taste,
        u'persistent_cough': persistent_cough,
        u'severe_fatigue': severe_fatigue,
        u'skipped_meals': skipped_meals,
        u'level_of_contact': level_of_contact,
        u'immuno_compromised': immuno_compromised,
        u'vaccinated': vaccinated,
        u'risk_string': risk_string,
        u'risk_value': risk_value
    }, merge = True)

    return

def send_json_to_database(filename):
    cred = credentials.Certificate('/root/mycovidtracker/mycovidtracker/service.json')
    initialized = firebase_admin._apps

    if not initialized:
        initialize_app(cred, {'storageBucket': 'mycovidtracker-5e186.appspot.com'})

    bucket = storage.bucket('mycovidtracker-5e186.appspot.com') if initialized else storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    blob.make_public()

    return

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

    send_json_to_database('forecast_data.json')

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

    send_state_info_to_database(state_data)

    # At this point a day will have passed
    days_since_last_retrain += 1

    if (days_since_last_retrain >= 15):
        days_since_last_retrain = 1

    post_new_retrain_time(days_since_last_retrain)

    # JSON is created for front end use
    create_json(state_data, forecast_dates)

    return


if __name__ == '__main__':
    api_call()
    refresh_data()
