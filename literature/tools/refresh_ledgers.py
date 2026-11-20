#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每批台账刷新：从最新裁决账重算 RESIDUAL.m1 机械计数，刷新合法变化文件的来源钉。

纪律：
- 仅 `sources.adjudication`（ADK_ADJUDICATION_LEDGER.json）是预期变化文件；
  其余任何来源钉不匹配 → FAIL（报警，不自动刷新）。
- 批次史（batch_*）、试点、M3/M5/M6 等人工记录段不动；由书记员按批增补。
- 刷新后须通过 codex_ledgers/verify.py。

用法: python literature/tools/refresh_ledgers.py [--dry-run]
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "codex_ledgers"
WORK = ROOT / "literature" / "workspace_m2_dhs834"
ADK_LEDGER = WORK / "collision_mr" / "ADK_ADJUDICATION_LEDGER.json"
DOCS = ("REPAIR_LEDGER.json", "INTERBOOK_FILL_LEDGER.json", "RESIDUAL_LEDGER.json")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_head():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def main():
    dry = "--dry-run" in sys.argv
    new_hash = sha(ADK_LEDGER)
    led = json.loads(ADK_LEDGER.read_text(encoding="utf-8"))
    stats = led["stats"]

    # 1. 检查三本台账来源钉：仅 adjudication 允许变化
    docs = {}
    for name in DOCS:
        docs[name] = json.loads((OUT / name).read_text(encoding="utf-8-sig"))
    for name, doc in docs.items():
        for key, source in doc.get("sources", {}).items():
            current = sha(ROOT / source["path"])
            if current == source["sha256"]:
                continue
            if key == "adjudication" and source["path"].endswith("ADK_ADJUDICATION_LEDGER.json"):
                source["_new_sha256"] = current  # 待刷新
            elif source["path"].endswith("BLIND_READ_MANIFEST.json"):
                source["_new_sha256"] = current  # 每次封存合法变化，待刷新
            else:
                print(f"[refresh] FAIL 来源钉不匹配且非预期变化文件：{name}.sources.{key} "
                      f"({source['path']})")
                return 2

    # 2. 重算 RESIDUAL.m1 机械计数（批次史/试点段不动）
    m1 = docs["RESIDUAL_LEDGER.json"]["m1"]
    m1["uniquely_matched_judged"] = stats["judged"]
    m1["unjudged_total"] = stats["unjudged"]
    m1["missing_verdict_pages_count"] = len(stats["missingPages"])
    m1["missing_verdict_pages"] = [p.split("(")[0] for p in stats["missingPages"]]
    m1["ambiguous_pending_count"] = len(led.get("pending", []))
    m1["ambiguous_pending_items"] = led.get("pending", [])
    unclear = [r for r in led.get("rows", []) if r.get("verdict") == "墨迹不明"]
    m1["matched_unclear_count"] = len(unclear)
    m1["matched_unclear_items"] = unclear
    assert m1["queue_items"] == m1["uniquely_matched_judged"] + m1["unjudged_total"], "数量守恒失败"

    # 3. 快照元数据
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
    head = git_head()
    for name, doc in docs.items():
        doc["snapshot_utc"] = stamp
        doc["git_head_at_snapshot"] = head
        for source in doc.get("sources", {}).values():
            if "_new_sha256" in source:
                source["sha256"] = source.pop("_new_sha256")

    if dry:
        print("[refresh] DRY-RUN 通过（未写盘）："
              f"judged={stats['judged']} unjudged={stats['unjudged']} "
              f"pending={len(led.get('pending', []))} unclear={len(unclear)} "
              f"missing={len(stats['missingPages'])}")
        return 0
    for name, doc in docs.items():
        (OUT / name).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
    print(f"[refresh] OK 台账已刷新 → 快照 {stamp} head={head[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
