#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复批落地后强制复扫（硬刹车 #12 的自动化工具）。

对当前封存库重跑音系扫查，与基线（PHONOTACTICS_BASELINE.json）比对**硬违类**
（音系非法声母/韵尾、官话非法声母、现代污染）：
  - 无基线        -> 建立基线，退出 0（首跑）
  - 硬违类 <= 基线 -> PASS，更新基线（单调下降允许），退出 0
  - 硬违类 > 基线  -> **熔断**（修复引入了新的音系非法），退出 2，基线不动

软类（稀有韵母、官话存疑韵尾）只报告不熔断——它们是裁决队列的来源，不是修复错误信号。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sweep_phonotactics import run_sweep, HARD_CLASSES  # noqa: E402

M2 = Path(__file__).resolve().parent.parent / "workspace_m2_dhs834"
BASE = M2 / "collision_mr" / "PHONOTACTICS_BASELINE.json"

res = run_sweep()
hard_cls = {k: n for k, n in res["classCounts"].items() if k.startswith(HARD_CLASSES)}
hard_total = sum(hard_cls.values())
soft_cls = {k: n for k, n in res["classCounts"].items() if not k.startswith(HARD_CLASSES)}

if not BASE.exists():
    BASE.write_text(json.dumps({"protocol": "PHONOTACTICS_BASELINE_V1",
                                "hardTotal": hard_total, "hardClasses": hard_cls},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"verdict": "BASELINE_ESTABLISHED", "hardTotal": hard_total,
                      "hardClasses": hard_cls}, ensure_ascii=False))
    sys.exit(0)

base = json.loads(BASE.read_text(encoding="utf-8"))
delta = hard_total - base["hardTotal"]
report = {"verdict": None, "baseline": base["hardTotal"], "current": hard_total,
          "delta": delta, "hardClasses": hard_cls, "baselineClasses": base["hardClasses"],
          "softClasses": soft_cls}

if delta > 0:
    report["verdict"] = "CIRCUIT_BREAK"
    print(json.dumps(report, ensure_ascii=False, indent=1))
    print("硬违类上升 +%.0f：修复引入了新的音系非法——熔断。请回滚修复批并复查。" % delta)
    sys.exit(2)

BASE.write_text(json.dumps({"protocol": "PHONOTACTICS_BASELINE_V1",
                            "hardTotal": hard_total, "hardClasses": hard_cls},
                           ensure_ascii=False, indent=1), encoding="utf-8")
report["verdict"] = "PASS" if delta < 0 else "PASS(持平)"
print(json.dumps(report, ensure_ascii=False, indent=1))
sys.exit(0)
