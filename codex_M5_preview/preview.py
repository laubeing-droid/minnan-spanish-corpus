#!/usr/bin/env python3
"""只读的同书互证候选；所有按行序的对应都需要原图复核。"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "literature" / "tools"))
from repair_batch_a import soup

WORK = ROOT / "literature" / "workspace_m2_dhs834"
OUT = ROOT / "codex_M5_preview"
BASE = "66b1a45^"
MANIFEST = "literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json"
ANCHOR = re.compile(r"第\s*(\d{1,2})\s*行\s*[（(]([^()（）]{1,25})[）)]")


def han_key(text):
    text = "".join(str(text or "").split())
    def han(c):
        n = ord(c)
        return 0x3400 <= n <= 0x9FFF or 0xF900 <= n <= 0xFAFF or 0x20000 <= n <= 0x323AF
    return text if text and all(han(c) for c in text) else ""


def index_letters(text):
    text = unicodedata.normalize("NFD", str(text or "")).lower()
    return "".join(c if unicodedata.category(c) == "Lm" or
                   unicodedata.name(c, "").startswith("COMBINING LATIN") else soup(c) for c in text)


def roman(text):
    text = str(text or "").strip()
    return bool(index_letters(text)) and not any(c in text for c in "[]〔〕⟨⟩?？�") and not any(
        han_key(c) for c in text
    )


def syllables(text):
    return tuple(index_letters(x) for x in re.split(r"[\s,;:./·\-]+", text) if index_letters(x))


def old_pages(pages, manifest):
    paths = [f"literature/workspace_m2_dhs834/blind_read_p{p}.json" for p in pages]
    result = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, check=True,
                            input="".join(f"{BASE}:{p}\n" for p in paths).encode(),
                            stdout=subprocess.PIPE)
    buf, offset, docs = result.stdout, 0, {}
    for page in pages:
        end = buf.index(b"\n", offset)
        head = buf[offset:end].decode("ascii").split()
        if len(head) != 3 or head[1] != "blob":
            raise ValueError(f"无法读取历史 V1：{page}")
        size = int(head[2]); offset = end + 1
        raw = buf[offset:offset + size]; offset += size + 1
        if hashlib.sha256(raw).hexdigest() != manifest[page]["blind_first_read_sha256"]:
            raise ValueError(f"历史 V1 摘要不一致：{page}")
        docs[page] = json.loads(raw.decode("utf-8-sig"))
    return docs


def build():
    old = json.loads(subprocess.run(["git", "show", f"{BASE}:{MANIFEST}"], cwd=ROOT,
                                    check=True, stdout=subprocess.PIPE).stdout.decode("utf-8-sig"))["pages"]
    current = json.loads((WORK / "BLIND_READ_MANIFEST.json").read_text(encoding="utf-8-sig"))["pages"]
    changed = [p for p in sorted(current) if p in old and
               old[p]["blind_first_read_sha256"] != current[p]["blind_first_read_sha256"]]
    snapshots = old_pages(changed, old)
    stats = Counter()
    sources, targets, anchors = [], [], []
    indexed = defaultdict(list)
    for page in sorted(current):
        sealed_path = WORK / f"blind_read_p{page}.json"
        rr_path = WORK / "reread_mr" / f"reread_mr_p{page}.json"
        data = sealed_path.read_bytes()
        if hashlib.sha256(data).hexdigest() != current[page]["blind_first_read_sha256"]:
            raise ValueError(f"现行封存清册摘要不一致：{page}")
        doc = json.loads(data.decode("utf-8-sig")); rr = json.loads(rr_path.read_text(encoding="utf-8-sig"))
        v1 = snapshots.get(page, doc) if page in old else None
        entries = doc["entries"]
        current_by_pos = {e["position"]: e for e in entries}
        stats["pages"] += 1
        if v1 is None:
            stats["pages_without_pre_reread_v1"] += 1
        else:
            stats["v1_snapshot_changed"] += page in snapshots
        for e in entries:
            h = han_key(e.get("source_H"))
            for field in ("M", "R"):
                value = e.get(f"source_{field}")
                if value not in ("[空]", "[残]"):
                    continue
                stats[f"target_{field}"] += 1
                if not h:
                    stats[f"target_{field}_without_exact_hanzi"] += 1
                targets.append({"page": int(page), "position": e["position"], "field": field,
                                "hanzi": h, "hanzi_raw": e.get("source_H", ""),
                                "current": value, "auto_fill": False})
        if v1 is None:
            continue
        ve = v1["entries"]
        for match in ANCHOR.finditer(str(rr.get("notes", ""))):
            number, raw_h = match.groups()
            h = han_key(raw_h)
            if not h:
                continue
            hits = [e["position"] for e in ve if han_key(e.get("source_H")) == h]
            anchors.append({"page": int(page), "rr_note_line": int(number), "hanzi": h,
                            "v1_positions": hits, "note_excerpt": match.group(0),
                            "status": "备注不是已证实行定位，需原图复核", "auto_fill": False})
        for field in ("M", "R"):
            lines = rr[f"{field.lower()}_lines"]
            if len(ve) != len(lines):
                stats[f"{field}_line_count_mismatch_pages"] += 1
                continue
            stats[f"{field}_line_count_equal_pages"] += 1
            for i, (e, reread) in enumerate(zip(ve, lines)):
                h = han_key(e.get("source_H")); value = e.get(f"source_{field}", "")
                current_row = current_by_pos.get(e["position"], {})
                if not h or han_key(current_row.get("source_H")) != h or not roman(value) or not roman(reread):
                    continue
                if soup(value) != soup(reread):
                    continue
                if index_letters(value) != index_letters(reread):
                    stats[f"{field}_modifier_disagreements_excluded"] += 1
                    continue
                # ponytail: this is a review candidate, not a positional alignment or a fill source.
                row = {"id": f"{page}:{e['position']}:{field}", "page": int(page),
                       "position": e["position"], "field": field, "hanzi": h,
                       "v1": value, "rr": reread, "rr_ordinal": i + 1,
                       "v1_syllables": syllables(value), "rr_syllables": syllables(reread),
                       "syllables_match": syllables(value) == syllables(reread),
                       "current_value": current_row.get(f"source_{field}"),
                       "v1_source": f"{BASE}:{sealed_path.relative_to(ROOT).as_posix()}",
                       "rr_source": rr_path.relative_to(ROOT).as_posix(),
                       "basis": "同序号且字母汤相同；行号仅为候选线索", "auto_fill": False}
                sources.append(row)
                indexed[(h, field)].append(row)
                stats[f"candidate_source_{field}"] += 1
    for target in targets:
        rows = indexed.get((target["hanzi"], target["field"]), [])
        groups = defaultdict(list)
        for row in rows:
            groups[row["v1_syllables"]].append(row["id"])
        target["candidate_groups"] = [{"syllables": key, "source_ids": ids} for key, ids in sorted(groups.items())]
        status = ("汉字缺损或歧义" if not target["hanzi"] else
                  "无候选来源" if not groups else
                  "一个候选音节组，定位未证" if len(groups) == 1 else "候选音节组冲突，定位未证")
        target["status"] = status
        stats[f"target_{target['field']}_{status}"] += 1
    repeats = [rows for rows in indexed.values() if len(rows) > 1]
    stats["repeated_hanzi_field_groups"] = len(repeats)
    stats["sources_in_repeated_hanzi_field_groups"] = sum(len(rows) for rows in repeats)
    stats["extra_source_occurrences"] = sum(len(rows) - 1 for rows in repeats)
    stats["note_hanzi_anchors"] = len(anchors)
    stats["note_unique_v1_hanzi_anchors"] = sum(len(x["v1_positions"]) == 1 for x in anchors)
    stats["note_unique_anchor_position_disagrees"] = sum(
        len(x["v1_positions"]) == 1 and x["v1_positions"][0] != x["rr_note_line"] for x in anchors)
    stats["proven_auto_fill_sources"] = 0
    meta = {"status": "只读候选，全部不可自动回填", "auto_fill": False, "v1_git_revision": BASE,
            "limits": ["同序号和同值不证明同行", "notes 行号可能出错", "候选汉字未完成独立复核",
                       "拉丁字母可能包含西语旁注", "声调变体保留原文", "上置或修饰字母按原字符保留", "音节拆分差异未裁定"]}
    OUT.mkdir(exist_ok=True)
    for name, body in (("summary.json", dict(meta, counts=dict(stats))),
                       ("candidate_sources.json", dict(meta, sources=sources)),
                       ("candidate_targets.json", dict(meta, targets=targets)),
                       ("note_anchors.json", dict(meta, anchors=anchors))):
        (OUT / name).write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(meta, counts=dict(stats)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
