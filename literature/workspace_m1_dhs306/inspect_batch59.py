import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

b59 = reg['batches'][59]
print("Batch 59 keys:", b59.keys())
print("Batch 59 pages:", b59.get('pages'))
print("Batch 59 ZH:", b59.get('ZH'))
print("Batch 59 evidence_detail:", b59.get('evidence_detail'))
