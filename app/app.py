import streamlit as st
import requests 
import json

from datetime import datetime
from datetime import timezone 

service_url=st.secrets['LANGFLOW_API_ENDPOINT']

# It must be called at the start 
st.set_page_config(page_title="Regulatory assistant", layout="centered")

# Methods to call Langflow
def Create_Payload() -> str:
    # payload required by Langflow API
    tweaks = dict()
    tweak_textinput = {"user_value" : "Streamlit app: anonymous"}
    tweaks['TextInput-ocdhC'] = tweak_textinput

    payload = dict()
    payload['input_value'] = st.session_state.user_input
    payload['output_type'] = "chat"
    payload['input_type'] = "chat"
    payload['tweaks'] = tweaks
    
    output = json.dumps(payload, ensure_ascii=False)
    return output

def on_make_question():
    if(st.session_state.user_input is not ""): 
        req_payload = Create_Payload()
        st.session_state.llm_answer = ""
    if(req_payload is not "" and req_payload is not None):
        r = requests.post(service_url, data=req_payload)
    if r.status_code == 200:
        response = json.loads(r.content)
        message = json.loads(response['outputs'][0]['outputs'][0]['results']['message']['data']['text'])
        st.session_state.llm_answer = message['tokens']['response']
        st.session_state.input_tokens = message['tokens']['input']
        st.session_state.output_tokens = message['tokens']['output']
        st.session_state.user_question = message['question']

# Session initialization
if 'prompt_tokens' not in st.session_state:
    st.session_state.prompt_tokens = 0
if 'output_tokens' not in st.session_state:
    st.session_state.output_tokens = 0
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""
if 'llm_answer' not in st.session_state:
    st.session_state.llm_answer = ""

st.title('Regulatory Assistant')
st.markdown("""This chatbot is able to answer questions related to regulations and policies.""")
st.markdown("""This assistant is powered by DataStax Astra and Langflow. Your inquiries will be passed to a Langflow application through its API.
            The Lanflow application will send to a Pulsar topic in Astra Streaming the metadata of this interaction for analysis, as well as retrieve the answer to your question for this app to show it you.""")
st.markdown("""Please write down your question:""")
st.text_input("Your question here... ", key="user_input", on_change=on_make_question)
container = st.container(border=True)

if st.session_state.llm_answer:
    container.write(st.session_state.llm_answer)
    with st.container(border=True):
        st.markdown("""If you are curious, this interaction consumed the following:""")
        st.write(f"Tokens used to ask the LLM: {st.session_state.input_tokens}")
        st.write(f"Tokens received from the LLM: {st.session_state.output_tokens}")
