#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人工校对工作台生成器（build_collation_workbench.py）
=====================================================

按 COLLATION_QUEUE.json 为每个待校页生成一份 Markdown 工作包，写入
literature/workspace_m2_dhs834/collation_workbench/ 并生成总索引 INDEX.md。

工作包内容：页图路径（横带/纵栏）、封存条目全表（四栏+调号）、机械缺陷清单
（调标白名单外 / 净化残留 / 四栏全空）、逐条裁决栏（忠实 / 需修 / 存疑）。

纪律：只读封存件与队列；不改任何数据；重跑可覆盖工作台目录（工作台本身不入封存账）。
"""
import json
import re
from collections import Counter
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
LITERATURE_DIR = TOOLS_DIR.parent
M2 = LITERATURE_DIR / "workspace_m2_dhs834"
OUT = M2 / "collation_workbench"

ALLOWED = {"T00 (無標號)", "T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)",
           "T04 (凹角)", "T05 (平橫)", "T06/T07 (交叉入聲號)", "T99 (污損難辨)"}
BRACKET = re.compile(r"\[[^\]]*\]|〔[^〕]*〕|⟨[^⟩]*⟩")


def page_defects(doc):
    """返回 {position: [缺陷描述...]} 与页级统计。"""
    defects = {}
    stats = Counter()
    for e in doc.get("entries", []):
        pos = e.get("position", 0)
        msgs = []
        for field, label in (("tone_marks_M", "M"), ("tone_marks_R", "R")):
            for t in (e.get(field) or []):
                if str(t).strip() not in ALLOWED:
                    msgs.append(f"调标非规范（{label}栏）: `{t}`")
        sm = e.get("source_M") or ""
        inside = "".join(BRACKET.findall(sm))
        outside = BRACKET.sub(" ", sm)
        if "\u207f" in outside or "\u030d" in outside:
            msgs.append("净化残留（括号外，须修）")
            stats["residue_outside"] += 1
        if "\u207f" in inside or "\u030d" in inside:
            msgs.append("括号内鼻化注记（核对是否良性）")
            stats["residue_in_brackets"] += 1
        cols = [(e.get(k) or "").strip() for k in ("source_L", "source_H", "source_M", "source_R")]
        if all(c in ("", "[空]") for c in cols):
            msgs.append("四栏全空（目验是否漏抄/真空白）")
            stats["four_empty"] += 1
        if msgs:
            defects[pos] = msgs
            stats["entries_with_defects"] += 1
    return defects, stats


def esc(s, n=90):
    s = (s or "").replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n] + "…"


def render_page(row, doc, defects):
    pk = f"{row['page']:04d}"
    base = f"literature/tiles/01_DHS/page_{pk}/pdf_{pk}"
    lines = []
    lines.append(f"# 校对工作包 · p{pk}（severity: {row['severity']}）")
    lines.append("")
    lines.append(f"- 封存件：`literature/workspace_m2_dhs834/blind_read_p{pk}.json`"
                 f"（{len(doc.get('entries', []))} 条）")
    lines.append(f"- 页图：`{base}_band_y0_top.png` · `_band_y1_mid.png` · `_band_y2_bot.png`；"
                 f"纵栏 `_subcol2_hanzi_full.png` / `_subcol3_minnan.png` / `_subcol4_mandarin_right.png`")
    lines.append(f"- 队列备注：{row.get('notes') or '（无）'}")
    lines.append("")
    lines.append("> 裁决：忠实（F）/ 需修（X：写出应录值）/ 存疑（Q：入四账并注明）。"
                 "字面忠实性以图为准，禁止以音韵知识改字。")
    lines.append("")
    lines.append("| position | 裁决 | L | H | M | R | tone_M | tone_R | 缺陷提示 / 你的备注 |")
    lines.append("| ---: | :---: | --- | --- | --- | --- | --- | --- | --- |")
    for e in doc.get("entries", []):
        pos = e.get("position", 0)
        hint = "；".join(defects.get(pos, []))
        tones_m = " ".join(str(t).split(" ")[0] for t in (e.get("tone_marks_M") or []))
        tones_r = " ".join(str(t).split(" ")[0] for t in (e.get("tone_marks_R") or []))
        lines.append(
            f"| {pos} |  | {esc(e.get('source_L'))} | {esc(e.get('source_H'), 40)} | "
            f"{esc(e.get('source_M'), 50)} | {esc(e.get('source_R'), 40)} | {esc(tones_m, 24)} | "
            f"{esc(tones_r, 24)} | {esc(hint, 80)} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    queue = json.loads((M2 / "COLLATION_QUEUE.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    index = []
    total_defect_entries = 0
    for row in queue:
        pk = f"{row['page']:04d}"
        doc = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        defects, stats = page_defects(doc)
        total_defect_entries += stats["entries_with_defects"]
        (OUT / f"p{pk}_{row['severity']}.md").write_text(render_page(row, doc, defects), encoding="utf-8")
        index.append(f"| p{pk} | {row['severity']} | {len(doc.get('entries', []))} | "
                     f"{stats['entries_with_defects']} | [工作包](p{pk}_{row['severity']}.md) |")
    index_md = "\n".join(
        ["# 校对工作台索引（DHS 第一书 · 0030–1140）", "",
         f"共 {len(queue)} 页入队；含缺陷条目 {total_defect_entries} 条。按 severity 处理：high 优先。", "",
         "| 页 | severity | 条目数 | 含缺陷条目 | 工作包 |", "| --- | --- | ---: | ---: | --- |"]
        + index) + "\n"
    (OUT / "INDEX.md").write_text(index_md, encoding="utf-8")
    print(f"[WORKBENCH] {len(queue)} 页工作包 -> {OUT}（含缺陷条目 {total_defect_entries}）")


if __name__ == "__main__":
    main()
