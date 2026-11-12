import zipfile
import json

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    tax_data = json.loads(zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_102_REV03_20261027T0907Z.json").decode('utf-8'))
    reg_data = json.loads(zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/L_GLOSS_102_POSITION_REGISTER_ZH_EN.json").decode('utf-8'))
    
    partial_ids = tax_data.get('IDs_by_status', {}).get('accepted_partial_only', [])
    print(f"Total partial IDs in Batch 00: {len(partial_ids)}")
    
    reg_map = {x['id']: x for x in reg_data}
    
    for idx, pid in enumerate(partial_ids):
        pos_info = reg_map.get(pid, {})
        print(f"[{idx+1:02d}] {pid} (p.{pos_info.get('page')}, #{pos_info.get('position')}):")
        print(f"     Source L: {pos_info.get('source_L')}")
        print(f"     ZH Gloss: {pos_info.get('zh')}")
        print(f"     EN Gloss: {pos_info.get('en')}")
