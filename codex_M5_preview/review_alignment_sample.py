#!/usr/bin/env python3
"""复算 M5 三条非盲核图样本及缺项错栏风险；不修改任何正式数据。"""
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

from preview import ROOT, WORK, han_key, soup

OUT = ROOT / "codex_M5_preview"
SNAPSHOT = "7c38bb8310f4fd5aa16adaee5f88488dccf8749d"
CASES = [
    {
        "target": (539, 12, "R", "mid", (360, 790, 2100, 930)),
        "sources": [(46, 3, "R", "top", (100, 560, 2000, 700)),
                    (267, 16, "R", "bot", (240, 390, 1900, 510))],
        "observation": "目标为重复小字词条，汉字隨及 M 栏音写在同一视觉行，R 栏空；两来源同一视觉行隨与 R 字母 chui 可见，附加小记号及调号归属不作推断。",
        "source_limits": {"0046:3:R": "V1 含上置 ᶜ，重读无；其字母或记号性质待核，不作双读完全同字母的依据。"},
    },
    {
        "target": (779, 11, "R", "mid", (240, 865, 1800, 1010)),
        "sources": [(164, 8, "R", "mid", (300, 130, 1900, 300)),
                    (348, 4, "R", "top", (240, 960, 1850, 1130))],
        "observation": "目标为重复小字词条，汉字片及 M 栏字迹在同一视觉行，R 栏空；两来源同行为片与 R 字母 pien，附加小记号及调号归属不作推断。",
        "source_limits": {"0164:8:R": "V1 含上置 ⁿ，重读为普通 n；鼻化、韵尾或记号性质待核，不作双读完全同字母的依据。"},
    },
    {
        "target": (988, 14, "M", "bot", (250, 190, 1700, 340)),
        "sources": [(1043, 3, "M", "top", (200, 725, 1500, 885))],
        "observation": "目标为重复小字词条，汉字韻及 M 栏圈涂残迹在同一视觉行，两次读法均记残；来源同行为韻与 M 字母 un，来源调号归属及目标音调不作推断。目标页存量调标数组非规范，须按现有封存规则延迟。",
        "source_limits": {},
    },
]


