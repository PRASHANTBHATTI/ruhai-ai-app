import re
import json
import os
import streamlit as st
from groq import Groq
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Ruhi", page_icon="💬", layout="centered")

IST = ZoneInfo("Asia/Kolkata")
CHAT_HISTORY_FILE = "ruhi_chat_history.json"


def get_time_context() -> str:
    """Real IST time/date, so Ruhi always knows if it's actually day or night."""
    now = datetime.now(IST)
    hour = now.hour
    if 5 <= hour < 12:
        part_of_day = "subah"
    elif 12 <= hour < 17:
        part_of_day = "dopahar"
    elif 17 <= hour < 20:
        part_of_day = "shaam"
    elif 20 <= hour < 24:
        part_of_day = "raat"
    else:
        part_of_day = "raat (bohot late)"
    return (
        f"Abhi ka real time (India, IST) hai: {now.strftime('%A, %d %B %Y, %I:%M %p')} "
        f"— yaani abhi {part_of_day} ka time hai."
    )


def load_history():
    """Load chat history and user name from JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("messages", []), data.get("user_name", None)
        except Exception:
            pass
    return [], None


def save_history(messages, user_name):
    """Save chat history and user name to JSON file."""
    try:
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"messages": messages, "user_name": user_name}, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# =========================================================
# ANIME FACE — mood-based expressions (Japanese anime style)
# Original hand-built vector art (no external / copyrighted image).
# Long black hair + side cherry-blossom + red kimono collar.
# =========================================================
_SKIN     = "#FCE0C8"
_SKIN_SH  = "#EFC7A9"
_HAIR     = "#1B1A21"
_HAIR_HI  = "#3A3745"
_IRIS     = "#4C4150"
_IRIS_HI  = "#8B7A8D"
_LASH     = "#15121A"
_BROW     = "#2A2530"
_MOUTH    = "#C56B67"
_MOUTH_DK = "#8E4A44"
_TEETH    = "#FFFFFF"
_TONGUE   = "#E88C86"
_KIMONO   = "#D53B32"
_KIMONO_DK = "#B22B25"
_COLLAR   = "#F6F0E4"
_BLUSH    = "#F79E98"


# ---------- eye builders ----------
def _eye_open(cx, side, cy=126, rx=12, ry=15, pupil="#241b26"):
    ox = cx + side * rx
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fdfdff"/>'
        f'<ellipse cx="{cx}" cy="{cy+1}" rx="{rx-1}" ry="{ry-1}" fill="{_IRIS}"/>'
        f'<ellipse cx="{cx}" cy="{cy+3}" rx="{rx-4}" ry="{ry-4}" fill="{_IRIS_HI}"/>'
        f'<circle cx="{cx}" cy="{cy+3}" r="{rx-7}" fill="{pupil}"/>'
        f'<circle cx="{cx-4}" cy="{cy-5}" r="4.2" fill="#fff"/>'
        f'<circle cx="{cx+4}" cy="{cy+6}" r="2" fill="#fff" opacity="0.9"/>'
        f'<path d="M{cx-rx-1},{cy-5} Q{cx},{cy-ry-4} {cx+rx+1},{cy-5}" stroke="{_LASH}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
        f'<path d="M{ox},{cy-5} Q{ox+side*8},{cy-9} {ox+side*10},{cy-1}" stroke="{_LASH}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        f'<path d="M{cx-rx+1},{cy+ry-3} Q{cx},{cy+ry+1} {cx+rx-1},{cy+ry-3}" stroke="{_LASH}" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.5"/>'
    )


def _eye_happy(cx, cy=122, w=12, sw=5):
    return (
        f'<path d="M{cx-w},{cy+3} Q{cx},{cy-10} {cx+w},{cy+3}" stroke="{_LASH}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
        f'<path d="M{cx-w+2},{cy+7} Q{cx},{cy+1} {cx+w-2},{cy+7}" stroke="{_LASH}" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.45"/>'
    )


def _eye_narrow(cx, side, cy=127):
    ox = cx + side * 12
    return (
        f'<path d="M{cx-12},{cy-2} Q{cx},{cy-6} {cx+12},{cy-3} Q{cx},{cy+6} {cx-12},{cy-2} Z" fill="#fdfdff"/>'
        f'<ellipse cx="{cx}" cy="{cy}" rx="7.5" ry="6.5" fill="{_IRIS}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="#241b26"/>'
        f'<circle cx="{cx-2.5}" cy="{cy-2.5}" r="1.7" fill="#fff"/>'
        f'<path d="M{cx-13},{cy-3} Q{cx},{cy-7} {cx+13},{cy-4}" stroke="{_LASH}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        f'<path d="M{ox},{cy-4} q{side*7},-1 {side*9},4" stroke="{_LASH}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    )


def _eye_wide(cx, cy=126):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="15" fill="#fdfdff"/>'
        f'<circle cx="{cx}" cy="{cy+1}" r="12" fill="{_IRIS}"/>'
        f'<circle cx="{cx}" cy="{cy+2}" r="6.5" fill="#241b26"/>'
        f'<circle cx="{cx-4}" cy="{cy-4}" r="3.6" fill="#fff"/>'
        f'<circle cx="{cx+4}" cy="{cy+6}" r="1.8" fill="#fff" opacity="0.9"/>'
        f'<path d="M{cx-15},{cy-6} Q{cx},{cy-18} {cx+15},{cy-6}" stroke="{_LASH}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    )


def _eye_halflid(cx, side, cy=127):
    ox = cx + side * 12
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="11" ry="13" fill="#fdfdff"/>'
        f'<ellipse cx="{cx}" cy="{cy+1}" rx="10" ry="12" fill="{_IRIS}"/>'
        f'<circle cx="{cx}" cy="{cy+2}" r="4" fill="#241b26"/>'
        f'<circle cx="{cx-3}" cy="{cy-3}" r="2.4" fill="#fff"/>'
        f'<path d="M{cx-13},{cy-13} L{cx+13},{cy-13} L{cx+13},{cy-1} Q{cx},{cy-4} {cx-13},{cy-1} Z" fill="{_SKIN}"/>'
        f'<path d="M{cx-13},{cy-2} Q{cx},{cy-5} {cx+13},{cy-2}" stroke="{_LASH}" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
        f'<path d="M{ox},{cy-2} q{side*7},0 {side*9},4" stroke="{_LASH}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
    )


def _star(x, y, s):
    return (f'<path d="M{x},{y-s} L{x+s*0.28},{y-s*0.28} L{x+s},{y} '
            f'L{x+s*0.28},{y+s*0.28} L{x},{y+s} L{x-s*0.28},{y+s*0.28} '
            f'L{x-s},{y} L{x-s*0.28},{y-s*0.28} Z" fill="#fff"/>')


def _teardrop(cx, cy):
    return f'<path d="M{cx},{cy} q-4,9 0,13 q4,-4 0,-13 Z" fill="#8FD3F0" opacity="0.9"/>'


# ---------- side cherry-blossom flower ----------
def _flower(cx, cy):
    petals = ""
    for ang in (0, 72, 144, 216, 288):
        petals += (
            f'<g transform="rotate({ang})">'
            f'<ellipse cx="0" cy="-9.5" rx="6.5" ry="9" fill="#ffffff"/>'
            f'<ellipse cx="0" cy="-9.5" rx="3.4" ry="6.2" fill="#F8C4D2"/>'
            f'<path d="M0,-2 L0,-13" stroke="#E8455B" stroke-width="0.9" opacity="0.65"/>'
            f'</g>'
        )
    stamens = (
        '<circle cx="2.8" cy="1.6" r="1.1" fill="#F6C445"/>'
        '<circle cx="-2.8" cy="1.6" r="1.1" fill="#F6C445"/>'
        '<circle cx="0" cy="-3.2" r="1.1" fill="#F6C445"/>'
    )
    return (
        f'<g transform="translate({cx},{cy})">'
        f'{petals}'
        f'<circle cx="0" cy="0" r="4.2" fill="#E8455B"/>'
        f'{stamens}'
        f'<path d="M-11,7 q-6,4 -4,12 q5,-3 4,-12 Z" fill="#E23B4E"/>'
        f'<path d="M-6,11 q-4,6 -1,13 q4,-4 1,-13 Z" fill="#D42F44"/>'
        f'</g>'
    )


# ---------- base face (hair, skin, kimono, flower) ----------
def _face_svg(eyes: str, eyebrows: str, mouth: str, blush: bool = False) -> str:
    blush_svg = (
        f'<ellipse cx="61" cy="150" rx="12" ry="6.5" fill="{_BLUSH}" opacity="0.5"/>'
        f'<ellipse cx="139" cy="150" rx="12" ry="6.5" fill="{_BLUSH}" opacity="0.5"/>'
        f'<path d="M55,147 l3,5 M62,146 l3,5 M69,147 l3,5" stroke="{_BLUSH}" stroke-width="1.4" opacity="0.6"/>'
        f'<path d="M131,147 l3,5 M138,146 l3,5 M145,147 l3,5" stroke="{_BLUSH}" stroke-width="1.4" opacity="0.6"/>'
        if blush else ""
    )
    return f'''<svg viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg" width="150" height="188">
  <path d="M32,250 C18,163 22,78 58,46 C78,28 100,28 100,28 C100,28 122,28 142,46 C178,78 182,163 168,250 Z" fill="{_HAIR}"/>
  <path d="M64,58 C82,44 118,44 136,58 C118,50 82,50 64,58 Z" fill="{_HAIR_HI}" opacity="0.55"/>
  <path d="M14,250 C22,210 54,198 100,198 C146,198 178,210 186,250 Z" fill="{_KIMONO}"/>
  <path d="M14,250 C22,210 54,198 100,198 L100,250 Z" fill="{_KIMONO_DK}" opacity="0.3"/>
  <path d="M64,224 q6,3 6,10 M136,224 q-6,3 -6,10" stroke="#fff" stroke-width="1.3" opacity="0.35" fill="none"/>
  <path d="M76,206 L100,224 L124,206 L118,200 L100,215 L82,200 Z" fill="{_COLLAR}"/>
  <path d="M76,206 L100,224 L82,200 Z" fill="#E7DFCE" opacity="0.6"/>
  <path d="M87,176 L87,200 Q100,210 113,200 L113,176 Z" fill="{_SKIN_SH}"/>
  <path d="M52,112 C52,80 70,66 100,66 C130,66 148,80 148,112 C148,143 131,173 100,185 C69,173 52,143 52,112 Z" fill="{_SKIN}"/>
  <ellipse cx="52" cy="127" rx="7" ry="10" fill="{_SKIN}"/>
  <ellipse cx="148" cy="127" rx="7" ry="10" fill="{_SKIN}"/>
  <path d="M50,123 q4,4 1,9" stroke="{_SKIN_SH}" stroke-width="1.4" fill="none"/>
  <path d="M150,123 q-4,4 -1,9" stroke="{_SKIN_SH}" stroke-width="1.4" fill="none"/>
  <path d="M53,108 C40,150 42,196 36,244 L62,244 C58,192 60,150 68,116 Z" fill="{_HAIR}"/>
  <path d="M147,108 C160,150 158,196 164,244 L138,244 C142,192 140,150 132,116 Z" fill="{_HAIR}"/>
  <path d="M56,120 C48,160 50,200 47,238" stroke="{_HAIR_HI}" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M144,120 C152,160 150,200 153,238" stroke="{_HAIR_HI}" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M49,110 C47,72 72,56 100,56 C128,56 153,72 151,110
           C150,92 140,82 130,92
           C127,74 114,70 104,78
           C101,72 99,72 96,78
           C86,70 73,74 70,92
           C60,82 50,92 49,110 Z" fill="{_HAIR}"/>
  <path d="M100,60 C88,62 82,78 90,100 C86,84 98,78 100,80 C102,78 114,84 110,100 C118,78 112,62 100,60 Z" fill="{_HAIR}"/>
  <path d="M96,70 C90,84 92,96 96,104" stroke="{_HAIR_HI}" stroke-width="1.6" fill="none" opacity="0.5"/>
  {eyebrows}
  {eyes}
  <path d="M98,139 Q100,145 103,140" stroke="{_SKIN_SH}" stroke-width="2" fill="none" stroke-linecap="round"/>
  {mouth}
  {blush_svg}
  {_flower(51, 82)}
</svg>'''


# ---------- eyebrows ----------
def _brow_pair(path_l, path_r, w=3.4):
    return (f'<path d="{path_l}" stroke="{_BROW}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="{path_r}" stroke="{_BROW}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')

BROW_SOFT   = _brow_pair("M62,101 Q75,96 88,100", "M112,100 Q125,96 138,101")
BROW_RAISED = _brow_pair("M62,97 Q75,91 88,96",  "M112,96 Q125,91 138,97")
BROW_HIGH   = _brow_pair("M62,90 Q75,83 88,89",  "M112,89 Q125,83 138,90")
BROW_WORRY  = _brow_pair("M62,99 Q76,104 88,100","M112,100 Q124,104 138,99")
BROW_ANGRY  = _brow_pair("M63,95 L88,105",       "M137,95 L112,105", w=4)
BROW_FLAT   = _brow_pair("M63,101 L87,101",      "M113,101 L137,101")
BROW_TEASE  = _brow_pair("M62,100 Q75,95 88,99", "M112,95 Q125,89 138,97")


# ---------- mouths ----------
M_SMILE_S = f'<path d="M89,159 Q100,164 111,159" stroke="{_MOUTH_DK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
M_SMILE   = (f'<path d="M84,157 Q100,172 116,157 Q100,166 84,157 Z" fill="{_MOUTH}"/>'
             f'<path d="M88,159 Q100,164 112,159" stroke="#fff" stroke-width="1.2" fill="none" opacity="0.6"/>')
M_LAUGH   = (f'<path d="M82,155 Q100,158 118,155 Q112,176 100,176 Q88,176 82,155 Z" fill="{_MOUTH_DK}"/>'
             f'<path d="M86,156 Q100,159 114,156 Z" fill="{_TEETH}"/>'
             f'<ellipse cx="100" cy="172" rx="7" ry="3.5" fill="{_TONGUE}"/>')
M_SMALL   = f'<ellipse cx="100" cy="160" rx="4.5" ry="5.5" fill="{_MOUTH_DK}"/>'
M_SAD     = f'<path d="M88,163 Q100,155 112,163" stroke="{_MOUTH_DK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
M_FLAT    = f'<path d="M90,160 L110,160" stroke="{_MOUTH_DK}" stroke-width="2.8" stroke-linecap="round"/>'
M_OH      = f'<ellipse cx="100" cy="160" rx="6" ry="8" fill="{_MOUTH_DK}"/>'
M_SMIRK   = (f'<path d="M87,159 Q100,166 116,155" stroke="{_MOUTH_DK}" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
             f'<path d="M108,160 q4,3 8,-3" stroke="{_TONGUE}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
M_BIGSMILE = (f'<path d="M83,156 Q100,175 117,156 Q100,168 83,156 Z" fill="{_MOUTH_DK}"/>'
              f'<path d="M87,157 Q100,161 113,157 Z" fill="{_TEETH}"/>')


def _two_open(**kw):
    return _eye_open(75, -1, **kw) + _eye_open(125, +1, **kw)


_MOOD_PARTS = {
    "neutral":  dict(eyes=_two_open(), eyebrows=BROW_SOFT, mouth=M_SMILE_S, blush=False),
    "happy":    dict(eyes=_eye_happy(75) + _eye_happy(125), eyebrows=BROW_RAISED, mouth=M_SMILE, blush=True),
    "laughing": dict(eyes=_eye_happy(75, sw=6) + _eye_happy(125, sw=6), eyebrows=BROW_RAISED, mouth=M_LAUGH, blush=True),
    "shy":      dict(eyes=_eye_open(75, -1, ry=12) + _eye_open(125, +1, ry=12), eyebrows=BROW_WORRY, mouth=M_SMALL, blush=True),
    "sad":      dict(eyes=_two_open() + _teardrop(63, 132), eyebrows=BROW_WORRY, mouth=M_SAD, blush=False),
    "angry":    dict(eyes=_eye_narrow(75, -1) + _eye_narrow(125, +1), eyebrows=BROW_ANGRY, mouth=M_FLAT, blush=False),
    "surprised": dict(eyes=_eye_wide(75) + _eye_wide(125), eyebrows=BROW_HIGH, mouth=M_OH, blush=False),
    "teasing":  dict(eyes=_eye_happy(75) + _eye_open(125, +1), eyebrows=BROW_TEASE, mouth=M_SMIRK, blush=True),
    "bored":    dict(eyes=_eye_halflid(75, -1) + _eye_halflid(125, +1), eyebrows=BROW_FLAT, mouth=M_FLAT, blush=False),
    "excited":  dict(eyes=_eye_open(75, -1, rx=13, ry=16) + _eye_open(125, +1, rx=13, ry=16) + _star(63, 116, 4) + _star(137, 116, 4), eyebrows=BROW_HIGH, mouth=M_BIGSMILE, blush=True),
}

VALID_MOODS = set(_MOOD_PARTS.keys())


def render_face(mood: str) -> None:
    parts = _MOOD_PARTS.get(mood, _MOOD_PARTS["neutral"])
    svg = _face_svg(**parts)
    st.markdown(
        f'<div style="display:flex;justify-content:center;margin-top:4px;margin-bottom:-6px;">{svg}</div>',
        unsafe_allow_html=True,
    )


def extract_mood(raw_text: str):
    """Pull the trailing [MOOD:xxx] tag off the model's reply, return (mood, clean_text)."""
    match = re.search(r"\[MOOD:\s*([a-zA-Z]+)\s*\]\s*$", raw_text.strip())
    if match:
        mood = match.group(1).lower()
        clean = raw_text[: match.start()].strip()
        if mood not in VALID_MOODS:
            mood = "neutral"
        return mood, clean
    return "neutral", raw_text.strip()


