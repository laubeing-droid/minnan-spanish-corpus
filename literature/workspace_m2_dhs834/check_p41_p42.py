with open("literature/historical_dhs/DHS_full_first_draft_body_v2.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
for p in [41, 42]:
    m = re.search(rf"## PDF {p:04d} · 原書頁 (\d+)", text)
    if m:
        s = m.start()
        print(f"--- PDF {p:04d} ---")
        print(text[s:s+350])
