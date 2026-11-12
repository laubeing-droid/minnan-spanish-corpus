import zipfile
import csv
import io

zip_path = "literature/assets/dhs306/DHS_0845_0849_REVIEW_CLOSED_WORKING_PACKAGE_20261027T0948Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    raw = zf.read("03_INDEPENDENT_REVIEW/FINAL_SEMANTIC_REVIEW_220_UNITS_v3.tsv").decode('utf-8')
    reader = csv.DictReader(io.StringIO(raw), delimiter='\t')
    print("Fieldnames:", reader.fieldnames)
    rows = list(reader)
    print("Total rows:", len(rows))
    main_l_rows = [r for r in rows if r.get('type') == 'MAIN_L']
    print("MAIN_L rows:", len(main_l_rows))
    
    # Check language and status
    by_id = {}
    for r in main_l_rows:
        rid = r.get('ID')
        by_id.setdefault(rid, {})[r.get('language')] = r
    
    print("Unique MAIN_L IDs:", len(by_id))
    statuses = {}
    for rid, langs in by_id.items():
        zh_status = langs.get('ZH', {}).get('reviewed_status')
        statuses[zh_status] = statuses.get(zh_status, 0) + 1
        if zh_status != 'full_core':
            print(f"  Non-core: ID={rid}, status={zh_status}, source={langs.get('ZH', {}).get('source')}, gloss={langs.get('ZH', {}).get('reviewed_gloss')}")
    print("Statuses distribution:", statuses)
