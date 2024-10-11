import os
import requests
import random
import csv
from dotenv import load_dotenv

load_dotenv()

service_url = os.getenv("API_ENDPOINT")
api_consumers_file = os.getenv("API_CONSUMERS_FILE")
api_call_data_file = os.getenv("API_CALL_DATA_FILE")
number_of_requests = int(os.getenv("NUMBER_OF_REQUESTS"))

consumers_local_path = os.getcwd() + '\\data\\' + api_consumers_file
api_calls_local_path = os.getcwd() + '\\data\\' + api_call_data_file

with open(consumers_local_path, newline='\n') as consumersfile:
    consumers_data = list(csv.reader(consumersfile))

with open(api_calls_local_path, newline='\n') as questionsfile:
    questions_data = list(csv.reader(questionsfile))

for x in range(number_of_requests):
    consumer = random.choice(consumers_data)[0]
    question = random.choice(questions_data)[0]

    # payload required by Langflow API
    payload = {}
    payload['question'] = question

    #r = requests.post(service_url+'/post', json=data)
    # r = requests.post('https://httpbin.org/post', data=data, cookies={'foo': 'bar', 'hello': 'world'}))
    #print(r.json())
    #pass