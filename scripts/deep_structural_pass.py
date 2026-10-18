#!/usr/bin/env python3
"""
Deep Structural & Linguistic Refinement Pass for vocab.json.

This pass targets the remaining structural redundancies:
1. Bare Verb Roots / Stem Duplicates:
   - 'देख' (intimate imperative of देखना)
   - 'चला' (past/stem of चलना)
   - 'कह' (intimate imperative of कहना)
   - 'बना' (past of बनना)
   - 'गा' (intimate imperative of गाना)
   - 'लिख' (intimate imperative of लिखना)
   - 'हँस' (intimate imperative of हँसना)
   - 'गिरा' (past of गिरना)
   - 'मिलेगा' (future indicative of मिलना)
   All base verbs (देखना, चलना, कहना, बनना, गाना, लिखना, हँसना, गिरना, मिलना) are present.

2. Artificial Multi-Word & Academic Dictionary Clutter:
   - 'पूर्व इतिहास' (calqued translation for prehistory)
   - 'पुरातत्व शास्त्र' (calqued translation for archaeology)
   - 'रेत पत्थर' (calqued translation for sandstone)
   - 'कृत्रिम उपग्रह' (calqued translation for artificial satellite)
   - 'विद्युत मोटर' (calqued translation for electric motor)
   - 'पूर्ण संख्या' (calqued translation for integer)
   - 'बीज गणित' (calqued translation for algebra)
   - 'कलन शास्त्र' (calqued translation for calculus)
   - 'रसायनिक प्रक्रिया' (calqued translation for chemical reaction)
   - 'आम तौर से' (duplicate of आम तौर पर)
   - 'बड़ा दिन' (archaic/calqued term for Christmas)

3. Non-Essential Proper Nouns & Redundant Geography:
   - 'काशी' (redundant duplicate of वाराणसी)
   - 'जम्मू' (redundant with जम्मू और कश्मीर)
   - 'ताज महल'
   - 'आकाश गंगा'
   - 'क्रिसमस'
   - 'क़ुरान'
   - 'बाइबिल'
   - 'ईसाई धर्म'
   - 'इस्लाम'
   - 'पाकिस्तान'
   - 'बांग्लादेश'
   - 'श्रीलंका'
   - 'सिक्किम'
   - 'उड़ीसा'
   - 'आसाम'
   - 'कर्नाटक'
   - 'गोवा'
   - 'मध्य प्रदेश'
   - 'चंडीगढ़'
   - 'भोपाल'
   - 'पटना'
   - 'जयपुर'
   - 'लखनऊ'
   - 'हैदराबाद'
   - 'चेन्नई'
   - 'कोलकाता'
   - 'बेंगलुरु'
   - 'कावेरी'
   - 'सरस्वती'

4. Definition Cleanups for Single-Letter Particles / Interjections:
   - 'आ': 'come [intimate imperative of आना] (v.)'
   - 'ऐ': 'hey / O [vocative interjection] (interj.)'
   - 'ओ': 'oh / hey [interjection] (interj.)'
   - 'व': 'and [formal / literary connective] (conj.)'
"""

import json

def apply_refinement_pass():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Prune list
    prune_set = {
        # Bare Verb Roots / Inflections
        'देख', 'चला', 'कह', 'बना', 'गा', 'लिख', 'हँस', 'गिरा', 'मिलेगा',

        # Academic / Artificial compounds
        'पूर्व इतिहास', 'पुरातत्व शास्त्र', 'रेत पत्थर', 'कृत्रिम उपग्रह', 'विद्युत मोटर',
        'पूर्ण संख्या', 'बीज गणित', 'कलन शास्त्र', 'रसायनिक प्रक्रिया', 'आम तौर से', 'बड़ा दिन',

        # Proper Nouns & Geography clutter
        'काशी', 'जम्मू', 'ताज महल', 'आकाश गंगा', 'क्रिसमस', 'क़ुरान', 'बाइबिल', 'ईसाई धर्म', 'इस्लाम',
        'पाकिस्तान', 'बांग्लादेश', 'श्रीलंका', 'सिक्किम', 'उड़ीसा', 'आसाम', 'कर्नाटक', 'गोवा', 'मध्य प्रदेश',
        'चंडीगढ़', 'भोपाल', 'पटना', 'जयपुर', 'लखनऊ', 'हैदराबाद', 'चेन्नई', 'कोलकाता', 'बेंगलुरु', 'कावेरी', 'सरस्वती'
    }

    # 2. Definition cleanups
    cleanups = {
        'आ': {'en': 'come [stem / intimate imperative of आना] (v.)'},
        'ऐ': {'en': 'hey / O [vocative particle] (interj.)'},
        'ओ': {'en': 'oh / hey [interjection] (interj.)'},
        'व': {'en': 'and [formal / literary connective] (conj.)'}
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

    # Re-index sequentially 1 to len(cleaned)
    for idx, item in enumerate(cleaned, start=1):
        item['id'] = idx

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("DEEP STRUCTURAL REFINEMENT PASS REPORT")
    print("=" * 60)
    print(f"Total input entries       : {len(data)}")
    print(f"Total entries pruned      : {len(pruned_items)}")
    print(f"Total optimized entries   : {len(cleaned)}")
    print(f"Definitions cleaned       : {len(cleanups)}")
    print("=" * 60)
    print("\nSummary of Pruned Categories:")
    print(f"  - Verb Stems / Inflections : 9")
    print(f"  - Calqued Multi-words      : 11")
    print(f"  - Proper Names / Regional  : 29")
    print("=" * 60)

if __name__ == '__main__':
    apply_refinement_pass()
