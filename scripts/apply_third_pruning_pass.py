#!/usr/bin/env python3
"""
Prunes the 11 identified plural nouns, irregular past plurals, and colloquial particles:
- 7 Plural nouns (सपने, कोने, कारखाने, तहखाने, घुटने, गहने, पैमाने)
- 2 Irregular past plurals (किए, दिए)
- 2 Colloquial / spurious particles (लग, पे)

Converts 3 oblique verb forms to standard dictionary infinitives:
- जगाने -> जगाना (to awaken / wake up)
- जलने -> जलना (to burn / be ablaze)
- फटने -> फटना (to burst / tear / crack)

Sorts strictly descending by frequency and re-indexes sequentially from 1 to N.
"""

import json

def apply_third_pruning_pass():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    drop_set = {
        # Plural nouns
        'सपने', 'कोने', 'कारखाने', 'तहखाने', 'घुटने', 'गहने', 'पैमाने',
        # Irregular past plurals
        'किए', 'दिए',
        # Colloquial / spurious particles
        'लग', 'पे'
    }

    infinitive_updates = {
        'जगाने': {'hi': 'जगाना', 'en': 'to awaken / to wake up / to raise (v.)'},
        'जलने': {'hi': 'जलना', 'en': 'to burn / to be ablaze / to catch fire (v.)'},
        'फटने': {'hi': 'फटना', 'en': 'to burst / to tear / to crack / to explode (v.)'}
    }

    cleaned = []
    pruned_count = 0
    updated_count = 0

    for item in data:
        w = item['hi'].strip()
        if w in drop_set:
            pruned_count += 1
            continue

        if w in infinitive_updates:
            for k, v in infinitive_updates[w].items():
                item[k] = v
            updated_count += 1

        cleaned.append(item)

    # Sort strictly descending by frequency
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially 1 to len(cleaned)
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("THIRD PRUNING & CONVERSION PASS COMPLETED")
    print("=" * 60)
    print(f"Original entries count  : {len(data)}")
    print(f"Entries pruned          : {pruned_count}")
    print(f"Entries converted to inf: {updated_count}")
    print(f"Cleaned entries count   : {len(cleaned)}")
    print("=" * 60)

if __name__ == '__main__':
    apply_third_pruning_pass()
