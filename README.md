# Hindi Vocabulary (`hindi-vocab`)

A curated, frequency-ranked dictionary of standard Hindi vocabulary designed for language learners, natural language processing, and language proficiency applications.

## Dataset Overview

* **File**: [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json)
* **Total Entries**: 5,332 lemmatized headwords
* **Order**: Strictly descending by natural usage frequency (`38,292` down to `1`)
* **Indexing**: Continuous, sequential IDs (`1` to `5332`)

## Schema

Each entry in [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json) follows this schema:

```json
{
  "id": 1,
  "hi": "है",
  "en": "is / exists (v.)",
  "freq": 38292
}
```

* `id` *(integer)*: 1-indexed sequential ranking.
* `hi` *(string)*: Standard Hindi headword in Devanagari script.
* `en` *(string)*: English definition and parts of speech tag (`v.`, `n.`, `adj.`, `adv.`, `postp.`, `conj.`, `pron.`, `num.`, `interj.`).
* `freq` *(integer)*: Usage frequency count derived from natural conversational Hindi corpora.

## Curation Standards

1. **Strict Lemmatization**: Words are indexed by their base citation lemma (e.g. verbs in infinitive `-ना`, adjectives and marked nouns in masculine singular `-ा`). Conjugated forms and case inflections are excluded.
2. **Orthographic Standardization**: Nuqta variations and spelling duplicates are consolidated into their standard Devanagari forms.
3. **Proficiency Alignment**: Correlated and cross-verified against real sentence corpora (such as `hindi-vakya`), removing artificial compound clutter, foreign language names, and archaic dictionary fossils while incorporating authentic high-yield vocabulary.

## Validation

To verify the integrity, schema conformance, and monotonic frequency sorting of [`vocab.json`](file:///home/zenhome/Projects/hindi-vocab/vocab.json):

```bash
python3 scripts/validate_vocab.py
```
