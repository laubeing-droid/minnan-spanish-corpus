# minnan-spanish-corpus · Early Minnan–Spanish Bilingual Historical Document Corpus

> The Chinese README ([README.md](README.md)) is canonical. This is an active work-in-progress corpus: pipeline sealing and automated gate passage (`[PASS]`) verify structural integrity and orthographic rules, but do not substitute for full page-by-page philological collation. The 22 sources count registered PDF files (3,139 physical page positions across 9 document lines), not 22 independent books.

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

> **22 early Minnan–Spanish bilingual historical document sources** left by the Dominican mission
> (Province of the Most Holy Rosary) and the Sangley (Southern Fujianese) community of 16th- and
> 17th-century Manila: diplomatic blind-read transcriptions, historical phonological derivations,
> and collation-ready corpus data produced through a reproducible, auditable engineering pipeline.

**Docs**: [Historical Background](docs/HISTORICAL_BACKGROUND.md) · [Methodology](docs/METHODOLOGY.md) · [Significance](docs/SIGNIFICANCE.md) · [Data Schema](docs/DATA_SCHEMA.md) · [Project History](docs/PROJECT_HISTORY.md) · [Engineering Lessons](docs/LESSONS.md) · [Usage](docs/USAGE.en.md) · [Changelog](CHANGELOG.md)

---

## 1. What Is Studied

Between ca. 1590 and 1700, Dominican friars in Manila—working closely with Sangley Chinese interpreters and scribes—recorded the Zhangzhou-based dialect of Hokkien (Southern Min, *lengua Chio Chiu*) in Golden Age Spanish orthography to evangelize and communicate with the overseas Chinese community, leaving dictionaries, grammars, catechisms, apologetic treatises, translations, and secular manuscripts. This repository structures all **22 surviving source PDFs — 3,139 physical page positions across 9 document lines**:

| Line | Work | Holding Institution & Shelfmark | PDF Pages |
| --- | --- | --- | ---: |
| 1 | *Dictionario Hispanico Sinicum* (Spanish–Chinese/Hokkien dictionary) | UST Archives, Manila (Libros 215, 2 PDFs) | 1,140 |
| 2 | *Arte de la Lengua Chio Chiu* (Zhangzhou Hokkien grammar, ca. 1620) | CRAI Univ. of Barcelona, Ms. 1027 | 122 |
| 3 | *Manila Chinese Manuscripts*, vols. 1–14 | HAB Wolfenbüttel, 91.2 Extrav. 01–14 | 461 |
| 4 | *Beng Sim Po Cam* (*Espejo rico del claro corazón*, trans. Juan Cobo, O.P.) | Biblioteca Nacional de España, MSS/6040 | 315 |
| 5 | *Apología de la verdadera religión* (*Shilu* 《無極天主正教真傳實錄》, 1593 woodblock) | Biblioteca Nacional de España, R/33396 | 164 |
| 6 | Chinese–Spanish dictionary, Paris copy | Bibliothèque nationale de France, Chinois 9276 | 178 |
| 7 | Chinese–Spanish dictionary, Rome copy | Biblioteca Angelica, Mss. Fondo Antico 60 | 169 |
| 8 | *Xinkan Liaoshi Zhengjiao Bianlan* (bilingual catechism) | Österreichische Nationalbibliothek, Sin 282-A | 580 |
| 9 | Zhangzhou catechism & *Arte Sangley* fragments | UST Archives, Manila, Tomo 211 | 10 |

## 2. Method (Summary)

* **Pure Blind-Read Protocol (v3.1, `WITHOUT_PRIOR_DRAFT`)**: Visual transcription on the M2 line follows the 300 dpi page slices alone without consulting legacy drafts; phonological hindsight must never "correct" manuscript spellings, and modern POJ/Tâi-lô orthography is strictly banned from `source_M`.
* **Six-Layer Data Isolation (`layer_0` to `layer_5`)**: The four diplomatic columns (Spanish headword `L`, Chinese character `H`, 17th-century Dominican Hokkien romanization `M`, and Mandarin gloss `R`) are transcribed verbatim; 17th-century Zhangzhou IPA reconstructions and modern MOE Tâi-lô equivalents are computed by deterministic engines into separate layers.
* **Pre-Collation SHA-256 Sealing & Immutable Gatekeeper**: Every committed blind-read page is SHA-256-sealed (`LOCKED_BEFORE_COLLATION`); `architect_gatekeeper.py` (declared unmodifiable) independently verifies orthographic purity, geometric tone-code validity (`T00–T07 / T99`), and `Counter`-based anti-template thresholds. Full details: **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**.

