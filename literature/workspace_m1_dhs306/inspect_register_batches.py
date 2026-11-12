import json

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

print(f"Total batches: {len(reg['batches'])}")

batch_types = {}
for i, b in enumerate(reg['batches']):
    pkg = b.get("package_path", "")
    pages = b.get("pages", [])
    zh = b.get("ZH", {})
    p = zh.get("partial", 0)
    c = zh.get("candidate", 0)
    u = zh.get("untranslated", 0)
    denom = b.get("main_L_denominator", 0)
    ev = b.get("evidence_detail", {})
    ev_keys = list(ev.keys())
    
    # print first 5 batches
    if i < 5:
        print(f"Batch {i}: pages {pages}, denom {denom}, ZH: partial={p}, candidate={c}, untranslated={u}")
        print(f"  evidence_detail keys: {ev_keys}")
        if "fresh_main_recount" in ev:
            print("  fresh_main_recount source:", ev["fresh_main_recount"].get("source"))
