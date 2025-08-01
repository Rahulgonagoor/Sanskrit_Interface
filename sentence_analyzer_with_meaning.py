import re
from shabda_vibhakti import get_vibhakti_details, get_raw_entry_for_word
from dhatu_search import load_dhatus, search_form
from karaka_lookup import find_apadana_sutra, get_karaka_sutra, get_vibhakti_karaka  # ✅ New import

# Load dhatus at start
DHATU_FILE_PATH = "/Users/rahulmariyappagoudar/Desktop/grammer/dhatu_all_combined.txt"
try:
    print("🔄 Loading dhātus...")
    dhatu_data = load_dhatus(DHATU_FILE_PATH)
    print(f"✅ Loaded {len(dhatu_data)} dhātu entries.\n")
except Exception as e:
    print(f"❌ Error loading dhātus: {e}")
    dhatu_data = []

def extract_basic_artha(raw_entry):
    info_section = re.search(r"<<INFO>>(.*?)</INFO>", raw_entry, re.DOTALL)
    if not info_section:
        return None
    content = info_section.group(1)
    match = re.search(r"अर्थः[^\s:：\-–—]*[：:–—\-]?\s*([^\s]+)", content)
    return match.group(1) if match else None

def extract_meanings(raw_entry):
    info = re.search(r"<<INFO>>(.*?)</INFO>", raw_entry, re.DOTALL)
    if not info:
        return {}

    info_text = info.group(1)
    meanings = {}

    if "Bharati Kosha" in info_text:
        bk_match = re.search(r"Sanskrit Detail:(.*?)(?=Sanskrit Detail:)", info_text, re.DOTALL)
        if bk_match:
            meanings["Sanskrit"] = bk_match.group(1).strip()

    if "(San → Hin)" in info_text:
        pattern = r"Sanskrit Detail:(.*?)(?=Sanskrit Detail:|$)"
        matches = list(re.finditer(pattern, info_text, re.DOTALL))
        if matches:
            if "Sanskrit" in meanings and len(matches) > 1:
                meanings["Hindi"] = matches[1].group(1).strip()
            elif "Sanskrit" not in meanings:
                meanings["Hindi"] = matches[0].group(1).strip()

    if "(San → Eng)" in info_text:
        eng_match = re.search(r"Sanskrit Detail:.*?Sanskrit Detail:(.*?)(?=$)", info_text, re.DOTALL)
        if not eng_match:
            eng_match = re.search(r"Sanskrit Detail:(.*?)(?=$)", info_text, re.DOTALL)
        if eng_match:
            meanings["English"] = eng_match.group(1).strip()

    return meanings

def analyze_word(word):
    try:
        shabda_info = get_vibhakti_details(word)
        if shabda_info:
            raw_entry = get_raw_entry_for_word(word)

            artha = extract_basic_artha(raw_entry) if raw_entry else None
            meanings = extract_meanings(raw_entry) if raw_entry else {}

            vibhakti = shabda_info["vibhakti"]
            karaka, karaka_meaning = get_vibhakti_karaka(vibhakti)

            # Detect sutra only if it's apādāna
            apadana_sutra = None
            if karaka == "अपादान":
                # Find verb root in sentence (if any)
                for w in sentence_words:
                    dhatu_info = search_form(dhatu_data, w)
                    if dhatu_info:
                        root = dhatu_info["metadata"]["dhatu"]
                        apadana_sutra = find_apadana_sutra(root)
                        break

            return {
                "word": word,
                "type": "नामपद (Noun)",
                "naamapada": shabda_info["naamapada"],
                "linga": shabda_info["linga"],
                "vibhakti": vibhakti,
                "vachana": shabda_info["vachana"],
                "karaka": f"{karaka} - {karaka_meaning}",
                "artha": artha,
                "meanings": meanings,
                "apadana_sutra": apadana_sutra
            }

        dhatu_info = search_form(dhatu_data, word)
        if dhatu_info:
            meta = dhatu_info["metadata"]
            return {
                "word": word,
                "type": "धातु (Verb)",
                "dhatu": meta["dhatu"],
                "arthah": meta["arthah"],
                "lakaara": dhatu_info["lakaara"],
                "purusha": dhatu_info["purusha"],
                "vachana": dhatu_info["vachana"],
                "ganah": meta["ganah"],
                "karaka_sutra": get_karaka_sutra(meta["dhatu"])
            }

    except Exception as e:
        print(f"⚠️ Error analyzing '{word}': {e}")

    return {
        "word": word,
        "type": "❓ Unknown"
    }

def clean_and_split(sentence):
    return re.findall(r'[ऀ-ॿ]+', sentence)

def main():
    global sentence_words  # To allow access inside analyze_word
    print("🧠 Sanskrit Sentence Analyzer + Meanings")
    print("🔠 Enter a sentence (in Devanagari). Type 'exit' to quit.\n")

    while True:
        sentence = input("🔍 Enter sentence (or 'exit'): ").strip()
        if sentence.lower() == "exit":
            print("👋 Exiting analyzer.")
            break

        sentence_words = clean_and_split(sentence)
        print(f"\n🔎 Analyzing {len(sentence_words)} word(s):\n")

        results = []

        for word in sentence_words:
            result = analyze_word(word)
            results.append(result)
            print(f"🔹 Word: {result['word']}")
            print(f"   Type: {result['type']}")

            if result["type"] == "नामपद (Noun)":
                print(f"   नामपद: {result['naamapada']}")
                print(f"   लिङ्गः: {result['linga']}")
                print(f"   विभक्तिः: {result['vibhakti']}")
                print(f"   वचनम्: {result['vachana']}")
                print(f"   कारकः: {result['karaka']}")
                if result.get("artha"):
                    print(f"   अर्थः: {result['artha']}")
                if result.get("apadana_sutra"):
                    print(f"   📜 सूत्रम्: {result['apadana_sutra']}")

            elif result["type"] == "धातु (Verb)":
                print(f"   धातुः: {result['dhatu']}")
                print(f"   अर्थः: {result['arthah']}")
                print(f"   लकारः: {result['lakaara']}")
                print(f"   पुरुषः: {result['purusha']}")
                print(f"   वचनम्: {result['vachana']}")
                print(f"   गणः: {result['ganah']}")
                if result.get("karaka_sutra"):
                    print(f"   📜 Kāaraka Sūtra: {result['karaka_sutra']}")
            else:
                print("   🛑 No grammatical info found.")
            print("-" * 50)

        for result in results:
            meanings = result.get("meanings", {})
            if meanings:
                print(f"\n📚 Meanings for: {result['word']}")
                options = list(meanings.keys())
                for idx, key in enumerate(options, 1):
                    print(f"{idx}. {key} Meaning")

                choice = input("🔍 Choose a meaning to view (number or Enter to skip): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    selected = options[int(choice) - 1]
                    print(f"\n📖 {selected} Meaning:\n{meanings[selected]}")
                else:
                    print("⏭️ Skipped.\n")

if __name__ == "__main__":
    main()
