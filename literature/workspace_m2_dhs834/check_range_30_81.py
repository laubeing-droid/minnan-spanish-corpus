import re

with open("literature/historical_dhs/DHS_full_first_draft_body_v2.md", "r", encoding="utf-8") as f:
    text = f.read()

for p in [30, 39, 40, 45, 50, 60, 70, 79, 80, 81]:
    pat = rf"## PDF {p:04d} · 原書頁 (\d+)"
    m = re.search(pat, text)
    if m:
        orig = m.group(1)
        start = m.start()
        print(f"PDF {p:04d} (orig {orig}):\n" + text[start:start+250])
        print("="*50)
