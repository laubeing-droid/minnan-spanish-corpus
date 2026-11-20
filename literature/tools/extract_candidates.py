#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从裁决台账抽取指定页的修复候选包（只读），供独立把门子代理使用。

用法:
  python literature/tools/extract_candidates.py --pages 30,31 --out candidates.json

候选定义：台账 rows 中 verdict ∈ {两皆误, 重读对} 且 field 可映射 source_M/source_R。
输出：每条候选含队列身份、判定、ink、封存锚（六字段+邻行 H）、页图路径。
"""
import argparse
import json
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")
LEDGER = M2 / "collision_mr" / "ADK_ADJUDICATION_LEDGER.json"
TILES = Path("literature/tiles/01_DHS")
CAND = {"两皆误", "重读对"}


def main():
    parser = argparse.ArgumentParser(description="抽取修复候选包（只读）")
    parser.add_argument("--pages", required=True, help="逗号分隔页码")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    pages = sorted({int(x.strip()) for x in args.pages.split(",")})

    led = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = [r for r in led.get("rows", []) if r.get("page") in pages and r.get("verdict") in CAND]

    by_page = {}
    for pg in pages:
        pk = f"{pg:04d}"
        try:
            seal = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        by_pos = {e["position"]: e for e in seal.get("entries", [])}
        tile_dir = TILES / f"page_{pk}"
        by_page[pg] = {
            "anchors": {str(pos): {k: e.get(k) for k in
                        ("source_H", "source_M", "source_R", "tone_marks_M", "tone_marks_R")}
                        for pos, e in by_pos.items()},
            "prev_H": {str(pos): by_pos.get(pos - 1, {}).get("source_H", "") for pos in by_pos},
            "tiles": {"hanzi": str(tile_dir / f"pdf_{pk}_subcol2_hanzi_full.png"),
                      "minnan": str(tile_dir / f"pdf_{pk}_subcol3_minnan.png"),
                      "mandarin": str(tile_dir / f"pdf_{pk}_subcol4_mandarin_right.png"),
                      "manifest": str(tile_dir / f"pdf_{pk}_tiles_manifest.json")},
        }

    out_rows = []
    for r in rows:
        pg = r["page"]
        fld = {"M": "source_M", "R": "source_R", "source_M": "source_M", "source_R": "source_R"}.get(r.get("field"))
        anchors = by_page.get(pg, {}).get("anchors", {}).get(str(r.get("position")), {})
        out_rows.append({
            "page": pg, "position": r.get("position"), "field": r.get("field"),
            "task_field": fld, "kind": r.get("kind"), "v1": r.get("v1"), "rr": r.get("rr"),
            "verdict": r.get("verdict"), "ink": r.get("ink"), "note": r.get("note"),
            "receipt": r.get("receipt"),
            "sealed_H": anchors.get("source_H", ""),
            "sealed_M": anchors.get("source_M", ""), "sealed_R": anchors.get("source_R", ""),
            "tone_marks": {"M": anchors.get("tone_marks_M", []), "R": anchors.get("tone_marks_R", [])},
            "prev_H": by_page.get(pg, {}).get("prev_H", {}).get(str(r.get("position")), ""),
            "tiles": by_page.get(pg, {}).get("tiles", {}),
        })

    payload = {"pages": pages, "candidateCount": len(out_rows), "candidates": out_rows}
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[candidates] {len(out_rows)} 条 → {args.out}（页 {pages}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