## 3. Why It Matters (Summary)

Provides essential **character-to-sound collation material** for early Zhangzhou-based Hokkien, and structured primary sources for the social history of the Manila Sangley community, the history of Chinese–Western translation (including the earliest known translation of a Chinese classic into a European language, Juan Cobo's *Beng Sim Po Cam*), and the history of Catholic Chinese printing. More importantly, using these documents as a testbed, the project explores a **complete research-engineering methodology for "Computational and Generative Minnan Historical & Philological Studies"**—progressing from source and material convergence, research questions, and evidentiary constraints to historical phenomenon identification, comparative analysis, hypothesis testing, and human scholarly judgment. **Corpora and collation are the foundation, not the endpoint; current philological-engineering outputs are kept strictly distinct from the full research workflow still under exploration, and engineering sealing is never conflated with completed historical scholarship.** See **[docs/SIGNIFICANCE.md](docs/SIGNIFICANCE.md)** and **[docs/HISTORICAL_BACKGROUND.md](docs/HISTORICAL_BACKGROUND.md)**.

## 4. Repository Map

| Path | Contents |
| --- | --- |
| `literature/workspace_m1_dhs306/` | Frozen M1 zone for dictionary pp. 835–1140 (5,762-entry master + 14 disambiguated batch packages; see scope note in [DATA_SCHEMA.md](docs/DATA_SCHEMA.md)) |
| `literature/workspace_m2_dhs834/` | Sealed M2 blind-read pages (pp. 0030–0834 + 140 gap-fill pages in pp. 0845–1140), SHA-256 manifest, non-lexicographic page register, and collation queue |
| `literature/baseline_all22_extracted/` | Legacy baseline drafts for all 22 sources (732 Markdown working files) |
| `literature/evidence_ledger/` | Four separated evidence ledgers (unresolved glyphs, unproven phonology, uncertain glosses, pending operations; see [LEDGERS.md](docs/LEDGERS.md)) |
| `literature/tools/` | Deterministic engines: tile slicing (`column_slicer.py`), 17c orthographic sanitization & phonology (`hokkien_17c_converter.py`), Spanish abbreviation expansion (`spanish_17c_expander.py`), and M2 pipeline (`zcode_m2_pipeline.py`) |
| `architect_gatekeeper.py` | Immutable acceptance gate (anti-fabrication and anti-template verifier) |
| `.zcode/workflow-drafts/` | Blind-read construction and audit workflow scripts |
| `literature/source22_actual_mapping.json` | Inventory of all 22 source PDFs, SHA-256 anchors, and transfer metadata |

> Source PDFs and scanned page tiles are **not** distributed in this repository for copyright reasons; all corpus coordinates reference original PDF page numbers.

## 5. Quick Start

```bash
python architect_gatekeeper.py                              # verify integrity of all sealed data
python literature/tools/zcode_m2_pipeline.py status         # check dictionary-line progress
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # rebuild tiles from local source PDF
```

Schemas, the three-step transcription protocol, and the collation queue:
**[docs/USAGE.en.md](docs/USAGE.en.md)** ([中文](docs/USAGE.md) / [Español](docs/USAGE.es.md)).

## 6. Current Status

Work in progress: M2 blind-read sealing covers pp. 0030–0834 (797 lexicographic pages sealed + 8 modern publisher pages excluded by registration) and is actively completing the 140 gap-fill pages in pp. 0845–1140; the project is transitioning into **manual philological collation** (`COLLATION_QUEUE.json`). For the full construction history and the forensic resolution of the 140-page gap mystery, see **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)** and **[docs/LESSONS.md](docs/LESSONS.md)**.

## 7. Rights & License

* Original transcriptions, code, and documentation in this repository: **[CC BY-NC-SA 4.0](LICENSE)** — attribution, **non-commercial**, share-alike.
* Modern facsimile and photographic editions of the 22 documents remain the property of their holding libraries and publishers (collection facsimile © National Tsing Hua University Press) and are not redistributed here; the underlying 17th-century manuscript texts are in the public domain.

## 8. Citation

```bibtex
@misc{minnan_spanish_corpus_2026,
  title  = {minnan-spanish-corpus: blind-read corpus and tooling for 22 early Minnan--Spanish bilingual historical document sources},
  author = {Minnan Historical Documents Working Group},
  year   = {2026},
  url    = {https://github.com/laubeing-droid/minnan-spanish-corpus},
  note   = {CC BY-NC-SA 4.0; source scans excluded for copyright reasons}
}
```
