#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批 A 修复器 v4：判决行直接对封存件现值应用（不经队列中转）。
- 陈旧自检：soup(现值)==soup(ink) 跳过（含 p0257 等已修页自动去重）
- 两栏版式页（0030-0040）剥离批 B
- 音系门禁：M 栏 ink 不得带 f/v/w/x 声母；R 栏不得带 v 声母（v 字形疑书写习惯类，照录不修）
- 合成 raw 输出；重封由主会话跑 commit 管线
"""
import json
import re
import unicodedata
from pathlib import Path
from collections import Counter

M2 = Path("literature/workspace_m2_dhs834")
ADK = M2 / "collision_mr" / "adk"

def soup(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).replace("ⁿ", "n")
    return re.sub(r"[^a-z0-9]", "", s.lower())

def strip_marks(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def synth_raw(pk4, entries):
    by_pos = {int(e.get("position") or 0): e for e in entries}
    return {"pages": [{"pdf_page": int(pk4), "historical_folio": "", "page_header": "",
                       "page_footer_printed": "", "page_footer_handwritten": "",
                       "entries": sorted(by_pos.values(), key=lambda x: int(x.get("position") or 0))}]}

# Phase 0: 回滚上一轮（v3/v4 的脏页）——从封存件重新合成
prev = json.loads((M2 / "collision_mr" / "REPAIR_BATCH_A_V4.json").read_text(encoding="utf-8"))
touched = sorted({int(a["page"]) for a in prev.get("applied", [])} |
                 {int(p) for p in prev.get("dirtyPages", []) if isinstance(p, int)})
for pg in touched:
    pk4 = "%04d" % pg
    sealed = json.loads((M2 / ("blind_read_p" + pk4 + ".json")).read_text(encoding="utf-8")).get("entries", [])
    (M2 / "raw_blind" / ("raw_part_p" + pk4 + ".json")).write_bytes(
        json.dumps(synth_raw(pk4, sealed), ensure_ascii=False, indent=1).encode("utf-8"))
print("Phase 0 回滚:", len(touched), "页")

applied = []
deferred = []
n_noink = n_equal = n_noentry = n_stale_drift = 0
dirty = {}
batch_b_pages = set()
batch_b_rows = []

for vf in sorted(ADK.glob("adk_verdict_p*.json")):
    pk4 = vf.stem.replace("adk_verdict_p", "")
    pg = int(pk4)
    sealed = json.loads((M2 / ("blind_read_p" + pk4 + ".json")).read_text(encoding="utf-8")).get("entries", [])
    by_pos = {int(e.get("position") or 0): e for e in sealed}
    try:
        vdata = json.loads(vf.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        continue
    for v in vdata.get("verdicts", []):
        pos = int(v.get("position") or 0)
        fld = str(v.get("field") or "")
        ink = (v.get("ink") or "").strip()
        vd = v.get("verdict") or ""
        if not ink or vd == "墨迹不明":
            n_noink += 1
            continue
        if pg in range(30, 41):
            batch_b_pages.add(pg)
            batch_b_rows.append({"page": pg, "position": pos, "field": fld,
                                 "v1": v.get("v1"), "rr": v.get("rr"), "ink": ink, "verdict": vd})
            continue
        e = by_pos.get(pos)
        if e is None or fld not in e:
            n_noentry += 1
            continue
        cur = str(e.get(fld) or "")
        si, sv = soup(ink), soup(cur)
        stale_drift = False
        sv1 = soup(v.get("v1"))
        if si == sv:
            n_equal += 1
            continue
        if sv != sv1:
            stale_drift = True  # 现值与判决时 V1 不同（先前已修或他修）
        fld_short = "M" if fld.endswith("M") else ("R" if fld.endswith("R") else "")
        st = strip_marks(ink).lower()
        legal = (st[0] not in "fvwx") if (fld_short == "M" and st) else \
                (st[0] != "v") if (fld_short == "R" and st) else True
        if not legal:
            deferred.append({"page": pg, "position": pos, "field": fld, "v1": v.get("v1"),
                             "ink": ink, "verdict": vd,
                             "reason": "ink 音系非法（f/v/w/x/v 声母）——疑书写习惯类照录或误读，不自动改"})
            continue
        e[fld] = ink
        dirty.setdefault(pk4, None)
        applied.append({"page": pg, "position": pos, "field": fld, "old": cur, "new": ink,
                        "verdict": vd, "staleDrift": stale_drift})
        if stale_drift:
            n_stale_drift += 1

for pk4 in dirty:
    sealed = json.loads((M2 / ("blind_read_p" + pk4 + ".json")).read_text(encoding="utf-8")).get("entries", [])
    (M2 / "raw_blind" / ("raw_part_p" + pk4 + ".json")).write_bytes(
        json.dumps(synth_raw(pk4, sealed), ensure_ascii=False, indent=1).encode("utf-8"))

cls = Counter(a["verdict"] for a in applied)
out = {
    "protocol": "REPAIR_BATCH_A_V4",
    "rolledBackPrev": len(prev.get("dirtyPages", [])),
    "appliedCount": len(applied),
    "pagesTouched": len(dirty),
    "staleDriftApplied": n_stale_drift,
    "verdictBreakdown": dict(cls),
    "deferredCount": len(deferred),
    "deferred": deferred[:1000],
    "skipped": {"ink空/不明": n_noink, "字母汤等价(含已修页自动去重)": n_equal, "条目缺位": n_noentry},
    "batchB": {"pages": sorted(batch_b_pages), "rows": batch_b_rows},
    "applied": applied,
}
Path(M2 / "collision_mr" / "REPAIR_BATCH_A_V4.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("Phase 3 应用:", len(applied), "条 /", len(dirty), "页 | 判定构成:", dict(cls), "| 陈旧漂移应用:", n_stale_drift)
print("门禁延迟:", len(deferred), "| 两栏页剥离:", len(batch_b_rows), "行 /", len(batch_b_pages), "页")
print("跳过: 墨迹空", n_noink, "| 汤等价(含已修自动去重)", n_equal, "| 条目缺位", n_noentry)
print("修复样本 10:")
for a in applied[:10]:
    print("  p%04d pos%s %s: %r -> %r [%s]" % (a["page"], a["position"], a["field"], a["old"], a["new"], a["verdict"]))
print()
print("下一步（重封+门禁+强制复扫一键）：python literature/tools/seal_and_verify.py")
