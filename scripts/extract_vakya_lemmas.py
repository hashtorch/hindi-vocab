#!/usr/bin/env python3
"""
Meticulous extraction of genuine base lemmas from ../hindi-vakya/data/
that are NOT yet in vocab.json.

Strict Rules:
- Must NOT be an inflected verb form (e.g., ता/ती/ते, या/यी/ये, ए, ई, कर/के, ंगा/ऊंगी).
- Must NOT be an oblique plural or feminine adjective ending in -े or -ी if base ends in -ा.
- Must NOT be a plural noun ending in -ें, -एं, -ों, -ियाँ.
- Must be a true dictionary base lemma (noun, adjective, adverb, or standard infinitive).
- Must be a high-yield, natural Hindi word used in multiple sentences in hindi-vakya.
"""

import json
import re
from collections import Counter
import glob

def normalize_nuqta(s):
    return s.replace('\u093c', '').strip()

def extract_genuine_missing_lemmas():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    vocab_exact = {x['hi'].strip() for x in vocab}
    vocab_norm = {normalize_nuqta(x['hi']) for x in vocab}

    with open('../hindi-vakya/data/dictionary.json', 'r', encoding='utf-8') as f:
        vakya_dict = json.load(f)

    # Count sentence occurrences across all 20 phrase files
    sentence_counts = Counter()
    for pf in sorted(glob.glob('../hindi-vakya/data/phrases*.json')):
        with open(pf, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                words = set(re.findall(r'[\u0900-\u097F]+', p['hi']))
                sentence_counts.update(words)

    # Disallowed suffixes that indicate inflection:
    inflected_endings = (
        'ों', 'ियों', 'ियां', 'ियाँ', 'ें', 'एं', 'कर', 'के',
        'ूंगा', 'ूंगी', 'ेंगे', 'ेंगी', 'ूँगा', 'ूँगी', 'ता', 'ती', 'ते',
        'या', 'यी', 'यीं', 'ईं', 'हीं'
    )

    valid_candidates = []

    for word, count in sentence_counts.most_common():
        # Minimum threshold of 3 distinct sentences to ensure it is authentic and practical
        if count < 3:
            continue

        # Check existing coverage
        if word in vocab_exact or normalize_nuqta(word) in vocab_norm:
            continue

        # Skip inflected endings
        if word.endswith(inflected_endings) and len(word) > 2:
            continue

        # Check definition
        defn = vakya_dict.get(word, '').strip()
        if not defn:
            continue

        # Skip if definition marks grammatical inflections
        if any(tag in defn.lower() for tag in ['(m pl)', '(f pl)', '(obl pl)', '(pl)', '(subjunctive)', 'past of', 'prog marker']):
            continue

        # If it ends in -े and definition has m pl/obl or pl, skip (e.g. बड़े, छोटे, किले, रास्ते)
        if word.endswith(('े', 'ी')) and any(tag in defn.lower() for tag in ['(f)', '(m pl/obl)', '(pl/obl)', 'plural', 'feminine']):
            continue

        # Check if it is a bare verb stem where the infinitive exists in vocab
        infinitive = word + 'ना'
        if infinitive in vocab_exact or normalize_nuqta(infinitive) in vocab_norm:
            continue

        # Check if base masculine adjective exists (e.g. if word is बारीक, check; if word ends in -ी and -ा exists, skip)
        if word.endswith('ी'):
            base_a = word[:-1] + 'ा'
            if base_a in vocab_exact or normalize_nuqta(base_a) in vocab_norm:
                continue

        # Clean definition
        clean_def = defn
        # Append part of speech if identifiable
        pos = ''
        if defn.startswith('to '):
            pos = ' (v.)'
        elif any(k in defn.lower() for k in ['sacred', 'holy', 'pure', 'grand', 'splendid', 'crooked', 'bent', 'fine', 'delicate', 'elderly', 'aged', 'strong', 'robust']):
            pos = ' (adj.)'
        else:
            pos = ' (n.)'

        if not clean_def.endswith('.'):
            clean_def += pos

        valid_candidates.append({
            'hi': word,
            'en': clean_def,
            'vakya_count': count
        })

    print(f"Total authentic, un-inflected base lemmas found: {len(valid_candidates)}")

    with open('scripts/extracted_vakya_lemmas.json', 'w', encoding='utf-8') as f:
        json.dump(valid_candidates, f, ensure_ascii=False, indent=2)

    print("\nTop 40 extracted lemmas:")
    for x in valid_candidates[:40]:
        print(f"  {x['hi']} (in {x['vakya_count']} sentences) -> {x['en']}")

if __name__ == '__main__':
    extract_genuine_missing_lemmas()
