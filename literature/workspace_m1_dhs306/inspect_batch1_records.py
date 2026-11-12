import zipfile
import json

zip_path = "literature/assets/dhs306/DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z.zip"
with zipfile.ZipFile(zip_path, 'r') as zf:
    n = "DHS0840_0844_ORIGINAL_ZH_EN_WORKPACK_20261027T093816Z/work/INDEPENDENT_L_GLOSS_ACCEPTANCE_TAXONOMY_99_20261027T0932Z.json"
    content = json.loads(zf.read(n).decode('utf-8'))
    print("accepted_complete_core_ids len:", len(content.get('accepted_complete_core_ids', [])))
    print("partial_only_ids len:", len(content.get('partial_only_ids', [])))
    print("candidate_ids len:", len(content.get('candidate_ids', [])))
    print("untranslated_ids len:", len(content.get('untranslated_ids', [])))
    print("records len:", len(content.get('records', [])))
    print("Sample record 0:", content.get('records', [])[0])
