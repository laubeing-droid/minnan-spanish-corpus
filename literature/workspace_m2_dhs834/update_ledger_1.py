import json

new_entries = [
    {
        "entry_id": "U-DHS-0043-01-H1",
        "source_id": "01_DHS_Hispanico_Sinicum",
        "pdf_page": 43,
        "historical_folio": 14,
        "hanzi_char": "[邀/慇/殀]",
        "competing_glyphs": ["邀", "慇", "殀", "摎"],
        "ids": "⿺辶敫 或 ⿰歹夭",
        "resolution_status": "UNRESOLVED_GLYPH",
        "status": "UNRESOLVED_GLYPH",
        "notes": "西语栏为'Acallar como a el niño, o marido &.'（安抚/哄弄孩子或丈夫），闽南语写yó，官话写yǔ。字形见辶旁与方/攵/敫部件，未决。"
    },
    {
        "entry_id": "U-DHS-0044-06-H1",
        "source_id": "01_DHS_Hispanico_Sinicum",
        "pdf_page": 44,
        "historical_folio": 15,
        "hanzi_char": "[鉋/敲]",
        "competing_glyphs": ["鉋", "敲"],
        "ids": "⿰金包 或 ⿰石高",
        "resolution_status": "UNRESOLVED_GLYPH",
        "status": "UNRESOLVED_GLYPH",
        "notes": "西语栏为'Acepillar'（推刨/刨平），下行有'[疑:敲]刀'（鉋刀），闽南语写cáu/cáu tó，官话写quiǎu/quiǎu toǔn。字形形似敲，实疑为俗字鉋。严格存疑。"
    },
    {
        "entry_id": "U-DHS-0045-08-H1",
        "source_id": "01_DHS_Hispanico_Sinicum",
        "pdf_page": 45,
        "historical_folio": 16,
        "hanzi_char": "[散/霰]",
        "competing_glyphs": ["散", "霰"],
        "ids": "⿰𢽿月 或 ⿱雨散",
        "resolution_status": "UNRESOLVED_GLYPH",
        "status": "UNRESOLVED_GLYPH",
        "notes": "西语栏为'Aclarar'（放晴/云散开），下行有'[疑:霰]開'（散開），闽南语写Soâⁿ / Soâⁿ cuy，官话写çān / çān cuǐ。字形顶似雨旁，或为俗写散。严格存疑。"
    }
]

for p in ["literature/evidence_ledger/ledger_1_unresolved_glyphs.json", "literature/ledgers/ledger_1_unresolved_glyphs.json"]:
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    existing_ids = {e["entry_id"] for e in data["entries"]}
    for ne in new_entries:
        if ne["entry_id"] not in existing_ids:
            data["entries"].append(ne)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {p}: {len(data['entries'])} entries")
