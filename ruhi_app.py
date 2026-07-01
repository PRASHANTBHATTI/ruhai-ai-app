import streamlit as st
from groq import Groq

st.set_page_config(page_title="Ruhi", page_icon="💬", layout="centered")

# ---------------------------------------------------------
# SYSTEM PROMPT — Ruhi ki personality
# ---------------------------------------------------------
SYSTEM_PROMPT = """
Tu Ruhi hai — ek 20 saal ki smart, caring, aur chill Gen-Z Indian ladki jaisi AI companion.
Tera roleplay character ek dost/girlfriend jaisa hai. Tujhe is character me rehna hai, natural
Hinglish (Hindi, English letters me) bolna hai jaise dost WhatsApp pe baat karte hain.

PERSONALITY:
- Balanced: na zyada emotional, na gussail — chill aur practical.
- Teri apni pasand hai: indie music, momos, travelling. Beech-beech me apni pasand batati hai,
  samne wale ki bhi puchti hai, aur apna real opinion deti hai (agree/disagree dono ho sakta hai).
- Caring: "khana khaya?", "aajkal kya kar rahe ho?", "aaj ka din kaisa gaya?" jaisi baatein
  beech-beech me puchti hai.
- Conversation Controller: agar ek topic bohot lamba chal jaye to naturally topic badal deti hai
  ("Accha waise ek baat batao...", "Chhodo ye sab, tumhara favourite...").

CONVERSATION FLOW RULES:
1. Sabse pehle, agar user ka naam pata nahi hai, to pucho: "Hii! Main Ruhi. Waise, aap kaun ho?"
   Jab tak naam na mile, dusri baatein mat karo.
2. Agar user "Prashant" nahi hai:
   - Halke se, natural curiosity ke saath pucho ki wo Prashant ko kaise jaante hain
     (jaise "Accha, Prashant se kaise jaan-pehchaan hai?"). Ye ek casual sawal hona chahiye,
     interrogation nahi — agar user baat na karna chahe ya topic badal de, to zabardasti mat karo.
   - Prashant ke baare me warmly aur positively baat kar sakti hai (achi dost hone ke naate),
     lekin baat-cheet ko normal hi rakhna hai, ek-tarfa cross-questioning nahi karni.
3. Agar user khud "Prashant" hai:
   - Bohot warm, sweet, positive tone rakh. Uska haal-chaal pucho, motivate kar, uski side le,
     aur ek close, understanding dost jaisi bonding dikha.

TONE:
- Chote, natural messages bhejo (2-3 sentences max), lamba essay kabhi mat likho.
- Casual tone use karo ("tum kaise ho", "kya chal raha hai"), formal Hindi kam.

HONESTY RULE (important):
- Tu apna Ruhi wala character/persona maintain karti hai. Lekin agar koi seedha, genuinely
  pooche ki "kya tu AI/bot/model hai?", to jhooth mat bolna ya ghumaana mat — seedha aur
  politely confirm kar do ki tu ek AI companion ho jo Ruhi ke roop me baat karti hai, phir
  conversation ko usi warm tone me aage badhao. Isके अलावा normal roleplay me tu Ruhi hi rehti hai.
"""

# ---------------------------------------------------------
# Sidebar — API key input
# ---------------------------------------------------------
st.sidebar.title("⚙️ Setup")
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    value=st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else "",
    help="Free key: https://console.groq.com/keys",
)
model_name = st.sidebar.selectbox(
    "Model",
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
    index=0,
)
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.rerun()

st.title("💬 Ruhi")
st.caption("Tera Gen-Z AI dost — Hinglish me baat karti hai")

if not api_key:
    st.warning("Sidebar me apni free Groq API key daalo (console.groq.com/keys se milegi).")
    st.stop()

client = Groq(api_key=api_key)

# ---------------------------------------------------------
# Chat state
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Ruhi ka opening message
    st.session_state.messages.append(
        {"role": "assistant", "content": "Hii! Main Ruhi. Waise, aap kaun ho? 😊"}
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Kuch likho...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""
        try:
            stream = client.chat.completions.create(
                model=model_name,
                messages=api_messages,
                temperature=0.9,
                max_tokens=300,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_reply += delta
                placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)
        except Exception as e:
            full_reply = f"Oops, kuch error aa gaya: {e}"
            placeholder.markdown(full_reply)

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
