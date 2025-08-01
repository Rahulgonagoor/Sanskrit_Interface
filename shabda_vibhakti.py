import re

def load_shabdas(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    raw_blocks = content.split("Sanskrit Header:")
    shabdas = []

    for block in raw_blocks[1:]:
        header_line = block.strip().split('\n')[0]
        table_match = re.search(r'<<TABLE>>(.*?)</TABLE>', block, re.DOTALL)
        info_match = re.search(r'<<INFO>>(.*?)</INFO>', block, re.DOTALL)

        table_text = table_match.group(1).strip() if table_match else ""
        info_text = info_match.group(1).strip() if info_match else ""

        forms = set()
        for line in table_text.split('\n'):
            columns = re.split(r'\t+', line.strip())
            if len(columns) == 4:
                eka = re.split(r'[,\s]', columns[1])
                dvi = re.split(r'[,\s]', columns[2])
                bahu = re.split(r'[,\s]', columns[3])
                for form in eka + dvi + bahu:
                    clean_form = form.strip()
                    if clean_form:
                        forms.add(clean_form)

        shabdas.append({
            "header": header_line.strip(),
            "table": table_text,
            "info": info_text,
            "forms": forms,
            "full_block": block.strip()
        })

    return shabdas


def extract_header_details(header):
    try:
        parts = header.split('. ', 1)[1].strip().split()
        naamapada = parts[0]
        anta = parts[1].rstrip('ः,')
        linga = parts[2].rstrip('ः,')
        meaning = parts[-1]
        return {
            "naamapada": naamapada,
            "anta": anta,
            "linga": linga,
            "meaning": meaning
        }
    except:
        return {
            "naamapada": "❌",
            "anta": "❌",
            "linga": "❌",
            "meaning": "❌"
        }


def get_vibhakti_vachana(table_text, target):
    rows = table_text.strip().split('\n')
    for row in rows:
        cols = re.split(r'\t+', row.strip())
        if len(cols) < 4:
            continue
        vibhakti = cols[0].strip()
        eka = re.split(r'[,\s]', cols[1].strip())
        dvi = re.split(r'[,\s]', cols[2].strip())
        bahu = re.split(r'[,\s]', cols[3].strip())

        if target in eka:
            return vibhakti, "एकवचन"
        elif target in dvi:
            return vibhakti, "द्विवचन"
        elif target in bahu:
            return vibhakti, "बहुवचन"
    return None, None


def search_shabda(shabdas, word):
    for entry in shabdas:
        if word not in entry["forms"]:
            continue
        metadata = extract_header_details(entry["header"])
        vibhakti, vachana = get_vibhakti_vachana(entry["table"], word)
        return {
            **metadata,
            "word": word,
            "vibhakti": vibhakti,
            "vachana": vachana,
            "full_block": entry["full_block"]
        }
    return None


def get_vibhakti_details(word):
    file_path = "/Users/rahulmariyappagoudar/Desktop/grammer/shabda_combined.txt"
    try:
        shabdas = load_shabdas(file_path)
        result = search_shabda(shabdas, word)
        if result:
            return {
                "word": result['word'],
                "naamapada": result['naamapada'],
                "anta": result['anta'],
                "linga": result['linga'],
                "meaning": result['meaning'],
                "vibhakti": result['vibhakti'],
                "vachana": result['vachana']
            }
        else:
            return None
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None


def get_raw_entry_for_word(word):
    file_path = "/Users/rahulmariyappagoudar/Desktop/grammer/shabda_combined.txt"
    try:
        shabdas = load_shabdas(file_path)
        for entry in shabdas:
            if word in entry["forms"]:
                return entry["full_block"]
        return None
    except Exception as e:
        print(f"⚠️ Error in get_raw_entry_for_word: {e}")
        return None


def main():
    file_path = "/Users/rahulmariyappagoudar/Desktop/grammer/shabda_combined.txt"
    print("🔄 Loading shabdas from file...")

    try:
        shabdas = load_shabdas(file_path)
        print(f"✅ Loaded {len(shabdas)} śabda entries.\n")
    except Exception as e:
        print(f"❌ Failed to load shabdas: {e}")
        return

    while True:
        user_input = input("🔍 Enter a noun form to search (or type 'exit'): ").strip()
        if user_input.lower() == 'exit':
            print("👋 Exiting. Goodbye!")
            break

        result = search_shabda(shabdas, user_input)
        if result:
            print("\n🎯 Match Found:\n")
            print(f"नामपद: {result['naamapada']}")
            print(f"अन्तः: {result['anta']}")
            print(f"लिङ्गः: {result['linga']}")
            print(f"अर्थः: {result['meaning']}")
            print(f"रूप: {result['word']}")
            print(f"विभक्तिः: {result['vibhakti']}")
            print(f"वचनम्: {result['vachana']}")
            print("=" * 60)
            choice = input("📜 Show full table and info? (y/n): ").strip().lower()
            if choice == 'y':
                print("\n🧾 Full Block:\n")
                print(result['full_block'])
                print("=" * 60)
        else:
            print("❌ No match found.\n")


if __name__ == "__main__":
    main()
