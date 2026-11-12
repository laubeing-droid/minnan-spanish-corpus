with open("literature/historical_dhs/DHS_full_first_draft_body_v2.md", "r", encoding="utf-8") as f:
    text = f.read()

for p in [43, 44, 45, 46]:
    pat = rf"## PDF {p:04d} · 原書頁 (\d+)"
    import re
    m = re.search(pat, text)
    if m:
        start = m.start()
        print(f"--- PDF {p:04d} ---")
        print(text[start:start+400])
