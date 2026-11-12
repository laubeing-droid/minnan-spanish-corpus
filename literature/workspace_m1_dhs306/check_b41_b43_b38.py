import json
import zipfile
import os
from collections import Counter

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

# Check Batch 41
zip41 = os.path.join(DHS306_DIR, "DHS1040_1044_ORIGINAL_ZH_EN_WORKPACK_RESUMED_20261027T181510Z.zip")
with zipfile.ZipFile(zip41) as zf:
    data = json.loads(zf.read("DHS1040_1044_ORIGINAL_ZH_EN_WORKPACK_RESUMED_20261027T181510Z/review_evidence/INDEPENDENT_L_HMR_BILINGUAL_ACCEPTANCE_RECOVERED_20261027T1812Z.json").decode('utf-8'))
    l_recs = data.get('L_records', [])
    c = Counter(x.get('status_ZH') for x in l_recs)
    print("Batch 41 status_ZH:", c)

# Check Batch 43
zip43 = os.path.join(DHS306_DIR, "DHS1050_1054_ORIGINAL_ZH_EN_WORKPACK_REVIEWED_20261027T183751Z.zip")
with zipfile.ZipFile(zip43) as zf:
    data = json.loads(zf.read("DHS1050_1054_ORIGINAL_ZH_EN_WORKPACK_REVIEWED_20261027T183751Z/review_evidence/INDEPENDENT_L_HMR_BILINGUAL_ACCEPTANCE_RECOVERED_20261027T1832Z.json").decode('utf-8'))
    l_recs = data.get('L_records', [])
    c = Counter(x.get('status_ZH') for x in l_recs)
    print("Batch 43 status_ZH:", c)

# Check Batch 38: why did it have 103 instead of 95?
# Let's inspect Batch 38 in register
with open(os.path.join(WORKSPACE_ROOT, "literature", "assets", "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json"), "r", encoding="utf-8") as f:
    reg = json.load(f)
b38 = reg["batches"][38]
print("Batch 38 register evidence_detail keys:", b38['evidence_detail'].keys())
print("Batch 38 fresh_main_recount:", b38['evidence_detail'].get('fresh_main_recount'))
