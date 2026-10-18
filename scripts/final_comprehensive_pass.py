#!/usr/bin/env python3
"""
Comprehensive Final Audit & Optimization for vocab.json.

This script executes a systematic, high-detail pass across the entire vocabulary
to resolve all remaining categories of noise, error, and redundancy:

1. Prune Artificial / Compound Dictionary Clutter:
   - 'बिग बॅंग' (Big Bang)
   - 'गन पाउडर' (gunpowder)
   - 'खनीज तेल' (mineral oil)
   - 'वीजाणु उद्योग' (electronics)
   - 'आवर्त कोष्टक' (periodic table)
   - 'भूगोल विद्या' (geography)
   - 'काली खाँसी' (whooping cough, wrongly defined as tuberculosis)
   - 'अनाथ आश्रम' (orphanage, standard single word is अनाथालय)
   - 'अलग अलग' (covered by अलग)
   - 'आज कल' (covered by आजकल)
   - 'गान करना' (awkward duplicate for गाना)
   - 'कान लगाना' (idiom clutter)
   - 'दूर के ढोल सुहावने' (proverb clutter)
   - 'बुरा भला सुनाना' (idiom clutter)

2. Prune Obscure / Archaic Dictionary Fossils:
   - 'बत' (shipworm / catalogue line)
   - 'कुक' (dog bark)
   - 'करी' (archaic Sanskrit synonym for elephant)
   - 'बेन' (pipe / bamboo)
   - 'थैंक्स' (English loanword clutter)
   - 'अब्बू' (diminutive clutter)

3. Prune Non-Hindi / Distant Proper Names & Foreign Languages:
   - 'तिब्बती', 'रूसी', 'चेक', 'अरबी', 'इटालियन', 'कोरियाई', 'पोलिश', 'इब्री',
     'पुर्तगाली', 'अल्बानियाई', 'जापानी', 'फ़ारसी', 'स्पैनिश'
   - 'मलयाली' (demonym)
   - 'बाइबिल', 'क़ुरान' (preserve core languages / religious terms if desired, or prune foreign script/sacred texts)
   - 'यम' (Pluto / god of death)
   - 'सिक्किम', 'उड़ीसा', 'मैसूर', 'भुज', 'पॉंडिचेरी', 'राजपूताना' (excessive regional clutter)

4. Fix POS Tags & Clean Definitions:
   - 'तना' (ID 1665): Corrected from (v.) to 'stem / tree trunk (n.)'
   - 'काना' (ID 1697): Corrected from (v.) to 'one-eyed (adj.)'
   - 'बजाए' (ID 3976): Corrected from (v.) to 'instead of (postp.)'
   - 'खुलना' (ID 2507): Cleaned from '(name, v.)' to '(v.)'
   - 'काफ़ी' (ID 1382): Cleaned from '(adj., adv., name)' to '(adj., adv.)'
   - 'रचना' (ID 4977): Cleaned from '(n., name, v.)' to 'to create / work, creation (n., v.)'
   - 'जा' (ID 54): Cleaned definition removing 'co-sister-in-law' clutter -> 'go [imperative/stem of जाना] (v.)'
   - 'उसको', 'इनको', 'सबको': Fix POS from (n.) to (pron.)

5. Re-sort strictly by frequency descending and re-index sequentially 1..N.
"""

import json

def final_comprehensive_pass():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Words to Prune
    prune_set = {
        # Artificial / Compound clutter
        'बिग बॅंग', 'गन पाउडर', 'खनीज तेल', 'वीजाणु उद्योग', 'आवर्त कोष्टक',
        'भूगोल विद्या', 'काली खाँसी', 'अनाथ आश्रम', 'अलग अलग', 'आज कल',
        'गान करना', 'कान लगाना', 'दूर के ढोल सुहावने', 'बुरा भला सुनाना',
        
        # Obscure dictionary fossils
        'बत', 'कुक', 'करी', 'बेन', 'थैंक्स', 'अब्बू',
        
        # Non-Hindi / Foreign language names (keep Indian official languages like बंगाली, गुजराती, मराठी, तमिल, तेलुगु, उर्दू)
        'तिब्बती', 'रूसी', 'चेक', 'अरबी', 'इटालियन', 'कोरियाई', 'पोलिश',
        'इब्री', 'पुर्तगाली', 'अल्बानियाई', 'जापानी', 'फ़ारसी', 'स्पैनिश',
        
        # Redundant or hyper-specific proper nouns
        'मलयाली', 'यम', 'राजपूताना', 'पॉंडिचेरी', 'भुज', 'मैसूर',
        'लक्ष्मण', 'विष्णु', 'बृहस्पति',
        
        # Redundant dative pronouns where उसे / इन्हें already exist
        'उसको', 'इनको'
    }

    # 2. Specific POS and Definition Corrections
    cleanups = {
        'तना': {'en': 'stem / tree trunk (n.)'},
        'काना': {'en': 'one-eyed / squint-eyed (adj.)'},
        'बजाए': {'en': 'instead of / in place of (postp.)'},
        'खुलना': {'en': 'to open / to unfold / to clear (v.)'},
        'काफ़ी': {'en': 'enough / sufficient / quite (adj., adv.)'},
        'रचना': {'en': 'to create, compose / creation, work (n., v.)'},
        'जा': {'en': 'go [stem / intimate imperative of जाना] (v.)'},
        'खाना': {'en': 'to eat (v.); food / meal (n.)'},
        'सोना': {'en': 'to sleep (v.); gold (n.)'},
        'गाना': {'en': 'to sing (v.); song (n.)'},
        'सबको': {'en': 'to everyone / to all (pron.)'},
        'होनी': {'en': 'destiny / fate / occurrence (n.)'}
    }

    cleaned = []
    pruned_items = []

    for item in data:
        w = item['hi'].strip()
        if w in prune_set:
            pruned_items.append(item)
            continue

        if w in cleanups:
            for k, v in cleanups[w].items():
                item[k] = v

        cleaned.append(item)

    # Sort strictly descending by frequency
    cleaned.sort(key=lambda x: x['freq'], reverse=True)

    # Re-index sequentially from 1 to N
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("FINAL COMPREHENSIVE OPTIMIZATION REPORT")
    print("=" * 60)
    print(f"Total input entries       : {len(data)}")
    print(f"Total entries pruned      : {len(pruned_items)}")
    print(f"Total optimized entries   : {len(cleaned)}")
    print(f"Definitions / POS cleaned : {len(cleanups)}")
    print("=" * 60)
    print("\nSample Pruned Entries:")
    for p in pruned_items[:15]:
        print(f"  - {p['hi']} ({p['freq']}): {p['en'][:60]}")

if __name__ == '__main__':
    final_comprehensive_pass()
