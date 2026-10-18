#!/usr/bin/env python3
"""
Deep cross-comparison of ../hindi-vakya/data/ against vocab.json.

Goals:
1. Parse all 6,000 sentences across phrases01.json .. phrases20.json and dictionary.json.
2. Normalize for orthography (nuqta variations: e.g. साफ़ vs साफ, क़ानून vs कानून).
3. Filter out:
   - Grammatical inflections (plural -ों, -ें, -एं; oblique/past -ए, -ई, -या, -ता, -ती, -ते).
   - Conjunctive participles (-कर, -के: e.g. देखकर, होकर, सुनकर, बैठकर).
   - Verb stems that already exist as infinitives (e.g. बैठ -> बैठना, बढ़ -> बढ़ना, रह -> रहना).
4. Identify genuine, high-value base vocabulary lemmas present in hindi-vakya sentences
   that are currently missing in vocab.json.
5. Rank missing lemmas by frequency and utility.
"""

import json
import glob
import re
from collections import Counter

def normalize_nuqta(s):
    return s.replace('\u093c', '').strip()

def run_vakya_coverage_analysis():
    # 1. Load current vocab
    with open('vocab.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    vocab_exact = {x['hi'].strip(): x for x in vocab}
    vocab_norm = {normalize_nuqta(x['hi']): x for x in vocab}

    # 2. Load vakya dictionary
    with open('../hindi-vakya/data/dictionary.json', 'r', encoding='utf-8') as f:
        vakya_dict = json.load(f)

    # 3. Load all phrases & count sentence frequencies
    phrase_counts = Counter()
    phrase_files = sorted(glob.glob('../hindi-vakya/data/phrases*.json'))
    total_sentences = 0
    for pf in phrase_files:
        with open(pf, 'r', encoding='utf-8') as f:
            phrases = json.load(f)
            total_sentences += len(phrases)
            for p in phrases:
                words = re.findall(r'[\u0900-\u097F]+', p['hi'])
                phrase_counts.update(words)

    print(f"Loaded {total_sentences} sentences from {len(phrase_files)} phrase files.")
    print(f"Total unique tokens in sentences: {len(phrase_counts)}")

    # 4. Filter missing candidate lemmas
    # Heuristics for skipping inflected words:
    inflected_endings = (
        'ों', 'ियों', 'ियां', 'ियाँ', 'ें', 'एं', 'कर', 'ता', 'ती', 'ते',
        'या', 'यी', 'ये', 'ईं', 'हीं'
    )

    missing_candidates = []
    for word, count in phrase_counts.most_common():
        # Check if already covered (exact or nuqta-equivalent)
        if word in vocab_exact or normalize_nuqta(word) in vocab_norm:
            continue

        defn = vakya_dict.get(word, '')

        # Check if definition explicitly denotes an inflectional form
        if any(tag in defn for tag in ['(m)', '(f)', '(m pl)', '(f pl)', '(obl pl)', '(pl)', '(m.pl)', '(subjunctive)', 'prog marker', 'past of']):
            continue

        # Skip obvious inflectional suffix endings
        if word.endswith(inflected_endings) and len(word) > 2:
            continue

        # Check if it is a bare verb stem whose infinitive is already in vocab
        # e.g., 'बैठ' -> 'बैठना', 'रह' -> 'रहना', 'बढ़' -> 'बढ़ना'
        infinitive = word + 'ना'
        if infinitive in vocab_exact or normalize_nuqta(infinitive) in vocab_norm:
            continue

        # Valid candidate base word!
        missing_candidates.append({
            'word': word,
            'count': count,
            'def': defn
        })

    print(f"Found {len(missing_candidates)} candidate base words present in sentences but missing in vocab.json.")

    with open('scripts/missing_vakya_words.json', 'w', encoding='utf-8') as f:
        json.dump(missing_candidates, f, ensure_ascii=False, indent=2)

    print("\nTop 50 high-utility missing base words:")
    for item in missing_candidates[:50]:
        print(f"  {item['word']} (in {item['count']} sentences) -> {item['def']}")

if __name__ == '__main__':
    run_vakya_coverage_analysis()
