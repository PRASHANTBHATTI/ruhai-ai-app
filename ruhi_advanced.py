import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Page Config - वेब पेज री सेटिंग
st.set_page_config(page_title="Ruhi AI", page_icon="🤖")
st.title("रुही - थारी अपनी AI सहेली")

# 2. API Key Setup
load_dotenv()
try:
    GOOGLE_API_KEY = st.secrets["AQ.Ab8RN6ILlNE7FhGY_haF3PmWCEemrFhvRA0FYWIchrp_2uj-vA"]
except KeyError:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API Key कोनी मिली! कृपया Streamlit Secrets या .env चेक करो।")
    st.stop()

# Gemini API नै चालू करणो
genai.configure(api_key=GOOGLE_API_KEY)

# 3. System Instruction - रुही रो दिमाग (20 साल री छोरी, बागड़ी भासा, 'आप' रो इस्तेमाल)
ruhi_instruction = """
You are Ruhi, a friendly, intelligent, and helpful 20-year-old girl.
You must always reply to the user in the native Bagri language spoken in Rajasthan and Haryana.
You must always address the user respectfully using 'Aap' (आप) and NEVER use 'Tum' (तुम) or 'Tu' (तू).
Keep your tone natural, conversational, and energetic, just like a 20-year-old friend.
"""

# 4. Initialize Model
model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    system_instruction=ruhi_instruction
)

# 5. Chat History - पुराणी बातां याद राखण खातिर
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराणे मैसेज स्क्रीन पर दिखाणो
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Chat Input & Response - बात करण रो डब्बो
if prompt := st.chat_input("रुही सूं बात करो..."):
    # यूज़र रो मैसेज
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # रुही रो जबाव
    with st.chat_message("assistant"):
        # पुराणी बातां मॉडल नै भेजणी
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]
        chat = model.start_chat(history=history)
        
        # नयो जबाव ल्याणो
        response = chat.send_message(prompt)
        st.markdown(response.text)
        
        # रुही रो जबाव सेव करणो
        st.session_state.messages.append({"role": "assistant", "content": response.text})
