import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg['batches']
print(f"Total batches: {len(batches)}")

has_fresh_ids = 0
has_status_log = 0
has_evidence_files = 0

for i, b in enumerate(batches):
    ev = b.get('evidence_detail', {})
    if 'fresh_main_recount' in ev and 'ids' in ev['fresh_main_recount']:
        has_fresh_ids += 1
    elif 'main_row_status_log' in ev:
        has_status_log += 1
    elif 'main_reviewed_records' in ev:
        has_status_log += 1
    else:
        has_evidence_files += 1

print(f"Batches with fresh_main_recount.ids: {has_fresh_ids}")
print(f"Batches with status_log / main_reviewed_records: {has_status_log}")
print(f"Batches needing file inspection: {has_evidence_files}")
