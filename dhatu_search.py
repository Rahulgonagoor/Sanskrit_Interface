import re

# List of primary and additional upasargas
UPASARGAS = [
    "प्र", "परा", "अप", "सम्", "अनु", "अव", "निस", "निर", "दुस", "दुर",
    "वि", "आ", "नि", "अधि", "अति", "अपि", "उत", "अभि", "उप", "सु", "परि", "अन्तर्", "तिरस्", "प्रति"
]

def load_dhatus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    raw_blocks = content.split("Heading:")
    dhatus = []

    for block in raw_blocks[1:]:
        heading_line = block.strip().split('\n')[0]
        full_block = "Heading:" + block.strip()
        words = re.findall(r'[ऀ-ॿ]+', full_block)

        dhatus.append({
            "heading": heading_line,
            "block": full_block,
            "forms": set(words)
        })

    return dhatus

def extract_metadata(heading_text):
    try:
        parts = heading_text.split(')')
        middle = parts[1].strip()
        before_meta, after_meta = middle.split('(')

        dhatu_parts = before_meta.strip().split()
        dhatu = dhatu_parts[0]
        artha = dhatu_parts[1]

        meta_parts = after_meta.strip(" )\n").split()
        ganah = meta_parts[0]
        pratyaya = meta_parts[1]
        karmakata = meta_parts[2]
        set_anit = meta_parts[3]

        return {
            "dhatu": dhatu,
            "arthah": artha,
            "ganah": ganah,
            "pratyaya": pratyaya,
            "karmakata": karmakata,
            "set_anit": set_anit
        }
    except Exception as e:
        print(f"⚠️ Error in metadata extraction: {e}")
        return {
            "dhatu": "❌",
            "arthah": "❌",
            "ganah": "❌",
            "pratyaya": "❌",
            "karmakata": "❌",
            "set_anit": "❌"
        }

def get_purusha_vachana(row, col):
    purushas = ["प्रथम पुरुष", "मध्यम पुरुष", "उत्तम पुरुष"]
    vachanas = ["एकवचन", "द्विवचन", "बहुवचन"]
    return purushas[row], vachanas[col]

def strip_upasarga(word):
    for upa in sorted(UPASARGAS, key=len, reverse=True):
        if word.startswith(upa):
            return word[len(upa):], upa
    return word, None

def search_form(dhatus, form):
    stripped_form, upasarga = strip_upasarga(form)

    for entry in dhatus:
        block = entry["block"]
        if form not in entry["forms"] and stripped_form not in entry["forms"]:
            continue

        metadata = extract_metadata(entry["heading"])
        lakaras = re.findall(r'कर्तरि\s+([^\n]+)\n((?:.+\n)+?)(?=\n\S|\Z)', block)
        for lakaara_line, table in lakaras:
            rows = [re.findall(r'[ऀ-ॿ]+', row) for row in table.strip().split('\n')]
            for r_idx, row in enumerate(rows):
                for c_idx, word in enumerate(row):
                    if word == form or word == stripped_form:
                        purusha, vachana = get_purusha_vachana(r_idx, c_idx)
                        return {
                            "metadata": metadata,
                            "lakaara": lakaara_line.strip(),
                            "form": form,
                            "purusha": purusha,
                            "vachana": vachana,
                            "upasarga": upasarga,
                            "full_block": block
                        }
    return None
