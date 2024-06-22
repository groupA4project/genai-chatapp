import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="GroupA4week9deliverable Demo Application",
    page_icon=":robot:",
    layout="wide"
)

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": st.secrets['api_key']}

# CSS for custom styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
    }
    .stTextInput input {
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .header h1 {
        color: #007bff;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'><h1>GroupA4week9deliverable Demo Application</h1></div>", unsafe_allow_html=True)
st.markdown("[Github](https://github.com/groupA4project/genai-chatapp)")

# Initializing session state
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_text():
    input_text = st.text_input("You:", "Hello, how are you?", key="input")
    return input_text 

user_input = get_text()

# Query and response handling
if user_input:
    output = query({
        "inputs": user_input,
        "parameters": {"repetition_penalty": 1.33},
    })
    st.session_state.past.append(user_input)
    try:
        st.session_state.generated.append(output[0]["generated_text"])
    except:
        st.session_state.generated.append("Sorry, unable to process your queries at this moment.")

# Displaying messages
if st.session_state['generated']:
    with st.container():
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
