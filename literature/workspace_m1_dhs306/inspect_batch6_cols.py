import zipfile
import csv
import io
import glob

pkg = glob.glob("literature/assets/dhs306/*0865_0869*")[0]
with zipfile.ZipFile(pkg, 'r') as zf:
    raw_tsv = zf.read("DHS_0865_0869_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1049Z/independent_review_0865_0869_NEW_20261027T1022Z/FINAL_SEMANTIC_REVIEW_206_UNITS_v2.tsv").decode('utf-8')
    reader = csv.DictReader(io.StringIO(raw_tsv), delimiter="\t")
    print("fieldnames:", reader.fieldnames)
    rows = list(reader)
    print("row 0:", rows[0])
    print("row 1:", rows[1])
