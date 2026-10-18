# Hindi Vocabulary (`hindi-vocab`)

A minimal, curated, frequency-ranked dictionary of standard Hindi base headwords designed for language learning and natural language applications.

## Dataset Overview

* **File**: [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json)
* **Total Entries**: 5,041 lemmatized single-word headwords
* **Order**: Ranked strictly from highest frequency to lowest frequency (implicit in sequential `id`)
* **Indexing**: Continuous, sequential IDs (`1` to `5041`)

## Schema

Each entry in [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json) consists of:

```json
{
  "id": 1,
  "hi": "है",
  "en": "is"
}
```

* `id` *(integer)*: 1-indexed rank ordered strictly from highest frequency to lowest frequency.
* `hi` *(string)*: Standard Hindi headword in Devanagari script (pure base citation lemma).
* `en` *(string)*: Concise single English translation word (no markers or multiple options).

## Curation Standards

1. **Pure Single-Word Citation Lemmas**: Only standard base forms (verbs in infinitive `-ना`, marked adjectives in masculine singular `-ा`, nouns in direct singular). All conjugated verb forms, pronominal case duplicates, and inflections are excluded.
2. **Concise English Equivalence**: Exactly one primary English translation per headword with zero grammatical markers or parenthetical clutter.
3. **100% Core Semantic Coverage**: Complete coverage across core categories (numbers, pronouns, kinship, body parts, colors, seasons, weather, nature, kitchenware, spices, fauna, flora, society, and time).
4. **Clean Orthography**: Standardized Devanagari spellings (standard candrabindu, consolidated nuqtas, zero multi-word collocations).

## Validation

To verify sequential indexing, zero duplicates, and strict single-word schema integrity:

```bash
python3 scripts/validate_vocab.py
```
