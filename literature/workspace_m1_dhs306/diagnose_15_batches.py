import json
import zipfile
import os

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
REGISTER_FILE = os.path.join(WORKSPACE_ROOT, "literature", "assets", "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]
target_indices = [10, 12, 14, 16, 24, 30, 32, 34, 36, 38, 40, 41, 43, 44, 45]

for idx in target_indices:
    b = batches[idx]
    pkg_name = os.path.basename(b["package_path"])
    zip_path = os.path.join(DHS306_DIR, pkg_name)
    ev = b.get("evidence_detail", {})
    zh = b.get("ZH", {})
    
    print(f"\n=================== BATCH {idx:02d} ({pkg_name[:35]}) ===================")
    print(f"ZH target: {zh}")
    print(f"ev keys: {list(ev.keys())}")
    
    if "recount_source" in ev:
        print(f"  recount_source: {ev['recount_source']}")
    if "fresh_main_recount" in ev:
        fmr = ev["fresh_main_recount"]
        print(f"  fresh_main_recount counts: {fmr.get('counts')}")
        print(f"  fresh_main_recount source: {fmr.get('source')}")
    if "recount_evidence" in ev:
        print(f"  recount_evidence: {ev['recount_evidence']}")
    if "main_row_evidence" in ev:
        print(f"  main_row_evidence: {ev['main_row_evidence']}")
    
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zf:
            tsv_files = [n for n in zf.namelist() if n.endswith('.tsv') and any(k in n for k in ['SEMANTIC', 'REVIEW', 'FIELD'])]
            json_files = [n for n in zf.namelist() if n.endswith('.json') and any(k in n for k in ['TAXONOMY', 'SUBSTANTIVE', 'SEMANTIC', 'REVIEW', 'CANDIDATE', 'REGISTER'])]
            print(f"  Relevant TSVs ({len(tsv_files)}): {tsv_files[:3]}")
            print(f"  Relevant JSONs ({len(json_files)}): {json_files[:3]}")
