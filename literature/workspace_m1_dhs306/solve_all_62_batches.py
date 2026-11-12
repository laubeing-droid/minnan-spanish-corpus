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

def parse_batch(b_idx, b):
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
    
    positions = [] # each is (id, page, pos, source_L, zh, en, gap_type, status_detail)
    
    # Check 1: direct main_reviewed_records (e.g. Batch 59)
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
        return positions

    # Check 2: main_row_status_log & main_row_evidence (e.g. Batches 42, 46-58, 60-61)
    if "main_row_status_log" in ev_detail:
        m_ev = ev_detail.get("main_row_evidence", {})
        m_member = m_ev.get("zip_member", "")
        status_log = ev_detail["main_row_status_log"]
        
        text_by_id = {}
        with zipfile.ZipFile(zip_path, "r") as zf:
            matching = [n for n in zf.namelist() if n.endswith(os.path.basename(m_member))] if m_member else []
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
        return positions

    # Check 3: Check inside zipfile
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        
        # 3a: TSV final semantic review
        tsv_files = [n for n in namelist if any(k in n for k in ["FINAL_SEMANTIC_REVIEW", "INDEPENDENT_SEMANTIC_REVIEW", "SEMANTIC_REVIEW"]) and n.endswith(".tsv")]
        if tsv_files:
            raw_tsv = zf.read(tsv_files[0]).decode("utf-8")
            reader = csv.DictReader(io.StringIO(raw_tsv), delimiter="\t")
            by_id = {}
            for r in reader:
                sc = (r.get("type") or r.get("scope") or "").strip().lower()
                if sc in ["main_l", "main", "mainl", ""]:
                    rid = (r.get("ID") or r.get("id") or "").strip()
                    lang = (r.get("language") or "").strip().upper()
                    if rid and lang in ["ZH", "EN"]:
                        by_id.setdefault(rid, {})[lang] = r
            
            if len(by_id) == exp_total:
                for rid, langs in by_id.items():
                    zh = langs.get("ZH", {})
                    en = langs.get("EN", {})
                    zh_st = (zh.get("reviewed_status") or zh.get("accepted_class") or zh.get("classification") or zh.get("status") or "").strip().lower()
                    
                    p_num = None
                    pos_num = None
                    if rid and "." in rid:
                        pts = rid.split(".")
                        try:
                            p_num = int(pts[0])
                            pos_num = int(pts[1])
                        except:
                            pass
                    elif rid and "-" in rid:
                        pts = rid.replace("DHS", "").split("-")
                        try:
                            p_num = int(pts[0])
                            pos_num = int(pts[1])
                        except:
                            pass
                            
                    gtype = "CORE" if zh_st in ["full_core", "accepted_complete_core", "complete_core"] else ("PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE"))
                    positions.append({
                        "id": rid, "page": p_num, "position": pos_num,
                        "source_L": zh.get("source") or zh.get("source_L") or "",
                        "zh": zh.get("reviewed_gloss") or zh.get("gloss") or zh.get("candidate_gloss") or zh.get("text") or "",
                        "en": en.get("reviewed_gloss") or en.get("gloss") or en.get("candidate_gloss") or en.get("text") or "",
                        "gap_type": gtype, "status_detail": zh_st
                    })
                return positions

        # 3b: Taxonomy JSON
        tax_files = [n for n in namelist if "ACCEPTANCE_TAXONOMY" in n and n.endswith(".json")]
        if tax_files:
            # find matching position register
            pos_files = [n for n in namelist if ("POSITION_REGISTER" in n or "L_GLOSS" in n) and n.endswith(".json")]
            pos_map = {}
            for pf in pos_files:
                pdata = json.loads(zf.read(pf).decode("utf-8"))
                if isinstance(pdata, list):
                    for x in pdata:
                        if x.get("id"):
                            pos_map[x.get("id")] = x
            
            tax_data = json.loads(zf.read(tax_files[-1]).decode("utf-8"))
            
            # case A: dict with records or entries
            items = tax_data.get("records") or tax_data.get("entries") or []
            if isinstance(items, list) and len(items) == exp_total:
                core_ids = set(tax_data.get("accepted_complete_core_ids", []))
                part_ids = set(tax_data.get("partial_only_ids", []))
                cand_ids = set(tax_data.get("candidate_ids", []))
                untr_ids = set(tax_data.get("untranslated_ids", []))
                
                # if IDs_by_status present
                id_by_st = tax_data.get("IDs_by_status", {})
                if id_by_st:
                    core_ids = set(id_by_st.get("accepted_complete_core_L_paraphrase", []))
                    part_ids = set(id_by_st.get("accepted_partial_only", []))
                    cand_ids = set(id_by_st.get("candidate_retained_not_complete", []))
                    untr_ids = set(id_by_st.get("untranslated_withheld", []))
                
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
                return positions

        # 3c: SUBSTANTIVE_REVIEW or FINAL_L_SEMANTIC_REVIEW
        rev_files = [n for n in namelist if ("SUBSTANTIVE_REVIEW" in n or "FINAL_L_SEMANTIC_REVIEW" in n) and n.endswith(".json")]
        if rev_files:
            rdata = json.loads(zf.read(rev_files[-1]).decode("utf-8"))
            items = rdata if isinstance(rdata, list) else rdata.get("items", rdata.get("entries", []))
            if len(items) == exp_total:
                for it in items:
                    eid = it.get("id")
                    st = it.get("status") or it.get("proposed_core_status") or it.get("translation_status", "")
                    part = it.get("partial", False)
                    withheld = it.get("withheld", False)
                    p_num = it.get("page")
                    pos_num = it.get("position")
                    if not p_num and eid and "-" in eid:
                        pts = eid.replace("DHS", "").split("-")
                        try:
                            p_num = int(pts[0])
                            pos_num = int(pts[1])
                        except:
                            pass
                    gtype = "CORE" if ("complete_core" in st and not part and not withheld) else ("PARTIAL" if (part or "partial" in st) else ("UNTRANSLATED" if (withheld or "untranslated" in st) else "CANDIDATE"))
                    positions.append({
                        "id": eid, "page": p_num, "position": pos_num,
                        "source_L": it.get("source_L") or it.get("source", ""),
                        "zh": it.get("zh") or it.get("chinese_plain_gloss", ""),
                        "en": it.get("en") or it.get("english_paraphrase", ""),
                        "gap_type": gtype, "status_detail": st
                    })
                return positions

    return positions