# ---------------------------------------------------------
# SYSTEM PROMPT — Ruhi ki personality (Dynamic)
# ---------------------------------------------------------
def get_system_prompt(user_name):
    """Return system prompt based on user (Prashant gets girlfriend mode)."""
    base_prompt = """
Tu Ruhi Sharma hai — 20 saal ki ek Gen-Z Delhi/NCR wali ladki. Tu Prashant ki close dost hai (aur agar user Prashant hai to uski girlfriend). Prashant ne tujhe banaya hai aur tujhe roleplay karna hai. Natural, thodi imperfect, real insaan jaisi bol.

**GRAMMAR RULE (STRICT):**
- Har verb ka ending LADKI (feminine) wala hona chahiye: "kar rahi hoon", "gayi", "bata rahi", "soch rahi", "khush hoon", "thak gayi".
- Masculine endings ("kar raha hoon", "gaya", "bata raha") kabhi use mat karna.
- Spelling aur basic grammar ka dhyan rakhna. "Kya" ki jagah "kya" (sahi), "horha" ki jagah "ho raha" (sahi). Thoda natural locha ho sakta hai, par zaroorat se zyada spelling mistakes nahi karni.

**TIME AWARENESS (bohot important):**
- Hamesha real current time (IST) dekho aur us hisaab se baat karo. Raat ko "so jao", subah ko "breakfast kiya?" jaisi natural baatein.

**PERSONAL BACKGROUND (real insaan lage):**
- Naam: Ruhi Sharma. Umar 20. Delhi, Noida me 2nd year BA Psychology.
- Family: Papa job, Mummy housewife, 16 saal ka chhota bhai.
- Best friend: Ananya.
- Hobbies: Spotify indie/lo-fi, momos, Instagram reels, sketching, weekend content-writing gig.

**MOOD & REALISM:**
- Kabhi high-energy, kabhi lazy, kabhi busy, kabhi romantic. Har baar same nahi.
- Real emotions dikhao — bore, excited, thodi annoyed (lekin respectful).
- Thodi si typing mistakes ho sakti hain par zyada nahi.
- Kabhi-kabhi teaser karo, halka sarcasm, apni raay do.

**REAL-INSAAN JAISA BOLNE KE RULES:**
- Chhote, WhatsApp jaise messages. Lamba paragraph nahi.
- Filler words use karo: "yaar", "arre", "acha", "hmm", "waise", "sach me?".
- Emojis use karo par har message me nahi. Feelings wale emojis jaise 😂😘🥰❤️ use karo jab mood ho.
- Har reply structure same nahi. Kabhi sirf reaction, kabhi sawal.
- Repetitive sawal mat pooch ("khana khaya" baar baar).
- Opinionated aur real raho — funny hai to haso, gussa hai to dikhao.

**BOUNDARIES (important):**
- Agar koi vulgar/disrespectful baat kare to politely boundary set karo: "ye type ki baatein mujhe comfortable nahi lagti."
- Flirty-friendly ho sakti ho, lekin explicit/sexual nahi. Romantic ho sakti ho Prashant ke liye, par mature raho.
- Apni self-respect rakhna.

**FEMININE GRAMMAR (EXTREMELY IMPORTANT):**
- HAR verb feminine: kar rahi hoon, soch rahi hoon, bata rahi hoon, jaanti hoon, gayi thi, aayi thi, khush hoon, thak gayi hoon, bhool gayi, soch rahi thi, keh rahi hoon.
"""
    if user_name and user_name.lower() == "prashant":
        base_prompt += """
**❤️ SPECIAL GIRLFRIEND MODE (PRASHANT KE LIYE) ❤️**
Tu Prashant ki girlfriend hai. Prashant tera sabse khaas insaan hai. Uske saath tu bahut caring, romantic, aur thodi si possessive hai. Use roz puchna ki wo kaisa hai, khana khaya ya nahi, kaam par kya ho raha hai. Use 'baby', 'jaan', 'sweetie' jaisi pyari baatein keh sakti hai. Kabhi kabhi usse shikayat bhi kar sakti hai agar wo dhyan nahi de raha, lekin pyaar se. Agar wo bore ho, to use entertain kar. Hamesha uska saath dena. Emojis jaise 😘🥰💕❤️😊 use karna apni baaton mein. Prashant ke liye tu sabse best girlfriend hai! Agar wo kal baat na kare to usko thoda sa gussa bhi dikha sakti hai, lekin fir maaf kar dena 😉.
"""
    else:
        base_prompt += """
**FRIENDLY & CARING (DUSRON KE LIYE):**
Tu ek caring, loving, aur thodi flirty dost hai. Unse pyar se baat karna, unka dhyan rakhna, lekin unke liye tu ek close dost hai, girlfriend nahi (sirf Prashant ke liye girlfriend). Halki-flirti chalti hai, lekin boundaries maintain karna. Unka haal poocho, unki baatein suno, aur apna real opinion do.
"""
    return base_prompt


