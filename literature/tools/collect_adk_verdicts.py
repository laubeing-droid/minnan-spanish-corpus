#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""收集裁决文件 -> ADK_ADJUDICATION_LEDGER.json，不修改任务和裁决文件。"""
import json
from collections import Counter, defaultdict
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")
CD = M2 / "collision_mr"
ADK = CD / "adk"

queues = sorted(ADK.glob("adk_p*.json"))
verdict_count = Counter()
unjudged = queue_items = 0
rows = []
missing = []
pending = []
unmatched_verdicts = []
receipt_sources = []

def identity(row):
    if not isinstance(row, dict) or not isinstance(row.get("position"), int):
        return None
    if not all(isinstance(row.get(k), str) for k in ("field", "v1", "rr")):
        return None
    return (row["position"], row["field"], row["v1"], row["rr"])

for q in queues:
    pk = q.stem.replace("adk_p", "")
    vf = ADK / ("adk_verdict_p" + pk + ".json")
    items = json.loads(q.read_text(encoding="utf-8")).get("items", [])
    queue_items += len(items)
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
    if not isinstance(vdata, dict) or not isinstance(vdata.get("verdicts"), list) or vdata.get("page") != int(pk):
        unjudged += len(items)
        missing.append(pk + "(回执格式或页码错误)")
        continue
    verdicts = vdata["verdicts"]
    receipt_sources.append({"file": vf.as_posix(), "metadata": {k: v for k, v in vdata.items() if k != "verdicts"}})
    item_ids = [identity(it) for it in items]
    item_keys = Counter(k for k in item_ids if k is not None)
    item_values = Counter(k[1:] for k in item_ids if k is not None)
    by_key, by_value, by_position = defaultdict(list), defaultdict(list), defaultdict(list)
    for index, verdict in enumerate(verdicts):
        key = identity(verdict)
        if key is not None:
            by_key[key].append(index)
            by_value[key[1:]].append(index)
            by_position[key[:2]].append(index)
    used = set()
    for index, (it, key) in enumerate(zip(items, item_ids)):
        candidates = by_key.get(key, []) if key is not None else []
        matched = None
        reason = ""
        method = "position_and_values"
        if key is None:
            reason = "任务缺少位置、字段或原文"
        elif item_keys[key] > 1 or len(candidates) > 1:
            reason = "完整键重复"
        elif len(candidates) == 1:
            matched = candidates[0]
        else:
            candidates = by_value.get(key[1:], [])
            if item_values[key[1:]] == 1 and len(candidates) == 1:
                matched = candidates[0]
                method = "unique_values"
            else:
                reason = "原文不匹配" if not candidates else "原文匹配不唯一"
        if matched is not None:
            v = verdicts[matched]
            vd = v.get("verdict")
            if vd not in ("V1对", "重读对", "两皆误", "等价", "墨迹不明"):
                reason = "判决无效"
            elif vd == "两皆误" and not str(v.get("ink") or "").strip():
                reason = "两皆误缺少 ink"
            elif matched in used:
                reason = "回执被重复匹配"
            else:
                used.add(matched)
                verdict_count[vd] += 1
                row = {"page": int(pk), **{k: it.get(k) for k in ("position", "field", "kind", "v1", "rr")},
                       "verdict": vd, "ink": v.get("ink"), "note": v.get("note"),
                       "receipt": {"file": vf.as_posix(), "index": matched + 1,
                                   "position": v.get("position"), "match": method,
                                   "metadata": {k: val for k, val in v.items() if k not in
                                                ("position", "field", "v1", "rr", "verdict", "ink", "note")}}}
                row.update({k: v[k] for k in ("letters", "tone_mark") if k in v})
                rows.append(row)
                continue
        unjudged += 1
        near = set(candidates)
        if key is not None:
            near.update(by_position.get(key[:2], []))
        pending.append({"page": int(pk), "queueIndex": index + 1,
                        **{k: it.get(k) for k in ("position", "field", "kind", "v1", "rr")},
                        "reason": reason, "receipt": vf.as_posix(),
                        "candidateIndexes": [i + 1 for i in sorted(near)]})
    unmatched_verdicts.extend({"page": int(pk), "receipt": vf.as_posix(), "index": i + 1, "value": v}
                              for i, v in enumerate(verdicts) if i not in used)

total = sum(verdict_count.values())
ledger = {
    "protocol": "ADK_ADJUDICATION_LEDGER_V1",
    "arbiter": None,
    "queuePages": len(queues),
    "queueItems": queue_items,
    "stats": {
        "judged": total,
        "V1对": verdict_count["V1对"],
        "重读对": verdict_count["重读对"],
        "两皆误": verdict_count["两皆误"],
        "等价": verdict_count["等价"],
        "墨迹不明": verdict_count["墨迹不明"],
        "unjudged": unjudged,
        "missingPages": missing,
        "verdictBreakdown": dict(verdict_count),
    },
    "rows": rows,
    "pending": pending,
    "unmatchedVerdicts": unmatched_verdicts,
    "receiptSources": receipt_sources,
    "limitations": [
        "裁决来源以回执文件中实际声明的元数据为准；未声明者不推断。",
        "本台账只收集判决；修复需走 raw 改写及重封管线。",
        "未完成页列入 missingPages；有回执但不能唯一匹配的条目列入 pending。",
    ],
}
out = CD / "ADK_ADJUDICATION_LEDGER.json"
out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
print("台账 ->", out)
print("判定分布:", dict(verdict_count), "| judged", total, "| unjudged", unjudged, "| 缺裁决页", len(missing))
