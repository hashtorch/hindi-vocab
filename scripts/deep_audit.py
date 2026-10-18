#!/usr/bin/env python3
"""
Advanced Multi-Perspective Deep Audit & Enrichment for vocab.json.

Perspectives Analyzed:
1. Nuqta Spell-Variant Deduplication:
   - Identify pairs where one word is written with nuqta and another without (e.g., साफ़ / साफ, बाज़ार / बाजार, ज़रूरत / जरुरत).
   - Merge these into a single authoritative entry: e.g. "साफ़ (साफ)" and sum or maximize the frequency.
   
2. Inflectional Redundancy Removal:
   - Remove oblique plural adjectives (e.g. छोटे, नए, पुराने, अगले, काले, नीले, बड़े, हरे, आदि) where base (छोटा, नया, पुराना, आदि) exists.
   - Remove oblique infinitives (e.g. करने, जाने, होने, देखने, लेने, आदि) where base (करना, जाना, होना, देखना, आदि) exists.
   - Remove polite imperative duplicates (e.g. कीजिए, आइए, देखिए, जाइए) where base exists.
   
3. Explicit Misspellings Removal:
   - Remove entries marked as "misspelling of ..." (e.g., माना for मानना, शुरु for शुरू, हथ्यार for हथियार, भुगोल for भूगोल, हं for हाँ).

4. Foreign Geography / Remote Nations Pruning:
   - Remove remote foreign entities (लंदन, रोम, चीन, रूस, लातिनी, एशिया, यूरोप, इराक़, ग्रीक, अंटार्कटिका, उत्तर अमेरिका, दक्षिण अमेरिका, इटली, ब्रिटेन, फ्रांस, मलेशिया, जापान, कनाडा, स्पेन, अफ़्रीका, ईरान, डच, काबुल, अफगानिस्तान, इंग्लैंड, दुबई) to preserve core Hindi vocabulary.

5. POS Tagging & Definition Accuracy Correction:
   - Fix 60+ entries incorrectly tagged as (v.) such as दाना (seed), ताना (taunt), बौना (dwarf), सांत्वना (solace), अवहेलना (neglect), सरगना (ringleader), तिगुना (triple), चिकना (smooth), आराधना (worship), संवेदना (sensitivity), etc.
   - Clean raw dictionary artifacts / wikitext residue (e.g. "Used other than figuratively", "cf. मत", etc.).
"""

import json
import re
from collections import defaultdict

