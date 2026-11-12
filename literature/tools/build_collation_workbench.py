#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人工校对工作台生成器（build_collation_workbench.py）v2
=======================================================

覆盖第一书（DHS，PDF 0030–1140）的全部可校对语料 1,103 页，分三类工作包：

  A. 已封存·带标记页（severity high/medium，来自 COLLATION_QUEUE.json）
  B. 已封存·干净页（无标记，severity clean）
  C. M1 独占页（仅 M1 主卷有数据；H/M/R 空壳待回填，severity pending）
     —— C 类工作包列出 M1 的 L 栏与中英释义，可先行校 L 层；H/M/R 待回填裁定后补校。

输出 literature/workspace_m2_dhs834/collation_workbench/（每页一份 md + INDEX.md）。
纪律：只读封存件/队列/M1 主卷；不改任何数据；重跑覆盖工作台目录。
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
LITERATURE_DIR = TOOLS_DIR.parent
M2 = LITERATURE_DIR / "workspace_m2_dhs834"
M1_MASTER = LITERATURE_DIR / "workspace_m1_dhs306" / "DHS_p0835_1140_M1_FULL_5762.json"
OUT = M2 / "collation_workbench"

ALLOWED = {"T00 (無標號)", "T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)",
           "T04 (凹角)", "T05 (平橫)", "T06/T07 (交叉入聲號)", "T99 (污損難辨)"}
BRACKET = re.compile(r"\[[^\]]*\]|〔[^〕]*〕|⟨[^⟩]*⟩")


def esc(s, n=90):
    s = (s or "").replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n] + "…"


def page_defects(doc):
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


def m2_packet(row_or_page, severity, doc, defects):
    page = row_or_page["page"] if isinstance(row_or_page, dict) else row_or_page
    pk = f"{page:04d}"
    base = f"literature/tiles/01_DHS/page_{pk}/pdf_{pk}"
    lines = [f"# 校对工作包 · p{pk}（severity: {severity}）", ""]
    if isinstance(row_or_page, dict):
        lines.append(f"- 队列备注：{row_or_page.get('notes') or '（无）'}")
    lines.append(f"- 封存件：`literature/workspace_m2_dhs834/blind_read_p{pk}.json`（{len(doc.get('entries', []))} 条）")
    lines.append(f"- 页图：`{base}_band_y0_top.png` · `_band_y1_mid.png` · `_band_y2_bot.png`；"
                 f"纵栏 `_subcol2_hanzi_full.png` / `_subcol3_minnan.png` / `_subcol4_mandarin_right.png`")
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


