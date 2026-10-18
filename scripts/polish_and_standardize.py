#!/usr/bin/env python3
"""
Final Polish & Standardization for vocab.json:
1. Prune redundant compound 'सूरज-मंडली' (duplicate of 'सूर्य-मंडल')
2. Normalize compound spelling: 'ग़लत फ़हमी' -> 'ग़लतफ़हमी'
3. Clean wikitext notes from languages/demonyms
"""

import json

def polish_and_standardize():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    prune_set = {'सूरज-मंडली'}

    normalized_hi = {
        'ग़लत फ़हमी': 'ग़लतफ़हमी'
    }

    cleanups = {
        'बंगाली': {'en': 'Bengali (language) / of Bengal / Bengali person (adj., n.)'},
        'गुजराती': {'en': 'Gujarati (language) / of Gujarat / Gujarati person (adj., n.)'},
        'मराठी': {'en': 'Marathi (language) / of Maharashtra (adj., n.)'},
        'उर्दू': {'en': 'Urdu (language) (n.)'},
        'मलयालम': {'en': 'Malayalam (language) (n.)'},
        'तमिल': {'en': 'Tamil (language) / of Tamil Nadu / Tamil person (adj., n.)'}
    }

    cleaned = []
    pruned_count = 0

    for item in data:
        w = item['hi'].strip()
        if w in prune_set:
            pruned_count += 1
            continue

        if w in normalized_hi:
            item['hi'] = normalized_hi[w]

        if item['hi'] in cleanups:
            for k, v in cleanups[item['hi']].items():
                item[k] = v

        cleaned.append(item)

    # Sort strictly descending by frequency
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially 1 to N
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Final polish complete. Pruned {pruned_count} entries. Total active entries: {len(cleaned)}.")

if __name__ == '__main__':
    polish_and_standardize()
