import json
import zipfile
import glob
import os

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

for b_idx in [38, 40, 41, 43, 44, 45]:
    b = reg['batches'][b_idx]
    pkg_name = os.path.basename(b['package_path'])
    pkg_file = os.path.join("literature/assets/dhs306", pkg_name)
    print(f"\n--- Batch {b_idx} ({pkg_name}) ---")
    print("ZH target:", b.get('ZH'))
    if not os.path.exists(pkg_file):
        print("FILE NOT FOUND:", pkg_file)
        continue
    with zipfile.ZipFile(pkg_file, 'r') as zf:
        for n in zf.namelist():
            if any(k in n for k in ["SUBSTANTIVE", "FINAL_L", "CANDIDATE_DATA", "REVIEW", "TAXONOMY"]) and (n.endswith(".json") or n.endswith(".tsv")):
                print(" ", n)
