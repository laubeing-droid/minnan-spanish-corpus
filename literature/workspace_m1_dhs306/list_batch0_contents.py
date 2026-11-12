import zipfile

zip_path = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    for n in zf.namelist():
        print(n)
