#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收集 Gemini 裁决文件 -> ADK_ADJUDICATION_LEDGER.json（主会话按账修复，本脚本只读不改数）。"""
import json
from collections import Counter
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")
CD = M2 / "collision_mr"
ADK = CD / "adk"

queues = sorted(ADK.glob("adk_p*.json"))
verdict_count = Counter()
v1_right = rr_right = both_wrong = unclear = equivalent = unjudged = 0
rows = []
missing = []
for q in queues:
    pk = q.stem.replace("adk_p", "")
    vf = ADK / ("adk_verdict_p" + pk + ".json")
    items = json.loads(q.read_text(encoding="utf-8")).get("items", [])
    if not vf.exists():
        unjudged += len(items)
        missing.append(pk)
        continue
    try:
        vdata = json.loads(vf.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        # 半截文件（中断时写盘）按未裁入账，不崩全局
        unjudged += len(items)
        missing.append(pk + "(损坏:" + str(ex.msg)[:20] + ")")
        continue
    vmap = {}
    for v in vdata.get("verdicts", []):
        vmap[(v.get("position"), v.get("field"), (v.get("v1") or "")[:12])] = v
    for it in items:
        v = vmap.get((it.get("position"), it.get("field"), (it.get("v1") or "")[:12]))
        if not v:
            unjudged += 1
            continue
        vd = v.get("verdict")
        verdict_count[vd] += 1
        if vd == "V1对":
            v1_right += 1
        elif vd == "重读对":
            rr_right += 1
        elif vd == "两皆误":
            both_wrong += 1
        elif vd == "等价":
            equivalent += 1
        elif vd == "墨迹不明":
            unclear += 1
        rows.append({"page": int(pk), **{k: it.get(k) for k in ("position", "field", "kind", "v1", "rr")},
                     "verdict": vd, "ink": v.get("ink"), "note": v.get("note")})

total = v1_right + rr_right + both_wrong + equivalent + unclear
ledger = {
    "protocol": "ADK_ADJUDICATION_LEDGER_V1",
    "arbiter": "Gemini（Antigravity，校准卷 9/10 通过 2026-11-17）",
    "queuePages": len(queues),
    "queueItems": v1_right + rr_right + both_wrong + equivalent + unclear + unjudged,
    "stats": {
        "judged": total,
        "V1对": v1_right,
        "重读对": rr_right,
        "两皆误": both_wrong,
        "等价": equivalent,
        "墨迹不明": unclear,
        "unjudged": unjudged,
        "missingPages": missing[:200],
        "verdictBreakdown": dict(verdict_count),
    },
    "rows": rows[:3000],
    "limitations": [
        "裁决人 Gemini 为异族模型（与 GLM 族无关联），经 10 点校准卷 9/10 通过",
        "本台账只收集判决；修复由主会话按 两皆误+V1误读类 行走管线（raw 改→重封→门禁）",
        "unjudged 条目 = 未完成页或行序对不上的条目，随库披露",
    ],
}
out = CD / "ADK_ADJUDICATION_LEDGER.json"
out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
print("台账 ->", out)
print("判定分布:", dict(verdict_count), "| judged", total, "| unjudged", unjudged, "| 缺裁决页", len(missing))
