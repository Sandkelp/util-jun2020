import pandas as pd
import pandas_gbq
import os


from google.oauth2 import service_account

import random 

from time import sleep

from datetime import datetime

def get_data():

    MIN = 100000
    MAX = 1000000
    BATCH_SLEEP = 10
    BATCH_SIZE = 10000

    path_to_credentials = os.environ.get('CRED_JSON_PATH', 'Quickstart-c97bee3c4606.json')
    print("Using credentials from ", path_to_credentials) 

    # Gets the info from google
    pandas_gbq.context.credentials = service_account.Credentials.from_service_account_file( path_to_credentials ) #gets the credentials
    
    pandas_gbq.context.project = os.environ.get('PROJECT_NAME', "quickstart-1584643705530")
    print("Project:", pandas_gbq.context.project)

    try: 

        from collections import abc as collections_abc

    except ImportError: 

        import collections as collections_abc

    

    number_of_responses = random.randrange(MIN, MAX) # sets a random value of vlues to retrieve
    print("number_of_responses:", number_of_responses)

    current_hour = int(datetime.now().hour) - 4

    if current_hour < 0:

        current_hour = 23


    date = datetime.now().strftime("%Y-%m-%d")
    query = 'SELECT * FROM `bigquery-public-data.wikipedia.pageviews_2020`  WHERE DATE(datehour) = "{}" AND TIME(datehour) = "{}:00:00" LIMIT {}'.format(date,current_hour,number_of_responses)
    print("query:", query)

    wiki = pandas_gbq.read_gbq(query)
    
    df = wiki.drop(["datehour"], axis=1)
    print("len(df):", len(df))
    
    start_of_batch=0
    end_of_batch = 0
    
    #response returner
    while end_of_batch < number_of_responses:
 
        end_of_batch = BATCH_SIZE + start_of_batch
        
        print(df[start_of_batch:end_of_batch])

        start_of_batch = start_of_batch + BATCH_SIZE

        BATCH_SIZE = random.randrange(0,10000)

        sleep(BATCH_SLEEP)
    
    
while True:

    get_data()
    start_time = 60 - int(datetime.now().minute)
    sleep(start_time * 60)