"""
Generate Batch 01 (First 50 PARTIAL entries) Disambiguation for Milestone M1,
strictly adhering to the 6-Layer Architecture (v3.1 Final Approved Blueprint):
- Layer 0: Visual Anchor (Coordinates, page, position)
- Layer 1: Diplomatic Raw Visual (Exact original L/H/M/R, including unexpanded abbreviations)
- Layer 2: Philological / Syntactic Disambiguation (Expanded abbreviations, explicit syntax, Chinese/English disambiguated translation)
- Layer 3: 17th-century Minnan Phonological Reconstruction (Historical Hokkien IPA / 7-tone classification T01~T07)
- Layer 4: Modern Taiwanese Romanization (MOE Tâi-lô benchmark)
- Layer 5: Semantic & Cultural Relation Tagging (TAG-1 ~ TAG-5)
"""

import json
import zipfile
import re
import os

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
ASSETS_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets")
DHS306_DIR = os.path.join(ASSETS_DIR, "dhs306")
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "literature", "workspace_m1_dhs306", "batch_01_m1_disambiguated_50.json")

# 1. Load baseline texts for DHS 835 - 844
baselines = {}
for zip_name, pages in [("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip", range(835, 840)),
                        ("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip", range(840, 845))]:
    zip_path = os.path.join(DHS306_DIR, zip_name)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for p in pages:
            matches = [n for n in zf.namelist() if f"DHS_P{p:04d}" in n and "BASELINE" in n and n.endswith(".md")]
            if matches:
                content = zf.read(matches[0]).decode('utf-8')
                # Parse positions
                pos_blocks = re.split(r'\n(?=\d{2}\s*\n)', content)
                p_map = {}
                for b in pos_blocks:
                    m = re.match(r'^(\d{2})\s*\nL:\s*(.*?)\nH:\s*(.*?)\nM:\s*(.*?)\nR:\s*(.*?)(?=\n\n|\Z)', b, re.DOTALL)
                    if m:
                        pos_num = int(m.group(1))
                        p_map[pos_num] = {
                            "L": m.group(2).strip(),
                            "H": m.group(3).strip(),
                            "M": m.group(4).strip(),
                            "R": m.group(5).strip()
                        }
                baselines[p] = p_map

# 2. Collect 36 partials from Batch 00 and 14 from Batch 01
selected_partials = []

# Batch 00
with zipfile.ZipFile(os.path.join(DHS306_DIR, "DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"), 'r') as zf:
    tax0 = json.loads(zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_102_REV03_20261027T0907Z.json").decode('utf-8'))
    reg0 = json.loads(zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/L_GLOSS_102_POSITION_REGISTER_ZH_EN.json").decode('utf-8'))
    reg_map0 = {x['id']: x for x in reg0}
    p_ids0 = tax0.get('IDs_by_status', {}).get('accepted_partial_only', [])
    for pid in p_ids0:
        info = reg_map0.get(pid, {})
        selected_partials.append((info.get('page'), info.get('position'), pid, info))

# Batch 01 (take first 14)
with zipfile.ZipFile(os.path.join(DHS306_DIR, "DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip"), 'r') as zf:
    tax1 = json.loads(zf.read("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_99_20261027T0932Z.json").decode('utf-8'))
    reg1 = json.loads(zf.read("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z/L_ZH_EN_99_POSITION_REGISTER.json").decode('utf-8'))
    reg_map1 = {x['id']: x for x in reg1}
    p_ids1 = tax1.get('partial_only_ids', [])
    for pid in p_ids1[:14]:
        info = reg_map1.get(pid, {})
        selected_partials.append((info.get('page'), info.get('position'), pid, info))

print(f"Total partial items collected for Batch 01: {len(selected_partials)} (Target: 50)")

# Inspect each entry and construct 6-layer representation
entries_out = []
for idx, (p, pos, eid, raw_info) in enumerate(selected_partials):
    base_data = baselines.get(p, {}).get(pos, {})
    raw_L = raw_info.get("source_L") or base_data.get("L", "")
    raw_H = base_data.get("H", "")
    raw_M = base_data.get("M", "")
    raw_R = base_data.get("R", "")
    
    entries_out.append({
        "index": idx + 1,
        "entry_id": eid,
        "page": p,
        "position": pos,
        "raw_L": raw_L,
        "raw_H": raw_H,
        "raw_M": raw_M,
        "raw_R": raw_R,
        "existing_zh": raw_info.get("zh", ""),
        "existing_en": raw_info.get("en", "")
    })

# Save inspect list
with open(os.path.join(WORKSPACE_ROOT, "literature", "workspace_m1_dhs306", "batch_01_pre_disambiguation.json"), "w", encoding="utf-8") as f:
    json.dump(entries_out, f, ensure_ascii=False, indent=2)

print("Saved pre-disambiguation table.")
