#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""甘为霖《厦门音新字典》本地检索（独立把门参考，只读）。

数据：_external_refs/campbell_amoy/main.csv（TongUanLab/CampbellAmoyDict，
MIT 许可；页码按 1961 年第 8 版/2006 年第 19 版 8 刷，非 1913 原版页码）。

用法:
  python literature/tools/campbell_lookup.py --hanji 約
  python literature/tools/campbell_lookup.py --tailo iok
  python literature/tools/campbell_lookup.py --contains iok --limit 20

独立把门使用纪律：本工具只回答「该字/词在约百年前厦门音中的通常读法与
台罗拼法」，作为 17 世纪漳州墨迹的桥接旁证；不能据其拼写改写历史字面，
调类/调值不与项目 T01–T99 几何码互相折算。
"""
import argparse
import csv
import sys
from pathlib import Path

DATA = Path("_external_refs/campbell_amoy/main.csv")


def load():
    with DATA.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="甘字典离线检索（只读旁证）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hanji", help="按汉字精确匹配")
    group.add_argument("--tailo", help="按台罗音节精确匹配（无条件匹配尾调号）")
    group.add_argument("--contains", help="按台罗/白话字子串检索")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if not DATA.exists():
        print("缺数据：先 git clone https://github.com/TongUanLab/CampbellAmoyDict "
              "到 _external_refs/campbell_amoy", file=sys.stderr)
        return 2
    rows = load()

    def strip_tones(s):
        return "".join(c for c in (s or "") if not c.isdigit())

    hits = []
    for r in rows:
        if args.hanji:
            matched = any(args.hanji == h for h in (r["hanji"] or "").split("/") if h)
        elif args.tailo:
            matched = strip_tones(r["tailo"]).lower() == args.tailo.lower()
        else:
            blob = f'{strip_tones(r["tailo"])} {strip_tones(r["poj_unicode"])}'.lower()
            matched = args.contains.lower() in blob
        if matched:
            hits.append(r)
        if len(hits) >= args.limit:
            break
    print(f"# 甘字典命中 {len(hits)} 条（上限 {args.limit}）")
    for r in hits:
        print(f"  汉字: {r['hanji'] or '●'} | 台罗: {r['tailo']} | 白话字: {r['poj_unicode']}"
              f" | 文读: {r['poj_bunim_unicode']} | 页: {r['page_number']}"
              f" | 注: {(r['hanlo_comment'] or r['comment'])[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