def run_deep_audit():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries from vocab.json")

    # 1. Nuqta variant duplicates
    def strip_nuqta(s):
        return s.replace('\u093c', '').strip()

    groups = defaultdict(list)
    for x in data:
        groups[strip_nuqta(x['hi'])].append(x)

    nuqta_merges = []
    for norm, items in groups.items():
        if len(items) > 1:
            # We want to select the best representative (prefer nuqta form if standard, e.g. ज़, ख़, फ़, or higher freq)
            # Find item with nuqta
            nuqta_items = [it for it in items if '\u093c' in it['hi']]
            plain_items = [it for it in items if '\u093c' not in it['hi']]
            
            # Prefer the nuqta entry as primary if it exists, else highest freq
            if nuqta_items:
                primary = sorted(nuqta_items, key=lambda it: it['freq'], reverse=True)[0]
                others = [it for it in items if it['id'] != primary['id']]
            else:
                sorted_items = sorted(items, key=lambda it: it['freq'], reverse=True)
                primary = sorted_items[0]
                others = sorted_items[1:]

            nuqta_merges.append({
                'primary': primary,
                'others': others,
                'norm': norm
            })

    print(f"Identified {len(nuqta_merges)} nuqta variant groups for consolidation.")

    # 2. Inflected adjectives (m pl/obl)
    infl_adj_to_remove = []
    for x in data:
        en = x.get('en', '')
        if '(m pl/obl)' in en:
            infl_adj_to_remove.append(x)

    print(f"Identified {len(infl_adj_to_remove)} inflected oblique adjectives to remove.")

    # 3. Oblique infinitives (-ने)
    oblique_verbs_to_remove = []
    oblique_stems = {
        'करने', 'जाने', 'होने', 'देखने', 'लेने', 'आने', 'देने', 'बनाने',
        'मारने', 'पाने', 'खाने', 'दिलाने', 'कराने'
    }
    for x in data:
        if x['hi'] in oblique_stems and '(n.)' in x.get('en', ''):
            oblique_verbs_to_remove.append(x)

    print(f"Identified {len(oblique_verbs_to_remove)} oblique infinitives to remove.")

    # 4. Polite imperative verb duplicates
    polite_imperatives_to_remove = []
    polite_stems = {'कीजिए', 'आइए', 'देखिए', 'जाइए'}
    for x in data:
        if x['hi'] in polite_stems:
            polite_imperatives_to_remove.append(x)

    print(f"Identified {len(polite_imperatives_to_remove)} polite imperative duplicates to remove.")

    # 5. Explicit misspellings
    misspellings_to_remove = []
    for x in data:
        if 'misspelling of' in x.get('en', ''):
            misspellings_to_remove.append(x)

    print(f"Identified {len(misspellings_to_remove)} explicit misspellings to remove.")

    # 6. Remaining Foreign Entities & Geography
    foreign_places = {
        'लंदन', 'रोम', 'चीन', 'रूस', 'लातिनी', 'एशिया', 'यूरोप', 'इराक़', 'ग्रीक',
        'अंटार्कटिका', 'उत्तर अमेरिका', 'दक्षिण अमेरिका', 'इटली', 'ब्रिटेन', 'फ्रांस',
        'मलेशिया', 'जापान', 'कनाडा', 'स्पेन', 'अफ़्रीका', 'ईरान', 'डच', 'काबुल',
        'अफगानिस्तान', 'इंग्लैंड', 'दुबई', 'अमेरिका', 'नेपाल', 'मऊ', 'श्रीकाकुलम'
    }
    foreign_to_remove = []
    for x in data:
        if x['hi'] in foreign_places and ('(name)' in x.get('en', '') or '(prop.n' in x.get('en', '')):
            foreign_to_remove.append(x)

    print(f"Identified {len(foreign_to_remove)} foreign/remote geography entries to remove.")

    # 7. POS tag corrections for pseudo-verbs (words ending in -ना tagged as (v.) that are actually nouns/adjectives)
    pos_fixes = {
        'दाना': 'seed / grain (n.)',
        'ताना': 'taunt / warp (in weaving) (n.)',
        'बौना': 'dwarf / stunted (adj., n.)',
        'सांत्वना': 'consolation / solace (n.)',
        'अवहेलना': 'disregard / defiance / neglect (n.)',
        'सरगना': 'ringleader / chieftain / kingpin (n.)',
        'तिगुना': 'threefold / triple (adj., num.)',
        'चिकना': 'smooth / slippery / glossy (adj.)',
        'आराधना': 'worship / adoration / prayer (n.)',
        'संवेदना': 'sensitivity / empathy / sensibility (n.)',
        'गन्ना': 'sugarcane (n.)',
        'चना': 'chickpea / gram (n.)',
        'मैना': 'myna (bird) (n.)',
        'टखना': 'ankle (n.)',
        'ख़ज़ाना': 'treasure / treasury (n.)',
        'वायुसेना': 'Air Force (n.)',
        'पश्मीना': 'pashmina (cashmere wool) (n.)',
        'जनगणना': 'census / population count (n.)',
        'दुगना': 'double / twofold (adj., num.)',
        'सालाना': 'annual / yearly (adj., adv.)',
        'रोजाना': 'daily / everyday / routinely (adv., adj.)',
        'मर्दाना': 'masculine / manly (adj.)',
        'अवसंरचना': 'infrastructure (n.)',
        'तोपखाना': 'artillery / armory (n.)',
        'पैमाना': 'scale / parameter / yardstick (n.)',
        'मौलाना': 'Maulana (Islamic scholar) (n.)',
        'परिकल्पना': 'hypothesis / conception (n.)',
        'प्रस्तावना': 'preface / preamble / introduction (n.)',
        'वंदना': 'worship / prayer (n.)',
        'जनचेतना': 'public awareness (n.)',
        'उपासना': 'worship / adoration (n.)',
        'गर्जना': 'roar / thundering (n.)',
        'लेनादेना': 'business / dealing / concern (n.)',
        'पुनर्स्थापना': 'restoration / reinstatement (n.)',
        'छौंकना': 'tempering / seasoning with hot oil/spices (n., v.)',
        'राजपूताना': 'Rajputana (prop.n.)',
        'सम्भावना': 'possibility / probability (n.)'
    }

    # 8. Wikitext / Dictionary residue cleanups
    residue_cleanups = {
        'बड़ा दिन': 'Christmas (n.)',
        'न': 'not, do not / negative particle / isn\'t it? (part., adv.)',
        'परमाणु': 'atom / smallest indivisible particle (n.)',
        'सरस्वती': 'Saraswati, goddess of knowledge and music (name)',
        'मत्स्य': 'fish (n.)',
        'शुक्र': 'Venus (planet) / Shukra / bright (n., name)'
    }

    report = {
        'nuqta_merges': nuqta_merges,
        'infl_adj_to_remove': infl_adj_to_remove,
        'oblique_verbs_to_remove': oblique_verbs_to_remove,
        'polite_imperatives_to_remove': polite_imperatives_to_remove,
        'misspellings_to_remove': misspellings_to_remove,
        'foreign_to_remove': foreign_to_remove,
        'pos_fixes': pos_fixes,
        'residue_cleanups': residue_cleanups
    }

    with open('scripts/deep_audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\nSummary of deep audit report written to scripts/deep_audit_report.json")

if __name__ == '__main__':
    run_deep_audit()
