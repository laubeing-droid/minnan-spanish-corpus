import zipfile
import csv
import io

zip_file = "literature/assets/dhs306/DHS_0925_0929_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1347Z.zip"
with zipfile.ZipFile(zip_file, 'r') as zf:
    target = "DHS_0925_0929_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1347Z/independent_review_0925_0929_NEW_20261027T1316Z/INDEPENDENT_SEMANTIC_REVIEW_v1.tsv"
    raw = zf.read(target).decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw), delimiter="\t")
    print("fieldnames:", reader.fieldnames)
    rows = list(reader)
    print("total rows:", len(rows))
    main = [r for r in rows if r.get("type") == "MAIN_L"]
    print("MAIN_L rows:", len(main))
    if main:
        print("Sample row 0:", main[0])
