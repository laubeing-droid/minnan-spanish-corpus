#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校准卷判卷 v2（判卷口径已封存：CALIBRATION_STANDARD_V1.json）。

用法：
  python literature/tools/grade_calibration.py [answers_json]
  python literature/tools/grade_calibration.py --selftest

v2 修复（Codex RSI 提案，2026-11-17 审批）：
  - 汉字虚假通过：soup() 曾把汉字删成空串致任意答案含 [未答] 皆过；cropD 改 CJK 精确比对
  - 题数口径：判级真值/门槛全部读自封存标准（core 9 条、≥8/9 且汉字 2/2），不再硬编码
  - 真值核实后冻结：y0 段 4 行降级排除（f/t/Z 三形混淆族等），排除行不评分只记录
  - 兼容原提示词的 cropD_hanzi、保留鼻尾 ŋ；核心题数不符时返回 2 且不判卷
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STD = TOOLS.parent / "workspace_m2_dhs834" / "collision_mr" / "calibration" / "CALIBRATION_STANDARD_V1.json"

def soup(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).replace("ⁿ", "n")
    return "".join(ch for ch in s.lower() if ch.isalnum())

def cjk(s: str) -> str:
    return re.sub(r"\s+", "", s or "")

def core_count(std):
    return sum(bool(line.get("core")) and not line.get("hard")
               for crop in std["crops"].values() for line in crop["lines"])

def selftest():
    std = json.loads(STD.read_text(encoding="utf-8"))
    cases = std.get("selftest", [])
    ok = 0
    for c in cases:
        got_pass = cjk(c["got"]) == cjk(c["truth"])
        expect_pass = c["expect"] == "PASS"
        r = "PASS" if got_pass == expect_pass else "判卷器自身错误"
        print("  selftest [%s] -> %s" % (c["case"], r))
        ok += r == "PASS"
    checks = [("ŋ 不得丢失", soup("Pēŋ") != soup("Pe")),
              ("核心题数与标准一致", core_count(std) == std["grading"]["coreCount"])]
    for name, passed in checks:
        print("  selftest [%s] -> %s" % (name, "PASS" if passed else "判卷标准或程序错误"))
        ok += passed
    total = len(cases) + len(checks)
    print("selftest: %d/%d" % (ok, total))
    return ok == total

def main(answers_path: Path) -> int:
    std = json.loads(STD.read_text(encoding="utf-8"))
    count = core_count(std)
    expected = std["grading"]["coreCount"]
    if count != expected:
        print("判卷标准无效：核心题标记 %d 条，标准要求 %d 条；未判卷。" % (count, expected))
        return 2
    ans = json.loads(answers_path.read_text(encoding="utf-8"))

    core_total = core_pass = 0
    rows = []
    hard_rows = []
    for crop, spec in std["crops"].items():
        got = (ans.get("cropD_hanzi", ans.get(crop)) if crop == "cropD" else ans.get(crop)) or []
        cjk_mode = spec.get("compare") == "CJK_EXACT"
        for ln in spec["lines"]:
            idx = ln["idx"]
            g = got[idx] if idx < len(got) else "[未答]"
            if cjk_mode:
                ok = cjk(g) == cjk(ln["truth"])
            else:
                ok = soup(g) == soup(ln["truth"])
            row = (crop, idx + 1, ln["truth"], g, ok, ln.get("core", False),
                   ln.get("verify", "")[:40], ln.get("hard", False))
            rows.append(row)
            if ln.get("hard"):
                hard_rows.append(row)
            elif ln.get("core", False):
                core_total += 1
                core_pass += ok

    print("%-6s %4s  %-24s %-24s %-5s %s" % ("crop", "行", "真值", "答案", "判", "核心"))
    for crop, idx, truth, g, ok, core, verify, hard in rows:
        mark = "难题" if hard else ("PASS" if ok else "FAIL")
        print("%-6s %4d  %-24s %-24s %-5s %s" % (crop, idx, truth, g, mark, "★" if core else "-"))

    hanzi = [r for r in rows if r[0] == "cropD"]
    hanzi_pass = sum(1 for r in hanzi if r[4])
    print()
    print("核心题： %d/%d 通过（冻结门槛：≥%d/%d 且汉字 %d/%d）"
          % (core_pass, core_total, std["grading"]["coreCount"] - 1, std["grading"]["coreCount"], hanzi_pass, len(hanzi)))
    gate = core_pass >= 8 and core_total == std["grading"]["coreCount"] and len(hanzi) == 2 and hanzi_pass == 2
    print("校准结论：", "通过——可执行 M1" if gate else "未通过——不得执行 M1")
    if hard_rows:
        print("难题试金（不入门槛）：")
        for crop, idx, truth, g, ok, core, verify, hard in hard_rows:
            print("  %-6s %s: 真值 %r | 答案 %r | %s" % (crop, idx, truth, g, "撞对" if ok else "未撞对"))
    return 0 if gate else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    ap = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_scratch_p0257/codex_calibration_answers.json")
    sys.exit(main(ap))
