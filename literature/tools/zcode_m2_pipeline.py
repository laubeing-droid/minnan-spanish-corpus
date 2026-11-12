#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZCode All-in-One M2 Execution Pipeline (zcode_m2_pipeline.py)
=============================================================
Designed specifically for ZCode (GLM / Qwen / Doubao / DeepSeek) so the model
ONLY performs visual transcription of the 4 columns (L, H, M, R + T01~T07),
while this local Python engine deterministically handles:
  1. 300 DPI Dual-Track Image Slicing (`slice --start N --end M`)
  2. 17th-c. Missionary Orthography Sanitization (removing modern k-, kh-, ts-, -̍, ⁿ)
  3. 17th-c. Spanish Abbreviation Expansion & Manila Sangley Loanword Annotation
  4. 17th-c. Zhangzhou Historical Phonology (IPA) & Standard MOE Tâi-lô Derivation
  5. Cryptographic SHA-256 Sealing into `BLIND_READ_MANIFEST.json` (`commit --input <json>`)
  6. Progress Tracking across DHS Pages 0030-0834 (`status`)
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding="utf-8")

TOOLS_DIR = Path(__file__).resolve().parent
LITERATURE_DIR = TOOLS_DIR.parent
WORKSPACE_ROOT = LITERATURE_DIR.parent
M2_DIR = LITERATURE_DIR / "workspace_m2_dhs834"
TILES_BASE = LITERATURE_DIR / "tiles" / "01_DHS"

sys.path.insert(0, str(TOOLS_DIR))
from minnan_engine import MinnanEngine
from spanish_17c_expander import expand_spanish_entry
from hokkien_17c_converter import (
    sanitize_17c_missionary_orthography,
    has_modern_tailo_contamination,
    missionary_to_17c_ipa_and_tailo,
)

VALID_TONE_LABELS = {
    "T00 (無標號)",
    "T01 (升斜)",
    "T02 (降斜)",
    "T03 (尖頂帽)",
    "T04 (凹角)",
    "T05 (平橫)",
    "T06/T07 (交叉入聲號)",
    "T99 (污損難辨)",
}

TONE_NORMALIZER = {
    "T00": "T00 (無標號)",
    "T01": "T01 (升斜)",
    "T02": "T02 (降斜)",
    "T03": "T03 (尖頂帽)",
    "T04": "T04 (凹角)",
    "T05": "T05 (平橫)",
    "T06": "T06/T07 (交叉入聲號)",
    "T07": "T06/T07 (交叉入聲號)",
    "T06/T07": "T06/T07 (交叉入聲號)",
    "T99": "T99 (污損難辨)",
}


def normalize_tone_list(tones: List[str]) -> List[str]:
    out = []
    for t in (tones or []):
        t_str = t.strip()
        if t_str in VALID_TONE_LABELS:
            out.append(t_str)
            continue
        code = t_str.split()[0]
        if code in TONE_NORMALIZER:
            out.append(TONE_NORMALIZER[code])
        else:
            out.append(t_str)
    return out


def cmd_slice(start_page: int, end_page: int) -> None:
    engine = MinnanEngine(LITERATURE_DIR)
    pdf_path = engine.get_source_pdf_path("01_DHS_Hispanico_Sinicum")
    if not pdf_path or not pdf_path.exists():
        print(f"[ERROR] Cannot locate 01_DHS PDF at {pdf_path}")
        sys.exit(1)

    results = []
    for p in range(start_page, end_page + 1):
        out_dir = TILES_BASE / f"page_{p:04d}"
        manifest = engine.extract_4column_tiles(pdf_path, p, out_dir)
        bands = [b["tile_path"] for b in manifest.get("horizontal_bands", [])]
        cols = [c["tile_path"] for c in manifest.get("columns", [])]
        results.append({
            "pdf_page": p,
            "page_type": manifest["page_type"],
            "horizontal_bands": bands,
            "columns": cols,
        })
        print(f"[SLICED] PDF {p:04d} ({manifest['page_type']}) -> {len(bands)} bands")

    print(f"\n[DONE] Sliced {len(results)} pages ({start_page:04d}..{end_page:04d}).")


