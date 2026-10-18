#!/usr/bin/env python3
"""
Prunes the 65 identified verbal oblique infinitives (-ने) and participle entries:
- 64 Verbal oblique infinitives (रहने, रखने, मिलने, कहने, बताने, etc.) whose base infinitives exist.
- 1 Participle duplicate (पहने -> पहनना).

Legitimate nouns and adverbs ending in -ने (सामने, दाहिने, सपने, गहने, घुटने, दस्ताने, इतने, कितने, आदि) are strictly preserved.
Sorts strictly descending by frequency and re-indexes sequentially from 1 to N.
"""

import json

def prune_oblique_infinitives():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Legitimate non-verb nouns/adverbs/pronouns ending in -ने to preserve:
    preserve_set = {
        'सामने', 'इतने', 'कितने', 'सपने', 'गहने', 'घुटने', 'तहखाने', 'कारखाने',
        'कोने', 'पैमाने', 'ठिकाने', 'दाहिने', 'सीने', 'माने', 'मायने', 'किसने',
        'इसने', 'जिसने', 'उन्होंने', 'आपने', 'तुमने', 'हमने', 'मैंने', 'ने'
    }

    # Identify verbal -ने entries whose base infinitive ends in -ना:
    v_words = {x['hi'] for x in data}
    v_norm = {x['hi'].replace('\u093c', '') for x in data}

    drop_set = set()
    for x in data:
        hi = x['hi'].strip()
        if hi.endswith('ने') and hi not in preserve_set and len(hi) > 2:
            inf = hi[:-1] + 'ा'
            inf_norm = inf.replace('\u093c', '')
            if inf in v_words or inf_norm in v_norm:
                drop_set.add(hi)

    # Also drop inflected participle 'पहने'
    drop_set.add('पहने')

    print(f"Total entries targeted for pruning: {len(drop_set)}")

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
    print("OBLIQUE INFINITIVE PRUNING COMPLETED")
    print("=" * 60)
    print(f"Original entries count  : {len(data)}")
    print(f"Entries pruned          : {pruned_count}")
    print(f"Cleaned entries count   : {len(cleaned)}")
    print("=" * 60)

if __name__ == '__main__':
    prune_oblique_infinitives()
