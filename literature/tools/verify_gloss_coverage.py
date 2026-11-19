#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""释义层只读验收（RSI 2026-11-18 提案，2026-11-19 用户批准实施）。

核对选层与封存件：可解析、page 匹配、逐页 position 集合一致且无重复、
zh/en 非空。缺项或完整性错误退出非零；与释义内容（语义）审校分开报告，
本工具不判断词义正确性。

用法:
  python literature/tools/verify_gloss_coverage.py [--layer main|v2|v3]
                                                   [--pages 0283,0284-0302] [--census]

- 默认（无 --pages --census）：全库核对选层，任何缺页/不齐/非空失败即退出 1。
- --pages：只核指定页（每批释义刷新后的工作流闸）。
- --census：全库普查；缺文件只报告不失败，已存在文件的完整性错误仍失败。

退出码：0 通过；1 覆盖或完整性失败；2 用法错误。
"""
import argparse
import json
import sys
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")
LAYERS = {"main": M2 / "gloss_layer", "v2": M2 / "gloss_layer_v2", "v3": M2 / "gloss_layer_v3"}


def parse_pages(text):
    pages = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            pages.extend(range(int(lo), int(hi) + 1))
        else:
            pages.append(int(part))
    if any(p < 30 or p > 1140 for p in pages):
        raise ValueError("页码须在 0030–1140 内")
    return sorted(set(pages))


def check_page(pk, layer_dir):
    """核对单页；返回 (问题列表, 缺文件布尔)。"""
    issues = []
    path = layer_dir / f"gloss_p{pk}.json"
    if not path.exists():
        return [], True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"不可解析: {exc}"], False
    if not isinstance(data, dict) or data.get("page") != int(pk):
        issues.append("page 字段缺失或与文件页码不一致")
        data_entries = None
    else:
        data_entries = data.get("entries")
    seal_positions, seal_error = seal_positions_for(pk)
    if seal_error:
        issues.append(f"封存件读取失败: {seal_error}")
    if not isinstance(data_entries, list) or any(
            not isinstance(e, dict) or type(e.get("position")) is not int for e in data_entries):
        issues.append("entries 缺失或存在无整数 position 的条目")
        data_entries = []
    positions = [e["position"] for e in data_entries]
    if len(set(positions)) != len(positions):
        issues.append("position 存在重复")
    if not seal_error and set(positions) != seal_positions:
        missing = sorted(seal_positions - set(positions))
        extra = sorted(set(positions) - seal_positions)
        issues.append(f"position 集合与封存不一致（缺 {len(missing)} 项{missing[:8]}，"
                      f"多 {len(extra)} 项{extra[:8]}）")
    for e in data_entries:
        if not isinstance(e, dict):
            continue
        for fld in ("zh", "en"):
            value = e.get(fld)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"position {e.get('position')} 的 {fld} 非空校验失败")
    return issues, False


def seal_positions_for(pk):
    try:
        sealed = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        return ({e["position"] for e in sealed["entries"]}, None)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return set(), str(exc)


def main():
    parser = argparse.ArgumentParser(description="释义层只读验收；内容语义另案审校")
    parser.add_argument("--layer", choices=sorted(LAYERS), default="main")
    parser.add_argument("--pages", help="逗号分隔页码或区间，如 0283,0284-0302")
    parser.add_argument("--census", action="store_true", help="普查模式：缺文件只报告不失败")
    args = parser.parse_args()

    layer_dir = LAYERS[args.layer]
    if args.pages:
        try:
            pages = parse_pages(args.pages)
        except ValueError as exc:
            parser.error(str(exc))
            return 2
        mode = "selected"
    else:
        # 以封存库全集为基准枚举（1,103 页），缺文件在普查模式只报告、
        # 在全库模式作为失败——避免只按已有文件自证覆盖。
        manifests = sorted(M2.glob("blind_read_p*.json"))
        pages = sorted({int(p.stem[len("blind_read_p"):]) for p in manifests})
        mode = "census" if args.census else "full"

    if not layer_dir.exists():
        print(json.dumps({"verdict": "FAIL", "layer": args.layer, "reason": "层目录不存在"},
                         ensure_ascii=False))
        return 1

    checked, missing, failed, issues = 0, [], [], {}
    for pg in pages:
        pk = f"{pg:04d}"
        page_issues, absent = check_page(pk, layer_dir)
        if absent:
            missing.append(pg)
            continue
        checked += 1
        if page_issues:
            failed.append(pg)
            issues[pk] = page_issues
    ok = not failed and (bool(mode == "census") or not missing)
    report = {"verdict": "PASS" if ok else "FAIL", "layer": args.layer, "mode": mode,
              "requestedPages": len(pages), "checked": checked,
              "missingCount": len(missing), "missingPagesFirst": missing[:20],
              "integrityFailedCount": len(failed), "integrityFailedPages": failed,
              "issuesFirst": {k: v[:4] for k, v in list(issues.items())[:10]},
              "note": "内容语义未审校；本工具只验结构与覆盖"}
    print(json.dumps(report, ensure_ascii=False))
    print(f"[gloss:{args.layer}:{mode}] 核对 {checked}/{len(pages)} 页；"
          f"缺文件 {len(missing)}；完整性失败 {len(failed)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
