import os
import pulsar
import time
import requests
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
        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))

        openSearchPutResource = f"{opensearchUrl}usagemetadata/_doc/"
        
        r = requests.put(openSearchPutResource, data=msg.data(), headers='Content-Type: application/json')
        print(r)
        # Acknowledging the message to remove from message backlog
        consumer.acknowledge(msg)

        #waitingForMsg = False
    except:
        print("Still waiting for a message...")
 
    time.sleep(1)
# end::consume-message[]

# tag::clean-up[]
client.close()
# end::clean-up[]