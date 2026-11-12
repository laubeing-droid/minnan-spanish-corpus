"""
Extract exactly the 656 certified M1 L-layer gaps from the 62 high-water dhs306 batches,
guaranteeing 100% mathematical closure against MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json:
- Total positions examined: 5,762
- Core completed: 5,106
- Partial gaps: 499
- Candidate gaps: 135
- Untranslated gaps: 22
- Total certified gaps: 656
"""

import json
import zipfile
import os
import csv
import io

WORKSPACE_ROOT = r"D:\Codex\2.闽南文史工作区\闽南文献迁移"
ASSETS_DIR = os.path.join(WORKSPACE_ROOT, "literature", "assets")
DHS306_DIR = os.path.join(ASSETS_DIR, "dhs306")
REGISTER_FILE = os.path.join(ASSETS_DIR, "MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json")
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "literature", "workspace_m1_dhs306", "l_layer_gaps_queue.json")

with open(REGISTER_FILE, "r", encoding="utf-8") as f:
    reg = json.load(f)

batches = reg["batches"]
print(f"Loaded master register with {len(batches)} batches.")

total_positions = 0
total_core = 0
total_partial = 0
total_candidate = 0
total_untranslated = 0

all_gap_entries = []

for b_idx, b in enumerate(batches):
    pages = b.get("pages", [])
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
    
    batch_positions = 0
    batch_core = 0
    batch_gaps = []
    
    # -------------------------------------------------------------
    # Pattern 1: Batch 59 has direct 'main_reviewed_records'
    # -------------------------------------------------------------
    if "main_reviewed_records" in ev_detail:
        records = ev_detail["main_reviewed_records"]
        for r_idx, r in enumerate(records):
            p = r.get("page")
            pos = r.get("position")
            eid = f"DHS{p:04d}-{pos:02d}"
            part = r.get("partial", False)
            withheld = r.get("withheld", False)
            st = r.get("proposed_core_status", "")
            
            if "complete_core" in st and not part and not withheld:
                batch_core += 1
            else:
                gtype = "PARTIAL" if part else ("UNTRANSLATED" if withheld else "CANDIDATE")
                batch_gaps.append({
                    "id": eid,
                    "page": p,
                    "position": pos,
                    "source_L": r.get("source_L", ""),
                    "zh": r.get("chinese_plain_gloss", ""),
                    "en": r.get("english_paraphrase", ""),
                    "package": pkg_name,
                    "gap_type": gtype,
                    "status_detail": st
                })
            batch_positions += 1

    # -------------------------------------------------------------
    # Pattern 2: 'main_row_status_log' and 'main_row_evidence' (e.g. Batches 42-61)
    # -------------------------------------------------------------
    elif "main_row_evidence" in ev_detail and "main_row_status_log" in ev_detail:
        m_ev = ev_detail["main_row_evidence"]
        m_member = m_ev.get("zip_member")
        status_log = ev_detail["main_row_status_log"]
        
        # Read the exact substantive review file for source texts
        text_by_id = {}
        with zipfile.ZipFile(zip_path, "r") as zf:
            matching = [n for n in zf.namelist() if n.endswith(os.path.basename(m_member))]
            if matching:
                rev_data = json.loads(zf.read(matching[0]).decode("utf-8"))
                # could be list or dict
                items = rev_data if isinstance(rev_data, list) else rev_data.get("items", rev_data.get("entries", []))
                for it in items:
                    it_id = it.get("id")
                    if it_id:
                        text_by_id[it_id] = it

        for item in status_log:
            eid = item.get("id")
            norm_st = item.get("normalized_status")
            src_info = text_by_id.get(eid, {})
            
            # parse page & pos from eid DHS1085-01
            p_num = None
            pos_num = None
            if eid and "-" in eid:
                p_parts = eid.replace("DHS", "").split("-")
                try:
                    p_num = int(p_parts[0])
                    pos_num = int(p_parts[1])
                except:
                    pass
            
            if norm_st == "core":
                batch_core += 1
            else:
                gtype = "PARTIAL" if norm_st == "partial" else ("UNTRANSLATED" if norm_st == "untranslated" else "CANDIDATE")
                batch_gaps.append({
                    "id": eid,
                    "page": p_num,
                    "position": pos_num,
                    "source_L": src_info.get("source_L") or src_info.get("source", ""),
                    "zh": src_info.get("zh") or src_info.get("chinese_plain_gloss", ""),
                    "en": src_info.get("en") or src_info.get("english_paraphrase", ""),
                    "package": pkg_name,
                    "gap_type": gtype,
                    "status_detail": item.get("source_status", "")
                })
            batch_positions += 1

    # -------------------------------------------------------------
    # Pattern 3: 'recount_evidence' contains MAIN_L evidence (JSON or TSV)
    # -------------------------------------------------------------
    elif "recount_evidence" in ev_detail:
        recount_ev = ev_detail["recount_evidence"]
        main_l_ev = next((rev for rev in recount_ev if rev.get("layer") == "MAIN_L"), None)
        
        if main_l_ev:
            ev_file = os.path.basename(main_l_ev.get("evidence", ""))
            with zipfile.ZipFile(zip_path, "r") as zf:
                matching = [n for n in zf.namelist() if n.endswith(ev_file)]
                target_path = matching[0]
                
                if ev_file.endswith(".tsv"):
                    raw_tsv = zf.read(target_path).decode("utf-8")
                    reader = csv.DictReader(io.StringIO(raw_tsv), delimiter="\t")
                    by_id = {}
                    for r in reader:
                        if r.get("type") == "MAIN_L":
                            rid = r.get("ID")
                            if rid:
                                by_id.setdefault(rid, {})[r.get("language")] = r
                    
                    for rid, langs in by_id.items():
                        zh = langs.get("ZH", {})
                        en = langs.get("EN", {})
                        zh_st = zh.get("reviewed_status", "")
                        
                        p_num = None
                        pos_num = None
                        if rid and "." in rid:
                            pts = rid.split(".")
                            try:
                                p_num = int(pts[0])
                                pos_num = int(pts[1])
                            except:
                                pass
                        
                        if zh_st == "full_core":
                            batch_core += 1
                        else:
                            gtype = "PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE")
                            batch_gaps.append({
                                "id": rid,
                                "page": p_num,
                                "position": pos_num,
                                "source_L": zh.get("source", ""),
                                "zh": zh.get("reviewed_gloss", ""),
                                "en": en.get("reviewed_gloss", ""),
                                "package": pkg_name,
                                "gap_type": gtype,
                                "status_detail": zh_st
                            })
                        batch_positions += 1

                elif ev_file.endswith(".json"):
                    content = json.loads(zf.read(target_path).decode("utf-8"))
                    
                    # Check if Type 1: dict with 'entries' and external position register
                    if isinstance(content, dict) and "entries" in content:
                        reg_files = [n for n in zf.namelist() if "POSITION_REGISTER_ZH_EN.json" in n]
                        pos_map = {}
                        if reg_files:
                            rdata = json.loads(zf.read(reg_files[0]).decode("utf-8"))
                            if isinstance(rdata, list):
                                pos_map = {x.get("id"): x for x in rdata}
                        
                        for entry in content.get("entries", []):
                            eid = entry.get("id")
                            zh_st = entry.get("ZH_status", "")
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
                            
                            if "accepted_complete_core" in zh_st:
                                batch_core += 1
                            else:
                                gtype = "PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE")
                                batch_gaps.append({
                                    "id": eid,
                                    "page": p_num,
                                    "position": pos_num,
                                    "source_L": pos_info.get("source_L") or pos_info.get("source", ""),
                                    "zh": pos_info.get("zh", ""),
                                    "en": pos_info.get("en", ""),
                                    "package": pkg_name,
                                    "gap_type": gtype,
                                    "status_detail": zh_st
                                })
                            batch_positions += 1

                    elif isinstance(content, list):
                        for item in content:
                            eid = item.get("id")
                            tax = item.get("independent_acceptance_taxonomy", "")
                            part = item.get("partial", False)
                            withheld = item.get("withheld", False)
                            
                            if "accepted_complete_core" in tax and not part and not withheld:
                                batch_core += 1
                            else:
                                gtype = "PARTIAL" if (part or "partial" in tax) else ("UNTRANSLATED" if (withheld or "untranslated" in tax) else "CANDIDATE")
                                batch_gaps.append({
                                    "id": eid,
                                    "page": item.get("page"),
                                    "position": item.get("position"),
                                    "source_L": item.get("source_L") or item.get("source", ""),
                                    "zh": item.get("zh", ""),
                                    "en": item.get("en", ""),
                                    "package": pkg_name,
                                    "gap_type": gtype,
                                    "status_detail": tax
                                })
                            batch_positions += 1

    # -------------------------------------------------------------
    # Pattern 4: Fallback / other batches with fresh_main_recount or light package
    # -------------------------------------------------------------
    if batch_positions == 0:
        # Check if zip contains SUBSTANTIVE_REVIEW or CANDIDATE_DATA or tsv
        with zipfile.ZipFile(zip_path, "r") as zf:
            sub_files = [n for n in zf.namelist() if "SUBSTANTIVE_REVIEW" in n and n.endswith(".json")]
            author_l = [n for n in zf.namelist() if ("FINAL_L_SEMANTIC_REVIEW" in n or "_L_ZH_EN" in n) and n.endswith(".json")]
            cand_files = [n for n in zf.namelist() if "CANDIDATE_DATA" in n and n.endswith(".json")]
            tsv_files = [n for n in zf.namelist() if "FINAL_SEMANTIC_REVIEW" in n and n.endswith(".tsv")]
            
            if sub_files:
                sdata = json.loads(zf.read(sub_files[0]).decode("utf-8"))
                items = sdata if isinstance(sdata, list) else sdata.get("items", sdata.get("entries", []))
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
                    
                    if "complete_core" in st and not part and not withheld:
                        batch_core += 1
                    else:
                        gtype = "PARTIAL" if (part or "partial" in st) else ("UNTRANSLATED" if (withheld or "untranslated" in st) else "CANDIDATE")
                        batch_gaps.append({
                            "id": eid,
                            "page": p_num,
                            "position": pos_num,
                            "source_L": it.get("source_L") or it.get("source", ""),
                            "zh": it.get("zh") or it.get("chinese_plain_gloss", ""),
                            "en": it.get("en") or it.get("english_paraphrase", ""),
                            "package": pkg_name,
                            "gap_type": gtype,
                            "status_detail": st
                        })
                    batch_positions += 1

            elif author_l:
                adata = json.loads(zf.read(author_l[0]).decode("utf-8"))
                items = adata if isinstance(adata, list) else adata.get("items", adata.get("entries", []))
                for it in items:
                    eid = it.get("id")
                    st = it.get("translation_status") or it.get("status") or ""
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
                    
                    if "complete_core" in st and not part and not withheld:
                        batch_core += 1
                    else:
                        gtype = "PARTIAL" if (part or "partial" in st) else ("UNTRANSLATED" if (withheld or "untranslated" in st) else "CANDIDATE")
                        batch_gaps.append({
                            "id": eid,
                            "page": p_num,
                            "position": pos_num,
                            "source_L": it.get("source_L") or it.get("source", ""),
                            "zh": it.get("zh") or it.get("chinese_plain_gloss", ""),
                            "en": it.get("en") or it.get("english_paraphrase", ""),
                            "package": pkg_name,
                            "gap_type": gtype,
                            "status_detail": st
                        })
                    batch_positions += 1

            elif cand_files:
                cdata = json.loads(zf.read(cand_files[-1]).decode("utf-8"))
                glosses = cdata.get("glosses", {})
                statuses = cdata.get("gloss_statuses", {})
                for item_id, st in statuses.items():
                    zh_st = st.get("zh_status", "") if isinstance(st, dict) else st
                    p_str, pos_str = item_id.split(".")
                    p_int = int(p_str)
                    pos_int = int(pos_str)
                    gloss_pair = ["", ""]
                    if p_str in glosses and len(glosses[p_str]) >= pos_int:
                        gloss_pair = glosses[p_str][pos_int - 1]
                    
                    if zh_st == "full_core":
                        batch_core += 1
                    else:
                        gtype = "PARTIAL" if "partial" in str(zh_st) else ("UNTRANSLATED" if "untranslated" in str(zh_st) else "CANDIDATE")
                        batch_gaps.append({
                            "id": item_id,
                            "page": p_int,
                            "position": pos_int,
                            "source_L": "", # Will pull from baseline text if needed
                            "zh": gloss_pair[0] if isinstance(gloss_pair, list) else "",
                            "en": gloss_pair[1] if isinstance(gloss_pair, list) and len(gloss_pair) > 1 else "",
                            "package": pkg_name,
                            "gap_type": gtype,
                            "status_detail": zh_st
                        })
                    batch_positions += 1

    # Check alignment for this batch
    p_count = sum(1 for g in batch_gaps if g["gap_type"] == "PARTIAL")
    c_count = sum(1 for g in batch_gaps if g["gap_type"] == "CANDIDATE")
    u_count = sum(1 for g in batch_gaps if g["gap_type"] == "UNTRANSLATED")
    
    total_positions += batch_positions
    total_core += batch_core
    total_partial += p_count
    total_candidate += c_count
    total_untranslated += u_count
    all_gap_entries.extend(batch_gaps)
    
    diff = (batch_positions != exp_total) or (batch_core != exp_c) or (p_count != exp_p) or (c_count != exp_cand) or (u_count != exp_u)
    if diff:
        print(f"Batch {b_idx:02d} ({pkg_name[:30]}): EXAMINED={batch_positions}/{exp_total}, CORE={batch_core}/{exp_c}, P={p_count}/{exp_p}, C={c_count}/{exp_cand}, U={u_count}/{exp_u} [MISMATCH]")

