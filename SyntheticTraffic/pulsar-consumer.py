import os
import pulsar
import pulsar.exceptions as pulsarExceptions
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

serviceUrl = os.getenv("PULSAR_SERVICE_URL")
pulsarToken = os.getenv("PULSAR_TOKEN")

tenantName = os.getenv("TENANT_NAME")
namespace = os.getenv("NAMESPACE")
topicName = os.getenv("TOPIC_NAME")

opensearchUrl = os.getenv("OPENSEARCH_ENDPOINT")

topic = "persistent://{0}/{1}/{2}".format(tenantName, namespace, topicName)

client = pulsar.Client(serviceUrl, authentication=pulsar.AuthenticationToken(pulsarToken))
# end::create-client[]

# tag::create-producer[]
producer = client.create_producer(topic)
# end::create-producer[]

# tag::create-consumer[]
consumer = client.subscribe(topic, 'test-subscription')
# end::create-consumer[]

# tag::consume-message[]
waitingForMsg = True
while waitingForMsg:
    try:
        msg = consumer.receive(2000)
        #print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))

        openSearchPutResource = f"{opensearchUrl}/usagemetadata/_doc/"
        print("\nPOST request to: " + openSearchPutResource)
        
        headers = {'Content-Type': 'application/json'}
        req_payload = msg.data()
        
        print("Start OpenSearch POST request...")
        r = requests.post(openSearchPutResource, data=req_payload, headers=headers)
        print("Finished posting to OpenSearch with code: " + str(r.status_code) + "\n")
        
        # Acknowledging the message to remove from message backlog
        consumer.acknowledge(msg)

    except pulsarExceptions.Timeout:
        print("Still waiting for a message...")
    except Exception as e: 
        print(e)
        waitingForMsg = False
 
    time.sleep(1)
# end::consume-message[]

# tag::clean-up[]
client.close()
# end::clean-up[]