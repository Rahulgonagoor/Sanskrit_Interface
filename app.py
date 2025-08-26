import streamlit as st
import base64
from pathlib import Path
import streamlit_authenticator as stauth
from sentence_analyzer_with_meaning import clean_and_split, analyze_word

# ================= Page Config =================
st.set_page_config(page_title="Sanskrit Sentence Analyzer", layout="wide")

# ================= Load secrets =================
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]

# Credentials dictionary for authenticator
credentials = {
    "usernames": {
        USERNAME: {
            "name": USERNAME,
            "password": PASSWORD  # plaintext for now, you can hash later
        }
    }
}

# Cookie config
cookie_name = "sanskrit_analyzer"
cookie_key = "some_random_secret_key"
cookie_expiry = 30  # days

# ================= Init Authenticator =================
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=cookie_name,
    key=cookie_key,
    expiry_days=cookie_expiry
)

# ================= Login =================
# New API: just call login(location=...)
authenticator.login(location="main")

# Retrieve login info from session_state
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

# ================= Auth Flow =================
if authentication_status is False:
    st.error("❌ Username/Password is incorrect")
elif authentication_status is None:
    st.warning("⚠️ Please enter your username and password")
elif authentication_status:
    # Logged in successfully
    authenticator.logout("Logout", "sidebar")
    st.success(f"✅ Welcome {name or ''}!")

    # ================= Helper to load image =================
    def get_base64_image(image_path: Path) -> str:
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return ""

    # ================= Logo =================
    assets_path = Path(__file__).parent / "assets"
    logo_path = assets_path / "logo.png"
    chip_b64 = get_base64_image(logo_path)

    if chip_b64:
        st.markdown(
            f"""
            <div style="text-align: center; padding-top: 20px; padding-bottom: 10px;">
                <img src="data:image/png;base64,{chip_b64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================= Title =================
    st.title("🧠 Sanskrit Sentence Analyzer with Meanings")
    st.markdown(
        "Enter a Sanskrit sentence in **Devanagari script**, and view noun/verb analysis with kāraka & meaning details."
    )

    # ================= Input field =================
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

                # ================= Meanings =================
                meanings = result.get("meanings", {})
                if meanings:
                    st.subheader("📚 Meanings")
                    for key, value in meanings.items():
                        with st.expander(f"{key} Meaning"):
                            st.write(value)
