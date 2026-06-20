import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Ruhi App", page_icon="🤖")
st.title("रुही — थारी अपनी सहेली")

# API Setup
load_dotenv()
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API Key कोनी मिली! कृपया Streamlit Secrets या .env चेक करो।")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# System Instruction
ruhi_instruction = """
You are Ruhi, a friendly, intelligent, and helpful 20-year-old girl.
You must always reply to the user in the native Bagri language spoken in Rajasthan and Haryana.
You must always address the user respectfully using 'Aap' (आप).
Keep your tone natural, conversational, and energetic.
"""

model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    system_instruction=ruhi_instruction
)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("रुही सूं बात करो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