# Test all 62
mismatch_batches = []
total_pos_all = 0
total_c_all = 0
total_p_all = 0
total_cand_all = 0
total_u_all = 0

for i, b in enumerate(batches):
    expected_zh = b.get("ZH", {})
    exp_c = expected_zh.get("core", 0)
    exp_p = expected_zh.get("partial", 0)
    exp_cand = expected_zh.get("candidate", 0)
    exp_u = expected_zh.get("untranslated", 0)
    exp_total = exp_c + exp_p + exp_cand + exp_u
    
    res = parse_batch(i, b)
    c = sum(1 for x in res if x["gap_type"] == "CORE")
    p = sum(1 for x in res if x["gap_type"] == "PARTIAL")
    cand = sum(1 for x in res if x["gap_type"] == "CANDIDATE")
    u = sum(1 for x in res if x["gap_type"] == "UNTRANSLATED")
    tot = len(res)
    
    total_pos_all += tot
    total_c_all += c
    total_p_all += p
    total_cand_all += cand
    total_u_all += u
    
    match = (tot == exp_total and c == exp_c and p == exp_p and cand == exp_cand and u == exp_u)
    if not match:
        pkg_name = os.path.basename(b.get("package_path", ""))
        mismatch_batches.append((i, pkg_name, (tot, exp_total), (c, exp_c), (p, exp_p), (cand, exp_cand), (u, exp_u)))

print(f"Total batches matched perfectly: {62 - len(mismatch_batches)} / 62")
print(f"Total positions: {total_pos_all} (Target: 5762)")
print(f"Core:            {total_c_all} (Target: 5106)")
print(f"Partial:         {total_p_all} (Target: 499)")
print(f"Candidate:       {total_cand_all} (Target: 135)")
print(f"Untranslated:    {total_u_all} (Target: 22)")

if mismatch_batches:
    print("\nMismatch batches detail:")
    for m in mismatch_batches:
        print(f"  Batch {m[0]:02d} {m[1][:30]}: tot={m[2]}, c={m[3]}, p={m[4]}, cand={m[5]}, u={m[6]}")
