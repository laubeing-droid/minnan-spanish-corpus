import zipfile
import csv
import io
from collections import Counter

zip_file = "literature/assets/dhs306/DHS_0925_0929_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1347Z.zip"
with zipfile.ZipFile(zip_file, 'r') as zf:
    target = "DHS_0925_0929_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1347Z/independent_review_0925_0929_NEW_20261027T1316Z/INDEPENDENT_SEMANTIC_REVIEW_v1.tsv"
    raw = zf.read(target).decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw), delimiter="\t")
    rows = list(reader)
    scopes = Counter(r.get('scope') for r in rows)
    print("Scopes:", scopes)
    main_rows = [r for r in rows if r.get('scope') in ['main', 'MAIN_L']]
    print("main rows len:", len(main_rows))
    zh_rows = [r for r in main_rows if r.get('language') in ['zh', 'ZH']]
    print("zh rows len:", len(zh_rows))
    statuses = Counter(r.get('status') for r in zh_rows)
    print("Statuses for ZH:", statuses)
