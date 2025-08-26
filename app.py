import streamlit as st
import base64
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

from sentence_analyzer_with_meaning import clean_and_split, analyze_word

# ================= Page Config (must be first Streamlit call) =================
st.set_page_config(page_title="Sanskrit Sentence Analyzer", layout="wide")

# ================= Load Config (supports user.yml OR users.yaml) ==============
config = None
repo_root = Path(__file__).parent

for fname in ("user.yml", "users.yaml"):
    user_file = repo_root / fname
    if user_file.exists():
        with open(user_file, "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=SafeLoader)
            break

if not config:
    st.error("⚠️ Could not find `user.yml` or `users.yaml` in the project root.")
    st.stop()

# Provide safe defaults if cookie block missing
cookie_cfg = config.get("cookie", {})
cookie_name = cookie_cfg.get("name", "sanskrit_cookie")
cookie_key = cookie_cfg.get("key", "random_key")
cookie_expiry = cookie_cfg.get("expiry_days", 30)

# ================= Init Authenticator ========================================
authenticator = stauth.Authenticate(
    credentials=config["credentials"],
    cookie_name=cookie_name,
    cookie_key=cookie_key,
    cookie_expiry_days=cookie_expiry
)

# ================= Login ======================================================
name = None
authentication_status = None
username = None

try:
    # Old API: returns tuple
    name, authentication_status, username = authenticator.login("Login", location="main")
except TypeError:
    # New API: use session_state
    authenticator.login(location="main")
    name = st.session_state.get("name")
    authentication_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")

# ================= Auth Flow ==================================================
if authentication_status is False:
    st.error("❌ Username/Password is incorrect")

elif authentication_status is None:
    st.warning("⚠️ Please enter your username and password")

elif authentication_status:
    # Logged in
    authenticator.logout("Logout", "sidebar")
    st.success(f"✅ Welcome {name or ''}!")

    # ==== Helper to load image as base64 ====
    def get_base64_image(image_path: Path) -> str:
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return ""

    # Path to assets / logo
    assets_path = repo_root / "assets"
    logo_path = assets_path / "logo.png"
    chip_b64 = get_base64_image(logo_path)

    # ===== Static Logo (only if found) =====
    if chip_b64:
        st.markdown(
            f"""
            <div style="text-align: center; padding-top: 20px; padding-bottom: 10px;">
                <img src="data:image/png;base64,{chip_b64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )

    # ===== Title and description =====
    st.title("🧠 Sanskrit Sentence Analyzer with Meanings")
    st.markdown(
        "Enter a Sanskrit sentence in **Devanagari script**, and view noun/verb analysis with kāraka & meaning details."
    )

    # ===== Input field =====
    sentence = st.text_input("🔠 Enter Sanskrit sentence (Devanagari):")

    if sentence:
        st.divider()
        st.subheader("📊 Word-by-word Analysis")

        sentence_words = clean_and_split(sentence)
        results = []

        for word in sentence_words:
            result = analyze_word(word)
            results.append(result)

            with st.expander(f"🔍 {result['word']} — {result['type']}"):
                if result["type"] == "नामपद (Noun)":
                    st.write(f"**नामपद**: {result['naamapada']}")
                    st.write(f"**लिङ्गः**: {result['linga']}")
                    st.write(f"**विभक्तिः**: {result['vibhakti']}")
                    st.write(f"**वचनम्**: {result['vachana']}")
                    st.write(f"**कारकः**: {result['karaka']}")
                    if result.get("artha"):
                        st.write(f"**अर्थः**: {result['artha']}")
                    if result.get("apadana_sutra"):
                        st.info(f"📜 **सूत्रम्**: {result['apadana_sutra']}")

                elif result["type"] == "धातु (Verb)":
                    st.write(f"**धातुः**: {result['dhatu']}")
                    st.write(f"**अर्थः**: {result['arthah']}")
                    st.write(f"**लकारः**: {result['lakaara']}")
                    st.write(f"**पुरुषः**: {result['purusha']}")
                    st.write(f"**वचनम्**: {result['vachana']}")
                    st.write(f"**गणः**: {result['ganah']}")
                    if result.get("karaka_sutra"):
                        st.info(f"📜 **Kāraka Sūtra**: {result['karaka_sutra']}")

                else:
                    st.warning("🛑 No grammatical info found.")

                # ===== Meanings =====
                meanings = result.get("meanings", {})
                if meanings:
                    st.subheader("📚 Meanings")
                    for key, value in meanings.items():
                        with st.expander(f"{key} Meaning"):
                            st.write(value)
