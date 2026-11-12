import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg['batches']

# Let's inspect Batch 0 (fresh_main_recount)
b0 = batches[0]
ev0 = b0['evidence_detail']['fresh_main_recount']
print("Batch 0 fresh_main_recount keys:", ev0.keys())
print("counts:", ev0.get('counts'))
print("ids sample:", ev0.get('ids', {}).get('ZH', [])[:5])

# Let's inspect Batch 6 (fresh_main_recount)
b6 = batches[6]
ev6 = b6['evidence_detail'].get('fresh_main_recount', {})
print("\nBatch 6 fresh_main_recount keys:", ev6.keys())
print("counts:", ev6.get('counts'))
print("ids sample:", ev6.get('ids', {}).get('ZH', [])[:5])

# Let's inspect Batch 50 (main_row_status_log)
b50 = batches[50]
ev50 = b50['evidence_detail'].get('main_row_status_log', [])
print("\nBatch 50 main_row_status_log len:", len(ev50))
print("Sample item 0:", ev50[0])

# Let's inspect Batch 59 (main_reviewed_records)
b59 = batches[59]
ev59 = b59['evidence_detail'].get('main_reviewed_records', [])
print("\nBatch 59 main_reviewed_records len:", len(ev59))
print("Sample item 0:", ev59[0])
