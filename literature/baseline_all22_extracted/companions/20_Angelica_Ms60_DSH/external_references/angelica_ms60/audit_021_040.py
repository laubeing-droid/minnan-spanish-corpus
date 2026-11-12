from pathlib import Path
import re,json,hashlib
s=Path('/workspace/shared/minnan_transcription/angelica_ms60/blind_v1');o=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation/angelica_ms60/collation_v1')
rows=[]
for n in range(21,41):
 p=s/f'pdf_{n:03}.md';a=p.read_text();v=o/f'pdf_{n:03}_visual_v2.md';r=o/f'pdf_{n:03}_review.md';assert v.exists() and r.exists(),n
 b=v.read_text().split('## 第二視覺校記')[0]
 get=lambda t:[l.split()[0] for l in t.splitlines() if re.match(r'^(?:R\d|C\d)',l) and '｜' in l]
 ai,bi=get(a),get(b); assert len(bi)==len(set(bi)),(n,'duplicate main IDs')
 if ai: assert ai==bi,(n,'source IDs')
 assert re.search(r'-\s*'+str(n-1)+r'\s*-',b),(n,'footer')
 # Preserve the unmodified source separately in the audit mapping; generated IDs refer to current v2 rows only.
 rows.append({'pdf':n,'original_had_ids':bool(ai),'original_ids':ai,'v2_ids':bi,'entry_count':len(bi),'id_check':'original sequence equal' if ai else 'new stable IDs; see per-batch source-block mapping','footer_preserved':True,'source':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'visual_v2':str(v),'review':str(r)})
obj={'scope':'021–040','visual_v2_count':20,'review_count':20,'main_entries':sum(x['entry_count'] for x in rows),'limits':'Coverage and ID checks are structural, not accuracy. Pages026–040 originally have no IDs; new IDs must not be represented as inherited source IDs. Physical same-leaf identification remains unresolved.','pages':rows}
with (o/'audit_manifest_021_040_complete.json').open('x') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
print(obj['main_entries'])
