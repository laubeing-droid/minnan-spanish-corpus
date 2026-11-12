import zipfile
import csv
import io
import glob

pkg = glob.glob("literature/assets/dhs306/*0865_0869*")[0]
with zipfile.ZipFile(pkg, 'r') as zf:
    raw_tsv = zf.read("DHS_0865_0869_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1049Z/independent_review_0865_0869_NEW_20261027T1022Z/FINAL_SEMANTIC_REVIEW_206_UNITS_v2.tsv").decode('utf-8')
    reader = csv.DictReader(io.StringIO(raw_tsv), delimiter="\t")
    rows = list(reader)
    print("Total rows:", len(rows))
    main_rows = [r for r in rows if r.get('type') == 'MAIN_L']
    print("MAIN_L rows:", len(main_rows))
    by_id = {}
    for r in main_rows:
        rid = r.get('ID')
        by_id.setdefault(rid, {})[r.get('language')] = r
    print("Unique IDs:", len(by_id))
    statuses = {}
    for rid, langs in by_id.items():
        st = langs.get('ZH', {}).get('reviewed_status')
        statuses[st] = statuses.get(st, 0) + 1
    print("Statuses:", statuses)
