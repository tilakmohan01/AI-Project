import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION (USING SECRETS) ---

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key nahi mili! Please Streamlit Secrets mein 'GEMINI_API_KEY' set karein.")

st.set_page_config(page_title="AI Success Hub", page_icon="💰", layout="wide")

# --- CSS FOR GREY BUTTONS AND WHITE TEXT ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    
    div.stButton > button {
        background-color: #333333 !important; 
        color: #FFFFFF !important;           
        font-weight: 700 !important;         
        border-radius: 8px !important;
        border: 1px solid #444444 !important; 
        width: 100% !important;
        height: 3em !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button:hover {
        background-color: #444444 !important; 
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.1) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #111 !important;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    div[data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
    }
    div[data-testid="stChatInput"] textarea { color: #000000 !important; }

    .login-box {
        border: 1px solid #222;
        padding: 30px;
        border-radius: 15px;
        background-color: #000000;
        text-align: center;
    }

    h1, h2, h3, p, span, label { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Memory Initialize
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- MULTI-USER DATA ---
USERS = {
    "Admin": "1234",
    "User1": "abcd",
    "Guest": "9999"
}

# --- LOGIN PAGE ---
def login_page():
    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.title("🔐 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        
        if st.button("Login"): 
            if user in USERS and USERS[user] == pwd:
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = user
                st.rerun()
            else:
                st.error("Wrong details!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
def main_dashboard():
    with st.sidebar:
        st.title(f"⚙️ {st.session_state.get('user_name', 'Dash')}")
        if st.button("Logout"): 
            st.session_state['logged_in'] = False
            st.rerun()
        
        if st.button("Clear History"): 
            st.session_state['chat_history'] = []
            st.rerun()
        
        st.divider()
        st.subheader("📜 History")
        for i, chat in enumerate(st.session_state['chat_history'][-5:]):
            st.markdown(f"<p style='color:white;'>{i+1}. {chat['user'][:20]}...</p>", unsafe_allow_html=True)

    st.title("🤖 AI Success Mentor")
    st.write(f"Clear your doubts, {st.session_state.get('user_name', '')}")
    st.markdown("---")
    
    for chat in st.session_state['chat_history']:
        with st.chat_message("user"): st.write(chat["user"])
        with st.chat_message("assistant"): st.write(chat["ai"])

    user_input = st.chat_input("Apni strategy pucho...")

    if user_input:
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0])
            with st.spinner('Thinking...'):
                response = model.generate_content(user_input)
                st.session_state['chat_history'].append({"user": user_input, "ai": response.text})
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# --- FLOW ---
if st.session_state['logged_in']:
    main_dashboard()
else:

    login_page()