def process_and_commit_page_dict(page_data: Dict[str, Any]) -> Path:
    pdf_page = int(page_data["pdf_page"])
    pkey = f"{pdf_page:04d}"
    layout_mode = page_data.get(
        "layout_mode",
        "DHS_2COL_SUPPLEMENT_NO_HANZI" if 30 <= pdf_page <= 40 else "DHS_4COL_BILINGUAL"
    )

    raw_entries = page_data.get("entries", [])
    enriched_entries = []

    for idx, e in enumerate(raw_entries, start=1):
        pos = e.get("position", idx)
        src_l = (e.get("source_L") or "").strip()
        src_h = (e.get("source_H") or "").strip()
        src_m_raw = (e.get("source_M") or "").strip()
        src_r = (e.get("source_R") or "").strip()

        # 1. Sanitize 17c missionary orthography in source_M
        src_m = sanitize_17c_missionary_orthography(src_m_raw, src_h)
        issues = has_modern_tailo_contamination(src_m)
        if issues:
            raise ValueError(f"Page {pkey} pos {pos} still has orthography issues: {issues} in '{src_m}'")

        # 2. Normalize tone marks
        t_m = normalize_tone_list(e.get("tone_marks_M", []))
        t_r = normalize_tone_list(e.get("tone_marks_R", []))

        # 3. Deterministic Spanish abbreviation & loanword expansion
        sp_auto = expand_spanish_entry(src_l)

        # 4. Deterministic 17c Zhangzhou IPA & MOE Tâi-lô derivation
        ph_auto = missionary_to_17c_ipa_and_tailo(src_m, src_h, t_m)

        entry_obj = {
            "position": pos,
            "source_L": src_l,
            "source_H": src_h,
            "source_M": src_m,
            "source_R": src_r,
            "tone_marks_M": t_m,
            "tone_marks_R": t_r,
            "auto_precomputed": {
                "spanish_disambiguated": sp_auto["spanish_disambiguated"],
                "abbreviations_expanded": sp_auto["abbreviations_expanded"],
                "loanwords_detected": sp_auto["loanwords_detected"],
                "reconstructed_17th_c_hokkien": ph_auto["reconstructed_17th_c_hokkien"],
                "tai_lo_standard": ph_auto["tai_lo_standard"],
                "phonological_basis": ph_auto["phonological_basis"],
            }
        }
        enriched_entries.append(entry_obj)

    out_doc = {
        "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
        "pdf_page": pdf_page,
        "historical_folio": page_data.get("historical_folio", pdf_page - 29),
        "layout_mode": layout_mode,
        "image_source": f"literature/tiles/01_DHS/page_{pkey}/pdf_{pkey}_300dpi.png",
        "page_header": page_data.get("page_header", ""),
        "page_footer_printed": page_data.get("page_footer_printed", ""),
        "page_footer_handwritten": page_data.get("page_footer_handwritten", ""),
        "total_positions_recorded": len(enriched_entries),
        "blind_state": "AUDITED_VISUALLY_VERIFIED",
        "entries": enriched_entries,
    }

    M2_DIR.mkdir(parents=True, exist_ok=True)
    out_path = M2_DIR / f"blind_read_p{pkey}.json"
    out_bytes = (json.dumps(out_doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    out_path.write_bytes(out_bytes)
    sha = hashlib.sha256(out_bytes).hexdigest()

    # Update BLIND_READ_MANIFEST.json
    manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"protocol": "v3.1_M2_BLIND_READ_MANIFEST", "pages": {}}

    manifest.setdefault("pages", {})[pkey] = {
        "pdf_page": pdf_page,
        "file": f"blind_read_p{pkey}.json",
        "entries_count": len(enriched_entries),
        "blind_first_read_sha256": sha,
        "status": "LOCKED_BEFORE_COLLATION",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[COMMITTED] Page {pkey}: {len(enriched_entries)} entries -> {out_path.name} (SHA-256: {sha[:12]}...)")
    return out_path


def cmd_commit(input_file: str) -> None:
    in_path = Path(input_file)
    if not in_path.exists():
        print(f"[ERROR] Input file not found: {in_path}")
        sys.exit(1)

    payload = json.loads(in_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        page_list = payload
    elif isinstance(payload, dict) and "pages" in payload and isinstance(payload["pages"], list):
        page_list = payload["pages"]
    else:
        page_list = [payload]

    for page_obj in page_list:
        if page_obj.get("page_class") in ("MODERN_FRONT_MATTER", "BLANK"):
            print(f"[SKIPPED] Page {page_obj.get('pdf_page')}: non-lexicographic modern page ({page_obj.get('page_class')})")
            continue
        process_and_commit_page_dict(page_obj)


def cmd_status() -> None:
    manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
    done_pages = set()
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for k in manifest.get("pages", {}).keys():
            done_pages.add(int(k))

    ledger_path = M2_DIR / "non_lexicographic_pages.json"
    excluded = set()
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        excluded = {int(k) for k in ledger.get("pages", {}).keys()}

    target_supp = set(range(30, 41)) - excluded    # 11 pages (0030-0040)
    target_main = set(range(41, 835)) - excluded   # 794 pages (0041-0834), minus modern front matter
    done_supp = sorted(target_supp & done_pages)
    rem_supp = sorted(target_supp - done_pages)
    done_main = sorted(target_main & done_pages)
    rem_main = sorted(target_main - done_pages)

    print("=== DHS M2 BLIND READING PROGRESS ===")
    print(f"1. 18c Supplement (PDF 0030-0040): {len(done_supp)}/{len(target_supp)} done | Next: {rem_supp[:5]}")
    print(f"2. 17c Main Body  (PDF 0041-0834): {len(done_main)}/{len(target_main)} done | Next: {rem_main[:5]}")
    print(f"3. Modern front matter excluded (non-lexicographic): {len(excluded)} {sorted(excluded)}")


def main():
    parser = argparse.ArgumentParser(description="ZCode All-in-One M2 Pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_slice = sub.add_parser("slice", help="Slice PDF pages into 300 DPI bands")
    p_slice.add_argument("--start", type=int, required=True, help="Start PDF page")
    p_slice.add_argument("--end", type=int, required=True, help="End PDF page")

    p_commit = sub.add_parser("commit", help="Sanitize, enrich, and commit blind-read JSON(s)")
    p_commit.add_argument("--input", type=str, required=True, help="Path to raw page or multi-page JSON")

    sub.add_parser("status", help="Show M2 completion status")

    args = parser.parse_args()
    if args.cmd == "slice":
        cmd_slice(args.start, args.end)
    elif args.cmd == "commit":
        cmd_commit(args.input)
    elif args.cmd == "status":
        cmd_status()


if __name__ == "__main__":
    main()
