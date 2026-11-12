from pathlib import Path
import json,hashlib,re
b=Path('/workspace/shared/minnan_transcription/hab_91_2_extrav_06/method_transfer_v3');r=b/'release'
for d in ['final_text','final_mapping','other_layers']:(r/d).mkdir(parents=True,exist_ok=True)
def put(p,s):
 with p.open('x') as f:f.write(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
allbody=['# HAB06 全45页正文候选（非全文核定）','汉文账正文另存；现代前附、馆藏题记、页码、图背与装帧层见review/映射，044西文题记另见other_layers。L/R沿旧稿原图半边，C/M/S沿旧稿定位；方括号、位置标签为编者层。保留未识音串、古拼写、圈号及乂交叉符号。']
findings=['# HAB06 全45页实际原图复核与限制','014 M13金额三→二有原像素二横字形依据；026侧注新增部分候选，尾串仍未识；044西文纸签转正可读91.2.Ms.Ext.，不展开缩写。其余密账、微注、重墨及淡损字大量保留疑读。实际看图覆盖不等于逐字核定。']
cover=[]
for n in range(1,46):
 m=json.loads((b/'review'/f'pdf_{n:03}_mapping.json').read_text());body=[];other=[]
 assert m['visually_reviewed'] and sha(Path(m['source']))==m['source_sha256'] and sha(Path(m['image']))==m['image_sha256']
 assert Path(m['source']).read_text().splitlines()==[x['source_text'] for x in m['source_lines']]
 for x in m['source_lines']:
  s=x['source_text'];take=5<=n<=41 and (bool(re.match(r'^[LRMCS]\d',s)) or s.startswith(('L下缘小字','右面框外下段')))
  x.update(body_line=None,new_text=None,disposition='editorial_or_other_layer')
  for old,new in m['changes']:s=s.replace(old,new)
  if take:
   body.append(s);x.update(body_line=len(body),new_text=s,disposition='manuscript_candidate_with_editorial_locator')
  elif n==44 and s.startswith(('Extravag.','下另小记','〔91.2.')):
   other.append(s);x.update(other_line=len(other),new_text=s,disposition='western_shelfmark_layer')
 p=r/'final_text'/f'pdf_{n:03}.md';put(p,'\n'.join(body)+'\n')
 m.update(body=str(p),body_sha256=sha(p),full_text_verified=False)
 if other:
  q=r/'other_layers'/f'pdf_{n:03}_western.md';put(q,'\n'.join(other)+'\n');m.update(other_layer=str(q),other_sha256=sha(q))
 put(r/'final_mapping'/f'pdf_{n:03}_mapping.json',json.dumps(m,ensure_ascii=False,indent=2))
 allbody+=['',f'## PDF {n:03}','\n'.join(body) if body else '〔编者：本页无新增可确认汉文正文；其他层见逐页review及映射。〕']
 findings+=['',f'## PDF {n:03}',m['finding']]
 cover.append(dict(pdf_page=n,visually_reviewed=True,full_text_verified=False,source_lines=len(m['source_lines']),body_lines=len(body),source_sha256=m['source_sha256'],image_sha256=m['image_sha256'],body_sha256=m['body_sha256'],changes=m['changes']))
put(r/'HAB06_all45_body_final_v3.md','\n'.join(allbody)+'\n')
put(r/'doubts_and_findings_all45_v3.md','\n'.join(findings)+'\n')
put(r/'coverage_all45_method_transfer_v3.json',json.dumps(cover,ensure_ascii=False,indent=2))
put(r/'integrity_check_v3.json',json.dumps(dict(pages=45,all_sources_and_images_unchanged=True,source_physical_lines=sum(x['source_lines'] for x in cover),all_final_bodies_hashed=True,full_text_verified=False),indent=2))
print(r, sum(x['source_lines'] for x in cover),sum(x['body_lines'] for x in cover))
