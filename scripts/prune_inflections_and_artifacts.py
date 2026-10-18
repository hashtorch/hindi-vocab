#!/usr/bin/env python3
"""
Prunes the 47 identified redundant, inflected, and illogical frequency artifact entries from vocab.json:
- 23 Inflected familiar imperatives (करो, चलो, देखो, etc.)
- 9 Oblique verbal infinitives (सोने, पीने, जीने, etc.)
- 5 Inflected plural/oblique nouns (कमरे, पैसे, लड़के, etc.)
- 4 Pronoun case duplicates (तुझे, तुमको, तूने, तुममें)
- 2 Duplicate feminine adjectives (हरी, चिकनी)
- 4 Illogical frequency artifacts (सालना, भ्रातृ, पितृ, हिजड़ा)

Sorts strictly descending by frequency and re-indexes sequentially from 1 to N.
"""

import json

def apply_pruning():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    drop_set = {
        # 1. Inflected familiar imperatives
        'करो', 'चलो', 'देखो', 'लो', 'रहो', 'सुनो', 'रखो', 'कहो', 'बैठो', 'बोलो',
        'खोलो', 'बनो', 'मिलो', 'समझो', 'खेलो', 'डरो', 'छोड़ो',
        'बताओ', 'बनाओ', 'उठाओ', 'खाओ', 'चलाओ', 'आओ',

        # 2. Oblique verbal infinitives
        'सोने', 'पीने', 'जीने', 'बेचने', 'छूने', 'बोलने', 'गाने', 'डराने', 'डरने',

        # 3. Inflected plural/oblique nouns
        'कमरे', 'पैसे', 'लड़के', 'महीने', 'दरवाजे',

        # 4. Pronoun case inflections
        'तुझे', 'तुमको', 'तूने', 'तुममें',

        # 5. Duplicate feminine adjectives
        'हरी', 'चिकनी',

        # 6. Illogical frequency artifacts
        'सालना', 'भ्रातृ', 'पितृ', 'हिजड़ा'
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
    print("PRUNING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Original entries count  : {len(data)}")
    print(f"Entries pruned          : {pruned_count}")
    print(f"Cleaned entries count   : {len(cleaned)}")
    print("=" * 60)

if __name__ == '__main__':
    apply_pruning()
