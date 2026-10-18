#!/usr/bin/env python3
"""
Applies comprehensive multi-perspective improvements to vocab.json:
1. Merges Nuqta variants:
   - Preserves authoritative spelling with standard nuqta (e.g. साफ़, ज़मीन, बाज़ार, ख़ून, क़ानून)
   - Consolidates frequencies (adds frequency from the variant)
   - Removes the duplicate un-nuqta'd or redundant variant
2. Removes redundant inflected forms:
   - Oblique adjectives (छोटे, नए, पुराने, काले, बड़े...)
   - Oblique infinitives (करने, जाने, होने, देखने...)
   - Polite imperatives (कीजिए, आइए, देखिए, जाइए)
3. Removes explicit misspellings (मानना misspelling 'माना', शुरू misspelling 'शुरु', etc.)
4. Removes foreign / remote geographical entries
5. Fixes POS tags on non-verbs mistakenly tagged as (v.)
6. Cleans wikitext / dictionary artifacts
7. Sequentially re-indexes all entries from ID 1 to N
"""

import json
import shutil

def apply_deep_cleaning():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('scripts/deep_audit_report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)

    # 1. Nuqta merges
    remove_ids = set()
    freq_additions = {} # primary_id -> additional freq

    for group in report['nuqta_merges']:
        primary = group['primary']
        p_id = primary['id']
        add_freq = 0
        for oth in group['others']:
            remove_ids.add(oth['id'])
            add_freq += oth.get('freq', 0)
        freq_additions[p_id] = freq_additions.get(p_id, 0) + add_freq

    # 2. Inflected adjectives
    for item in report['infl_adj_to_remove']:
        remove_ids.add(item['id'])

    # 3. Oblique verbs
    for item in report['oblique_verbs_to_remove']:
        remove_ids.add(item['id'])

    # 4. Polite imperatives
    for item in report['polite_imperatives_to_remove']:
        remove_ids.add(item['id'])

    # 5. Misspellings
    for item in report['misspellings_to_remove']:
        remove_ids.add(item['id'])

    # 6. Foreign geography
    for item in report['foreign_to_remove']:
        remove_ids.add(item['id'])

    pos_fixes = report['pos_fixes']
    residue_cleanups = report['residue_cleanups']

    print(f"Total entries marked for removal: {len(remove_ids)}")

    cleaned = []
    for item in data:
        if item['id'] in remove_ids:
            continue

        # Add consolidated frequency if primary
        if item['id'] in freq_additions:
            item['freq'] += freq_additions[item['id']]

        # Apply POS fixes
        if item['hi'] in pos_fixes:
            item['en'] = pos_fixes[item['hi']]

        # Apply residue cleanups
        if item['hi'] in residue_cleanups:
            item['en'] = residue_cleanups[item['hi']]

        cleaned.append(item)

    # Sort cleaned vocabulary by frequency descending (standard frequency dictionary order)
    # or keep existing order? In vocab.json, items were sorted by freq descending initially.
    # Sorting by freq descending makes the vocabulary list strictly frequency-ordered!
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially from 1 to len(cleaned)
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    # Save to vocab.json
    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Cleaning complete! Saved {len(cleaned)} high-quality entries to vocab.json.")

if __name__ == '__main__':
    apply_deep_cleaning()
