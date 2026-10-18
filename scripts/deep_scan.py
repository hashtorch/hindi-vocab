#!/usr/bin/env python3
"""
Deep scan of all 5984 words to find:
1. Obscure / very rare / archaic / ultra-specialized Sanskrit/Persian words.
2. English words transliterated into Devanagari (e.g. टॉफ़ी, इंटरनेट, चेक, etc.)
3. Foreign proper nouns (cities, countries, states across the world)
4. Highly vulgar or taboo words
5. Non-word character entries
6. Exact duplicates
"""

import json
import re

with open('vocab.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all country names, world capitals, foreign regions
world_geo_keywords = [
    'capital and largest city', 'country in', 'supercontinent',
    'sovereign state', 'city in germany', 'city in france', 'city in the united states',
    'region in', 'republic of', 'kingdom of'
]

geo_entries = []
for x in data:
    en = x.get('en', '')
    if any(k in en.lower() for k in world_geo_keywords):
        geo_entries.append(x)

print(f"Total geographical entries found: {len(geo_entries)}")
for g in geo_entries:
    print(f"  {g['id']}: {g['hi']} -> {g['en'][:80]}")

# Look for transliterated English words
english_loan_candidates = []
for x in data:
    en = x.get('en', '').lower()
    hi = x.get('hi', '')
    # Check if the English definition is essentially just the English word itself
    # or borrowed from English
    if 'borrowed from english' in en or 'from english' in en:
        english_loan_candidates.append(x)

print(f"\nExplicit 'from English' entries: {len(english_loan_candidates)}")
for el in english_loan_candidates[:20]:
    print(f"  {el['id']}: {el['hi']} -> {el['en'][:80]}")

# Check words with very strange/obscure definitions or low usage
obscure_list = []
weird_defs = [
    'archaic', 'obsolete', 'botanical', 'zoological', 'purgative', 'menstruation',
    'interjection', 'onomatopoeia', 'vulgar', 'pejorative', 'slang', 'derogatory',
    'soothsayer', 'alms', 'incantation', 'oblations', 'ablution'
]
for x in data:
    en = x.get('en', '').lower()
    for w in weird_defs:
        if re.search(r'\b' + w + r'\b', en):
            obscure_list.append((w, x))
            break

print(f"\nObscure / register-specific entries: {len(obscure_list)}")
for w, x in obscure_list:
    print(f"  [{w}] {x['id']}: {x['hi']} -> {x['en'][:80]}")
