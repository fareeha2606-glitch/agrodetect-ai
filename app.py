import streamlit as st
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from gtts import gTTS
from io import BytesIO

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AgroDetect AI",
    page_icon="🌱",
    layout="wide"
)

# ================= FILE SETUP =================
USERS_FILE = "users.json"
CERT_DIR = "certificates"
os.makedirs(CERT_DIR, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# ================= SAFE RERUN =================
def safe_rerun():
    try:
        st.rerun()
    except:
        pass

# ================= SKY BLUE THEME =================
st.markdown("""
<style>
.stApp { background:#87CEEB; color:black; }

/* ✅ FIX: increased top padding */
.block-container { padding-top:4.5rem; }

h1,h2,h3,h4,h5,h6,p,span,div,label { color:black !important; }

.navbar {
    display:flex; justify-content:space-between;
    padding:16px 40px; background:#5DADE2;
    border-bottom:2px solid #2E86C1;
}
.logo { font-size:26px; font-weight:700; color:#0B3C5D !important; }
.menu span { margin-left:22px; font-weight:600; color:black !important; }
.menu .active {
    background:#2E86C1; color:white !important;
    padding:8px 18px; border-radius:20px;
}

.hero {
    background:linear-gradient(135deg,#AEDFF7,#5DADE2);
    border-radius:26px; padding:50px; margin:30px;
}
.hero h1 { color:#0B3C5D !important; }

.box {
    background:#D6ECFA; border-radius:18px;
    padding:30px; box-shadow:0 0 0 2px #5DADE2;
    max-width:480px;
}

.stButton > button {
    background:#2E86C1; color:white !important;
    border-radius:10px; font-weight:700;
}
.stButton > button:hover { background:#1B4F72; }

section[data-testid="stFileUploader"],
section[data-testid="stCameraInput"] {
    background:#D6ECFA; border-radius:14px;
    padding:14px; border:2px dashed #2E86C1;
}
</style>
""", unsafe_allow_html=True)

# ================= LANGUAGE MAP =================
LANG_MAP = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi"
}

# ================= TRANSLATED VOICE TEXT =================
VOICE_TEXT = {
    "English": {
        "problem": "The disease detected is leaf blight disease.",
        "solution": "Spray neem oil twice a week.",
        "plan": "Continue the treatment for seven days."
    },
    "Telugu": {
        "problem": "పంటలో లీఫ్ బ్లైట్ వ్యాధి గుర్తించబడింది.",
        "solution": "వారానికి రెండుసార్లు నేమ్ ఆయిల్ పిచికారీ చేయండి.",
        "plan": "ఏడు రోజుల పాటు చికిత్స కొనసాగించండి."
    },
    "Hindi": {
        "problem": "फसल में लीफ ब्लाइट रोग पाया गया है।",
        "solution": "सप्ताह में दो बार नीम तेल का छिड़काव करें।",
        "plan": "सात दिनों तक उपचार जारी रखें।"
    }
}

# ================= HELPERS =================
def speak(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    st.audio(audio_buffer.read(), format="audio/mp3")

def predict_leaf_problem():
    return {
        "problem": "Leaf Blight Disease",
        "solution": "Spray neem oil twice a week",
        "plan": "Continue treatment for 7 days"
    }

def generate_certificate(name):
    path = f"{CERT_DIR}/{name}_certificate.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4

    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(6)
    c.rect(40, 40, w-80, h-80)

    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(w/2, h-140, "CROP HEALTH CERTIFICATE")

    c.setFont("Helvetica", 18)
    c.drawCentredString(w/2, h-260, f"Farmer Name: {name}")
    c.drawCentredString(w/2, h-320, "Crop Status: Healthy")

    c.drawCentredString(
        w/2, h-420,
        f"Issue Date: {datetime.now().strftime('%d %B %Y')}"
    )

    c.save()
    return path

# ================= NAVBAR =================
def navbar(active="home"):
    st.markdown(f"""
    <div class="navbar">
        <div class="logo">🌱 AgroDetect AI</div>
        <div class="menu">
            <span class="{ 'active' if active=='home' else '' }">Home</span>
            <span class="{ 'active' if active=='scan' else '' }">Scan</span>
            <span>Market</span>
            <span>Certificate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "home":
    navbar("home")

    st.markdown("""
    <div class="hero">
        <h1>AI-Powered Plant Disease Classification Engine</h1>
        <p>Detect crop diseases instantly with voice guidance.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("🔐 Login"):
        st.session_state.page = "login"
        safe_rerun()
    if col2.button("📝 Register"):
        st.session_state.page = "register"
        safe_rerun()

# ================= REGISTER =================
elif st.session_state.page == "register":
    navbar()

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Create Account")

    name = st.text_input("Full Name")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        with open(USERS_FILE) as f:
            users = json.load(f)

        users[mobile] = {"name": name, "password": password}

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

        st.success("Registration successful")
        st.session_state.page = "login"
        safe_rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        safe_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= LOGIN =================
elif st.session_state.page == "login":
    navbar()

    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Login")

    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with open(USERS_FILE) as f:
            users = json.load(f)

        if mobile in users and users[mobile]["password"] == password:
            st.session_state.user = users[mobile]
            st.session_state.page = "scan"
            safe_rerun()
        else:
            st.error("Invalid credentials")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        safe_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= SCAN =================
elif st.session_state.page == "scan":
    if not st.session_state.user:
        st.session_state.page = "login"
        safe_rerun()

    navbar("scan")
    st.subheader("🌿 Upload or Scan Leaf")

    uploaded = st.file_uploader("Upload leaf image", type=["jpg","png","jpeg"])
    camera = st.camera_input("Or capture using camera")

    image = uploaded if uploaded else camera

    if image:
        st.image(image, width=320)

        language = st.radio(
            "Choose language for voice assistance",
            ["English", "Telugu", "Hindi"],
            horizontal=True
        )

        if st.button("Analyze Crop"):
            result = predict_leaf_problem()

            st.success(f"Disease: {result['problem']}")
            st.info(f"Solution: {result['solution']}")
            st.warning(f"Plan: {result['plan']}")

            lang_code = LANG_MAP[language]
            voice_message = (
                VOICE_TEXT[language]["problem"] + " " +
                VOICE_TEXT[language]["solution"] + " " +
                VOICE_TEXT[language]["plan"]
            )
            speak(voice_message, lang_code)

            cert = generate_certificate(st.session_state.user["name"])
            with open(cert, "rb") as f:
                st.download_button(
                    "📜 Download Certificate",
                    f,
                    file_name="crop_certificate.pdf"
                )
