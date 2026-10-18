#!/usr/bin/env python3
"""
Prunes the 26 identified inflectional duplicates, verb participles, and spelling duplicates:
- 11 Verb participles & reach family inflections (जला, पढ़ा, पहुँचा, पहुंचे, आदि)
- 9 Possessive pronoun oblique and feminine duplicates (अपने, अपनी, मेरी, हमारे, आदि)
- 5 Bare verb stems (सुन, ला, चुन, निकल, लड़)
- 1 Spelling duplicate headword (पहुँचना vs पहुंचना)

Sorts strictly descending by frequency and re-indexes sequentially from 1 to N.
"""

import json

def prune_participles_and_pronouns():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    drop_set = {
        # 1. Possessive pronoun gender & oblique duplicates
        'अपने', 'मेरी', 'अपनी', 'हमारे', 'उसके', 'तुम्हारे', 'उसकी', 'तुम्हारी', 'इसके',

        # 2. Verb participles & reach family inflections
        'जला', 'पढ़ा', 'पहुँचने', 'खरीदा', 'पहुंचे', 'जलाने', 'पहुंचने', 'पहुँचा', 'पहुँचे', 'पहुंचा', 'पहुँचाने',

        # 3. Bare verb stems
        'सुन', 'ला', 'चुन', 'निकल', 'लड़',

        # 4. Exact duplicate infinitive
        'पहुँचना'
    }

    cleaned = []
    pruned_count = 0

    for item in data:
        w = item['hi'].strip()
        if w in drop_set:
            pruned_count += 1
            continue
        cleaned.append(item)

    # Sort strictly descending by frequency
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially 1 to len(cleaned)
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("SECOND PRUNING PASS COMPLETED")
    print("=" * 60)
    print(f"Original entries count  : {len(data)}")
    print(f"Entries pruned          : {pruned_count}")
    print(f"Cleaned entries count   : {len(cleaned)}")
    print("=" * 60)

if __name__ == '__main__':
    prune_participles_and_pronouns()
