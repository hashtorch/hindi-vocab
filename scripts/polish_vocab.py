#!/usr/bin/env python3
"""
Prunes remaining redundant synonyms, past-tense verb duplicates, and hyper-niche mythological names.
Fixes remaining POS anomalies (e.g. काना, बजाए).
Re-sorts by frequency and re-indexes IDs 1..N.
"""

import json

def polish_vocab():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Specific words to prune:
    prune_words = {
        'बनारस',    # Redundant with वाराणसी (ID 881) & काशी (ID 935)
        'बंगलौर',   # Redundant variant of बेंगलुरु (ID 692)
        'ईसाइयत',   # Redundant synonym of ईसाई धर्म (ID 2930)
        'काहकशान',  # Obscure Persian synonym of आकाश गंगा (ID 2612)
        'इंडिया',    # Redundant with भारत (ID 344) & हिंदुस्तान (ID 496)
        'कैथी',     # Obsolete medieval script, not relevant for Hindi proficiency
        'कौशल्या',  # Low-utility mythological figure (freq 3)
        'सुमित्रा',  # Low-utility mythological figure (freq 3)
        'अरुंधती',  # Low-utility mythological star/figure (freq 3)
        'छीना',     # Past-tense inflected form of छीनना
        'पहचाना'    # Past-tense inflected form of पहचानना
    }

    # POS fixes for remaining anomalies
    pos_fixes = {
        'काना': 'one-eyed / squint-eyed (adj.)',
        'बजाए': 'instead of / in place of (postp., prep.)'
    }

    cleaned = []
    removed_count = 0
    for item in data:
        if item['hi'] in prune_words:
            removed_count += 1
            continue

        if item['hi'] in pos_fixes:
            item['en'] = pos_fixes[item['hi']]

        cleaned.append(item)

    # Sort strictly by frequency descending
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index IDs sequentially 1 to len(cleaned)
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Polishing complete! Removed {removed_count} redundant entries. Final high-impact word count: {len(cleaned)}.")

if __name__ == '__main__':
    polish_vocab()
