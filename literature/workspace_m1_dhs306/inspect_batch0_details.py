import json
import zipfile

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    n = "DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_102_REV03_20261027T0907Z.json"
    content = json.loads(zf.read(n).decode('utf-8'))
    print("IDs_by_status keys:", content.get('IDs_by_status', {}).keys())
    for k, v in content.get('IDs_by_status', {}).items():
        print(f"  {k}: len={len(v)}, samples={v[:3]}")
    print("Entries count:", len(content.get('entries', {})))
    first_entry_id = list(content.get('entries', {}).keys())[0]
    print(f"Sample entry [{first_entry_id}]:", content['entries'][first_entry_id])
