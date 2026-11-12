import re

with open("literature/historical_dhs/DHS_full_first_draft_body_v2.md", "r", encoding="utf-8") as f:
    text = f.read()

matches = list(re.finditer(r"## PDF (\d{4}) · 原書頁 (\d+)", text))
print("Total page headers found:", len(matches))
for m in matches:
    p_pdf = int(m.group(1))
    p_orig = m.group(2)
    start_pos = m.start()
    chunk = text[start_pos:start_pos+600]
    if "\nH:" in chunk or "\nL:" in chunk:
        print(f"First 4-column page found at: PDF {p_pdf:04d} (orig page {p_orig})")
        print(chunk[:300])
        break
