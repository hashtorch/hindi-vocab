#!/usr/bin/env python3
"""
Applies improvements to vocab.json:
- Removes duplicate entries (keeping the one with higher frequency & richer definition)
- Removes pure alphabet character letters (Devanagari vowels/consonants/ligatures)
- Removes distant foreign proper nouns and foreign brands (leaving core Hindi/Indian cultural geography)
- Removes obscure/archaic/crude entries
- Fixes critical definition errors (e.g. 'सकता' and 'दे')
- Re-indexes IDs sequentially from 1 to N
- Optionally creates a backup (vocab.json.bak)
"""

import json
import sys
import shutil

def clean_and_improve(input_file='vocab.json', output_file='vocab.json', backup=True):
    if backup:
        shutil.copyfile(input_file, input_file + '.bak')
        print(f"Created backup at {input_file}.bak")

    # Load audit report
    try:
        with open('scripts/full_audit_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
    except FileNotFoundError:
        import generate_audit_report
        generate_audit_report.run_audit()
        with open('scripts/full_audit_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    remove_ids = set()
    for item in report['exact_duplicates']:
        remove_ids.add(item['id'])
    for item in report['alphabet_entries']:
        remove_ids.add(item['id'])
    for item in report['foreign_proper_names']:
        remove_ids.add(item['id'])
    for item in report['obscure_words']:
        remove_ids.add(item['id'])

    # Definition fixes map
    fixes = {f['id']: f['recommended_en'] for f in report['definition_errors']}

    cleaned = []
    for item in data:
        if item['id'] in remove_ids:
            continue
        # Apply definition fix if applicable
        if item['id'] in fixes:
            item['en'] = fixes[item['id']]
        cleaned.append(item)

    # Re-index IDs sequentially
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"Successfully processed {input_file}:")
    print(f"Original entries : {len(data)}")
    print(f"Removed entries  : {len(remove_ids)}")
    print(f"Cleaned entries  : {len(cleaned)}")
    print(f"Saved to         : {output_file}")

if __name__ == '__main__':
    clean_and_improve()
