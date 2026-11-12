import json
import zipfile

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

b2 = reg['batches'][2] # 845-849
print("Batch 2 pages:", b2['pages'])
print("Batch 2 ZH:", b2['ZH'])
pkg_name = b2['package_path'].split('/')[-1]
print("Batch 2 package:", pkg_name)

zip_path = f"literature/assets/dhs306/{pkg_name}"
with zipfile.ZipFile(zip_path, 'r') as zf:
    for n in zf.namelist():
        if "FINAL_SEMANTIC_REVIEW" in n or "TAXONOMY" in n or "REGISTER" in n or "CANDIDATE" in n:
            print("  ", n)
