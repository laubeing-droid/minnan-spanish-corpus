import json
from pathlib import Path

raw_all = json.loads(Path("literature/workspace_m1_dhs306/extracted_raw_251_656.json").read_text(encoding="utf-8"))

def show_slice(start, end, label):
    print(f"=== {label} (entries {start+251} to {end+250}) ===")
    for i, r in enumerate(raw_all[start:end]):
        print(f"[{start+251+i}] id={r['id']} page={r.get('page')} pos={r.get('pos')} | L='{r.get('source_L','')}' | H='{r.get('source_H','')}' | M='{r.get('source_M','')}' | zh='{r.get('zh','')}' | en='{r.get('en','')}'")

if __name__ == "__main__":
    import sys
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    e = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    show_slice(s, e, f"Slice {s}:{e}")
