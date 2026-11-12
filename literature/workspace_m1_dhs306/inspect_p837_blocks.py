import zipfile

with zipfile.ZipFile("literature/assets/dhs306/DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip", 'r') as zf:
    content = zf.read("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z/source/baseline_text/20261025_reference_collation/DHS_P0837_BASELINE_NOT_NEWLY_REVIEWED.md").decode('utf-8')
    for block in content.split("\n\n"):
        if any(f"{i:02d}" in block[:4] for i in range(8, 14)):
            print(block)
            print("-" * 30)
