#!/usr/bin/env python3
import json
import re
from collections import Counter

def analyze():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total entries: {len(data)}")

    # 1. Duplicates check
    hi_words = [x.get('hi', '').strip() for x in data]
    counts = Counter(hi_words)
    duplicates = {k: v for k, v in counts.items() if v > 1}
    print(f"\n1. Duplicate Hindi words count: {len(duplicates)}")
    if duplicates:
        print("Sample duplicates:", list(duplicates.items())[:10])

    # 2. English transliterations / English loan words that are pure English or jargon
    # e.g., 'इंटरनेट', 'कंप्यूटर', or English script
    has_english_script = [x for x in data if re.search(r'[a-zA-Z]', x.get('hi', ''))]
    print(f"\n2. Entries with English script in 'hi': {len(has_english_script)}")
    for x in has_english_script[:10]:
        print("  ", x)

    # 3. Punctuation, symbols, numbers in 'hi'
    has_symbols = [x for x in data if re.search(r'[0-9०-९\-_/\\.,;:!?@#$%^&*()=+~`"\'<>{}\[\]|]', x.get('hi', ''))]
    print(f"\n3. Entries with punctuation/numbers/symbols in 'hi': {len(has_symbols)}")
    for x in has_symbols[:15]:
        print("  ", x)

    # 4. Word length analysis
    one_char = [x for x in data if len(x.get('hi', '').strip()) == 1]
    print(f"\n4. Single character entries: {len(one_char)}")
    for x in one_char[:15]:
        print("  ", x)

    # 5. Grammatical particles / inflections / duplicated stems
    # Check parts of speech in 'en'
    pos_tags = Counter()
    for x in data:
        en = x.get('en', '')
        tags = re.findall(r'\(([a-zA-Z\.\s/]+)\)', en)
        for t in tags:
            pos_tags[t.strip()] += 1
    print("\n5. Most common POS tags in 'en':")
    for tag, c in pos_tags.most_common(15):
        print(f"   {tag}: {c}")

    # 6. Look for transliterated English names/places or English technical terms
    # e.g., names of foreign cities/countries or modern English transliterations
    # Check frequency distribution
    freqs = [x.get('freq', 0) for x in data]
    print(f"\n6. Frequency stats: min={min(freqs)}, max={max(freqs)}, median={sorted(freqs)[len(freqs)//2]}")
    freq_1 = [x for x in data if x.get('freq', 0) == 1]
    print(f"   Entries with freq == 1: {len(freq_1)}")
    freq_under_5 = [x for x in data if x.get('freq', 0) < 5]
    print(f"   Entries with freq < 5: {len(freq_under_5)}")

if __name__ == '__main__':
    analyze()
