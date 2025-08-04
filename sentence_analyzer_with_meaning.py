import os
from shabda_vibhakti import get_vibhakti_details
from dhatu_search import get_dhatu_details
from karaka_lookup import get_karaka_for_vibhakti

def analyze_sentence(sentence):
    words = sentence.strip().split()
    results = []

    for word in words:
        noun_info = get_vibhakti_details(word)
        if noun_info:
            karaka = get_karaka_for_vibhakti(noun_info['vibhakti'])
            results.append({
                "word": word,
                "type": "noun",
                "linga": noun_info['linga'],
                "vachana": noun_info['vachana'],
                "vibhakti": noun_info['vibhakti'],
                "karaka": karaka,
                "meaning": noun_info['meaning']
            })
            continue

        verb_info = get_dhatu_details(word)
        if verb_info:
            results.append({
                "word": word,
                "type": "verb",
                "tense": verb_info.get('lakara'),
                "person": verb_info.get('purusha'),
                "number": verb_info.get('vachana'),
                "root": verb_info.get('dhatu'),
                "meaning": verb_info.get('meaning')
            })
            continue

        results.append({
            "word": word,
            "type": "unknown",
            "message": "No grammatical info found."
        })

    return results


def main():
    print("🔠 Enter Sanskrit sentence (Devanagari):")
    sentence = input().strip()

    print("📊 Word-by-word Analysis")
    results = analyze_sentence(sentence)

    for res in results:
        print(f"\n🔍 {res['word']} —", end=' ')
        if res["type"] == "noun":
            print("📘 Noun")
            print(f"   लिङ्गः       : {res['linga']}")
            print(f"   वचनम्       : {res['vachana']}")
            print(f"   विभक्तिः    : {res['vibhakti']}")
            print(f"   कारकः       : {res['karaka']}")
            print(f"   अर्थः       : {res['meaning']}")
        elif res["type"] == "verb":
            print("📙 Verb")
            print(f"   धातुः       : {res['root']}")
            print(f"   लकारः       : {res['tense']}")
            print(f"   पुरुषः       : {res['person']}")
            print(f"   वचनम्       : {res['number']}")
            print(f"   अर्थः       : {res['meaning']}")
        else:
            print("❓ Unknown")
            print(f"   🛑 {res['message']}")


if __name__ == "__main__":
    main()
