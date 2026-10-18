#!/usr/bin/env python3
"""
Comprehensive cross-verification between:
  vocab.json (our frequency dictionary)
  ../hindi-vakya/data/ (6,000 real sentences + dictionary.json)

Identifies high-value authentic base lemmas from the sentence corpus
that are genuinely absent from vocab.json and provides full coverage metrics.
"""

import json
import glob
import re
from collections import Counter

def full_cross_verification():
    # 1. Load current vocab
    with open('vocab.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    vocab_exact = {x['hi'].strip(): x for x in vocab}
    vocab_norm = {x['hi'].replace('\u093c', '').strip(): x for x in vocab}

    # 2. Load vakya dictionary
    with open('../hindi-vakya/data/dictionary.json', 'r', encoding='utf-8') as f:
        vakya_dict = json.load(f)

    # 3. Load all 20 phrase files (6,000 sentences)
    phrase_files = sorted(glob.glob('../hindi-vakya/data/phrases*.json'))
    sentence_counts = Counter()
    total_tokens = 0
    total_sentences = 0

    for pf in phrase_files:
        with open(pf, 'r', encoding='utf-8') as f:
            phrases = json.load(f)
            total_sentences += len(phrases)
            for p in phrases:
                tokens = re.findall(r'[\u0900-\u097F]+', p['hi'])
                total_tokens += len(tokens)
                sentence_counts.update(set(tokens))

    # Coverage measurement
    covered_tokens = 0
    missing_tokens = Counter()
    for pf in phrase_files:
        with open(pf, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                tokens = re.findall(r'[\u0900-\u097F]+', p['hi'])
                for t in tokens:
                    norm = t.replace('\u093c', '')
                    if t in vocab_exact or norm in vocab_norm:
                        covered_tokens += 1
                    else:
                        missing_tokens[t] += 1

    token_coverage = (covered_tokens / total_tokens) * 100

    print("=" * 65)
    print("HINDI-VAKYA CORPUS COVERAGE REPORT")
    print("=" * 65)
    print(f"Total Sentences in hindi-vakya    : {total_sentences}")
    print(f"Total Token Occurrences in corpus: {total_tokens}")
    print(f"Token Occurrences Covered in Vocab: {covered_tokens} ({token_coverage:.2f}%)")
    print(f"Unique Word Forms in Sentences    : {len(sentence_counts)}")
    print("=" * 65)

    # Identify clean, non-inflected base lemmas missing in vocab.json
    # Filter out verb conjugations, case endings, plurals, and participles
    blacklist_tags = [
        '(m)', '(f)', '(m pl)', '(f pl)', '(obl pl)', '(pl)', '(m.pl)', '(f.pl)',
        'past of', 'prog marker', 'subjunctive', 'second person', 'first person'
    ]
    past_verbs = [
        'went', 'became', 'sat', 'saw', 'said', 'spoke', 'wrote', 'caught',
        'could', 'fell', 'kept', 'dropped', 'put', 'took', 'gave', 'heard'
    ]

    candidate_lemmas = []
    for word, count in sentence_counts.most_common():
        if count < 3:
            continue
        norm = word.replace('\u093c', '')
        if word in vocab_exact or norm in vocab_norm:
            continue
        # Skip bare stems if infinitive exists
        if (word + 'ना') in vocab_exact or (norm + 'ना') in vocab_norm:
            continue
        # Skip oblique plurals or participle endings
        if word.endswith(('ों', 'ियों', 'ियां', 'ियाँ', 'ें', 'एं', 'कर', 'के', 'ूंगा', 'ूंगी', 'ेंगे', 'ेंगी', 'ता', 'ती', 'ते')):
            continue

        defn = vakya_dict.get(word, '').strip()
        if not defn:
            continue

        if any(t in defn.lower() for t in blacklist_tags):
            continue
        if any(v in defn.lower() for v in past_verbs):
            continue

        # Clean POS
        pos = ' (n.)'
        if defn.startswith('to '):
            pos = ' (v.)'
        elif any(k in defn.lower() for k in ['sacred', 'holy', 'pure', 'grand', 'splendid', 'crooked', 'bent', 'fine', 'delicate', 'elderly', 'aged', 'strong', 'robust', 'fragrant']):
            pos = ' (adj.)'

        clean_def = defn
        if not clean_def.endswith('.'):
            clean_def += pos

        candidate_lemmas.append({
            'hi': word,
            'en': clean_def,
            'sentence_freq': count
        })

    print(f"\nIdentified {len(candidate_lemmas)} genuine, high-value base lemmas missing from vocab.json.")
    with open('scripts/valuable_missing_from_vakya.json', 'w', encoding='utf-8') as f:
        json.dump(candidate_lemmas, f, ensure_ascii=False, indent=2)

    print("\nSample 30 High-Value Base Words from Sentences:")
    for item in candidate_lemmas[:30]:
        print(f"  - {item['hi']} (in {item['sentence_freq']} sentences): {item['en']}")

if __name__ == '__main__':
    full_cross_verification()
