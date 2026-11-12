# Usage / 使用方法 (English)

> [中文](USAGE.md) | [English](USAGE.en.md) | [Español](USAGE.es.md)
> Requirements: Python ≥ 3.10, **no third-party dependencies** (standard library only).
> Run all commands from the repository root.

---

## 1. Where is the data

| What you want | Where |
| --- | --- |
| Frozen M1 zone for dictionary pp. 835–1140 (six layers: disambiguation/phonology/Tâi-lô; see scope note in [DATA_SCHEMA.md](DATA_SCHEMA.md)) | `literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json` |
| Per-page sealed blind reads (pp. 0030–0834 and gap-fill pages in pp. 0845–1140) | `literature/workspace_m2_dhs834/blind_read_pXXXX.json` |
| Master manifest with SHA-256 seals | `literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json` |
| Manual philological collation queue (sorted by severity) | `literature/workspace_m2_dhs834/COLLATION_QUEUE.json` |
| Register of non-lexicographic pages (modern title pages, etc.) | `literature/workspace_m2_dhs834/non_lexicographic_pages.json` |
| Baseline first drafts of all 22 sources | `literature/baseline_all22_extracted/body/` |

## 2. Verify data integrity

```bash
python architect_gatekeeper.py
```

`[PASS] M1 ...` and `[PASS] M2 Gate: N blind-read pages verified` mean that the consistency conditions covered by the checker have passed. They do not certify manuscript readings, historical sound values, or the philological quality of the whole corpus. See §3 of [METHODOLOGY.md](METHODOLOGY.md) for the checks and their limits.

`architect_gatekeeper.py` is **declared unmodifiable** and also checks for fabrication. Do not change the verifier to make data pass.

## 3. Progress

```bash
python literature/tools/zcode_m2_pipeline.py status
```

## 4. Rebuild page tiles from the source PDF

Scan tiles are not distributed (rights), but can be **deterministically rebuilt** from a lawfully
held copy of the source PDF:

```bash
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849
# produces literature/tiles/01_DHS/page_XXXX/: 3 horizontal bands + 4 columns + full 300dpi page
```

## 5. Three-step transcription protocol (new or repaired pages)

1. `slice --start X --end Y`;
2. **Pure visual transcription**: write `literature/workspace_m2_dhs834/raw_blind/raw_part_pXXXX.json`,
   shape `{"pages":[{ ...this page only... }]}` with page fields `pdf_page / historical_folio /
   page_header / page_footer_printed / page_footer_handwritten / entries`; each entry is
   `{position, source_L, source_H, source_M, source_R, tone_marks_M, tone_marks_R}`;
3. Seal and gate:

```bash
python literature/tools/zcode_m2_pipeline.py commit --input literature/workspace_m2_dhs834/raw_blind/<merged>.json
python architect_gatekeeper.py
```

**Iron rules**: `source_M` only allows 17th-century Dominican spelling (c-/qu-/ch-/g-/s-/z-/ttz-);
modern k-/kh-/ts-/tsh-/chh- are forbidden. `tone_marks` only allow
`T00 (無標號) / T01 (升斜) / T02 (降斜) / T03 (尖頂帽) / T04 (凹角) / T05 (平橫) /
T06/T07 (交叉入聲號) / T99 (污損難辨)`. Empty column `[空]`, illegible `[残]`, uncertain `[疑:A/B]`.
**Never hand-write `blind_read_pXXXX.json`** — sealed files are produced only by the commit pipeline.

## 6. Using the collation queue

`COLLATION_QUEUE.json` is a page list sorted by severity:

```json
{"page": 621, "can": 2, "yi": 3, "t99": 1, "estimated": true,
 "severity": "high", "notes": "..."}
```

* `can`/`yi`/`t99` = counts of `[残]`/`[疑:]`/T99 on the page; `estimated` = folio estimated or
  notes flagged for human review.
* Recommended order: `high` → `medium`; entries with `page ≥ 835` are newly read gap pages —
  read them together with their neighbors.

## 7. Prohibitions

* Modifying `architect_gatekeeper.py` (a self-modified verifier is void);
* Hand-writing or directly editing `blind_read_pXXXX.json` (produced only via the commit pipeline);
* Mixing accounting across book lines (each line's completion ledger is separate; never summed);
* Writing modern romanization or speculative phonetics into `source_M`.

## 8. FAQ

* **Why no PDFs/images?** Rights: the modern facsimile belongs to the press/libraries. Corpus
  coordinates are PDF page numbers; with a lawful copy you can rebuild all tiles (§4).
* **Encoding errors?** All JSON is UTF-8 (`ensure_ascii=False`); read with `encoding="utf-8"`.
* **Line-ending/CRLF warnings?** This repository is **byte-exact**: `.gitattributes` sets `* -text`,
  so no line-ending conversion is ever applied — conversion would rewrite SHA-256-sealed bytes and
  make the gate fail (measured incident, 0.2.3: git eol conversion broke the p0905/p0041 seals; all
  937 pages were reconstructed from the manifest). Do not enable `core.autocrlf` for this repo.
