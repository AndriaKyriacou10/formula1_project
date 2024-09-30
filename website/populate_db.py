from . import create_app
from .acquire_data import fetch_data_api
from flask import current_app
import datetime
import requests


def update_database(app):
    
    with app.app_context():
        print('Starting update_database...')
        logs = open('database_logs.txt', 'a')
        logs.write('--------------------------------------------------------\n')
        logs.write(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
        
        url = 'https://ergast.com/mrd/'
        try:
            response = requests.get(url, timeout=90)
            if response.status_code == 503:
                logs.write('Ergast API is offline - Error 503 Backend fetch failed\n')
                return
        except requests.Timeout:
            logs.write('Request has timed out\n')
            return
        
        data = fetch_data_api(app, logs)
        with app.app_context():
            data.fetch_drivers()  
            data.fetch_constructors()
            data.fetch_circuits()
            data.fetch_races()
            data.fetch_results_driverCon()
            data.fetch_driver_standings()
            data.fetch_constructor_standings()
        
        logs.close()

# update_database()