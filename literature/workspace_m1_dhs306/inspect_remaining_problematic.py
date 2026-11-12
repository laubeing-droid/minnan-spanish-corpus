import json
import zipfile
import csv
import io
import os

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
REGISTER_FILE = os.path.join(WORKSPACE_ROOT, "literature", "assets", "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]

# Let's inspect each batch
for idx in [12, 14, 16, 24, 30, 32, 34, 36, 38, 40, 41, 43, 44, 45]:
    b = batches[idx]
    pkg_name = os.path.basename(b["package_path"])
    zip_path = os.path.join(DHS306_DIR, pkg_name)
    ev = b.get("evidence_detail", {})
    zh_target = b.get("ZH", {})
    
    print(f"\n--- Batch {idx} ({pkg_name}) ---")
    print("ZH Target:", zh_target)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        
        # Check recount_source
        rs = ev.get("recount_source")
        if rs and "zip_member" in rs:
            zm = rs["zip_member"]
            matching = [n for n in namelist if n.endswith(os.path.basename(zm))]
            if matching:
                print(f"  Found recount_source member: {matching[0]}")
                raw = zf.read(matching[0]).decode('utf-8', errors='ignore')
                try:
                    data = json.loads(raw)
                    print(f"  JSON type: {type(data)}, keys: {list(data.keys())[:5] if isinstance(data, dict) else len(data)}")
                except:
                    print(f"  Not JSON or parse error, length={len(raw)}")
                    
        # Check fresh_main_recount source
        fmr = ev.get("fresh_main_recount", {})
        if "source" in fmr and fmr["source"]:
            src = os.path.basename(fmr["source"])
            matching = [n for n in namelist if n.endswith(src)]
            if matching:
                print(f"  Found fmr source: {matching[0]}")
                if src.endswith('.tsv'):
                    raw = zf.read(matching[0]).decode('utf-8')
                    r = csv.DictReader(io.StringIO(raw), delimiter='\t')
                    print(f"  TSV fieldnames: {r.fieldnames}")
                    rows = list(r)
                    zh_rows = [x for x in rows if (x.get('language') or '').lower() == 'zh' and (x.get('type') or x.get('scope') or '').lower() in ['main', 'main_l']]
                    print(f"  TSV ZH main count: {len(zh_rows)}")
                    # check statuses
                    st_keys = ['requested_classification', 'v1_classification', 'classification', 'status', 'accepted_class', 'reviewed_status']
                    for sk in st_keys:
                        vals = set(x.get(sk) for x in zh_rows if x.get(sk) is not None)
                        if vals:
                            print(f"    Key '{sk}': {vals}")
