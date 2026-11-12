import json
import zipfile

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    for n in zf.namelist():
        if "INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_102_REV03" in n:
            print("Found:", n)
            content = json.loads(zf.read(n).decode('utf-8'))
            print("Type of content:", type(content))
            if isinstance(content, dict):
                print("Keys:", list(content.keys())[:10])
                first_k = list(content.keys())[0]
                print(f"Sample item [{first_k}]:", content[first_k])
            elif isinstance(content, list):
                print("Length:", len(content))
                print("Sample item 0:", content[0])
