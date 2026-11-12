import json
import zipfile

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    n = "DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/L_GLOSS_102_POSITION_REGISTER_ZH_EN.json"
    content = json.loads(zf.read(n).decode('utf-8'))
    print("Content type:", type(content))
    if isinstance(content, list):
        print("Length:", len(content))
        print("Sample 0:", json.dumps(content[0], ensure_ascii=False, indent=2))
        for item in content:
            if item.get("id") == "DHS0835-11":
                print("Item DHS0835-11:", json.dumps(item, ensure_ascii=False, indent=2))
                break
    elif isinstance(content, dict):
        print("Keys:", list(content.keys())[:10])
