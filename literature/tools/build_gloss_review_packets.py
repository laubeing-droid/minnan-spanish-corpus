#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""释义复核工作包生成器（build_gloss_review_packets.py）v1
====================================================

把 GLOSS_REVIEW_QUEUE.json 抽中的页做成**中文复核包**：复核人只依据原书
汉字栏（H）与官话对音栏（R）判定 zh 释义是否贴切，全程不需西班牙语。

  - 复核范围：GLOSS_REVIEW_QUEUE.json 的抽样页（25% 跳抽分层随机）。
  - 每页一份 md：H / M / R 三栏原文 + zh 释义 + 置信 + 释义员备注 + 裁决空列（F/X/Q）。
  - en 层不在本包复核范围（双模型对读另行处理）；L 栏仅作参考背景附注。

输出 literature/workspace_m2_dhs834/gloss_review_workbench/（每页一份 md + INDEX.md）。
纪律：只读封存件与释义层；不改任何数据；重跑覆盖工作台目录。
"""
import json
from collections import Counter
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
LITERATURE_DIR = TOOLS_DIR.parent
M2 = LITERATURE_DIR / "workspace_m2_dhs834"
OUT = M2 / "gloss_review_workbench"

VERDICT_NOTE = ("裁决口径：**F** 忠实（zh 释义与 H 栏字义相符）/ **X** 需改（在备注写出应改值）"
                "/ **Q** 存疑（写一句理由，入账不强判）。判定以 H 栏汉字义为主，"
                "R 栏官话对音为辅；M 栏与 L 栏仅作背景，不要求核。")


def esc(s, n=60):
    s = (s or "").replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n] + "…"


def main() -> None:
    queue = json.loads((M2 / "GLOSS_REVIEW_QUEUE.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)

    index_rows = []
    stats = Counter()
    for row in queue["pages"]:
        page = row["page"]
        pk = f"{page:04d}"
        sealed = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        gloss = json.loads((M2 / "gloss_layer" / f"gloss_p{pk}.json").read_text(encoding="utf-8"))
        by_pos = {e.get("position"): e for e in gloss.get("entries", [])}

        low_n = 0
        med_n = 0
        rows = []
        for e in sealed.get("entries", []):
            pos = e.get("position", 0)
            g = by_pos.get(pos, {})
            zh = g.get("zh") or ""
            conf = g.get("confidence") or ""
            note = g.get("notes") or ""
            if conf == "low":
                low_n += 1
            elif conf == "medium":
                med_n += 1
            rows.append(
                f"| {pos} |  | {esc(e.get('source_H'), 36)} | {esc(e.get('source_M'), 40)} | "
                f"{esc(e.get('source_R'), 24)} | {esc(zh, 44)} | {esc(conf, 8)} | {esc(note, 50)} |"
            )
        total_n = len(sealed.get("entries", []))
        lines = [f"# 释义复核包 · p{pk}（25% 跳抽抽样页）", "",
                 f"- 封存件：`blind_read_p{pk}.json`（{total_n} 条）｜释义层：`gloss_p{pk}.json`",
                 f"- 页图（需对验原图时看）：`literature/tiles/01_DHS/page_{pk}/pdf_{pk}_band_y0_top.png` 等三横带",
                 f"- 本页置信分布：high {total_n - low_n - med_n}｜medium {med_n}｜low {low_n}"
                 f"（low＝释义员自标存疑，medium＝依赖推断，均请过目）", "",
                 VERDICT_NOTE, "",
                 "| pos | 裁决 | H 汉字 | M 原稿音写 | R 官话 | zh 释义 | 置信 | 你的备注 / 应改值 |",
                 "| ---: | :---: | --- | --- | --- | --- | :---: | --- |"] + rows
        lines.append("")
        fname = f"p{pk}.md"
        (OUT / fname).write_text("\n".join(lines), encoding="utf-8")
        index_rows.append((page, len(sealed.get("entries", [])), low_n, med_n, fname))
        stats["pages"] += 1
        stats["entries"] += len(sealed.get("entries", []))
        stats["low"] += low_n
        stats["medium"] += med_n

    index_rows.sort(key=lambda r: (-(r[2] + r[3]), r[0]))  # medium+low 多的排前面
    top = "\n".join(f"- p{r[0]:04d}（low {r[2]} + medium {r[3]}，共 {r[2] + r[3]}/{r[1]} 条）"
                    for r in index_rows[:10])
    index_md = "\n".join(
        ["# 释义复核索引（zh 层 · 25% 跳抽抽样）", "",
         f"- 抽样页 {stats['pages']} 页 / {stats['entries']} 条：high {stats['entries'] - stats['low'] - stats['medium']}"
         f"｜medium {stats['medium']}｜low {stats['low']}（非高置信合计 {stats['low'] + stats['medium']}）",
         "- 复核顺序建议：先做非高置信密集页（下表已按 medium+low 降序），F/X/Q 口径见各包页首",
         "- 本包只复核 **zh 中文释义**；en 层走双模型对读，分歧升级包另行生成", "",
         "## 非高置信最密集的 10 页", top, "",
         "| 页 | 条目 | low | medium | 复核包 |", "| ---: | ---: | ---: | ---: | --- |"]
        + [f"| p{r[0]:04d} | {r[1]} | {r[2]} | {r[3]} | [{r[4]}]({r[4]}) |" for r in index_rows]) + "\n"
    (OUT / "INDEX.md").write_text(index_md, encoding="utf-8")
    print(f"[GLOSS-REVIEW] {stats['pages']} 页 / {stats['entries']} 条复核包"
          f"（low {stats['low']} + medium {stats['medium']}）-> {OUT}")


if __name__ == "__main__":
    main()
