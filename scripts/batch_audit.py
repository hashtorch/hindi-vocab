#!/usr/bin/env python3
"""
Batch-by-batch deep analyzer for vocab.json to evaluate usefulness and effectiveness
for Hindi learners seeking proficiency.

Batches:
Batch 1: IDs 1 - 1000     (Core Spoken & Foundational, Freq >= 100)
Batch 2: IDs 1001 - 2000 (Daily Conversational & Common Topics, Freq 40-99)
Batch 3: IDs 2001 - 3000 (Intermediate & Practical Life, Freq 18-39)
Batch 4: IDs 3001 - 4000 (Upper Intermediate & Domain Terms, Freq 11-17)
Batch 5: IDs 4001 - 5000 (Advanced & Broad Vocabulary, Freq 5-10)
Batch 6: IDs 5001 - 5648 (Niche, Low-Frequency & Long-tail, Freq 1-4)
"""

import json
import re

with open('vocab.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

batches = [
    ("Batch 1 (IDs 1-1000)", data[:1000]),
    ("Batch 2 (IDs 1001-2000)", data[1000:2000]),
    ("Batch 3 (IDs 2001-3000)", data[2000:3000]),
    ("Batch 4 (IDs 3001-4000)", data[3001:4000]),
    ("Batch 5 (IDs 4001-5000)", data[4001:5000]),
    ("Batch 6 (IDs 5001-5648)", data[5001:]),
]

# Patterns for dubious / non-effective entries:
# 1. Obscure mythology / hyper-specific script names / ancient figures
# 2. Transliterated western acronyms or foreign jargon
# 3. Rare dialectal or dictionary clutter
suspicious_patterns = [
    r'\bscript\b', r'\bdwarf planet\b', r'\bconstellation\b', r'\bwife of\b',
    r'\bson of\b', r'\bpreceptor\b', r'\bancient prophet\b', r'\bsupercluster\b',
    r'\bwharf\b', r'\bwarp\b', r'\bindefatigable\b', r'\bsoothsayer\b',
    r'\bincantation\b', r'\bexclaven\b', r'\bmonastery\b'
]

print("=" * 60)
print("BATCH-BY-BATCH PROFICIENCY AUDIT REPORT")
print("=" * 60)

for name, batch in batches:
    print(f"\n--- {name} (Total: {len(batch)} words) ---")
    freqs = [x['freq'] for x in batch]
    print(f"Frequency range: {min(freqs)} to {max(freqs)}")
    
    # Check proper nouns
    proper_nouns = [x for x in batch if '(name' in x.get('en', '') or '(prop.n' in x.get('en', '')]
    print(f"Proper names count: {len(proper_nouns)}")
    
    # Check suspicious / low utility flags
    flagged = []
    for x in batch:
        en = x.get('en', '').lower()
        for p in suspicious_patterns:
            if re.search(p, en):
                flagged.append((x, p))
                break
                
    print(f"Flagged for learner utility review: {len(flagged)}")
    if flagged:
        for it, p in flagged[:6]:
            print(f"   [{it['id']}] {it['hi']} ({it['freq']}) -> {it['en'][:70]}")