print("\n================ FINAL MASTER ALIGNMENT ================")
print(f"Total positions: {total_positions} (Expected: 5762, Diff: {total_positions - 5762})")
print(f"Core completed:  {total_core} (Expected: 5106, Diff: {total_core - 5106})")
print(f"Partial gaps:    {total_partial} (Expected: 499, Diff: {total_partial - 499})")
print(f"Candidate gaps:  {total_candidate} (Expected: 135, Diff: {total_candidate - 135})")
print(f"Untranslated:    {total_untranslated} (Expected: 22, Diff: {total_untranslated - 22})")
print(f"Total gap queue: {len(all_gap_entries)} (Expected: 656, Diff: {len(all_gap_entries) - 656})")

if len(all_gap_entries) == 656 and total_positions == 5762 and total_core == 5106:
    output_obj = {
        "audit_metadata": {
            "status": "CERTIFIED_100_PERCENT_ALIGNED_WITH_REGISTER_306P",
            "total_batches": len(batches),
            "total_positions_examined": total_positions,
            "core_completed": total_core,
            "gaps_count_certified": len(all_gap_entries),
            "breakdown": {
                "partial": total_partial,
                "candidate": total_candidate,
                "untranslated": total_untranslated
            }
        },
        "queue_entries": all_gap_entries
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_obj, f, ensure_ascii=False, indent=2)
    print(f"\n[SUCCESS] Certified M1 Queue successfully saved to {OUTPUT_FILE}")
else:
    print(f"\n[WARNING] Mathematical closure not yet 100% - see diffs above.")
