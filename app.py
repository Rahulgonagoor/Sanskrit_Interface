import streamlit as st
from sentence_analyzer_with_meaning import clean_and_split, analyze_word

st.set_page_config(page_title="Sanskrit Sentence Analyzer", layout="wide")

# ===== Rotating Mandala Logo =====
st.markdown(
    """
    <style>
    .logo-wrapper {
        position: relative;
        width: 250px; /* Adjust overall size */
        margin: auto;
    }

    .chip {
        width: 100%;
        display: block;
    }

    .mandala {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 70%; /* Size relative to chip */
        transform: translate(-50%, -50%);
        animation: spin 10s linear infinite;
    }

    @keyframes spin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    </style>

    <div class="logo-wrapper">
        <img class="chip" src="assets/logo.png">
        <img class="mandala" src="assets/mandala.png">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🧠 Sanskrit Sentence Analyzer with Meanings")
st.markdown("Enter a Sanskrit sentence in **Devanagari script**, and view noun/verb analysis with kāraka & meaning details.")

# Input field
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

            # Meanings
            meanings = result.get("meanings", {})
            if meanings:
                st.subheader("📚 Meanings")
                for key, value in meanings.items():
                    with st.expander(f"{key} Meaning"):
                        st.write(value)
