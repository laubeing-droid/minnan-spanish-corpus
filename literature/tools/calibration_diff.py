#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多份回执对比：逐 identity 输出一致/分歧矩阵（校准与抽验共用，只读）。

用法:
  python literature/tools/calibration_diff.py --files a.json b.json [c.json …] [--labels 名A 名B …]

对比维度：verdict / letters / tone_mark / ink（字母汤层面，经 soup 归一）。
退出码：0=全一致；1=存在分歧；2=用法错误。输出 JSON + 人类可读摘要。
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from repair_batch_a import soup, soup_with_modifiers  # noqa: E402


def load_verdicts(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for v in data.get("verdicts", []):
        key = (v.get("position"), v.get("field"), v.get("v1"), v.get("rr"))
        out[key] = v
    return out


def main():
    parser = argparse.ArgumentParser(description="回执对比（只读）")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--labels", nargs="*")
    args = parser.parse_args()
    if len(args.files) < 2:
        parser.error("至少两份回执")
        return 2
    labels = args.labels or [Path(f).name for f in args.files]
    if len(labels) != len(args.files):
        parser.error("--labels 数量须与 --files 一致")
        return 2

    sources = []
    for f in args.files:
        try:
            sources.append(load_verdicts(f))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[diff] FAIL 读取 {f}: {exc}")
            return 2

    all_keys = set()
    for s in sources:
        all_keys |= set(s.keys())
    # identity 键含 v1/rr 字符串，可能含组合字符——排序仅作稳定输出
    items = []
    disagreements = 0
    for key in sorted(all_keys, key=lambda k: (k[0] or 0, k[1] or "", str(k[2]))):
        per_dim = {}
        for dim in ("verdict", "letters", "tone_mark"):
            values = {s[key].get(dim) for s in sources if key in s}
            per_dim[dim] = sorted(str(v) for v in values)
        inks = set()
        ink_mod = set()
        for s in sources:
            if key in s:
                ink = str(s[key].get("ink") or "")
                inks.add(soup(ink))
                ink_mod.add(soup_with_modifiers(ink))
        ink_uniform = len(inks) == 1
        ink_mod_uniform = len(ink_mod) == 1
        agree = (len(per_dim["verdict"]) == 1 and len(per_dim["letters"]) == 1
                 and len(per_dim["tone_mark"]) == 1 and ink_uniform and ink_mod_uniform)
        if not agree:
            disagreements += 1
        items.append({"position": key[0], "field": key[1],
                      "agree": agree,
                      "verdict": per_dim["verdict"], "letters": per_dim["letters"],
                      "tone_mark": per_dim["tone_mark"],
                      "ink_soup_uniform": ink_uniform,
                      "ink_modifier_uniform": ink_mod_uniform,
                      "ink_variants": sorted(inks) if not ink_uniform else []})
    total = len(items)
    print(json.dumps({"files": args.files, "labels": labels,
                      "total": total, "agree": total - disagreements,
                      "disagree": disagreements,
                      "disagreements": [it for it in items if not it["agree"]]},
                     ensure_ascii=False))
    for it in items:
        if not it["agree"]:
            print(f"[diff] 分歧 pos={it['position']} {it['field']}: "
                  f"verdict={it['verdict']} letters={it['letters']} "
                  f"tone_mark={it['tone_mark']}")
    print(f"[diff] 一致 {total - disagreements}/{total}")
    return 0 if disagreements == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
