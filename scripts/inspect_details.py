#!/usr/bin/env python3
"""
Deep inspection of all entries in vocab.json to identify:
1. Exact duplicates and slight spelling variants of same word
2. Alphabet/vowel/consonant letters that are not words
3. Overly obscure foreign place names/languages
4. Ultra-rare / archaic / redundant or awkward entries
5. Crude / vulgar or dictionary-bloat entries that learners do not need
"""

import json
import re

with open('vocab.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Examine character entries
chars = [x for x in data if '(character' in x.get('en', '')]
print(f"=== 1. Alphabet / Character Entries ({len(chars)}) ===")
for x in chars:
    print(f"ID {x['id']}: {x['hi']} -> {x['en']}")

# Examine proper nouns
prop_nouns = [x for x in data if '(prop.n' in x.get('en', '') or '(name' in x.get('en', '') or '(language' in x.get('en', '')]
print(f"\n=== 2. Sample Proper Nouns / Foreign names ({len(prop_nouns)}) ===")
for x in prop_nouns[:40]:
    print(f"ID {x['id']}: {x['hi']} -> {x['en']}")

# Examine duplicate Hindi words
from collections import defaultdict
by_word = defaultdict(list)
for x in data:
    by_word[x['hi'].strip()].append(x)
duplicates = {k: v for k, v in by_word.items() if len(v) > 1}
print(f"\n=== 3. Duplicate Hindi Words ({len(duplicates)}) ===")
for k, v in list(duplicates.items())[:20]:
    print(f"Word: {k} -> {[(item['id'], item['freq'], item['en'][:40]) for item in v]}")
