import json

with open('literature/workspace_m1_dhs306/batch_01_m1_disambiguated_50.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total entries: {len(d.get('entries', []))}")
for i, e in enumerate(d.get('entries', [])):
    eid = e['entry_id']
    h = e['layer_1_diplomatic_raw'].get('source_H', '')
    m = e['layer_1_diplomatic_raw'].get('source_M', '')
    tc = e['layer_3_historical_phonology'].get('dhs_tone_class', [])
    rec = e['layer_3_historical_phonology'].get('reconstructed_17th_c_hokkien', '')
    tl = e['layer_4_modern_tai_lo'].get('tai_lo_standard', '')
    moe = e['layer_4_modern_tai_lo'].get('moe_code', '')
    abbrs = e['layer_2_disambiguation'].get('abbreviations_expanded', [])
    print(f"{i+1:02d}. {eid}: H='{h}' | M='{m}' | rec='{rec}' | tones={tc} | moe='{moe}' | abbrs={abbrs}")
