import streamlit as st
from util import detect_intent_texts
import uuid

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="💬 Support Chatbot", page_icon="💬", layout="centered")

# ----------------- Session State Setup -----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #f0f4f8, #e0f0ff) !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-title {
        font-size: 2.4rem;
        font-weight: bold;
        text-align: center;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    .chat-bubble {
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 12px;
        max-width: 75%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        word-wrap: break-word;
        font-size: 1rem;
    }
    .user {
        background-color: #d0f0ff;
        color: #003a4d;
        margin-left: auto;
        margin-right: 0;
        text-align: right;
    }
    .bot {
        background-color: #ffffff;
        color: #222;
        margin-right: auto;
        margin-left: 0;
        text-align: left;
    }
    .input-container {
        position: fixed;
        bottom: 1rem;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 600px;
        background-color: #ffffff;
        padding: 12px 16px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Sidebar Menu -----------------
st.sidebar.markdown("<div class='sidebar-title'>💡 Quick Options</div>", unsafe_allow_html=True)

QUICK_OPTIONS = [
    "Track my order",
    "Return an item",
    "Shipping info",
    "Payment methods",
    "Contact support",
    "Refund status",
    "Product availability"
]

for option in QUICK_OPTIONS:
    if st.sidebar.button(option):
        st.session_state.chat_history.append(("You", option))
        bot_reply = detect_intent_texts(option, session_id=st.session_state.session_id)
        st.session_state.chat_history.append(("Bot", bot_reply))

# ----------------- Title -----------------
st.markdown("<div class='chat-title'>💬 Customer Support Chatbot</div>", unsafe_allow_html=True)

# ----------------- Chat Display -----------------
if st.session_state.chat_history:
    for sender, message in st.session_state.chat_history:
        role = "user" if sender == "You" else "bot"
        st.markdown(f"""
            <div class='chat-bubble {role}'>
                <strong>{'You' if role == 'user' else 'Bot'}:</strong><br>{message}
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='text-align:center; margin-top: 40px; color: #888;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='80'><br>
            <span style='font-size: 1.2rem;'>How can I help you today?</span>
        </div>
    """, unsafe_allow_html=True)

# ----------------- Message Submission -----------------
def submit():
    user_msg = st.session_state.user_input.strip()
    if user_msg:
        st.session_state.chat_history.append(("You", user_msg))
        bot_response = detect_intent_texts(user_msg, session_id=st.session_state.session_id)
        st.session_state.chat_history.append(("Bot", bot_response))
        st.session_state.user_input = ""

# ----------------- Input Box -----------------
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
st.text_input(
    "Your message",
    key="user_input",
    placeholder="Type your message and hit Enter...",
    label_visibility="collapsed",
    on_change=submit
)
st.markdown("</div>", unsafe_allow_html=True)
