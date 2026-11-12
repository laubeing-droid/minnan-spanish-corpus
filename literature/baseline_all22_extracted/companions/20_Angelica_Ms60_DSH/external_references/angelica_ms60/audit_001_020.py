from pathlib import Path
import re,json,hashlib
s=Path('/workspace/shared/minnan_transcription/angelica_ms60/blind_v1');o=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation/angelica_ms60/collation_v1')
records=[]
for n in range(1,21):
 a=(s/f'pdf_{n:03}.md').read_text();p=o/f'pdf_{n:03}_visual_v2.md';q=o/f'pdf_{n:03}_review.md';assert p.exists() and q.exists(),n
 b=p.read_text().split('## 第二視覺校記')[0]
 # Only main entry lines contain vertical bar. Annotation lines may repeat IDs and are not extra entries.
 ids=lambda t:[line.split()[0] for line in t.splitlines() if re.match(r'^(?:R\d|C\d)',line) and '｜' in line]
 assert ids(a)==ids(b),(n,ids(a),ids(b))
 footer=re.findall(r'-\s*\d+\s*-',a)
 assert all(f in b for f in footer),(n,'footer')
 records.append({'pdf':n,'entry_ids':ids(a),'id_order_equal':True,'entry_count':len(ids(a)),'facsimile_footer_preserved':True,'visual_v2':str(p),'review':str(q),'visual_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'review_sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
obj={'scope':'Angelica PDF001–020','count_visual_v2':20,'count_review':20,'entry_count':sum(x['entry_count'] for x in records),'caveat':'ID/頁腳核驗僅證結構完整，不是轉寫準確率；封面及題記無格組ID；附註重複ID不另算詞條。物理同葉、淡墨、異體與音寫細筆仍有未解項。','pages':records}
with (o/'audit_manifest_001_020_complete.json').open('x') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
print(obj['entry_count'])
