import json
import re

with open('literature/workspace_m1_dhs306/l_layer_gaps_queue.json', 'r', encoding='utf-8') as f:
    queue_all = json.load(f)['queue_entries']

target_queue = queue_all[50:250]
print(f"Target queue length: {len(target_queue)} (indices 50 to 249)")

md_text = open('literature/historical_dhs/DHS_full_first_draft_body_v2.md', 'r', encoding='utf-8').read()

missing = []
found = []
for idx, e in enumerate(target_queue, start=51):
    p = e['page']
    pos = e['position']
    p_pat = rf'PDF {p:04d}'
    m_p = re.search(p_pat, md_text)
    if not m_p:
        missing.append((idx, e['id'], f'page {p} not found'))
        continue
    m_next = re.search(r'PDF \d{4}', md_text[m_p.end():])
    p_block = md_text[m_p.end(): m_p.end() + m_next.start()] if m_next else md_text[m_p.end():]
    
    # Try Format A (multi-line)
    pos_pat_a = rf'(?m)^{pos:02d}\s*$'
    m_pos_a = re.search(pos_pat_a, p_block)
    
    # Try Format B (pipe delimited: 01. or 1. or 01)
    pos_pat_b = rf'(?m)^{pos:02d}\.\s*(.*?)$'
    m_pos_b = re.search(pos_pat_b, p_block)
    
    if m_pos_a:
        sub = p_block[m_pos_a.end():m_pos_a.end()+350]
        l_m = re.search(r'L:\s*(.*)', sub)
        h_m = re.search(r'H:\s*(.*)', sub)
        m_m = re.search(r'M:\s*(.*)', sub)
        r_m = re.search(r'R:\s*(.*)', sub)
        found.append({
            'index': idx,
            'id': e['id'],
            'page': p,
            'pos': pos,
            'queue_gap_type': e['gap_type'],
            'queue_zh': e.get('zh', ''),
            'queue_en': e.get('en', ''),
            'source_L': l_m.group(1).strip() if l_m else e.get('source_L', ''),
            'source_H': h_m.group(1).strip() if h_m else '',
            'source_M': m_m.group(1).strip() if m_m else '',
            'source_R': r_m.group(1).strip() if r_m else ''
        })
    elif m_pos_b:
        line_content = m_pos_b.group(1).strip()
        parts = [p.strip() for p in re.split(r'\s*[|｜]\s*', line_content)]
        l_val = parts[0] if len(parts) > 0 else ''
        h_val = parts[1] if len(parts) > 1 else ''
        m_val = parts[2] if len(parts) > 2 else ''
        r_val = parts[3] if len(parts) > 3 else ''
        found.append({
            'index': idx,
            'id': e['id'],
            'page': p,
            'pos': pos,
            'queue_gap_type': e['gap_type'],
            'queue_zh': e.get('zh', ''),
            'queue_en': e.get('en', ''),
            'source_L': l_val,
            'source_H': h_val,
            'source_M': m_val,
            'source_R': r_val
        })
    else:
        missing.append((idx, e['id'], f'pos {pos} not found in page {p}'))

print(f"Checked 200 entries. Found: {len(found)}, Missing: {len(missing)}")
if missing:
    print("First 10 missing:", missing[:10])
else:
    print("ALL 200 FOUND PERFECTLY!")

# Save to json for reference
with open("literature/workspace_m1_dhs306/extracted_raw_51_250.json", "w", encoding="utf-8") as f:
    json.dump(found, f, ensure_ascii=False, indent=2)