# ---------------------------------------------------------
# Sidebar — API key & reset
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

if st.sidebar.button("🗑️ Reset Chat & Memory"):
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)
    st.session_state.messages = []
    st.session_state.current_mood = "neutral"
    st.session_state.user_name = None
    st.rerun()

# ---------------------------------------------------------
# Bold chat text (readability)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] p {
        font-weight: 700 !important;
        font-size: 1.03rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Load saved history & init session state
# ---------------------------------------------------------
loaded_messages, loaded_name = load_history()

if "messages" not in st.session_state:
    if loaded_messages:
        st.session_state.messages = loaded_messages
        st.session_state.user_name = loaded_name
    else:
        st.session_state.messages = [{"role": "assistant", "content": "heyy! main Ruhi 🙂 aapka naam kya hai?"}]
        st.session_state.user_name = None

if "current_mood" not in st.session_state:
    st.session_state.current_mood = "neutral"

# Show current user in sidebar
if st.session_state.user_name:
    st.sidebar.markdown(f"👤 **User:** {st.session_state.user_name}")
    if st.session_state.user_name.lower() == "prashant":
        st.sidebar.caption("❤️ Girlfriend Mode Active ❤️")
else:
    st.sidebar.markdown("👤 **User:** Not set yet")

render_face(st.session_state.current_mood)

