#!/usr/bin/env python3
"""
Deep inspection script for vocab.json.
Categorizes potential candidates for removal / refinement:
1. Exact Hindi word duplicates
2. Single Devanagari characters / vowels / consonants / ligatures (e.g. क, ख, ऋ, क्ष)
3. Foreign proper nouns & obscure geography (cities, countries, states unlikely for core vocab)
4. Obscure / ultra-formal Sanskrit or archaic / Urdu terms rarely needed in everyday Hindi
5. English transliterations / technical loanwords where original English is used or weird forms
6. Non-word entries, grammatical artifacts, or noisy dictionary definitions
7. Vulgar / derogatory / taboo or unnecessary slang
"""

import json
import re

def main():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Exact duplicates
    from collections import defaultdict
    by_word = defaultdict(list)
    for x in data:
        by_word[x['hi'].strip()].append(x)
    duplicates = {k: v for k, v in by_word.items() if len(v) > 1}

    # 2. Characters / Alphabet letters / Ligatures
    characters = []
    for x in data:
        en = x.get('en', '')
        hi = x.get('hi', '').strip()
        if '(character' in en or 'vowel' in en or 'consonant' in en or 'ligature' in en:
            # Check if it is really just an alphabet letter
            if len(hi) <= 2 and not hi in ['आ', 'न', 'ओ', 'ना', 'माँ', 'जा', 'गा', 'खा', 'पी', 'दी', 'ले']: # valid short words
                characters.append(x)
            elif 'the first vowel' in en or 'the second consonant' in en or 'ligature of' in en:
                characters.append(x)

    # 3. Country / city / place names
    geographical = []
    for x in data:
        en = x.get('en', '')
        # Check if country / capital / city / province
        if re.search(r'\b(capital and largest city|country in|supercontinent|province of|city in|district of)\b', en, re.I):
            geographical.append(x)

    # 4. Low frequency words (freq <= 3) with obscure definitions
    obscure_candidates = []
    # Keywords indicating esoteric, botanical, religious-specific or archaic definitions
    obscure_keywords = [
        'botany', 'zoology', 'anatomy', 'archaic', 'obsolete', 'rare', 
        'species of', 'genus', 'purgative', 'menstruation', 'vulgar',
        'effigy', 'pagoda', 'sinless', 'unfordable', 'indefatigable',
        'soothsayer', 'alms', 'ascetic', 'ablution'
    ]
    for x in data:
        en = x.get('en', '').lower()
        freq = x.get('freq', 999)
        matched = [kw for kw in obscure_keywords if re.search(r'\b' + kw + r'\b', en)]
        if matched:
            obscure_candidates.append((x, matched))

    print(f"Duplicates: {len(duplicates)}")
    print(f"Alphabet/Character entries: {len(characters)}")
    print(f"Geographical/Place entries: {len(geographical)}")
    print(f"Obscure keyword matches: {len(obscure_candidates)}")

if __name__ == '__main__':
    main()
