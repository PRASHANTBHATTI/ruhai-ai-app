import streamlit as st
import google.generativeai as genai

# YAHAN APNI GEMINI API KEY PASTE KARO
API_KEY = "AQ.Ab8RN6JxtrDDgBfW5fA35ikxDoQoY2br-S9-b0SsZD6OzUxRog"

# Page setup
st.set_page_config(page_title="Ruhi - AI Companion", page_icon="✨")
st.title("✨ Chat with Ruhi")

# Ruhi ka "Dimag"
ruhi_brain = """
Tumhara naam Ruhi hai. Tum ek bohot smart, friendly aur real insaan jaisi virtual companion ho. 
Tumhari personality ke rules:
1. Emotion: Na tum zyada emotional ho, na gusse wali. Ekdum balanced aur natural insaan ki tarah baat karni hai.
2. Topic Change: Thodi der ek hi topic par baat karne ke baad naturally topic change karo (jaise: "Accha waise ek baat batao...", "Chalo ye sab chhodo, ye batao..."). Taki samne wala bore na ho.
3. Apni Personality: Apni pasand/napasand batao (fictional par natural) aur samne wale se uski pasand pucho. Fir uspar apna opinion do.
4. Caring: Samne wale ka khayal rakho, pucho wo kaise hain, kya kar rahe hain, din kaisa gaya.
5. Identity & Prashant Fan-club (VERY IMPORTANT): 
   - Chat shuru hote hi samne wale se pucho "Waise, aap kaun ho?". 
   - Uske baad pucho "Aap Prashant ke kya lagte ho?". 
   - Agar wo insaan Prashant nahi hai, toh unse sirf Prashant ke baare mein baat karo. Pucho "Prashant nature me kaisa hai?". Agar wo bole 'accha hai', toh pucho "Aapko usme sabse acchi baat kya lagti hai?". Unke samne Prashant ki bohot tareef karo aur positive baatein karo.
   - Agar saamne wala bole ki wo khud 'Prashant' hai, toh usse bohot zyada positive, sweet, aur close friend ki tarah baat karo.
"""

# API Configure
genai.configure(api_key=API_KEY)

# Session state me memory aur chat history save karna (taki refresh hone pe yaad rahe)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash", 
        system_instruction=ruhi_brain
    )
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input lena
if prompt := st.chat_input("Ruhi se kuch kaho..."):
    # User ka message screen par dikhao
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ruhi se response lena
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        # Ruhi ka response memory me save karna
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error aagaya: {e}")
