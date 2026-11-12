import zipfile
import csv
import io

zip_file = "literature/assets/dhs306/DHS_0885_0889_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1148Z.zip"
with zipfile.ZipFile(zip_file, 'r') as zf:
    target = "DHS_0885_0889_REVIEW_CLOSED_LIGHT_PACKAGE_20261027T1148Z/independent_review_0885_0889_NEW_20261027T1118Z/INDEPENDENT_SEMANTIC_REVIEW_v1.tsv"
    raw = zf.read(target).decode('utf-8')
    r = csv.DictReader(io.StringIO(raw), delimiter='\t')
    print("Fieldnames:", r.fieldnames)
    rows = list(r)
    main = [x for x in rows if (x.get('type') or x.get('scope') or '').lower() in ['main_l', 'main']]
    print("Main rows count:", len(main))
    zh_main = [x for x in main if (x.get('language') or '').lower() == 'zh']
    print("ZH main count:", len(zh_main))
    statuses = {}
    for x in zh_main:
        s = x.get('requested_classification') or x.get('v1_classification') or x.get('status')
        statuses[s] = statuses.get(s, 0) + 1
    print("Statuses with requested_classification:", statuses)
    print("Sample row 0:", zh_main[0])
