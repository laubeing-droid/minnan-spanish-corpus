import json

ne = {
    "entry_id": "U-DHS-0046-16-H1",
    "source_id": "01_DHS_Hispanico_Sinicum",
    "pdf_page": 46,
    "historical_folio": 17,
    "hanzi_char": "[焦/炰/𤆬]",
    "competing_glyphs": ["𤆬", "娶", "焦", "炰"],
    "ids": "⿱𤈦灬 或 ⿱爪灬",
    "resolution_status": "UNRESOLVED_GLYPH",
    "status": "UNRESOLVED_GLYPH",
    "notes": "西语栏为acompañar及acompañar los desposados（送嫁/娶嫁），闽南语写choǎ（现代台罗tshuā/娶/𤆬），官话写chǒa。原图字形似焦、炰或俗字𤆬，保留未决字形状态。"
}

for p in ["literature/evidence_ledger/ledger_1_unresolved_glyphs.json", "literature/ledgers/ledger_1_unresolved_glyphs.json"]:
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not any(e["entry_id"] == ne["entry_id"] for e in data["entries"]):
        data["entries"].append(ne)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {p}: {len(data['entries'])} entries")
