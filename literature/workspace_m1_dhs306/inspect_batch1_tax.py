import zipfile
import json

zip_path = "literature/assets/dhs306/DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    n = "DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_99_20261027T0932Z.json"
    content = json.loads(zf.read(n).decode('utf-8'))
    print("Keys:", content.keys())
    print("entries len:", len(content.get('entries', [])))
    print("Sample entry 0:", content.get('entries', [])[0])
    reg_n = "DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z/L_ZH_EN_99_POSITION_REGISTER.json"
    rdata = json.loads(zf.read(reg_n).decode('utf-8'))
    print("reg len:", len(rdata))
    print("Sample reg 0:", rdata[0])
