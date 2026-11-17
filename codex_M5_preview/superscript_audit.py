#!/usr/bin/env python3
"""记录旧互证候选中被字母汤忽略或改写的上置字符，供人工及模型复核。"""
import hashlib
import json
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

from preview import soup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SNAPSHOT = "7c38bb8310f4fd5aa16adaee5f88488dccf8749d"


def load(name):
    raw = subprocess.run(["git", "show", f"{SNAPSHOT}:codex_M5_preview/{name}"],
                         cwd=ROOT, check=True, stdout=subprocess.PIPE).stdout
    return json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()


def marks(value):
    return sorted({c for c in value if c.isalpha() and
                   ("SUPERSCRIPT" in unicodedata.name(c, "") or "MODIFIER LETTER" in unicodedata.name(c, ""))})


def main():
    source_doc, source_sha = load("candidate_sources.json")
    target_doc, target_sha = load("candidate_targets.json")
    marked = []
    for row in source_doc["sources"]:
        v1_marks, rr_marks = marks(row["v1"]), marks(row["rr"])
        if not v1_marks and not rr_marks:
            continue
        marked.append({"id": row["id"], "page": row["page"], "position": row["position"],
                       "field": row["field"], "hanzi": row["hanzi"],
                       "v1": row["v1"], "rr": row["rr"],
                       "v1_marks": v1_marks, "rr_marks": rr_marks,
                       "v1_rr_mark_sets_differ": v1_marks != rr_marks,
                       "v1_soup": soup(row["v1"]), "rr_soup": soup(row["rr"]),
                       "rr_ordinal": row["rr_ordinal"], "v1_source": row["v1_source"],
                       "rr_source": row["rr_source"]})
    flagged_ids = {x["id"] for x in marked if x["v1_rr_mark_sets_differ"]}
    affected = []
    for target in target_doc["targets"]:
        hits = sorted({source_id for group in target["candidate_groups"]
                       for source_id in group["source_ids"] if source_id in flagged_ids})
        if hits:
            all_ids = {source_id for group in target["candidate_groups"] for source_id in group["source_ids"]}
            affected.append({"page": target["page"], "position": target["position"],
                             "field": target["field"], "hanzi": target["hanzi"],
                             "status": target["status"], "affected_source_ids": hits,
                             "all_sources_flagged": bool(all_ids) and all_ids <= flagged_ids})
    char_counts = Counter(c for row in marked for value in (row["v1_marks"], row["rr_marks"]) for c in value)
    report = {
        "status": "旧预览的规范化风险统计；均不是已证错误，不可自动填充。",
        "input_version": SNAPSHOT,
        "input_sha256": {"candidate_sources.json": source_sha, "candidate_targets.json": target_sha},
        "definition": "将 Unicode 名称含 SUPERSCRIPT 或 MODIFIER LETTER 且 isalpha 的字符作集合；比较 V1、重读集合。字符性质需核原图，集合统计不检测同字符次数差异。",
        "counts": {
            "candidate_sources": len(source_doc["sources"]),
            "sources_with_special_chars": len(marked),
            "M": sum(x["field"] == "M" for x in marked),
            "R": sum(x["field"] == "R" for x in marked),
            "v1_rr_sets_differ": len(flagged_ids),
            "targets_with_flagged_source": len(affected),
            "targets_with_only_flagged_sources": sum(x["all_sources_flagged"] for x in affected),
            "affected_targets_by_status": dict(Counter(x["status"] for x in affected)),
            "affected_targets_by_field": dict(Counter(x["field"] for x in affected)),
            "special_char_counts_in_v1_and_rr_sets": dict(char_counts),
        },
        "sources": marked,
        "affected_targets": affected,
        "interpretation": "当前 soup 去除 ᶜ 等 Unicode 上置字符，并把 ⁿ 映射为 n；某些上置笔画也可能是声调记号，不能仅据编码判错，亦不能无说明地算作完全同字母。",
    }
    (HERE / "superscript_audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
