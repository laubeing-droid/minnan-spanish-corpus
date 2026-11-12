import zipfile

def read_p(zip_name, p_name):
    with zipfile.ZipFile(f"literature/assets/dhs306/{zip_name}", 'r') as zf:
        matching = [n for n in zf.namelist() if p_name in n and n.endswith(".md") and "BASELINE" in n]
        if matching:
            return zf.read(matching[0]).decode('utf-8')
    return ""

print("P837 len:", len(read_p("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip", "DHS_P0837")))
print("P838 len:", len(read_p("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip", "DHS_P0838")))
print("P839 len:", len(read_p("DHS0835_0839_ORIGINAL_ZH_EN_WORKPACK_20261027T090912Z.zip", "DHS_P0839")))
print("P840 len:", len(read_p("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip", "DHS_P0840")))
print("P842 len:", len(read_p("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip", "DHS_P0842")))
print("P843 len:", len(read_p("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip", "DHS_P0843")))
print("P844 len:", len(read_p("DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip", "DHS_P0844")))
