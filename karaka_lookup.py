from dhatu_search import load_dhatus, search_form

# Apādāna kāraka sūtras
APADANA_SUTRAS = [
    {
        "sutra": "1.4.31 भुवः प्रभवः",
        "meaning": "Source from which something originates.",
        "verbs": ["भू", "प्रभव"]
    },
     {
        "sutra": "1.4.24 ध्रुवमपायेऽपादानम्",
        "meaning": "Fixed point from which departure happens.",
        "verbs": ["गम्", "व्रज्", "अवरोह्", "पत्"]
    },
    {
        "sutra": "1.4.25 भीत्रार्थानां भयहेतुः",
        "meaning": "Cause/source of fear or danger.",
        "verbs": ["बिभे", "उद्विज्", "त्रै", "रक्ष्"]
    },
    {
        "sutra": "1.4.26 पराजेरसोढः",
        "meaning": "Something that becomes unbearable.",
        "verbs": ["पराजि"]
    },
    {
        "sutra": "1.4.27 वारणार्थानामीप्सितः",
        "meaning": "Desired object from which one is prevented.",
        "verbs": ["वारय", "निवर्त", "निवार"]
    },
    {
        "sutra": "1.4.28 अन्तर्द्धौ येनादर्शनमिच्छति",
        "meaning": "The one from whom one hides (concealment).",
        "verbs": ["अन्तर्धा", "निल", "दृश्"]
    },
    {
        "sutra": "1.4.29 आख्यातोपयोगे",
        "meaning": "In relation to learning from a teacher.",
        "verbs": ["धी", "शिक्ष", "आगम"]
    },
    {
        "sutra": "1.4.30 जनिकर्तुः प्रकृतिः",
        "meaning": "Prime cause of something's origin.",
        "verbs": ["जन्"]
    },
]

def find_apadana_sutra(verb_root):
    for sutra in APADANA_SUTRAS:
        for dhatu in sutra["verbs"]:
            if dhatu in verb_root:
                return f"{sutra['sutra']} — {sutra['meaning']}"
            
    return None

def get_karaka_sutra(dhatu_root):
    return find_apadana_sutra(dhatu_root)

# ------------------- VIBHAKTI to KARAKA Mapping -------------------

VIBHAKTI_KARAKA_MAP = {
    "प्रथमा": ("कर्तृ", "The doer of the action."),
    "द्वितीया": ("कर्म", "The object of the action."),
    "तृतीया": ("करण", "Instrument or means."),
    "चतुर्थी": ("सम्प्रदान", "Recipient."),
    "पञ्चमी": ("अपादान", "Point of separation or origin."),
    "षष्ठी": ("सम्बन्ध", "Relation or possession."),
    "सप्तमी": ("अधिकरण", "Location or context.")
}

def get_vibhakti_karaka(vibhakti):
    return VIBHAKTI_KARAKA_MAP.get(vibhakti, ("❓", "❓"))