def m1_only_packet(page, entries):
    pk = f"{page:04d}"
    lines = [f"# 校对工作包 · p{pk}（severity: pending——M1 独占页，H/M/R 待回填）", ""]
    lines.append(f"- 本页仅 M1 主卷有数据（{len(entries)} 条）；H/M/R 原稿栏多为空壳/占位，"
                 f"回填裁定（架构师解冻 M1 或另立新账）后才能逐条校音。")
    lines.append(f"- 页图：`literature/tiles/01_DHS/page_{pk}/pdf_{pk}_band_y0_top.png` 等三横带"
                 f"（若未切片，先运行 slice --start {page} --end {page}）。")
    lines.append("- **现在可做**：校 layer_1 的 L 栏（西语词头照录）与 layer_2 中英释义是否忠于图/文献。")
    lines.append("")
    lines.append("| entry_id | L 栏（照录） | 中文释义 | 英文释义 | H/M/R 空壳 | 音系占位 | 你的备注 |")
    lines.append("| --- | --- | --- | --- | :---: | :---: | --- |")
    for e in entries:
        raw = e.get("layer_1_diplomatic_raw", {}) or {}
        l2 = e.get("layer_2_disambiguation", {}) or {}
        ph = e.get("layer_3_historical_phonology", {}) or {}
        hollow = not any((raw.get(k) or "").strip() for k in ("source_H", "source_M", "source_R"))
        placeholder = (ph.get("reconstructed_17th_c_hokkien") or "").strip() in ("sio¹ hue⁵",)
        lines.append(f"| {esc(e.get('entry_id'), 24)} | {esc(raw.get('source_L'))} | "
                     f"{esc(l2.get('zh_disambiguated'), 30)} | {esc(l2.get('en_disambiguated'), 30)} | "
                     f"{'是' if hollow else '否'} | {'是' if placeholder else '否'} |  |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    queue = json.loads((M2 / "COLLATION_QUEUE.json").read_text(encoding="utf-8"))
    manifest = json.loads((M2 / "BLIND_READ_MANIFEST.json").read_text(encoding="utf-8"))
    m2_pages = {int(k) for k in manifest.get("pages", {})}
    flagged = {row["page"] for row in queue}
    clean_pages = sorted(m2_pages - flagged)

    master = json.loads(M1_MASTER.read_text(encoding="utf-8"))
    m1_by_page = defaultdict(list)
    for e in master.get("entries", []):
        la = e.get("layer_0_visual_anchor", {}) or {}
        pp = la.get("page_pdf")
        if pp:
            m1_by_page[int(pp)].append(e)
    m1_only = sorted(p for p in m1_by_page if p not in m2_pages and p >= 835)

    OUT.mkdir(exist_ok=True)
    index_rows = []
    counts = Counter()

    for row in queue:
        pk = f"{row['page']:04d}"
        doc = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        defects, stats = page_defects(doc)
        counts["flagged"] += 1
        counts["defect_entries"] += stats["entries_with_defects"]
        fname = f"p{pk}_{row['severity']}.md"
        (OUT / fname).write_text(m2_packet(row, row["severity"], doc, defects), encoding="utf-8")
        index_rows.append((row["page"], row["severity"], len(doc.get("entries", [])),
                           stats["entries_with_defects"], fname, "A 已封存·带标记"))

    for page in clean_pages:
        pk = f"{page:04d}"
        doc = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        fname = f"p{pk}_clean.md"
        (OUT / fname).write_text(m2_packet(page, "clean", doc, {}), encoding="utf-8")
        index_rows.append((page, "clean", len(doc.get("entries", [])), 0, fname, "B 已封存·干净页"))

    for page in m1_only:
        pk = f"{page:04d}"
        fname = f"p{pk}_pending.md"
        (OUT / fname).write_text(m1_only_packet(page, m1_by_page[page]), encoding="utf-8")
        index_rows.append((page, "pending", len(m1_by_page[page]), 0, fname, "C M1独占·待回填"))
        counts["m1_only"] += 1

    index_rows.sort(key=lambda r: ({"high": 0, "medium": 1, "pending": 2, "clean": 3}.get(r[1], 4), r[0]))
    index_md = "\n".join(
        ["# 校对工作台索引（DHS 第一书 · PDF 0030–1140 全覆盖）", "",
         f"- A 已封存·带标记：{counts['flagged']} 页（含缺陷条目 {counts['defect_entries']} 条）",
         f"- B 已封存·干净页：{counts['clean_pages'] if 'clean_pages' in counts else len(clean_pages)} 页",
         f"- C M1 独占·待回填：{counts['m1_only']} 页（裁定后升格）",
         "- 合计 1,103 页可校对语料 = PDF 1,140 − 29 现代前言 − 8 现代分册页", "",
         "| 页 | severity | 条目数 | 含缺陷 | 工作包 | 类别 |", "| ---: | --- | ---: | ---: | --- | --- |"]
        + [f"| p{r[0]:04d} | {r[1]} | {r[2]} | {r[3]} | [{r[4]}]({r[4]}) | {r[5]} |" for r in index_rows]) + "\n"
    (OUT / "INDEX.md").write_text(index_md, encoding="utf-8")
    print(f"[WORKBENCH] A 带标记 {counts['flagged']} + B 干净 {len(clean_pages)} + C M1独占 {counts['m1_only']}"
          f" = {counts['flagged'] + len(clean_pages) + counts['m1_only']} 页工作包 -> {OUT}")


if __name__ == "__main__":
    main()
