#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁决判定 JSON → 正式回执（程序化回显 + 全量校验），供工作流确定性门禁使用。

流程：裁决子代理产出判定 JSON（按 queueIndex 键），本工具从冻结队列程序化
回显 position/field/v1/rr（杜绝手抄错），校验枚举与字段约束后写回执文件。

用法:
  python literature/tools/apply_verdicts.py --page 283 --judgments <判定.json> [--out <回执路径>]

校验规则（任一违反→整页拒绝，退出非零，不写文件）:
  - 判定必须覆盖队列全部 queueIndex，且不得有额外索引
  - verdict ∈ V1对/重读对/两皆误/等价/墨迹不明
  - letters ∈ V1/rr/两皆误/等价，或「待核」（仅当 verdict=墨迹不明，诚实落 pending）
  - tone_mark ∈ 一致/位置差/缺失/存疑
  - verdict=两皆误 → ink 必填且不含未决括注
  - tone_marks_new ∈ T00–T99 允许清单且非空列表；tone_marks_unchanged 须为 true；
    tone_basis 须非空字符串（三选一，可缺省——缺省由修复器延迟）
  - 回执含 arbiter/method 元数据（透传判定文件顶层，供审计）
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from repair_batch_a import ALLOWED, M2, ADK  # noqa: E402

VERDICTS = {"V1对", "重读对", "两皆误", "等价", "墨迹不明"}
LETTERS = {"V1", "rr", "两皆误", "等价", "待核"}
TONE_MARKS = {"一致", "位置差", "缺失", "存疑"}


def main():
    parser = argparse.ArgumentParser(description="判定 JSON → 正式回执（校验+程序化回显）")
    parser.add_argument("--page", required=True, help="PDF 页码")
    parser.add_argument("--judgments", required=True, help="裁决员判定 JSON 路径")
    parser.add_argument("--out", help="回执输出路径（缺省=正式回执位置）")
    parser.add_argument("--allow-subset", action="store_true",
                        help="抽验模式：只校验提供的 queueIndex（不要求覆盖全页），输出亦仅含子集")
    parser.add_argument("--require-full", action="store_true",
                        help="显式声明全页覆盖校验（默认行为；供调用方标记模式）")
    args = parser.parse_args()
    pg = int(args.page)
    pk = f"{pg:04d}"

    qpath = ADK / f"adk_p{pk}.json"
    if not qpath.exists():
        print(f"[apply] FAIL 缺队列文件 {qpath}")
        return 2
    queue = json.loads(qpath.read_text(encoding="utf-8"))
    items = queue.get("items")
    if not isinstance(items, list) or not items:
        print("[apply] FAIL 队列无 items")
        return 2

    jtext = Path(args.judgments).read_text(encoding="utf-8")
    jdata = json.loads(jtext)
    judgments = jdata.get("judgments")
    if not isinstance(judgments, dict):
        print("[apply] FAIL 判定文件缺 judgments 对象（键=queueIndex）")
        return 2

    errors = []
    expected = {str(i) for i in range(1, len(items) + 1)}
    got = set(judgments.keys())
    unknown = got - expected
    if unknown:
        errors.append(f"queueIndex 超出队列：{sorted(unknown)[:10]}")
    if not args.allow_subset and got != expected:
        errors.append(f"queueIndex 覆盖不符：缺 {sorted(expected - got)[:10]} 多 {sorted(got - expected)[:10]}")
    got = got & expected

    verdicts = []
    for idx, item in enumerate(items, 1):
        j = judgments.get(str(idx))
        if j is None:
            continue  # 已计入覆盖错误
        if not isinstance(j, dict):
            errors.append(f"q{idx}: 判定须为对象")
            continue
        v = {"position": item.get("position"), "field": item.get("field"),
             "v1": item.get("v1"), "rr": item.get("rr")}
        vd = j.get("verdict")
        if vd not in VERDICTS:
            errors.append(f"q{idx}: verdict 非法：{vd!r}")
            continue
        letters = j.get("letters")
        if letters not in LETTERS:
            errors.append(f"q{idx}: letters 非法：{letters!r}")
            continue
        if letters == "待核" and vd != "墨迹不明":
            errors.append(f"q{idx}: letters=待核 仅允许 verdict=墨迹不明")
            continue
        tm = j.get("tone_mark")
        if tm not in TONE_MARKS:
            errors.append(f"q{idx}: tone_mark 非法：{tm!r}")
            continue
        v["verdict"], v["letters"], v["tone_mark"] = vd, letters, tm
        ink = j.get("ink")
        if ink is not None and not isinstance(ink, str):
            errors.append(f"q{idx}: ink 须为字符串")
            continue
        ink = (ink or "").strip()
        if ink and ("[" in ink or "]" in ink or "〔" in ink or "〕" in ink):
            errors.append(f"q{idx}: ink 含未决括注（不落盘）：{ink!r}")
            continue
        if vd == "两皆误" and not ink:
            errors.append(f"q{idx}: 两皆误缺 ink")
            continue
        if ink:
            v["ink"] = ink
        if j.get("note") is not None:
            v["note"] = str(j["note"])
        if j.get("evidence") is not None:
            v["evidence"] = str(j["evidence"])
        # 声调处置三选一（可缺省；缺省由修复器延迟待核）
        tnew = j.get("tone_marks_new")
        if tnew is not None:
            # 空数组=裁决员经原图确认该条目无调号（封存数据本存在空数组，如 p019 監定），
            # 合法；非空时逐码校验。2026-11-20 校准盲验乙实证后放开。
            if not isinstance(tnew, list):
                errors.append(f"q{idx}: tone_marks_new 须为数组")
                continue
            if any(t not in ALLOWED for t in tnew):
                errors.append(f"q{idx}: tone_marks_new 含允许清单外代码")
                continue
            v["tone_marks_new"] = tnew
        if j.get("tone_marks_unchanged") is not None:
            if j["tone_marks_unchanged"] is not True:
                errors.append(f"q{idx}: tone_marks_unchanged 只接受 true")
                continue
            v["tone_marks_unchanged"] = True
        basis = j.get("tone_basis")
        if basis is not None:
            if not isinstance(basis, str) or not basis.strip():
                errors.append(f"q{idx}: tone_basis 须非空字符串")
                continue
            v["tone_basis"] = basis.strip()
        verdicts.append(v)

    if errors:
        print("[apply] FAIL 整页拒绝：")
        for e in errors[:20]:
            print("  -", e)
        return 1

    out = Path(args.out) if args.out else (ADK / f"adk_verdict_p{pk}.json")
    payload = {"page": pg,
               "arbiter": str(jdata.get("arbiter", "unknown")),
               "method": str(jdata.get("method", "unspecified")),
               "verdicts": verdicts}
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(out)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"[apply] OK {out}（{len(verdicts)} 条）sha256={sha[:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
