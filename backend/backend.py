from os import path
import schedule, time, requests
from urllib.error import HTTPError

from model import regression

import numpy as np
import pandas as pd


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
    limit = '?$limit=30000'

    response = make_request(url)
    success = 200

    while (response == None or response.status_code != success):
        response = make_request(url)
        print('Trying again...')

    df = pd.read_csv(url + limit)
    dir_path = path.dirname(path.realpath(__file__)) + '/dataset.csv'
    df.to_csv(dir_path)

    return

def refresh_data():

    # Data is updated daily
    schedule.every().day.at('19:30').do(api_call)
    schedule.every(1).seconds.do(api_call)

    # Only make the api call if the dataset doesn't exist in the current
    # directory
    while not path.exists('dataset.csv'):
        schedule.run_pending()
        time.sleep(1)

    return

def main():

    refresh_data()

    df = pd.read_csv('dataset.csv')

    print(df.head())

    return

if __name__ == '__main__':
    main()
