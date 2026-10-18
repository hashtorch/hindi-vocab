#!/usr/bin/env python3
"""
Adds high-utility base lemmas discovered from ../hindi-vakya/data/
into vocab.json to guarantee comprehensive sentence corpus coverage.

Only genuine headwords/lemmas are integrated:
- Verbs in base infinitive (-ना).
- Singular masculine base nouns/adjectives.
- Standard spellings with nuqta where standard.
"""

import json

def enrich_vocab_from_vakya():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    existing_words = {x['hi'].strip() for x in vocab}

    # High-value base additions discovered from real sentences in hindi-vakya:
    new_lemmas = [
        {'hi': 'सुलझाना', 'en': 'to solve / to unravel / to resolve (v.)', 'freq': 33},
        {'hi': 'इतिहासकार', 'en': 'historian (n.)', 'freq': 26},
        {'hi': 'सुनार', 'en': 'goldsmith (n.)', 'freq': 25},
        {'hi': 'पावन', 'en': 'sacred / holy / pure (adj.)', 'freq': 24},
        {'hi': 'टेढ़ा', 'en': 'crooked / bent / complicated (adj.)', 'freq': 21},
        {'hi': 'भव्य', 'en': 'grand / splendid / magnificent (adj.)', 'freq': 20},
        {'hi': 'रूपक', 'en': 'metaphor / allegory (n.)', 'freq': 20},
        {'hi': 'सुलझना', 'en': 'to be solved / to unravel (v.)', 'freq': 15},
        {'hi': 'कारीगर', 'en': 'artisan / craftsman / mechanic (n.)', 'freq': 14},
        {'hi': 'मुसाफ़िर', 'en': 'traveler / wayfarer / passenger (n.)', 'freq': 14},
        {'hi': 'सेनापति', 'en': 'general / commander-in-chief (n.)', 'freq': 13},
        {'hi': 'वर्णित', 'en': 'described / narrated / depicted (adj.)', 'freq': 13},
        {'hi': 'परिश्रम', 'en': 'hard work / labor / diligence (n.)', 'freq': 11},
        {'hi': 'बारीक', 'en': 'fine / delicate / subtle (adj.)', 'freq': 11},
        {'hi': 'वृद्ध', 'en': 'elderly / aged person (adj., n.)', 'freq': 10},
        {'hi': 'ग्रंथ', 'en': 'scripture / treatise / tome (n.)', 'freq': 10},
        {'hi': 'आँकड़ा', 'en': 'data / statistic / figure (n.)', 'freq': 10},
        {'hi': 'कंगाली', 'en': 'poverty / destitution (n.)', 'freq': 10},
        {'hi': 'पंचायत', 'en': 'panchayat / village council (n.)', 'freq': 10},
        {'hi': 'गूँज', 'en': 'echo / reverberation / resonance (n.)', 'freq': 10},
        {'hi': 'सुगंधित', 'en': 'fragrant / aromatic / scented (adj.)', 'freq': 9},
        {'hi': 'साधु', 'en': 'ascetic / monk / holy person (n., adj.)', 'freq': 9},
        {'hi': 'पुश्तैनी', 'en': 'ancestral / hereditary (adj.)', 'freq': 9},
        {'hi': 'पहरेदार', 'en': 'watchman / guard / sentry (n.)', 'freq': 9},
        {'hi': 'तूफ़ानी', 'en': 'stormy / tempestuous (adj.)', 'freq': 9}
    ]

    added_count = 0
    for item in new_lemmas:
        if item['hi'] not in existing_words:
            vocab.append(item)
            existing_words.add(item['hi'])
            added_count += 1

    # Sort strictly descending by frequency
    vocab.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially from 1 to N
    for idx, item in enumerate(vocab, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("VAKYA ENRICHMENT COMPLETED")
    print("=" * 60)
    print(f"High-value base lemmas added: {added_count}")
    print(f"Total vocabulary size       : {len(vocab)}")
    print("=" * 60)

if __name__ == '__main__':
    enrich_vocab_from_vakya()
