import json
import zipfile
from collections import Counter

zip38 = "literature/assets/dhs306/DHS1025_1029_REVIEWED_PORTABLE_20261027T2007Z.zip"
with zipfile.ZipFile(zip38) as zf:
    data = json.loads(zf.read("DHS1025_1029_REVIEWED_PORTABLE_20261027T2007Z/independent_review/SEMANTIC_REVIEW_206_FINAL_REV04.json").decode('utf-8'))
    zh_items = [x for x in data if x.get('language') == 'zh']
    print("ZH scopes:", Counter(x.get('scope') for x in zh_items))
    print("ZH types:", Counter(x.get('type') for x in zh_items))
    l_zh = [x for x in zh_items if x.get('scope') == 'L']
    print("Batch 38 scope L count:", len(l_zh))
    print("Batch 38 scope L statuses:", Counter(x.get('translation_status') for x in l_zh))
    print("Batch 38 target:", b38['ZH'])
