import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

for idx in [26, 38, 50]:
    b = reg['batches'][idx]
    print(f"\nBatch {idx}: {b.get('package_path')}")
    print("ZH:", b.get('ZH'))
    print("evidence_detail keys:", list(b.get('evidence_detail', {}).keys()))
    ev = b.get('evidence_detail', {})
    if 'recount_evidence' in ev:
        print("recount_evidence:", ev['recount_evidence'])
    if 'fresh_main_recount' in ev:
        print("fresh_main_recount:", ev['fresh_main_recount'])
