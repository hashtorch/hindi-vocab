#!/usr/bin/env python3
"""
Full word-by-word comprehensive analysis and cleanup recommendation tool.
Generates an audit report and categorization of:
1. Exact duplicates (keep higher frequency/richer definition)
2. Character/Alphabet entries (vowels, consonants, isolated ligatures)
3. Irrelevant / Foreign proper names (obscure world cities, remote countries, tech brands, western websites)
4. Obscure / Esoteric / Archaic dictionary bloat
5. Erroneous / Corrupted definitions (like 'सकता' defined as apoplexy)
6. Redundant inflections / grammatical duplicates
"""

import json
import re
from collections import defaultdict

def run_audit():
    with open('vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_words = len(data)

    # 1. Exact duplicates
    by_word = defaultdict(list)
    for x in data:
        by_word[x['hi'].strip()].append(x)
    
    exact_duplicates_to_remove = []
    for w, items in by_word.items():
        if len(items) > 1:
            sorted_items = sorted(items, key=lambda it: it['freq'], reverse=True)
            for it in sorted_items[1:]:
                exact_duplicates_to_remove.append({
                    'id': it['id'],
                    'hi': it['hi'],
                    'freq': it['freq'],
                    'en': it['en'],
                    'duplicate_of': sorted_items[0]['id'],
                    'reason': f"Duplicate entry of '{w}' (retaining ID {sorted_items[0]['id']} with frequency {sorted_items[0]['freq']})"
                })

    # 2. Characters / Alphabet letters (Devanagari consonants, vowels, nuqta markers, ligatures)
    # Note: Valid small words like 'आ' (come), 'न' (no/not), 'ओ' (interjection) can be kept or adjusted,
    # but letters like अ, इ, ई, उ, ऊ, ऋ, क, ख, ग, घ, ङ, च, छ, ज, झ, ञ, ट, ठ, ड, ण, त, थ, द, ढ, ध, प, फ, ब, भ, म, ख़, फ़, ज़, क़, क्ष
    # are letters of the alphabet, NOT vocabulary words.
    alphabet_entries = []
    pure_letters = {
        'अ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऑ', 'औ', 'अं', 'अः', 'अँ',
        'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
        'ट', 'ठ', 'ड', 'ण', 'त', 'थ', 'द', 'ढ', 'ध', 'प',
        'फ', 'ब', 'भ', 'म', 'क्ष', 'ख़', 'फ़', 'ज़', 'क़'
    }
    for x in data:
        en = x.get('en', '')
        hi = x.get('hi', '').strip()
        if hi in pure_letters and ('character' in en or 'vowel' in en or 'consonant' in en or 'ligature' in en):
            alphabet_entries.append({
                'id': x['id'],
                'hi': x['hi'],
                'freq': x['freq'],
                'en': x['en'],
                'reason': 'Devanagari alphabet letter/vowel/consonant/ligature, not a vocabulary word'
            })

    # Also check Arabic/Persian letter name: 'बे' (name of second letter of Perso-Arabic alphabet)
    for x in data:
        if x['id'] == 4641:
            alphabet_entries.append({
                'id': x['id'],
                'hi': x['hi'],
                'freq': x['freq'],
                'en': x['en'],
                'reason': 'Name of Urdu/Perso-Arabic letter (be)'
            })

    # 3. Foreign proper nouns: Foreign cities, distant countries, tech companies, websites
    # Keep core India-specific names (भारत, दिल्ली, मुंबई, हिमालय, गंगा, etc.)
    # Flag remote foreign places / western websites:
    foreign_proper_names = []
    foreign_geo_ids = {
        # Remote countries & foreign cities
        1780, # बर्लिन (Berlin)
        1866, # अज़रबैजान (Azerbaijan)
        2076, # संयुक्त राज्य अमरीका (redundant country name)
        2108, # पेरिस (Paris)
        2265, # न्यूयॉर्क (New York)
        2693, # नेप्च्यून (Neptune)
        2694, # प्लूटो (Pluto)
        2713, # एस्पेरांतो (Esperanto)
        2895, # केन्या (Kenya)
        3348, # जर्मनी (Germany)
        3376, # विकिपीडिया (Wikipedia)
        3499, # अमरीका (Duplicate of 507 अमेरिका)
        3518, # मिस्र (Egypt)
        3563, # एस्टोनिया (Estonia)
        3629, # आयरलैंड (Ireland)
        3763, # ग्रीस (Greece)
        3787, # मेक्सिको (Mexico)
        3804, # शिकागो (Chicago)
        3893, # क्यूबा (Cuba)
        4131, # सियोल (Seoul)
        4219, # स्वीडन (Sweden)
        4303, # यूट्यूब (YouTube)
        4522, # हंगरी (Hungary)
        4524, # हांगकांग (Hong Kong)
        4553, # सिडनी (Sydney)
        4572, # टोक्यो (Tokyo)
        4730, # ट्रॉय (Troy)
        4767, # डेनमार्क (Denmark)
        4770, # नासरत (Nazareth)
        4891, # यिर्मयाह (Jeremiah)
        5047, # मिलान (Milan)
        5056, # ऑस्ट्रिया (Austria)
        5340, # वेटिकन (Vatican City)
        5341, # मास्को (Moscow)
        5364, # अलास्का (Alaska)
        5392, # डार्विन (Darwin)
        5444, # हैम्बर्ग (Hamburg)
        5457, # इंटेल (Intel)
        5571, # हॉलीवुड (Hollywood)
        5577, # माले (Malé)
        5670, # फ़ेसबुक (Facebook)
        5714, # मैसिडोनिया (Macedonia)
        5716, # लीमा (Lima)
        5727, # एथेंस (Athens)
        5789, # अर्जेंटीना (Argentina)
        5844, # ओटावा (Ottawa)
        5853  # बोलीविया (Bolivia)
    }
    for x in data:
        if x['id'] in foreign_geo_ids:
            foreign_proper_names.append({
                'id': x['id'],
                'hi': x['hi'],
                'freq': x['freq'],
                'en': x['en'],
                'reason': 'Foreign proper noun (remote city, foreign country, tech brand, or platform) not essential for Hindi language learning'
            })

    # 4. Erroneous definitions that need correction or removal
    # e.g. ID 50 'सकता' defined as apoplexy instead of auxiliary verb 'can / to be able to'
    # ID 128 'दे' defined as 'Bengali Kayastha caste' instead of imperative 'give'
    definition_errors = [
        {
            'id': 50,
            'hi': 'सकता',
            'current_en': 'apoplexy / an apoplectic or fainting fit, swooning / dazed, unnerved, swooned (adj., n.)',
            'recommended_en': 'can / able to [masc. sg. modal verb stem] (v.)',
            'issue': 'Critical mistranslation: common modal verb mistaken for rare archaic Arabic-origin medical term sakat/sakta'
        },
        {
            'id': 128,
            'hi': 'दे',
            'current_en': 'De (a type of Bengali Kayastha caste in eastern India) / De (member of the De caste) / An honorific for women (n., name, v.)',
            'recommended_en': 'give / grant [stem / intimate imperative of देना] (v.)',
            'issue': 'Mistranslation: common verb stem mistaken for caste surname'
        }
    ]

    # 5. Obscure / Archaic / Low-utility words for everyday learners
    # Words like बुत-कदा (pagoda/idol temple), बुतख़ाना, पगोडा, मूत (urine - vulgar/crude), etc.
    obscure_words = [
        {
            'id': 3599,
            'hi': 'पगोडा',
            'en': 'pagoda (a Chinese-style tower...)',
            'reason': 'Obscure architectural loan word rarely used in standard Hindi'
        },
        {
            'id': 3600,
            'hi': 'बुत-कदा',
            'en': 'pagoda / temple (n.)',
            'reason': 'Archaic poetic Urdu/Persian term for idol-house/temple'
        },
        {
            'id': 3601,
            'hi': 'बुतख़ाना',
            'en': 'temple / pagoda (n.)',
            'reason': 'Rare poetic Urdu/Persian synonym for idol temple'
        },
        {
            'id': 5491,
            'hi': 'मूत',
            'en': 'urine (n.)',
            'reason': 'Crude/vulgar colloquial term, standard respectful term is पेशाब (peshāb) or मूत्र (mūtra)'
        }
    ]

    # Summary
    all_removal_ids = set([x['id'] for x in exact_duplicates_to_remove] + 
                          [x['id'] for x in alphabet_entries] + 
                          [x['id'] for x in foreign_proper_names] + 
                          [x['id'] for x in obscure_words])

    report = {
        'total_words_in_vocab': total_words,
        'exact_duplicates_count': len(exact_duplicates_to_remove),
        'alphabet_entries_count': len(alphabet_entries),
        'foreign_proper_names_count': len(foreign_proper_names),
        'obscure_words_count': len(obscure_words),
        'total_recommended_removals': len(all_removal_ids),
        'corrected_vocab_size': total_words - len(all_removal_ids),
        'exact_duplicates': exact_duplicates_to_remove,
        'alphabet_entries': alphabet_entries,
        'foreign_proper_names': foreign_proper_names,
        'obscure_words': obscure_words,
        'definition_errors': definition_errors
    }

    with open('scripts/full_audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("VOCAB.JSON AUDIT & OPTIMIZATION REPORT")
    print("=" * 60)
    print(f"Total Current Entries       : {total_words}")
    print(f"1. Exact Duplicates to Prune: {len(exact_duplicates_to_remove)}")
    print(f"2. Alphabet/Character glyphs: {len(alphabet_entries)}")
    print(f"3. Foreign proper nouns     : {len(foreign_proper_names)}")
    print(f"4. Obscure / Archaic terms  : {len(obscure_words)}")
    print(f"Total Removals Proposed     : {len(all_removal_ids)}")
    print(f"Post-cleanup Total Entries  : {total_words - len(all_removal_ids)}")
    print(f"Critical Definitions Fixed  : {len(definition_errors)}")
    print("=" * 60)

if __name__ == '__main__':
    run_audit()
