import zipfile

zip_path = "literature/assets/dhs306/DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    for n in zf.namelist():
        if any(k in n for k in ["TAXONOMY", "REGISTER", "SUBSTANTIVE", "FINAL", "work/"]):
            print(n)
