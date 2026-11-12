import json
import zipfile
import os

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

for i in range(5):
    b = reg['batches'][i]
    ev = b.get("evidence_detail", {})
    revs = ev.get("recount_evidence", [])
    print(f"\n--- Batch {i} (pages {b['pages']}) ---")
    for r in revs:
        layer = r.get("layer")
        evidence_path = r.get("evidence")
        basename = os.path.basename(evidence_path)
        sha = r.get("evidence_sha256")
        counts = r.get("per_language_recomputed_counts", {})
        print(f"  Layer: {layer}, File: {basename}, SHA: {sha[:8]}..., Counts: {counts}")
