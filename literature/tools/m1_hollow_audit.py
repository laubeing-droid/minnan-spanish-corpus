#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M1 主卷空壳审计（回填对勘工作清单生成器）
==============================================

枚举 M1 主卷（DHS_p0835_1140_M1_FULL_5762.json）中 H/M/R 全空或音系占位
（`sio¹ hue⁵` / `sio-huê`）的条目，按 PDF 页分组输出回填工作清单。

用途：166 页 Core 词条回填对勘专案（见 docs/COLLATION_GUIDE.md §4）的工作清单来源。
纪律：对 M1 目录**只读**；输出清单写在 M2 工作区（校对线家目录），不触碰任何封存件。
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
LITERATURE_DIR = TOOLS_DIR.parent
MASTER = LITERATURE_DIR / "workspace_m1_dhs306" / "DHS_p0835_1140_M1_FULL_5762.json"
OUT = LITERATURE_DIR / "workspace_m2_dhs834" / "M1_HOLLOW_BACKFILL_QUEUE.json"

PLACEHOLDER_IPA = "sio¹ hue⁵"
PLACEHOLDER_TAILO = "sio-huê"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = json.loads(MASTER.read_text(encoding="utf-8"))
    by_page = defaultdict(list)
    for e in d.get("entries", []):
        raw = e.get("layer_1_diplomatic_raw", {}) or {}
        ph = e.get("layer_3_historical_phonology", {}) or {}
        tl = e.get("layer_4_modern_tai_lo", {}) or {}
        hollow_cols = not any(
            (raw.get(k) or "").strip() for k in ("source_H", "source_M", "source_R")
        )
        placeholder = (ph.get("reconstructed_17th_c_hokkien") or "").strip() == PLACEHOLDER_IPA or (
            (tl.get("tai_lo_standard") or "").strip() == PLACEHOLDER_TAILO
        )
        if not (hollow_cols or placeholder):
            continue
        la = e.get("layer_0_visual_anchor", {}) or {}
        page = int(la.get("page_pdf", 0) or 0)
        by_page[page].append(
            {
                "entry_id": e.get("entry_id"),
                "page_folio": la.get("page_folio"),
                "position_in_page": la.get("position_in_page"),
                "hollow_cols": hollow_cols,
                "placeholder_phonology": placeholder,
                "source_L_head": (raw.get("source_L") or "")[:60],
            }
        )

    entries_total = sum(len(v) for v in by_page.values())
    queue = {
        "protocol": "M1_HOLLOW_BACKFILL_WORKLIST_v1",
        "note": "M1 主卷 CORE 空壳/占位回填对勘工作清单（生成器 m1_hollow_audit.py，只读 M1）。"
        "回填属结构性修改，须先经架构师裁定解冻（或另立新版账）；当前仅限取证对勘入账。",
        "total_entries": entries_total,
        "total_pages": len(by_page),
        "pages": {str(k): by_page[k] for k in sorted(by_page)},
    }
    OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[M1 HOLLOW AUDIT] 需回填 {entries_total} 条，分布 {len(by_page)} 页 -> {OUT.name}")
    heavy = sorted(by_page.items(), key=lambda kv: -len(kv[1]))[:5]
    for page, items in heavy:
        print(f"  重灾区 p{page}: {len(items)} 条")


if __name__ == "__main__":
    main()
