import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

b50 = reg['batches'][50]
ev = b50['evidence_detail']
print("main_row_evidence:", ev.get('main_row_evidence'))
print("main_row_status_log sample:", ev.get('main_row_status_log')[:5] if isinstance(ev.get('main_row_status_log'), list) else ev.get('main_row_status_log'))
