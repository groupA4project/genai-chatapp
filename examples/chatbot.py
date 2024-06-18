import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
        page_title="GroupA4week8deliverable Demo Application",
    page_icon=":robot:"
)
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": st.secrets['api_key']}

st.header("GroupA4week8deliverable Demo Application")
st.markdown("[Github](https://github.com/groupA4project/genai-chatapp)")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
   i return input_text 


user_input = get_text()

if user_input:
    output = query({
        # "inputs": {
        #     "past_user_inputs": st.session_state.past,
        #     "generated_responses": st.session_state.generated,
        #     "text": user_input,
        # }
        "inputs": user_input
        ,"parameters": {"repetition_penalty": 1.33},
    })
    print(output)
    st.session_state.past.append(user_input)
    try:
        st.session_state.generated.append(output[0]["generated_text"])
    except:
         st.session_state.generated.append("sorry unable to process your qureis at this moment")
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

