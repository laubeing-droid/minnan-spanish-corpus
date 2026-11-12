import json
import zipfile
import os
import csv
import io

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
ASSETS_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets")
DHS306_DIR = os.path.join(ASSETS_DIR, "dhs306")
REGISTER_FILE = os.path.join(ASSETS_DIR, "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]

results = []

for b_idx, b in enumerate(batches):
    pkg_path = b.get("package_path", "")
    pkg_name = os.path.basename(pkg_path)
    zip_path = os.path.join(DHS306_DIR, pkg_name)
    ev_detail = b.get("evidence_detail", {})
    expected_zh = b.get("ZH", {})
    exp_c = expected_zh.get("core", 0)
    exp_p = expected_zh.get("partial", 0)
    exp_cand = expected_zh.get("candidate", 0)
    exp_u = expected_zh.get("untranslated", 0)
    exp_total = exp_c + exp_p + exp_cand + exp_u
    
    positions = []
    
    # Method 1: main_reviewed_records (Batch 59)
    if "main_reviewed_records" in ev_detail:
        for r in ev_detail["main_reviewed_records"]:
            p = r.get("page")
            pos = r.get("position")
            eid = f"DHS{p:04d}-{pos:02d}"
            part = r.get("partial", False)
            withheld = r.get("withheld", False)
            st = r.get("proposed_core_status", "")
            gtype = "CORE" if ("complete_core" in st and not part and not withheld) else ("PARTIAL" if part else ("UNTRANSLATED" if withheld else "CANDIDATE"))
            positions.append({
                "id": eid, "page": p, "position": pos,
                "source_L": r.get("source_L", ""), "zh": r.get("chinese_plain_gloss", ""),
                "en": r.get("english_paraphrase", ""), "gap_type": gtype, "status_detail": st
            })
            
    # Method 2: main_row_status_log (Batches with status log)
    elif "main_row_status_log" in ev_detail:
        m_ev = ev_detail.get("main_row_evidence", {})
        m_member = m_ev.get("zip_member", "")
        status_log = ev_detail["main_row_status_log"]
        text_by_id = {}
        if m_member:
            with zipfile.ZipFile(zip_path, "r") as zf:
                matching = [n for n in zf.namelist() if n.endswith(os.path.basename(m_member))]
                if matching:
                    rev_data = json.loads(zf.read(matching[0]).decode("utf-8"))
                    items = rev_data if isinstance(rev_data, list) else rev_data.get("items", rev_data.get("entries", []))
                    for it in items:
                        it_id = it.get("id")
                        if it_id:
                            text_by_id[it_id] = it
                            
        for item in status_log:
            eid = item.get("id")
            norm_st = item.get("normalized_status")
            src_info = text_by_id.get(eid, {})
            p_num = None
            pos_num = None
            if eid and "-" in eid:
                pts = eid.replace("DHS", "").split("-")
                try:
                    p_num = int(pts[0])
                    pos_num = int(pts[1])
                except:
                    pass
            gtype = "CORE" if norm_st == "core" else ("PARTIAL" if norm_st == "partial" else ("UNTRANSLATED" if norm_st == "untranslated" else "CANDIDATE"))
            positions.append({
                "id": eid, "page": p_num, "position": pos_num,
                "source_L": src_info.get("source_L") or src_info.get("source", ""),
                "zh": src_info.get("zh") or src_info.get("chinese_plain_gloss", ""),
                "en": src_info.get("en") or src_info.get("english_paraphrase", ""),
                "gap_type": gtype, "status_detail": item.get("source_status", "")
            })
            
    # Method 3: fresh_main_recount with source file
    elif "fresh_main_recount" in ev_detail and "source" in ev_detail["fresh_main_recount"]:
        src_path = ev_detail["fresh_main_recount"]["source"]
        src_base = os.path.basename(src_path)
        
        with zipfile.ZipFile(zip_path, "r") as zf:
            matching = [n for n in zf.namelist() if n.endswith(src_base)]
            if matching:
                target_file = matching[0]
                if src_base.endswith(".tsv"):
                    raw_tsv = zf.read(target_file).decode("utf-8")
                    reader = csv.DictReader(io.StringIO(raw_tsv), delimiter="\t")
                    by_id = {}
                    for r in reader:
                        if r.get("type") == "MAIN_L":
                            rid = r.get("ID") or r.get("id")
                            if rid:
                                by_id.setdefault(rid, {})[r.get("language")] = r
                    
                    for rid, langs in by_id.items():
                        zh = langs.get("ZH", {})
                        en = langs.get("EN", {})
                        zh_st = zh.get("reviewed_status") or zh.get("accepted_class") or ""
                        p_num = None
                        pos_num = None
                        if rid and "." in rid:
                            pts = rid.split(".")
                            try:
                                p_num = int(pts[0])
                                pos_num = int(pts[1])
                            except:
                                pass
                        gtype = "CORE" if zh_st in ["full_core", "accepted_complete_core"] else ("PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE"))
                        positions.append({
                            "id": rid, "page": p_num, "position": pos_num,
                            "source_L": zh.get("source", ""), "zh": zh.get("reviewed_gloss") or zh.get("gloss", ""),
                            "en": en.get("reviewed_gloss") or en.get("gloss", ""), "gap_type": gtype, "status_detail": zh_st
                        })
                elif src_base.endswith(".json"):
                    tax_data = json.loads(zf.read(target_file).decode("utf-8"))
                    pos_files = [n for n in zf.namelist() if ("POSITION_REGISTER" in n or "L_GLOSS" in n) and n.endswith(".json")]
                    pos_map = {}
                    for pf in pos_files:
                        pdata = json.loads(zf.read(pf).decode("utf-8"))
                        if isinstance(pdata, list):
                            for x in pdata:
                                if x.get("id"):
                                    pos_map[x.get("id")] = x
                                    
                    items = tax_data.get("records") or tax_data.get("entries") or []
                    core_ids = set(tax_data.get("accepted_complete_core_ids", []))
                    part_ids = set(tax_data.get("partial_only_ids", []))
                    cand_ids = set(tax_data.get("candidate_ids", []))
                    untr_ids = set(tax_data.get("untranslated_ids", []))
                    
                    id_by_st = tax_data.get("IDs_by_status", {})
                    if id_by_st:
                        core_ids = set(id_by_st.get("accepted_complete_core_L_paraphrase", []))
                        part_ids = set(id_by_st.get("accepted_partial_only", []))
                        cand_ids = set(id_by_st.get("candidate_retained_not_complete", []))
                        untr_ids = set(id_by_st.get("untranslated_withheld", []))
                    
                    if isinstance(items, list):
                        for it in items:
                            eid = it.get("id")
                            pos_info = pos_map.get(eid, {})
                            p_num = pos_info.get("page")
                            pos_num = pos_info.get("position")
                            if not p_num and eid and "-" in eid:
                                pts = eid.replace("DHS", "").split("-")
                                try:
                                    p_num = int(pts[0])
                                    pos_num = int(pts[1])
                                except:
                                    pass
                            zh_st = it.get("ZH_status") or it.get("status_ZH") or ""
                            if eid in core_ids or "complete_core" in zh_st:
                                gtype = "CORE"
                            elif eid in part_ids or "partial" in zh_st:
                                gtype = "PARTIAL"
                            elif eid in untr_ids or "untranslated" in zh_st:
                                gtype = "UNTRANSLATED"
                            else:
                                gtype = "CANDIDATE"
                            positions.append({
                                "id": eid, "page": p_num, "position": pos_num,
                                "source_L": pos_info.get("source_L") or pos_info.get("source", ""),
                                "zh": pos_info.get("zh", ""), "en": pos_info.get("en", ""),
                                "gap_type": gtype, "status_detail": zh_st or gtype
                            })

    c = sum(1 for x in positions if x["gap_type"] == "CORE")
    p = sum(1 for x in positions if x["gap_type"] == "PARTIAL")
    cand = sum(1 for x in positions if x["gap_type"] == "CANDIDATE")
    u = sum(1 for x in positions if x["gap_type"] == "UNTRANSLATED")
    tot = len(positions)
    match = (tot == exp_total and c == exp_c and p == exp_p and cand == exp_cand and u == exp_u)
    results.append({
        "batch_idx": b_idx, "pkg_name": pkg_name, "positions": positions,
        "tot": tot, "c": c, "p": p, "cand": cand, "u": u,
        "exp_total": exp_total, "exp_c": exp_c, "exp_p": exp_p, "exp_cand": exp_cand, "exp_u": exp_u,
        "match": match
    })

perfect_matches = [r for r in results if r["match"]]
print(f"Perfect matches: {len(perfect_matches)} / {len(results)}")
print(f"Total positions extracted: {sum(r['tot'] for r in results)} / 5762")
print(f"Total core:                {sum(r['c'] for r in results)} / 5106")
print(f"Total partial:             {sum(r['p'] for r in results)} / 499")
print(f"Total candidate:           {sum(r['cand'] for r in results)} / 135")
print(f"Total untranslated:        {sum(r['u'] for r in results)} / 22")

mismatches = [r for r in results if not r["match"]]
if mismatches:
    print(f"\nRemaining {len(mismatches)} mismatches:")
    for m in mismatches:
        print(f"  Batch {m['batch_idx']:02d} ({m['pkg_name'][:30]}): tot={m['tot']}/{m['exp_total']}, c={m['c']}/{m['exp_c']}, p={m['p']}/{m['exp_p']}, cand={m['cand']}/{m['exp_cand']}, u={m['u']}/{m['exp_u']}")
