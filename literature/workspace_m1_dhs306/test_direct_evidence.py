import json
import zipfile
import os
import csv
import io

with open("literature/assets/MINNAN_CURRENT_HANDOFF_REGISTER_306P_20261027T2126Z.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

print(f"Total batches: {len(reg['batches'])}")

all_extracted_gaps = []
stats = {
    "total_batches": len(reg['batches']),
    "total_positions": 0,
    "core": 0,
    "partial": 0,
    "candidate": 0,
    "untranslated": 0
}

for i, b in enumerate(reg['batches']):
    pkg_path = b.get("package_path", "")
    pkg_name = os.path.basename(pkg_path)
    zip_path = os.path.join("literature/assets/dhs306", pkg_name)
    ev_detail = b.get("evidence_detail", {})
    recount_ev = ev_detail.get("recount_evidence", [])
    
    # find MAIN_L recount evidence
    main_l_ev = None
    for rev in recount_ev:
        if rev.get("layer") == "MAIN_L":
            main_l_ev = rev
            break
            
    if not main_l_ev:
        print(f"Batch {i} ({pkg_name}): NO MAIN_L evidence in recount_evidence!")
        continue
        
    ev_file = os.path.basename(main_l_ev.get("evidence", ""))
    target_counts = main_l_ev.get("per_language_recomputed_counts", {}).get("ZH", {})
    
    # open zip and locate ev_file
    with zipfile.ZipFile(zip_path, 'r') as zf:
        matching = [n for n in zf.namelist() if n.endswith(ev_file)]
        if not matching:
            print(f"Batch {i}: Could not find {ev_file} in {pkg_name}!")
            continue
        target_path = matching[0]
        
        # parse according to file type
        batch_gaps = []
        if ev_file.endswith(".json"):
            content = json.loads(zf.read(target_path).decode('utf-8'))
            # check if list of positions (Type 1)
            if isinstance(content, list):
                for item in content:
                    tax = item.get("independent_acceptance_taxonomy", "")
                    part = item.get("partial", False)
                    withheld = item.get("withheld", False)
                    if "accepted_complete_core" in tax and not part:
                        stats["core"] += 1
                    else:
                        gtype = "PARTIAL" if (part or "partial" in tax) else ("UNTRANSLATED" if (withheld or "untranslated" in tax) else "CANDIDATE")
                        stats[gtype.lower()] += 1
                        batch_gaps.append({
                            "id": item.get("id"),
                            "page": item.get("page"),
                            "position": item.get("position"),
                            "source_L": item.get("source_L") or item.get("source"),
                            "zh": item.get("zh"),
                            "en": item.get("en"),
                            "package": pkg_name,
                            "gap_type": gtype,
                            "raw_taxonomy": tax
                        })
                    stats["total_positions"] += 1
            elif isinstance(content, dict) and "entries" in content:
                # Type 1 format with separate entries and position register
                # let's also read L_GLOSS_*_POSITION_REGISTER_ZH_EN.json if available
                reg_files = [n for n in zf.namelist() if "POSITION_REGISTER_ZH_EN.json" in n]
                pos_map = {}
                if reg_files:
                    rdata = json.loads(zf.read(reg_files[0]).decode('utf-8'))
                    if isinstance(rdata, list):
                        pos_map = {x.get("id"): x for x in rdata}
                
                entries = content.get("entries", [])
                for entry in entries:
                    zh_st = entry.get("ZH_status", "")
                    eid = entry.get("id")
                    pos_info = pos_map.get(eid, {})
                    if "accepted_complete_core" in zh_st:
                        stats["core"] += 1
                    else:
                        gtype = "PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE")
                        stats[gtype.lower()] += 1
                        batch_gaps.append({
                            "id": eid,
                            "page": pos_info.get("page"),
                            "position": pos_info.get("position"),
                            "source_L": pos_info.get("source_L") or pos_info.get("source"),
                            "zh": pos_info.get("zh"),
                            "en": pos_info.get("en"),
                            "package": pkg_name,
                            "gap_type": gtype,
                            "raw_taxonomy": zh_st
                        })
                    stats["total_positions"] += 1
            elif isinstance(content, dict) and "items" in content:
                for item in content.get("items", []):
                    st = item.get("translation_status", "")
                    if "complete_core" in st:
                        stats["core"] += 1
                    else:
                        gtype = "PARTIAL" if "partial" in st else ("UNTRANSLATED" if "untranslated" in st else "CANDIDATE")
                        stats[gtype.lower()] += 1
                        batch_gaps.append({
                            "id": item.get("id"),
                            "page": item.get("page"),
                            "position": item.get("position"),
                            "source_L": item.get("source"),
                            "zh": item.get("zh"),
                            "en": item.get("en"),
                            "package": pkg_name,
                            "gap_type": gtype,
                            "raw_taxonomy": st
                        })
                    stats["total_positions"] += 1
                    
        elif ev_file.endswith(".tsv"):
            raw_tsv = zf.read(target_path).decode('utf-8')
            reader = csv.DictReader(io.StringIO(raw_tsv), delimiter='\t')
            by_id = {}
            for r in reader:
                if r.get('type') == 'MAIN_L':
                    rid = r.get('ID')
                    if rid not in by_id:
                        by_id[rid] = {}
                    by_id[rid][r.get('language')] = r
            
            for rid, langs in by_id.items():
                zh = langs.get('ZH', {})
                en = langs.get('EN', {})
                zh_st = zh.get('reviewed_status', '')
                if zh_st == 'full_core':
                    stats["core"] += 1
                else:
                    gtype = "PARTIAL" if "partial" in zh_st else ("UNTRANSLATED" if "untranslated" in zh_st else "CANDIDATE")
                    stats[gtype.lower()] += 1
                    
                    # parse page and position from rid (e.g. 0845.01)
                    p_num = None
                    pos_num = None
                    if rid and "." in rid:
                        parts = rid.split(".")
                        try:
                            p_num = int(parts[0])
                            pos_num = int(parts[1])
                        except:
                            pass
                    batch_gaps.append({
                        "id": rid,
                        "page": p_num,
                        "position": pos_num,
                        "source_L": zh.get("source"),
                        "zh": zh.get("reviewed_gloss"),
                        "en": en.get("reviewed_gloss"),
                        "package": pkg_name,
                        "gap_type": gtype,
                        "raw_taxonomy": zh_st
                    })
                stats["total_positions"] += 1
                
        all_extracted_gaps.extend(batch_gaps)

print("\n--- Direct Recount Evidence Extraction Summary ---")
print(f"Total positions processed: {stats['total_positions']} (Target: 5762)")
print(f"Core: {stats['core']} (Target: 5106)")
print(f"Partial: {stats['partial']} (Target: 499)")
print(f"Candidate: {stats['candidate']} (Target: 135)")
print(f"Untranslated: {stats['untranslated']} (Target: 22)")
print(f"Total gaps: {len(all_extracted_gaps)} (Target: 656)")
