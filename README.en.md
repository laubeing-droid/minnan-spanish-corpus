# minnan-spanish-corpus · Early Minnan–Spanish Bilingual Historical Document Corpus

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

> **22 early Minnan–Spanish bilingual historical documents** left by the Dominican mission
> and the Sangley (Chinese) community of 17th-century Manila: full-text blind-read
> transcriptions, historical phonological derivations, and collation-ready corpus data,
> produced with a reproducible engineering pipeline.

**Docs**: [Methodology](docs/METHODOLOGY.md) · [Significance](docs/SIGNIFICANCE.md) · [Project History](docs/PROJECT_HISTORY.md) · [Usage](docs/USAGE.en.md) · [Changelog](CHANGELOG.md)

---

## 1. What is studied

Around 1590–1700, Dominican friars in Manila recorded the Zhangzhou dialect of Hokkien
(Minnan) in Spanish-based orthography to evangelize the Sangley Chinese, leaving
dictionaries, grammars, catechisms, translations and lay documents. This project
industrially curates all **22 surviving originals — 3,139 physical pages across 9 book lines**:

| Line | Work | Holding | Pages |
| --- | --- | --- | ---: |
| 1 | *Dictionario Hispánico Sinicum* (Spanish–Chinese dictionary) | UST Archives, Manila | 1,140 |
| 2 | *Arte de la Lengua Chio Chiu* (Zhangzhou grammar) | UB Ms. 1027 | 122 |
| 3 | *Manila Chinese Manuscripts*, vols. 1–14 | HAB 91.2 Extrav 01–14 | 461 |
| 4 | *Beng Sim Po Cam* (Mirror of the Clear Heart), Chinese–Spanish | BNE MSS/6040 | 315 |
| 5 | *Apología de la Verdadera Religión* (woodblock print) | BNE R/33396 | 164 |
| 6 | Chinese–Spanish dictionary, Paris parallel copy | BnF Chinois 9276 | 178 |
| 7 | Chinese–Spanish dictionary, Rome copy | Biblioteca Angelica Ms. 60 | 169 |
| 8 | *Xinkan Liaoshi Zhengjiao Bianlan* (catechism) | ONB Sin 282-A | 580 |
| 9 | Zhangzhou catechism / *Arte Sangley* fragments | AUST Tomo 211 | 10 |

## 2. Method (summary)

* **Pure blind-read protocol (v3.1)** — transcription follows the page image only; phonological
  knowledge must never "correct" the lettering, so the corpus remains independent 17th-century evidence.
* **Six-layer data isolation** — the four manuscript columns (Spanish head L, Chinese characters H,
  Hokkien manuscript spelling M, Mandarin gloss R) are transcribed verbatim; 17th-century Zhangzhou
  IPA and modern MOE Tâi-lô are derived by deterministic engines into separate layers.
* **Blind hash sealing + immutable gate** — every page is SHA-256 sealed on commit;
  `architect_gatekeeper.py` (declared unmodifiable) independently checks orthographic purity,
  tone-code validity and seal integrity, with anti-template and anti-fabrication rules.
  Full details: **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**.

## 3. Why it matters (summary)

The earliest and largest synchronic character–sound corpus of 17th-century Zhangzhou Hokkien;
structured primary material for the history of the Manila Sangley community, of Chinese–Western
translation (including the earliest known Western translation of a Chinese book, *Beng Sim Po Cam*),
and of Catholic printing in Chinese; plus a reproducible-data paradigm for endangered-manuscript
philology. See **[docs/SIGNIFICANCE.md](docs/SIGNIFICANCE.md)**.

## 4. Repository map

| Path | Contents |
| --- | --- |
| `literature/workspace_m1_dhs306/` | Sealed corpus for dictionary pp. 835–1140 (5,762-entry master + 14 batch packages) |
| `literature/workspace_m2_dhs834/` | Sealed blind-read pages for pp. 0030–0834, SHA-256 manifest, non-lexicographic page register, collation queue |
| `literature/baseline_all22_extracted/` | Baseline first drafts for all 22 sources (732 markdown working files) |
| `literature/historical_dhs/` · `ledgers/` | Dictionary full first-draft body; unresolved-glyph ledgers |
| `literature/tools/` | Deterministic engines: tile slicing, 17c sanitization & phonology, Spanish abbreviation expansion, sealing pipeline |
| `architect_gatekeeper.py` | Immutable acceptance gate |
| `.zcode/workflow-drafts/` | Blind-read construction protocols (workflow scripts) |
| `literature/source22_actual_mapping.json` etc. | Source inventory, integrity checks, transfer manifests, metadata |

> Source PDFs and page-scan tiles are **not** in this repository (rights); corpus coordinates
> refer to PDF page numbers.

## 5. Quick start

```bash
python architect_gatekeeper.py                              # verify integrity of all sealed data
python literature/tools/zcode_m2_pipeline.py status         # dictionary-line progress
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # rebuild tiles from the source PDF
```

Schemas, the three-step transcription protocol and the collation queue:
**[docs/USAGE.md](docs/USAGE.md)** ([English](docs/USAGE.en.md) / [Español](docs/USAGE.es.md)).

## 6. Status

Work in progress: blind-read sealing covers the entire dictionary line; the project is now in the
**manual collation** stage. Fine-grained progress and incident log: **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)**;
version history: **[CHANGELOG.md](CHANGELOG.md)**.

## 7. Rights & license

* Corpus, code and docs: **[CC BY-NC-SA 4.0](LICENSE)** — attribution, **non-commercial**, share-alike.
* Modern facsimile/photographic editions of the 22 documents remain with their holding libraries
  and publishers (dictionary facsimile © National Tsing Hua University Press) and are not
  redistributed here; the 17th-century manuscripts themselves are in the public domain.

## 8. Citation

```bibtex
@misc{minnan_spanish_corpus_2026,
  title  = {minnan-spanish-corpus: blind-read corpus and tooling for 22 early Minnan--Spanish bilingual historical documents},
  author = {Minnan Historical Documents Working Group},
  year   = {2026},
  url    = {https://github.com/laubeing-droid/minnan-spanish-corpus},
  note   = {CC BY-NC-SA 4.0; source scans excluded for rights reasons}
}
```
