#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校准卷判卷：Gemini 答案 vs 主会话墨迹真值（字母汤比对——去声调符/去空格/小写）。"""
import json
import re
import unicodedata
from pathlib import Path

ANS = Path("_scratch_p0257/gemini_calibration_answers.json")

def soup(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace("ⁿ", "n")
    return re.sub(r"[^a-z0-9]", "", s.lower())

# 真值：主会话墨迹判读（排除 2 条首字母存疑行）
TRUTH = {
    "cropA": {0: "ante.", 2: "fo fva", 3: "yō fvā", 4: "yo.", 5: "chiē̃ pē"},   # 行1(0基) hiūfvā 首字母存疑，不入评分
    "cropB": {0: "chiē̃ pē", 1: "piēn", 3: "tāū cōu", 4: "cûa pūe", 5: "cûa ciòng guêng pūē", 6: "Pēŋ."},  # 行2(0基2) ŷuān 首字母存疑，不入评分
    "cropC": {0: "aña ti Zūñ tûñ"},  # 难题试金：预计各家都会失分，单独看
    "cropD_hanzi": {0: "割 皮", 1: "割玉脛皮"},
}

if not ANS.exists():
    raise SystemExit("答案文件不存在：先让 Gemini 完成 _scratch_p0257/GEMINI_CALIBRATION_PROMPT.md")

ans = json.loads(ANS.read_text(encoding="utf-8"))
core_total = core_pass = 0
rows = []
for crop in ("cropA", "cropB", "cropC", "cropD_hanzi"):
    got = ans.get(crop) or []
    for idx, truth in TRUTH[crop].items():
        g = got[idx] if idx < len(got) else "[未答]"
        ok = soup(g) == soup(truth)
        hard = crop == "cropC"
        if not hard:
            core_total += 1
            core_pass += ok
        rows.append((crop, idx, truth, g, ok, hard))

print("%-6s %4s  %-24s %-24s %s" % ("crop", "行", "真值", "Gemini", "判"))
for crop, idx, truth, g, ok, hard in rows:
    tag = "难题" if hard else ("PASS" if ok else "FAIL")
    print("%-6s %4d  %-24s %-24s %s" % (crop, idx + 1, truth, g, tag))

print()
print("核心题： %d/%d 通过（门槛 ≥8/10）" % (core_pass, core_total))
if core_total:
    print("结论：", "校准通过——放全量" if core_pass >= 8 else "校准未过——Gemini 不具备裁判资格，退 $max 抽样方案")
# 汤级一致的行也单独列（声调符位置差=等价仍算过，因为 soup 比对天然忽略声调符）
