from pathlib import Path
import re,json,hashlib,datetime
O=Path(__file__).resolve().parent
src=O/'Arte_Grammar_all122_method_transfer_v3.md'; rows=src.read_text().splitlines(); clean=[]; moved=[]; mp=[];page=0;skip=False
for i,l in enumerate(rows,1):
 if l.startswith('## PDF '):page=int(l.split()[-1]);skip=False
 elif l.startswith('## '):skip=bool(re.search('当前|首稿自检|不确定|空白及不确定',l))
 drop=skip or bool(re.match(r'^(仅视觉|仅据|封存首稿|外部比较|日期：|已读visual|这是真实|原ID、|以下为|本次|本稿|原文中)',l))
 # General historical workflow remarks, not transcription lines.
 if not re.match(r'^[A-Z]\d|^\s+|^〔|^#',l) and any(w in l for w in ['首稿','未联网','未查参考','未读参考','不覆盖','刊本定位','external_check']):drop=True
 if l.startswith('- ') or re.match(r'^\d+\. .*首稿',l):drop=True
 if drop:
  moved.append({'page':page,'source_line':i,'text':l});mp.append({'source_line':i,'destination':'relocated_workflow_and_residual_notes_v3.json','final_line':None});continue
 mp.append({'source_line':i,'destination':'Arte_Grammar_all122_body_clean_v3.md','final_line':len(clean)+1});clean.append(l)
def write(name,s):
 with (O/name).open('x') as f:f.write(s)
write('Arte_Grammar_all122_body_clean_v3.md','\n'.join(clean)+'\n')
write('relocated_workflow_and_residual_notes_v3.json',json.dumps(moved,ensure_ascii=False,indent=2)+'\n')
write('final_body_line_mapping_v3.json',json.dumps({'source':str(src),'mapping':mp},ensure_ascii=False,indent=2)+'\n')
coverage=json.loads((O/'coverage_all122_method_transfer_v3.json').read_text())
assert len(coverage['pages'])==122
assert len(re.findall(r'^## PDF \d+$','\n'.join(clean),re.M))==122
# Preserve all numbered manuscript row labels from per-page layer in final output.
checks=[]
for n in range(1,123):
 orig=(O/'text'/f'pdf_{n:03}.md').read_text(); final='\n'.join(clean).split(f'## PDF {n:03}\n',1)[1].split('\n## PDF ',1)[0]
 a=re.findall(r'^([A-Z]\d\d[a-z]?)\s',orig,re.M);b=re.findall(r'^([A-Z]\d\d[a-z]?)\s',final,re.M)
 checks.append({'page':n,'source_row_ids':len(a),'final_row_ids':len(b),'row_sequence_equal':a==b})
assert all(x['row_sequence_equal'] for x in checks)
files=[p for p in O.iterdir() if p.is_file()]
write('final_integrity_acceptance_v3.json',json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':122,'all_122_images_directly_viewed':True,'full_text_verified':False,'row_checks':checks,'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in files],'prior_files_overwritten':False,'prior_hash_baseline_available':False,'note':'源文件现存哈希用于追溯；没有本轮启动前哈希基线，不能虚称通过前后哈希不变验证。源行映射是文字保全核验，不是识读准确率。'},ensure_ascii=False,indent=2)+'\n')
print('final',len(clean),'lines;',sum(x['source_row_ids'] for x in checks),'row labels preserved; moved',len(moved))
