import json
import re

with open('literature/workspace_m1_dhs306/l_layer_gaps_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)['queue_entries']

assert len(queue) == 656
print(f"Total queue entries: {len(queue)}")

md_text = open('literature/historical_dhs/DHS_full_first_draft_body_v2.md', 'r', encoding='utf-8').read()

found_count = 0
missing = []

# Pre-index pages in md_text
page_indices = {}
for m in re.finditer(r'PDF (\d{4})', md_text):
    p_num = int(m.group(1))
    page_indices[p_num] = m.start()

sorted_pages = sorted(page_indices.keys())

for idx, e in enumerate(queue):
    p = e.get('page')
    pos = e.get('position')
    clean_id = (e.get('id') or '').replace('DHS', '')
    if p is None and '.' in clean_id:
        pts = clean_id.split('.')
        try:
            p = int(pts[0])
            pos = int(pts[1])
        except:
            pass
    elif p is None and '-' in clean_id:
        pts = clean_id.split('-')
        try:
            p = int(pts[0])
            pos = int(pts[1])
        except:
            pass
    if p not in page_indices:
        missing.append((idx, e['id'], f'page {p} not found in md'))
        continue
    
    start_pos = page_indices[p]
    # find end of page block
    next_p_idx = sorted_pages.index(p) + 1
    end_pos = page_indices[sorted_pages[next_p_idx]] if next_p_idx < len(sorted_pages) else len(md_text)
    p_block = md_text[start_pos:end_pos]
    
    # Format A: pos\nL: ...
    pos_pat_a = rf'(?m)^{pos:02d}\s*$'
    m_pos_a = re.search(pos_pat_a, p_block)
    
    # Format B: pos. L | H | M | R
    pos_pat_b = rf'(?m)^{pos:02d}\.\s*(.*?)$'
    m_pos_b = re.search(pos_pat_b, p_block)
    
    if m_pos_a or m_pos_b:
        found_count += 1
    else:
        missing.append((idx, e['id'], f'pos {pos} not found in page {p}'))

print(f"Extraction test: Found {found_count} / {len(queue)}, Missing: {len(missing)}")
if missing:
    print("First 10 missing:", missing[:10])
