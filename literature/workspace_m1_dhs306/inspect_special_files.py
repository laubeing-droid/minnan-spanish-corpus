import json
import zipfile
import os

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

def check_zip(zip_name, member):
    p = os.path.join(DHS306_DIR, zip_name)
    with zipfile.ZipFile(p, 'r') as zf:
        matching = [n for n in zf.namelist() if n.endswith(member)]
        if matching:
            data = json.loads(zf.read(matching[0]).decode('utf-8'))
            print(f"\n--- {zip_name} :: {member} ---")
            if isinstance(data, list):
                print(f"List of {len(data)} items. Sample item 0:")
                print(json.dumps(data[0], ensure_ascii=False, indent=2))
            elif isinstance(data, dict):
                print(f"Dict keys: {list(data.keys())}")
                if "gloss_statuses" in data:
                    print(f"Sample gloss_status: {list(data['gloss_statuses'].items())[0]}")
                if "selected_originals" in data:
                    print(f"Sample selected_originals: {list(data['selected_originals'].items())[0] if isinstance(data['selected_originals'], dict) else data['selected_originals'][0]}")

# Batch 24
check_zip("DHS_0955_0959_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1533Z.zip", "CANDIDATE_DATA_v2.json")
# Batch 30
check_zip("DHS_0985_0989_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1706Z.zip", "CANDIDATE_DATA_v2.json")
# Batch 38
check_zip("DHS1025_1029_REVIEWED_PORTABLE_20261027T2007Z.zip", "SEMANTIC_REVIEW_206_FINAL_REV04.json")
# Batch 40
check_zip("DHS1035_1039_REV03_LIMITED.zip", "L_SEMANTIC_REVIEW_100_REV03.json")
# Batch 41
check_zip("DHS1040_1044_ORIGINAL_ZH_EN_WORKPACK_RESUMED_20261027T181510Z.zip", "INDEPENDENT_L_HMR_BILINGUAL_ACCEPTANCE_RECOVERED_20261027T1812Z.json")
# Batch 44
check_zip("DHS1055_1059_REVIEWED_PORTABLE_20261027T2019Z.zip", "SEMANTIC_REVIEW_101_REV03.json")
# Batch 45
check_zip("DHS1060_1064_REVIEWED_PORTABLE_20261027T2011Z.zip", "SEMANTIC_REVIEW_102_L_v1.json")
