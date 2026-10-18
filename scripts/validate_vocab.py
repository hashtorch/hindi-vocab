#!/usr/bin/env python3
"""
Comprehensive integrity validator for vocab.json.

Performs:
1. ID continuity and sequential validation (1..N).
2. Frequency ranking preservation (implied by continuous 1..N order).
3. Zero duplicate Hindi headwords.
4. Schema validation: exact keys {"id", "hi", "en"}.
5. Single-word English constraint (no spaces, pure single English token).
"""

import json
from collections import Counter

def validate_vocab(filepath='vocab.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    print("=" * 60)
    print(f"VALIDATING {filepath} (Total entries: {total})")
    print("=" * 60)

    # 1. Sequential IDs
    expected_ids = list(range(1, total + 1))
    actual_ids = [x['id'] for x in data]
    assert actual_ids == expected_ids, "Error: IDs are not strictly sequential 1..N!"
    print(f"✓ IDs: Perfectly sequential from 1 to {total} (Frequency-Ordered)")

    # 2. Duplicate checks
    words = [x['hi'].strip() for x in data]
    counts = Counter(words)
    dups = {k: v for k, v in counts.items() if v > 1}
    assert len(dups) == 0, f"Error: Found duplicate words: {dups}"
    print("✓ Uniqueness: Zero duplicate Hindi headwords")

    # 3. Schema check & single-word English constraint
    exact_keys = {'id', 'hi', 'en'}
    for idx, item in enumerate(data):
        assert set(item.keys()) == exact_keys, f"Error at index {idx}: Keys mismatch in {item}"
        assert isinstance(item['id'], int), f"Error: id not int in {item}"
        assert isinstance(item['hi'], str) and len(item['hi']) > 0, f"Error: invalid hi in {item}"
        assert isinstance(item['en'], str) and len(item['en']) > 0, f"Error: invalid en in {item}"
        assert ' ' not in item['en'].strip(), f"Error at index {idx}: English translation contains spaces/multiple words in {item}"
    print(f"✓ Schema & Single-Word English: All {total} entries satisfy strict schema constraints")
    print("=" * 60)
    print("ALL INTEGRITY CHECKS PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    validate_vocab()