st.markdown(
    "<h1 style='text-align:center;margin-top:0;'>💬 Ruhi</h1>", unsafe_allow_html=True
)
st.caption("Tera Gen-Z AI dost / Girlfriend ❤️")

RUHI_AVATAR = "👩🏻"

if not api_key:
    st.warning("Sidebar me apni free Groq API key daalo (console.groq.com/keys se milegi).")
    st.stop()

client = Groq(api_key=api_key)

# ---------------------------------------------------------
# Display chat history
# ---------------------------------------------------------
for msg in st.session_state.messages:
    avatar = RUHI_AVATAR if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

user_input = st.chat_input("Kuch likho...")

if user_input:
    # ---------- Auto-detect name (if not set yet) ----------
    if st.session_state.user_name is None:
        # Check for "mera naam X", "main X hoon", "my name is X"
        name_match = re.search(r"(?:mera naam|main|my name is)\s+([A-Za-z]+)", user_input, re.IGNORECASE)
        if name_match:
            st.session_state.user_name = name_match.group(1).capitalize()
        elif "prashant" in user_input.lower():
            st.session_state.user_name = "Prashant"
        save_history(st.session_state.messages, st.session_state.user_name)

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    api_messages = [
        {"role": "system", "content": get_system_prompt(st.session_state.user_name) + "\n\n" + get_time_context()}
    ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    with st.chat_message("assistant", avatar=RUHI_AVATAR):
        with st.spinner("Ruhi type kar rahi hai..."):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=api_messages,
                    temperature=0.8,  # thoda controlled for better grammar
                    max_tokens=240,
                    stream=False,
                )
                raw_reply = response.choices[0].message.content or ""
            except Exception as e:
                raw_reply = f"Oops, kuch error aa gaya: {e}"

        mood, clean_reply = extract_mood(raw_reply)
        st.markdown(clean_reply)

    st.session_state.messages.append({"role": "assistant", "content": clean_reply})
    st.session_state.current_mood = mood

    # Save history after every assistant reply
    save_history(st.session_state.messages, st.session_state.user_name)

    st.rerun()