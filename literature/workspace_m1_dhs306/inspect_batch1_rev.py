import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

b1 = reg['batches'][1]
print("Batch 1 recount_evidence:", b1.get('evidence_detail', {}).get('recount_evidence'))
