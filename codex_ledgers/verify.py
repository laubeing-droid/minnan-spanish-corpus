#!/usr/bin/env python3
"""只读复验进行中台账的来源、数量和互证引用。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codex_ledgers"
WORK = ROOT / "literature" / "workspace_m2_dhs834"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    repair, mutual, residual = (read(OUT / name) for name in
                                ("REPAIR_LEDGER.json", "INTERBOOK_FILL_LEDGER.json", "RESIDUAL_LEDGER.json"))
    for doc in (repair, mutual, residual):
        assert doc["status"] == "IN_PROGRESS"
        for source in doc["sources"].values():
            assert hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() == source["sha256"], source["path"]

    historical = repair["historical_reported_applied"]
    assert historical["declared_count"] == historical["observed_sealed_and_raw_equal_old_count"] == len(historical["items"])
    for row in historical["items"]:
        page, position, field = row["page"], row["position"], row["field"]
        seal = read(WORK / f"blind_read_p{page:04d}.json")
        raw = read(WORK / "raw_blind" / f"raw_part_p{page:04d}.json")
        actual_seal = next(e[field] for e in seal["entries"] if e["position"] == position)
        actual_raw = next(e[field] for p in raw["pages"] if p["pdf_page"] == page
                          for e in p["entries"] if e["position"] == position)
        assert (actual_seal, actual_raw) == (row["sealed_current"], row["raw_current"]), (page, position, field)

    counts = mutual["counts"]
    assert mutual["filled_count"] == len(mutual["filled"])
    assert len(mutual["one_group_candidates_not_filled"]) == counts["one_candidate_group_unverified"]
    assert len(mutual["conflicts_not_filled"]) == counts["conflicting_candidate_groups_unverified"]
    assert sum(counts[k] for k in ("one_candidate_group_unverified", "conflicting_candidate_groups_unverified",
                                    "no_candidate_source", "hanzi_missing_or_ambiguous")) == counts["all_current_empty_or_damaged_targets"]
    sources = {row["id"]: row for row in read(ROOT / "codex_M5_preview/candidate_sources.json")["sources"]}
    for target in mutual["one_group_candidates_not_filled"] + mutual["conflicts_not_filled"]:
        assert target["auto_fill"] is False
        for group in target["candidate_groups"]:
            for key in group["source_ids"]:
                source = sources[key]
                assert (source["field"], source["hanzi"]) == (target["field"], target["hanzi"]), key

    m1 = residual["m1"]
    assert m1["queue_items"] == m1["uniquely_matched_judged"] + m1["unjudged_total"]
    for name in ("missing_verdict_pages", "ambiguous_pending_items", "matched_unclear_items"):
        count = {"missing_verdict_pages": "missing_verdict_pages_count",
                 "ambiguous_pending_items": "ambiguous_pending_count",
                 "matched_unclear_items": "matched_unclear_count"}[name]
        assert len(m1[name]) == m1[count], name
    for page in m1["pilot_candidate_pages"]:
        doc = read(ROOT / page["file"])
        items = doc.get("items", doc.get("verdicts", []))
        assert len(items) == page["items"]
        assert sum(item.get("verdict") == "墨迹不明" for item in items) == page["unclear"]
    for page in residual["m3"]["two_column_pages"]:
        doc = read(ROOT / page["file"])
        entries = doc.get("entries") or doc["pages"][0]["entries"]
        assert len(entries) == page["candidate_rows"]
        assert sum("[残]" in str(e.get("source_L", "")) or "[残]" in str(e.get("source_M", ""))
                   for e in entries) == page["rows_containing_partial"]

    m6 = residual["m6"]
    manifest = read(WORK / "BLIND_READ_MANIFEST.json")["pages"]
    assert len(manifest) == m6["primary_gloss_structural_pages"]
    entry_count = 0
    for page in manifest:
        seal = read(WORK / f"blind_read_p{page}.json")
        gloss = read(WORK / "gloss_layer" / f"gloss_p{page}.json")
        positions = [entry["position"] for entry in gloss["entries"]]
        assert gloss["page"] == int(page) and len(positions) == len(set(positions))
        assert set(positions) == {entry["position"] for entry in seal["entries"]}
        assert all(isinstance(entry.get(k), str) and entry[k].strip()
                   for entry in gloss["entries"] for k in ("zh", "en"))
        entry_count += len(positions)
    assert entry_count == m6["primary_gloss_structural_entries"]
    v3_files = sorted((WORK / "gloss_layer_v3").glob("gloss_p*.json"))
    assert len(v3_files) == m6["v3_present_parsed"]
    for path in v3_files:
        read(path)
    missing = sorted(set(manifest) - {path.stem[-4:] for path in v3_files})
    assert missing == m6["v3_missing_pages"] and len(missing) == m6["v3_missing_count"]
    print("PASS: 台账来源、历史现值、互证候选引用、裁决数量及缺页清单")


if __name__ == "__main__":
    main()
