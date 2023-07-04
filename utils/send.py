import ee
from google.oauth2 import service_account
import os
import subprocess
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
creds_filename = config["default"]["creds_filename"]
prefix = config["default"]["project_prefix"]
ee_project = config["default"]["ee_project"]


SCOPES = ['https://www.googleapis.com/auth/devstorage.full_control',
          'https://www.googleapis.com/auth/earthengine']

credentials = service_account.Credentials.from_service_account_file(creds_filename, scopes=SCOPES)

ee.Initialize(credentials=credentials, project=ee_project)


def sendToEarthEngine(source, target_name):
    print(f"Sending gs://{prefix}-data/{target_name}.csv to Earth Engine")
    
    subprocess.call(f'gcloud storage cp {source}.csv gs://{prefix}-data/{target_name}.csv', shell=True)

    taskId = subprocess.check_output(f'earthengine --service_account_file={creds_filename} upload table --force --asset_id=projects/{ee_project}/assets/{target_name} gs://{prefix}-data/{target_name}.csv', shell=True).decode('utf-8').strip()
    taskId = taskId.split(' ')[-1]

    while True:
        progress = subprocess.check_output(f'earthengine --service_account_file={creds_filename} task list', shell=True).decode('utf-8').strip()
        progress = [line for line in progress.split('\n') if line.startswith(taskId)][0]
        # find status from this pattern match RUNNING, READY, COMPLETED, FAILED or CANCELLED
        status = [word for word in progress.split(' ') if word in ['RUNNING', 'READY', 'COMPLETED', 'FAILED', 'CANCELLED']][0]
        print(status)
        time.sleep(5)
        
        if status == 'FAILED':
            break

        if status == 'COMPLETED':
            break

def sendToGoogleStorage(source, target_name):
    
    print(f"Uploading {source}.csv gs://{prefix}-data/{target_name}.csv")
    subprocess.call(f'gcloud storage cp {source}.csv gs://{prefix}-data/{target_name}.csv', shell=True)
