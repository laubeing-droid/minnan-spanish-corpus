import json

with open("literature/workspace_m1_dhs306/batch_01_m1_disambiguated_50.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data.get("entries", [])
assert len(entries) == 50, f"Expected 50 entries, got {len(entries)}"

raw_str = json.dumps(data, ensure_ascii=False)

# Check forbidden strings
assert "Collated from DHS original diacritics" not in raw_str, "Found forbidden string 'Collated from DHS original diacritics'!"
assert '"moe_code": "verified"' not in raw_str, "Found forbidden placeholder 'moe_code: verified'!"
assert '"abbr": "expanded"' not in raw_str, "Found forbidden placeholder 'abbr: expanded'!"

# Check historical Zhangzhou phonology
# Entry 3 (DHS0835-19: 封): must have hɔŋ¹ and NOT pɔŋ¹
e3 = entries[2]
assert "hɔŋ¹" in e3["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 3 missing hɔŋ¹: {e3['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"
assert "pɔŋ¹" not in e3["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 3 contains pɔŋ¹: {e3['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"

# Entry 5 (DHS0836-04: 勅 封): must have tʰit⁷ and NOT tʰik⁷
e5 = entries[4]
assert "tʰit⁷" in e5["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 5 missing tʰit⁷: {e5['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"
assert "tʰik⁷" not in e5["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 5 contains tʰik⁷: {e5['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"
assert "hɔŋ¹" in e5["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 5 missing hɔŋ¹: {e5['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"

# Entry 6 (DHS0836-05: 勅 賜): must have tʰit⁷
e6 = entries[5]
assert "tʰit⁷" in e6["layer_3_historical_phonology"]["reconstructed_17th_c_hokkien"], f"Entry 6 missing tʰit⁷: {e6['layer_3_historical_phonology']['reconstructed_17th_c_hokkien']}"

# Verify all 50 entries have valid tones
for i, e in enumerate(entries):
    eid = e["entry_id"]
    tc = e["layer_3_historical_phonology"]["dhs_tone_class"]
    # If the MS row is not blank (e.g. not 46 or 49 which are MS cancellations / headings), tones must be populated
    if e["layer_1_diplomatic_raw"]["source_M"] not in ["", "〔空〕"]:
        assert len(tc) > 0, f"{eid} missing tones!"
        for t in tc:
            assert any(k in t for k in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"]), f"Invalid tone string: {t} in {eid}"

print("[PASS] All automated quality checks on batch_01_m1_disambiguated_50.json PASSED 100%!")
