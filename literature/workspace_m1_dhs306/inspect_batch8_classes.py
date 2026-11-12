import zipfile
import csv
import io
import glob

pkg = glob.glob("literature/assets/dhs306/*0875_0879*")[0]
with zipfile.ZipFile(pkg, 'r') as zf:
    # find all tsv files
    tsvs = [n for n in zf.namelist() if n.endswith('.tsv') and 'SEMANTIC' in n]
    print("TSVs:", tsvs)
    raw = zf.read(tsvs[0]).decode('utf-8')
    r = csv.DictReader(io.StringIO(raw), delimiter='\t')
    print("Fieldnames:", r.fieldnames)
    rows = list(r)
    main = [x for x in rows if x.get('type') == 'MAIN_L']
    classes = set(x.get('accepted_class') or x.get('reviewed_status') for x in main)
    print("Classes in Batch 8:", classes)
    for c in classes:
        sample = next(x for x in main if (x.get('accepted_class') or x.get('reviewed_status')) == c)
        print(f"Sample of class '{c}':", sample)
