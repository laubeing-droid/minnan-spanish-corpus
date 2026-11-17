#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复批一键落地驱动器（硬刹车 #12 的管线化）。

用法：python literature/tools/seal_and_verify.py [--source REPAIR_BATCH_A_V4.json]

流程：
  1. 从修复批报告读脏页（默认 REPAIR_BATCH_A_V4.json 的 applied[].page）；
  2. 逐页重封（含存量非规范调标字面的页**单页跳过入账**——学 p0041 先例，修复留 raw 不丢）；
  3. 跑 architect_gatekeeper.py 全库门禁；
  4. 跑 post_repair_verify.py 强制复扫（硬违类单调下降断言，熔断退出 2）。
任一环节 FAIL：退出码非 0，报告指明卡在哪一步——**不带病宣布完成**。
"""
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
M2 = TOOLS.parent / "workspace_m2_dhs834"
ALLOWED = {"T00 (無標號)", "T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)", "T04 (凹角)",
           "T05 (平橫)", "T06/T07 (交叉入聲號)", "T99 (污損難辨)"}

args = sys.argv[1:]
source = M2 / "collision_mr" / "REPAIR_BATCH_A_V4.json"
if "--source" in args:
    source = Path(args[args.index("--source") + 1])

rep = json.loads(source.read_text(encoding="utf-8"))
pages = sorted({int(a["page"]) for a in rep.get("applied", [])})
print("[seal] 修复批脏页:", len(pages))

# 1. 逐页重封（存量非规范调标页单页跳过）
ok = []
defer_tone = []
for pg in pages:
    pk = "%04d" % pg
    raw = json.loads((M2 / ("raw_blind/raw_part_p" + pk + ".json")).read_text(encoding="utf-8"))
    bad_tone = False
    for p0 in raw.get("pages") or []:
        for e in (p0.get("entries") or []):
            for fld in ("tone_marks_M", "tone_marks_R"):
                for t in (e.get(fld) or []):
                    if str(t).strip() not in ALLOWED:
                        bad_tone = True
                        break
                if bad_tone:
                    break
            if bad_tone:
                break
        if bad_tone:
            break
    if bad_tone:
        defer_tone.append(pg)
        print("[seal] p%s 延迟：含存量非规范调标字面（修复留 raw，待调标线）" % pk)
        continue
    out = M2 / ("raw_blind/merged_seal_p" + pk + ".json")
    out.write_bytes(json.dumps(raw, ensure_ascii=False, indent=1).encode("utf-8"))
    r = subprocess.run([sys.executable, str(TOOLS / "zcode_m2_pipeline.py"),
                        "commit", "--input", str(out)], capture_output=True, text=True)
    if r.returncode == 0:
        ok.append(pg)
    else:
        print("[seal] p%s FAIL:" % pk, (r.stderr or r.stdout or "")[-200:])
        defer_tone.append(pg)
print("[seal] 重封完成: %d 页 OK / %d 页延迟" % (len(ok), len(defer_tone)))

# 2. 全库门禁
ROOT = TOOLS.parent.parent
gate = subprocess.run([sys.executable, str(ROOT / "architect_gatekeeper.py")],
                      capture_output=True, text=True)
gate_pass = gate.returncode == 0 and "[FAIL]" not in gate.stdout
print("[gate]", "PASS" if gate_pass else "FAIL")

# 3. 强制复扫（硬刹车 #12）
pv = subprocess.run([sys.executable, str(TOOLS / "post_repair_verify.py")],
                    capture_output=True, text=True)
print("[resweep]", (pv.stdout or "").strip()[-400:])
print("[resweep] exit:", pv.returncode)

verdict = "PASS" if (gate_pass and pv.returncode == 0 and not defer_tone) else \
          "PASS_WITH_DEFERRED" if (gate_pass and pv.returncode == 0) else "FAIL"
print(json.dumps({"verdict": verdict, "sealedPages": len(ok),
                  "deferredTonePages": defer_tone, "gatePass": gate_pass,
                  "resweepExit": pv.returncode}, ensure_ascii=False))
sys.exit(0 if (gate_pass and pv.returncode == 0) else 1)
