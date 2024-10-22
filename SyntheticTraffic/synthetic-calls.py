import os
import requests
import random
import csv
import json
import time
from dotenv import load_dotenv

load_dotenv()

service_url = os.getenv("API_ENDPOINT")
api_consumers_file = os.getenv("API_CONSUMERS_FILE")
api_call_data_file = os.getenv("API_CALL_DATA_FILE")
number_of_requests = int(os.getenv("NUMBER_OF_REQUESTS"))
time_between_requests = int(os.getenv("WAIT_TIME"))

consumers_local_path = os.getcwd() + api_consumers_file
api_calls_local_path = os.getcwd() + api_call_data_file

with open(consumers_local_path, newline='\n', encoding='utf-8') as consumersfile:
    consumers_data = list(csv.reader(consumersfile))

with open(api_calls_local_path, newline='\n', encoding='utf-8') as questionsfile:
    questions_data = list(csv.reader(questionsfile))

def Create_Payload() -> str:
    consumer = random.choice(consumers_data)[0]
    question = random.choice(questions_data)[0]

    # payload required by Langflow API
    tweaks = dict()
    tweak_textinput = {"user_value" : consumer}
    tweaks['TextInput-ocdhC'] = tweak_textinput

    payload = dict()
    payload['input_value'] = question
    payload['output_type'] = "chat"
    payload['input_type'] = "chat"
    payload['tweaks'] = tweaks
    
    output = json.dumps(payload, ensure_ascii=False)
    return output


for x in range(number_of_requests):
    req_payload = Create_Payload()
    print("\nStarting new request...")
    print(req_payload)
    
    r = requests.post(service_url, data=req_payload)
    print(str(r.status_code))
    
    time.sleep(time_between_requests)
