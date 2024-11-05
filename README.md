# LLM cost and observability using DataStax
With every GenAI initiative LLM cost is one the main concerns along with observability. There are some platforms/frameworks to approach this challenges, which require additional licenses and management of custom integrations. 

In this demo we explore how to develop a GenAI application using Langflow, modify existing funtionality and extend it to collect metadata from the LLM interaction, and send this data a Astra Streaming topic, to later consume the topic and export the data for further analysis. Integration between the components of this demo is done through each platform APIs.

## 1. Pre-requisites
The guide to this demo assumes you have:
1. Access to [Astra DB account](https://astra.datastax.com)
2. Python 3.10 or superior installed.
3. Docker and permission to create new containers for OpenSearch or an OpenSearch deployment with a ready index.
4. Langflow, either installed locally (v1.0.18 or superior), using docker image or in the cloud ([Astra Langflow](https://astra.datastax.com/langflow/))

## 2. Installation
### Langflow
Inside the "langflow" folder you can find the "RAG to Astra Streaming.json" flow file, which can be imported to Langflow. Also you can create your own RAG app in Langflow and import the custom components from the "Components" subfolder. 

The ["PulsarProducer_CustomComponent"](https://www.langflow.store/store/3403c9aa-c411-4596-89cf-d3b033dca015) is also available in the Langflow store if you want to import it from there. 

### OpenSearch
Edit the docker-compose.yml for OpenSearch to assign an admin password for both nodes.
- OPENSEARCH_INITIAL_ADMIN_PASSWORD=

Also make sure the environment variable DISABLE_SECURITY_PLUGIN is set to true in the nodes configuration and the DISABLE_SECURITY_DASHBOARDS_PLUGIN variable is set to true in the opensearch-dashboards section. 

## 3. Create some synthetic requests to populate the Dashboard (optional)
Inside the "Synthetic Traffic" folder there is a synthetic-calls.py script that can generate API calls to Langflow API endpoint, using entries at random from the csv files located it the data subfolder.

The pulsar-consumer.py script as the name implies, create a pulsar consumer for the topic created in Astra Streaming, each call to the Langflow flow will create a new message and sent it to the Astra Streaming topic, the pulsar-consumer script will "hear" this message and export it to OpenSearch API.

## Show and Demo
In the "app" folder there is a simple Streamlit app to show the RAG application working, is works with Lanflow RAG flow by means of consuming the API. It can be seen that the Langflow app sends a message to Astra Streaming with the "pulsar-consumer.py" script, this script will export the metadata in the message to OpenSearch.

OpenSearch dashboards is accesible at http://localhost:5601 if using the docker compose included. Within OpenSearch dashboards is required that an index is created, then a new dashboard, inside the dashboard a new visualization can be created to show the metadata collected.


