#!/usr/bin/env python3
"""
Full word-by-word comprehensive evaluation script.
Flags candidate entries into specific buckets:
- BUCKET A: Alphabet / Character isolated letters (क, ख, अं, अः, etc.)
- BUCKET B: Exact Duplicate entries (e.g. किसान, लेखक, दुकानदार appearing twice)
- BUCKET C: Foreign proper nouns / cities / countries that are English/foreign transliterations (e.g. बर्लिन, हैम्बर्ग, मैसिडोनिया, एस्टोनिया, न्यूयॉर्क, बोलीविया)
- BUCKET D: Obsolete, ultra-formal, or extremely low-utility words for a core Hindi learner vocab
- BUCKET E: Non-standard spellings or minor anomalies
"""

import json
import re
from collections import defaultdict

def full_analysis():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Bucket A: Characters
    bucket_a = []
    # 2. Bucket B: Duplicates
    seen_words = defaultdict(list)
    for idx, item in enumerate(data):
        w = item['hi'].strip()
        seen_words[w].append(item)

    duplicate_items_to_remove = []
    for w, items in seen_words.items():
        if len(items) > 1:
            # keep the higher frequency or richer entry, flag the other
            # sort by freq desc
            sorted_items = sorted(items, key=lambda x: x['freq'], reverse=True)
            for dup in sorted_items[1:]:
                duplicate_items_to_remove.append({
                    'remove': dup,
                    'keep': sorted_items[0],
                    'reason': f"Duplicate of '{w}' (ID {sorted_items[0]['id']}, freq {sorted_items[0]['freq']})"
                })

    # Character letters:
    # Notice: 'आ', 'न', 'ओ' can be valid words, but entries 1808 to 1842 are pure Devanagari alphabet letters (अ, इ, क, ख, etc.)
    # Also 226 (क्ष ligature), 2601 (ख़), 2605 (फ़), 2606 (ज़), 2607 (क़)
    for item in data:
        en = item.get('en', '')
        hi = item.get('hi', '').strip()
        # If explicitly marked as character and definition describes vowel/consonant number
        if re.search(r'the (first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty-\w+) (vowel|consonant|nuqta consonant)', en, re.I) \
           or 'An irregular ligature of' in en \
           or ('(character)' in en and len(hi) == 1):
            bucket_a.append(item)

    # Bucket C: Foreign cities, countries, places (not core Hindi vocabulary)
    # Countries/cities like बर्लिन, हैम्बर्ग, एस्टोनिया, बोलीविया, मैसिडोनिया, न्यूयॉर्क, अज़रबैजान, केन्या, हंगरी, आदि
    foreign_geo = []
    # Let's inspect all items with '(name)' or '(prop.n.)'
    for item in data:
        en = item.get('en', '')
        hi = item.get('hi', '').strip()
        # Exclude Indian names, cultural terms, core geography (भारत, दिल्ली, मुंबई, हिमालय, गंगा)
        # Check foreign countries and cities
        foreign_patterns = [
            r'\b(germany|france|russia|united states|north america|south america|caucasus|central europe|scandinavia|balkans|middle east|qatar|bolivia|argentina|estonia|azerbaijan|macedonia|hamburg|berlin|new york|paris|kenya|hungary|denmark|austria|mexico|ireland|poland|spain|czech)\b'
        ]
        if any(re.search(p, en, re.I) for p in foreign_patterns):
            # Check if it is a foreign proper name
            if '(name)' in en or '(prop.n' in en:
                foreign_geo.append(item)

    # Bucket D: Rare / Esoteric / Low utility entries
    # Let's inspect words with freq <= 2 that are archaic, extremely rare, or strange
    rare_esoteric = []
    # Examples to check
    esoteric_words = [
        'बुत-कदा', 'तिगुना', 'रखवाना', 'अक्षम्य', 'मूत', 'हकला', 'गर्त', 'सन्निहित'
    ]
    for item in data:
        if item['hi'] in esoteric_words:
            rare_esoteric.append(item)

    print(f"Bucket A (Alphabet letters): {len(bucket_a)}")
    print(f"Bucket B (Duplicate entries to remove): {len(duplicate_items_to_remove)}")
    print(f"Bucket C (Foreign cities/countries): {len(foreign_geo)}")
    print(f"Bucket D (Sample rare/esoteric): {len(rare_esoteric)}")

    with open('scripts/audit_summary.json', 'w', encoding='utf-8') as f:
        json.dump({
            'bucket_a_alphabet': bucket_a,
            'bucket_b_duplicates': duplicate_items_to_remove,
            'bucket_c_foreign_geo': foreign_geo,
            'bucket_d_sample_rare': rare_esoteric
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    full_analysis()
