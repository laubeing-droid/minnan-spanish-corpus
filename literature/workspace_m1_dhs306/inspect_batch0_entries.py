import json
import zipfile

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    n = "DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_102_REV03_20261027T0907Z.json"
    content = json.loads(zf.read(n).decode('utf-8'))
    entries = content.get('entries', [])
    print("Entry 0:", json.dumps(entries[0], ensure_ascii=False, indent=2))
    
    # find DHS0835-11
    for e in entries:
        if e.get('id') == 'DHS0835-11':
            print("Entry DHS0835-11:", json.dumps(e, ensure_ascii=False, indent=2))
            break
