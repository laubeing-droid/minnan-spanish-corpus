import json
import zipfile
import csv
import io
import os
from collections import Counter

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
REGISTER_FILE = os.path.join(WORKSPACE_ROOT, "literature", "assets", "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]

# Test Batch 24
b24 = batches[24]
zip24 = os.path.join(DHS306_DIR, os.path.basename(b24['package_path']))
with zipfile.ZipFile(zip24) as zf:
    cdata = json.loads(zf.read("DHS_0955_0959_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1533Z/rebuild_0955_0959_NEW_20261027/v2_REVIEW_FIXES_20261027T1530Z/CANDIDATE_DATA_v2.json").decode('utf-8'))
    statuses = cdata['gloss_statuses']
    c = Counter(v.get('zh_status') for v in statuses.values())
    print("Batch 24 statuses from CANDIDATE_DATA_v2:", c)
    print("Batch 24 target:", b24['ZH'])

# Test Batch 30
b30 = batches[30]
zip30 = os.path.join(DHS306_DIR, os.path.basename(b30['package_path']))
with zipfile.ZipFile(zip30) as zf:
    cdata = json.loads(zf.read("DHS_0985_0989_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1706Z/rebuild_0985_0989_NEW_20261027/v2_REVIEW_FIXES_20261027T1704Z/CANDIDATE_DATA_v2.json").decode('utf-8'))
    statuses = cdata['gloss_statuses']
    c = Counter(v.get('zh_status') for v in statuses.values())
    print("Batch 30 statuses from CANDIDATE_DATA_v2:", c)
    print("Batch 30 target:", b30['ZH'])

# Test Batch 38
b38 = batches[38]
zip38 = os.path.join(DHS306_DIR, os.path.basename(b38['package_path']))
with zipfile.ZipFile(zip38) as zf:
    data = json.loads(zf.read("DHS1025_1029_REVIEWED_PORTABLE_20261027T2007Z/independent_review/SEMANTIC_REVIEW_206_FINAL_REV04.json").decode('utf-8'))
    zh_items = [x for x in data if x.get('language') == 'zh']
    c = Counter(x.get('translation_status') for x in zh_items)
    print("Batch 38 zh items count:", len(zh_items), "statuses:", c)
    print("Batch 38 target:", b38['ZH'])

# Test Batch 40
b40 = batches[40]
zip40 = os.path.join(DHS306_DIR, os.path.basename(b40['package_path']))
with zipfile.ZipFile(zip40) as zf:
    data = json.loads(zf.read("DHS1035_1039_REV03_LIMITED/02_INDEPENDENT_REVIEW_EXACT/L_SEMANTIC_REVIEW_100_REV03.json").decode('utf-8'))
    c = Counter(x.get('independent_disposition') for x in data)
    print("Batch 40 items count:", len(data), "statuses:", c)
    print("Batch 40 target:", b40['ZH'])

# Test Batch 41
b41 = batches[41]
zip41 = os.path.join(DHS306_DIR, os.path.basename(b41['package_path']))
with zipfile.ZipFile(zip41) as zf:
    data = json.loads(zf.read("DHS1040_1044_ORIGINAL_ZH_EN_WORKPACK_RESUMED_20261027T181510Z/review_evidence/INDEPENDENT_L_HMR_BILINGUAL_ACCEPTANCE_RECOVERED_20261027T1812Z.json").decode('utf-8'))
    l_recs = data.get('L_records', [])
    c = Counter(x.get('translation_status') or x.get('status') for x in l_recs)
    print("Batch 41 L_records count:", len(l_recs), "statuses:", c)
    print("Batch 41 target:", b41['ZH'])
    if l_recs:
        print("Sample L_record 0:", l_recs[0])

# Test Batch 43
b43 = batches[43]
zip43 = os.path.join(DHS306_DIR, os.path.basename(b43['package_path']))
with zipfile.ZipFile(zip43) as zf:
    data = json.loads(zf.read("DHS1050_1054_ORIGINAL_ZH_EN_WORKPACK_REVIEWED_20261027T183751Z/review_evidence/INDEPENDENT_L_HMR_BILINGUAL_ACCEPTANCE_RECOVERED_20261027T1832Z.json").decode('utf-8'))
    l_recs = data.get('L_records', [])
    c = Counter(x.get('translation_status') or x.get('status') for x in l_recs)
    print("Batch 43 L_records count:", len(l_recs), "statuses:", c)
    print("Batch 43 target:", b43['ZH'])

# Test Batch 44
b44 = batches[44]
zip44 = os.path.join(DHS306_DIR, os.path.basename(b44['package_path']))
with zipfile.ZipFile(zip44) as zf:
    data = json.loads(zf.read("DHS1055_1059_REVIEWED_PORTABLE_20261027T2019Z/independent_review/SEMANTIC_REVIEW_101_REV03.json").decode('utf-8'))
    c = Counter(x.get('accepted_scope') for x in data)
    print("Batch 44 items count:", len(data), "statuses:", c)
    print("Batch 44 target:", b44['ZH'])

# Test Batch 45
b45 = batches[45]
zip45 = os.path.join(DHS306_DIR, os.path.basename(b45['package_path']))
with zipfile.ZipFile(zip45) as zf:
    data = json.loads(zf.read("independent_review/SEMANTIC_REVIEW_102_L_v1.json").decode('utf-8'))
    c = Counter(x.get('accepted_taxonomy') for x in data)
    print("Batch 45 items count:", len(data), "statuses:", c)
    print("Batch 45 target:", b45['ZH'])
