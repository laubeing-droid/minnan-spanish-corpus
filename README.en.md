# minnan-spanish-corpus · Early Minnan–Spanish Bilingual Historical Document Corpus

> The Chinese README ([README.md](README.md)) is canonical. This is an active work-in-progress corpus: pipeline sealing and automated gate passage (`[PASS]`) verify structural integrity and orthographic rules, but do not substitute for full page-by-page philological collation. The 22 sources count registered PDF files (3,139 physical page positions across 9 document lines), not 22 independent books.

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

This repository brings together legacy drafts, layered data and sealed blind-read records for 22 registered source PDFs concerning early Hokkien–Spanish language contact. It is intended for finding material, comparing readings and continuing collation. These outputs come from different stages of work and have not all undergone independent philological review.

**Docs**: [Historical Background](docs/HISTORICAL_BACKGROUND.md) · [Methodology](docs/METHODOLOGY.md) · [Significance](docs/SIGNIFICANCE.md) · [Data Schema](docs/DATA_SCHEMA.md) · [Project History](docs/PROJECT_HISTORY.md) · [Engineering Lessons](docs/LESSONS.md) · [Usage](docs/USAGE.en.md) · [Changelog](CHANGELOG.md)

---

## 1. What Is Studied

Between ca. 1590 and 1700, Dominican friars in Manila—working closely with Sangley Chinese interpreters and scribes—recorded the Zhangzhou-based dialect of Hokkien (Southern Min, *lengua Chio Chiu*) in Golden Age Spanish orthography to evangelize and communicate with the overseas Chinese community, leaving dictionaries, grammars, catechisms, apologetic treatises, translations, and secular manuscripts. The project organizes **22 registered source PDFs: 3,139 physical page positions across 9 document lines**. PDF page positions are not original folio numbers or a count of fully collated pages:

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

Transcription and interpretation are separate tasks. The M2 blind-read protocol (v3.1, `WITHOUT_PRIOR_DRAFT`) requires reading 300 dpi page slices without consulting legacy drafts. Modern phonological expectations must not be used to rewrite historical spellings. Earlier reference-assisted drafts remain available, but are not retrospectively treated as independent blind readings.

For DHS, the four source columns contain Spanish headwords (`L`), Chinese characters (`H`), Hokkien romanization (`M`) and Mandarin readings (`R`). Historical phonological reconstructions and modern MOE Tâi-lô comparisons are stored separately from these observations. Deterministic conversion makes a procedure repeatable; it does not by itself establish the correct reading or historical sound value. The DHS layout is not a template for every source. See the [data schema](docs/DATA_SCHEMA.md) for the six stored layers (`layer_0` to `layer_5`).

SHA-256 hashes register sealed blind-read pages (`LOCKED_BEFORE_COLLATION`). The immutable `architect_gatekeeper.py` checks the orthographic, tone-code (`T00–T07 / T99`) and integrity conditions it implements, including `Counter`-based anti-template thresholds. Passing those checks does not replace collation. The [methodology](docs/METHODOLOGY.md) explains the procedure and its limits.

## 3. Why It Matters

The documents offer material for comparing characters and early Zhangzhou-based Hokkien spellings, and for studying the Manila Sangley community, Chinese–Western translation and Catholic Chinese printing. Juan Cobo's *Beng Sim Po Cam*, for example, is the earliest known translation of a Chinese classic into a European language. Dictionaries and secular manuscripts record other settings of language use; their interpretation requires attention to each work's history and witnesses.

The wider aim is to explore how computational and generative methods can support Minnan historical research. That means defining sources and questions, identifying patterns worth investigating, comparing evidence, testing explanations and leaving the final judgment to researchers. Transcription and collation provide the basis for this work, not a substitute for it. The [significance document](docs/SIGNIFICANCE.md) distinguishes existing outputs from the full research workflow still under development; the [historical background](docs/HISTORICAL_BACKGROUND.md) introduces the sources' setting.

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

## 5. Getting Started

For reading and citation, begin with the [usage guide](docs/USAGE.en.md) or the [Agent guide](docs/AGENT_GUIDE.md); no script execution is needed. The commands below are for maintainers. Slicing creates local files and requires lawful access to the source PDF and authorization for that work.

```bash
python architect_gatekeeper.py                              # verify integrity of all sealed data
python literature/tools/zcode_m2_pipeline.py status         # check dictionary-line progress
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # rebuild tiles from local source PDF
```

Schemas, the three-step transcription protocol, and the collation queue:
**[docs/USAGE.en.md](docs/USAGE.en.md)** ([中文](docs/USAGE.md) / [Español](docs/USAGE.es.md)).

## 6. Current Status

Gap-fill complete (2026-11-12): M2 blind-read sealing now covers the full dictionary line — pp. 0030–0834 (797 lexicographic pages / 15,417 entries) plus the 140 gap-fill pages of pp. 0845–1140 (2,733 entries), totaling **937 sealed pages / 18,150 entries**; final gate PASS; 8 modern publisher pages excluded by registration. The project has entered **manual philological collation** (queue: 884 pages — 671 high / 213 medium — see `COLLATION_QUEUE.json`; a further 1,810 mechanical-defect findings were transferred to the collation line). For the full construction history and the forensic resolution of the 140-page gap mystery, see **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)** and **[docs/LESSONS.md](docs/LESSONS.md)**.

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
