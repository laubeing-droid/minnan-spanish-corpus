import zipfile

zip_file = "literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip"
with zipfile.ZipFile(zip_file, 'r') as zf:
    content = zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/source/baseline_text/20261025_reference_collation/DHS_P0836_BASELINE_NOT_NEWLY_REVIEWED.md").decode('utf-8')
    print("Length:", len(content))
    print(content)
