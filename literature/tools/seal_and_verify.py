#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复批一键落地驱动器（硬刹车 #12 的管线化）。

用法：python literature/tools/seal_and_verify.py [--source REPAIR_BATCH_A_V4.json] [--pages 0030,0031]

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
if "--source" in args or "--pages" not in args:
    rep = json.loads(source.read_text(encoding="utf-8"))
    if "status" in rep and rep["status"] != "READY_FOR_SEAL":
        print(json.dumps({"verdict": "FAIL", "reason": "source_not_ready", "status": rep["status"]}, ensure_ascii=False))
        sys.exit(1)
if "--pages" in args:
    pages = sorted({int(x) for x in args[args.index("--pages") + 1].split(",")})
else:
    pages = sorted({int(a["page"]) for a in rep.get("applied", [])})
    # 页集覆盖：显式脏页（如 M3 两栏重构新增页）可经 --pages 注入，默认取修复批账
if not pages:
    print(json.dumps({"verdict": "NO_OP", "reason": "no_pages"}, ensure_ascii=False))
    sys.exit(1)
print("[seal] 修复批脏页:", len(pages))

# 1. 逐页重封（存量非规范调标页单页跳过；其余 commit 错误判 FAIL 不与调标延迟混类）
ok = []
defer_tone = []
commit_errors = []
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
        err = (r.stderr or r.stdout or "")
        if "非规范调标" in err or "normalize_tone_list" in err:
            defer_tone.append(pg)
            print("[seal] p%s 延迟：非规范调标（修复留 raw）" % pk)
        else:
            commit_errors.append({"page": pg, "err": err[-200:]})
            print("[seal] p%s COMMIT_ERROR:" % pk, err[-200:])
print("[seal] 重封完成: %d 页 OK / %d 页调标延迟 / %d 页 commit 错误"
      % (len(ok), len(defer_tone), len(commit_errors)))

# 1b. 覆盖断言：处理页 + 延迟页 + 错误页 必须等于输入页集（Codex RSI 提案）
covered = set(ok) | set(defer_tone) | {c["page"] for c in commit_errors}
coverage_ok = covered == set(pages)
print("[seal] 页集覆盖断言:", "OK" if coverage_ok else "FAIL %s"
      % sorted(set(pages) - covered))

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

verdict = "PASS" if (gate_pass and pv.returncode == 0 and not defer_tone and not commit_errors) else \
          "PASS_WITH_DEFERRED" if (gate_pass and pv.returncode == 0 and not commit_errors) else "FAIL"
print(json.dumps({"verdict": verdict, "sealedPages": len(ok),
                  "deferredTonePages": defer_tone, "commitErrors": commit_errors,
                  "coverageOK": coverage_ok, "gatePass": gate_pass,
                  "resweepExit": pv.returncode}, ensure_ascii=False))
# Codex RSI 提案采纳：commit 错误（非调标延迟）→ 最终 FAIL 非零退出，不得当成功
sys.exit(0 if (gate_pass and pv.returncode == 0 and not commit_errors and coverage_ok) else 1)