def data(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def old_candidate(name):
    raw = subprocess.run(["git", "show", f"{SNAPSHOT}:codex_M5_preview/{name}"],
                         cwd=ROOT, check=True, stdout=subprocess.PIPE).stdout
    return json.loads(raw.decode("utf-8-sig"))


def roman(text):
    text = str(text or "").strip()
    return bool(soup(text)) and not any(c in text for c in "[]〔〕⟨⟩?？�") and not any(han_key(c) for c in text)


def syllables(text):
    return tuple(soup(x) for x in re.split(r"[\s,;:./·\-]+", text) if soup(x))


def page_line(page, position, field):
    sealed = WORK / f"blind_read_p{page:04}.json"
    rr_path = WORK / "reread_mr" / f"reread_mr_p{page:04}.json"
    entries = data(sealed)["entries"]
    rr = data(rr_path)[field.lower() + "_lines"]
    idx, row = next((i, row) for i, row in enumerate(entries) if row["position"] == position)
    return {
        "page": page, "position": position, "field": field,
        "current_source_L": row.get("source_L"), "current_source_H": row.get("source_H"),
        "current_source_M": row.get("source_M"), "current_source_R": row.get("source_R"),
        "current_seal": sealed.relative_to(ROOT).as_posix(),
        "rr_source": rr_path.relative_to(ROOT).as_posix(),
        "rr_ordinal": idx + 1, "entries_count": len(entries), "rr_count": len(rr),
        "rr_same_ordinal": rr[idx] if idx < len(rr) else None,
        "json_paths": {"source_H": f"$.entries[{idx}].source_H",
                       "field": f"$.entries[{idx}].source_{field}",
                       "rr": f"$.{field.lower()}_lines[{idx}]"},
    }


FIELDS = ("source_L", "source_H", "source_M", "source_R", "tone_marks_M", "tone_marks_R")


def raw_comparison(page, position):
    raw_path = WORK / "raw_blind" / f"raw_part_p{page:04}.json"
    pages = data(raw_path)["pages"]
    pi, raw_page = next((i, p) for i, p in enumerate(pages) if p["pdf_page"] == page)
    sealed = data(WORK / f"blind_read_p{page:04}.json")["entries"]
    raw = raw_page["entries"]
    index, raw_target = next((i, e) for i, e in enumerate(raw) if e["position"] == position)
    sealed_by_pos = {e["position"]: e for e in sealed}
    raw_by_pos = {e["position"]: e for e in raw}
    if set(raw_by_pos) != set(sealed_by_pos):
        raise ValueError(f"raw 与封存行集不同: {page}")
    differences = [{"position": pos, "field": f, "raw": raw_by_pos[pos].get(f),
                    "sealed": sealed_by_pos[pos].get(f)}
                   for pos in sorted(raw_by_pos) for f in FIELDS
                   if raw_by_pos[pos].get(f) != sealed_by_pos[pos].get(f)]
    return {"path": raw_path.relative_to(ROOT).as_posix(),
            "json_path": f"$.pages[{pi}].entries[{index}]",
            "target_fields": {f: raw_target.get(f) for f in FIELDS},
            "sealed_target_fields": {f: sealed_by_pos[position].get(f) for f in FIELDS},
            "page_differences": differences, "page_difference_count": len(differences)}


def historical_source(source):
    raw = subprocess.run(["git", "show", source["v1_source"]], cwd=ROOT,
                         check=True, stdout=subprocess.PIPE).stdout
    entries = json.loads(raw.decode("utf-8-sig"))["entries"]
    idx, entry = next((i, e) for i, e in enumerate(entries) if e["position"] == source["position"])
    if entry[f"source_{source['field']}"] != source["v1"] or "".join(entry["source_H"].split()) != source["hanzi"]:
        raise ValueError(f"历史 V1 词条变化: {source['id']}")
    rr = data(ROOT / source["rr_source"])[source["field"].lower() + "_lines"]
    if rr[source["rr_ordinal"] - 1] != source["rr"]:
        raise ValueError(f"重读条目变化: {source['id']}")
    return {"historical_v1_json_path": f"$.entries[{idx}].source_{source['field']}",
            "historical_hanzi_json_path": f"$.entries[{idx}].source_H",
            "rr_json_path": f"$.{source['field'].lower()}_lines[{source['rr_ordinal'] - 1}]"}


def image_region(page, band, bbox):
    index = {"top": 0, "mid": 1, "bot": 2}[band]
    tile_dir = ROOT / "literature" / "tiles" / "01_DHS" / f"page_{page:04}"
    image = tile_dir / f"pdf_{page:04}_band_y{index}_{band}.png"
    manifest = data(tile_dir / f"pdf_{page:04}_tiles_manifest.json")
    expected = next(x["tile_sha256"] for x in manifest["horizontal_bands"] if x["name"] == f"band_y{index}_{band}")
    actual = hashlib.sha256(image.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"原图切带摘要不符: {image}")
    return {"path": image.relative_to(ROOT).as_posix(), "sha256": actual,
            "bbox_xyxy_in_band_pixels": bbox}


def build():
    targets = old_candidate("candidate_targets.json")["targets"]
    source_by_id = {row["id"]: row for row in old_candidate("candidate_sources.json")["sources"]}
    examples = []
    for case in CASES:
        page, position, field, band, bbox = case["target"]
        target = next(x for x in targets if (x["page"], x["position"], x["field"]) == (page, position, field))
        if target["status"] != "一个候选音节组，定位未证":
            raise ValueError(f"目标的候选状态已变化: {page}:{position}:{field}")
        detail = {"target": page_line(page, position, field), "target_image": image_region(page, band, bbox),
                  "hanzi": target["hanzi"], "letter_group": target["candidate_groups"][0]["syllables"],
                  "target_raw_comparison": raw_comparison(page, position),
                  "candidate_group_count": len(target["candidate_groups"]),
                  "candidate_groups": target["candidate_groups"], "conflicting_candidate_groups": [],
                  "group_limit": "唯一仅指旧候选索引；它依赖行序粗筛和旧 soup，不证明全书无异读。",
                  "observation": case["observation"], "sources": [], "auto_fill": False}
        for sp, spos, sf, sb, sbox in case["sources"]:
            source = source_by_id[f"{sp:04}:{spos}:{sf}"]
            if source["id"] not in target["candidate_groups"][0]["source_ids"]:
                raise ValueError(f"来源不属于目标候选组: {source['id']}")
            detail["sources"].append({**page_line(sp, spos, sf), "historical_v1": source["v1"],
                                      "rr_value": source["rr"], "v1_source": source["v1_source"],
                                      "rr_source": source["rr_source"],
                                      "v1_syllables": source["v1_syllables"],
                                      "rr_syllables": source["rr_syllables"],
                                      "reading_mark": "既存 V1 与既存独立重读；本次核图有先验，非新盲读",
                                      "source_limit": case["source_limits"].get(source["id"], "音调与附加记号仍待核"),
                                      **historical_source(source),
                                      "image": image_region(sp, sb, sbox)})
        examples.append(detail)

    risk = Counter()
    risk_rows = []
    for target in targets:
        if target["status"] != "一个候选音节组，定位未证":
            continue
        f = target["field"]
        group = tuple(target["candidate_groups"][0]["syllables"])
        row = page_line(target["page"], target["position"], f)
        other = row["current_source_R" if f == "M" else "current_source_M"]
        rr = row["rr_same_ordinal"]
        matches = lambda value: roman(value) and syllables(value) == group
        flags = []
        if matches(other):
            flags.append("other_column_equal")
        if rr is not None and matches(rr):
            flags.append("same_ordinal_equal_length" if row["entries_count"] == row["rr_count"]
                         else "same_ordinal_unequal_length")
        if row["rr_count"] == 0:
            flags.append("no_rr_column_lines")
        for flag in flags:
            risk[f"{f}_{flag}"] += 1
        if flags:
            risk_rows.append({"page": target["page"], "position": target["position"], "field": f,
                              "hanzi": target["hanzi"], "letter_group": list(group),
                              "other_column": other, "rr_same_ordinal": rr,
                              "entries_count": row["entries_count"], "rr_count": row["rr_count"],
                              "flags": flags})

    def special_chars(value):
        return {c for c in value if c.isalpha() and
                ("SUPERSCRIPT" in unicodedata.name(c, "") or "MODIFIER LETTER" in unicodedata.name(c, ""))}
    special_sources = [x for x in source_by_id.values() if special_chars(x["v1"]) or special_chars(x["rr"])]
    special_different = [x for x in special_sources if special_chars(x["v1"]) != special_chars(x["rr"])]
    result = {
        "status": "已核图的非盲模型候选，未自动填充，须复核",
        "scope": "仅核目标与来源视觉行、汉字及音写字母；未证明目标声调，未作人审，未改变正式数据。",
        "source_snapshot": "66b1a45^",
        "candidate_snapshot": SNAPSHOT,
        "examples": examples,
        "risk_counts_overlapping": dict(risk),
        "risk_rows": risk_rows,
        "superscript_and_modifier_letter_counts": {
            "candidate_sources_total": len(source_by_id), "sources_containing_special_letters": len(special_sources),
            "M": sum(x["field"] == "M" for x in special_sources),
            "R": sum(x["field"] == "R" for x in special_sources),
            "v1_rr_special_character_sets_differ": len(special_different),
            "status": "纯统计，差异未必为错误；原图与记号性质均需复核。"},
        "risk_explanation": "同序号或另一栏同字母仅为疑似错栏/已有墨迹的筛查线索，须看原图；无 R 重读行不证明该页有或无独立官话栏。各旗标可重叠。",
        "confirmed_counterexample": {
            "target": page_line(922, 1, "M"),
            "image": image_region(922, "top", (200, 330, 1800, 520)),
            "observation": "連同行的 lien 位于 M 栏、黑色竖线左侧，现行封存却记 M=[空]、R=lien；不应当作普通互证缺项。",
            "auto_fill": False,
        },
    }
    (OUT / "review_alignment_sample.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"examples": len(examples), "risk_counts_overlapping": dict(risk),
                      "risk_rows": len(risk_rows), "auto_fill": False}, ensure_ascii=False))


if __name__ == "__main__":
    build()
