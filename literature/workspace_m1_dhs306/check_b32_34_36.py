import json
import zipfile
import os
from collections import Counter

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
REGISTER_FILE = os.path.join(WORKSPACE_ROOT, "literature", "assets", "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")
DHS306_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets", "dhs306")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]

for idx in [32, 34, 36]:
    b = batches[idx]
    pkg = os.path.basename(b["package_path"])
    with zipfile.ZipFile(os.path.join(DHS306_DIR, pkg)) as zf:
        cand_files = [n for n in zf.namelist() if n.endswith("CANDIDATE_DATA_v2.json")]
        if cand_files:
            data = json.loads(zf.read(cand_files[0]).decode('utf-8'))
            st = data.get('gloss_statuses', {})
            c = Counter(v.get('zh_status') for v in st.values())
            print(f"Batch {idx} ({pkg[:30]}): count={len(st)}, statuses={c}")
            print(f"  Target: {b['ZH']}")
