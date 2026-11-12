import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

print(f"Total batches: {len(reg['batches'])}")

evidence_types = {}
for i, b in enumerate(reg['batches']):
    ev = b.get('evidence_detail', {})
    pages = b.get('pages', [])
    zh = b.get('ZH', {})
    
    # check keys
    pattern = []
    if 'main_row_evidence' in ev:
        pattern.append('main_row_evidence')
    if 'recount_evidence' in ev:
        pattern.append('recount_evidence')
    if 'fresh_main_recount' in ev:
        pattern.append('fresh_main_recount')
    if 'acceptance_evidence' in ev:
        pattern.append('acceptance_evidence')
        
    pat_str = "+".join(pattern)
    evidence_types.setdefault(pat_str, []).append(i)

for pat, b_indices in evidence_types.items():
    print(f"Pattern '{pat}': {len(b_indices)} batches (Indices: {b_indices[:5]}...)")
