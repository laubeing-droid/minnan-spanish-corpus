from pathlib import Path
import json,hashlib,re
b=Path('/workspace/shared/minnan_transcription/hab_91_2_extrav_05/method_transfer_v3')
r=b/'release'
for d in ['final_text','final_mapping']:(r/d).mkdir(parents=True,exist_ok=True)
def put(p,s):
 with p.open('x') as f:f.write(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ranges={4:set(range(9,16))|{17,18,20,21,22},5:{9}|set(range(11,17))|set(range(18,23))|{24},6:set(range(9,20))|set(range(21,25))}
allbody=['# HAB05 全43页正文候选（非全文核定）','仅收汉文账目和017西文手写批记；页码、馆藏题记、摄影附属和图背另留逐页review及完整映射。行内方括号/位置标识属编者层。']
findings=['# 全43页实际复核发现与限制','实质字形改进：038 五十六尺→五十〔八?〕尺。原像素局部所见十下为分离两笔，保留候选。017未能最终核定首词。账目勾销、微字及交叉金额符号仍未读清。']
cover=[]
for n in range(1,44):
 m=json.loads((b/'review'/f'pdf_{n:03}_mapping.json').read_text());body=[];other=[]
 assert sha(Path(m['source']))==m['source_sha256'] and sha(Path(m['image']))==m['image_sha256']
 for x in m['source_lines']:
  s=x['source_text'];take=x['source_line'] in ranges.get(n,set())
  if n==17:take=s.startswith('〔首词疑读')
  if n==38:take=bool(re.match(r'^[LR]\d',s))
  x['body_line']=None;x['new_text']=None;x['disposition']='editorial_or_other_layer'
  if take:
   for old,new in m['changes']:s=s.replace(old,new)
   body.append(s);x.update(body_line=len(body),new_text=s,disposition='manuscript_candidate_with_editorial_locator')
  elif n in [40,41,42] and s.strip():other.append(s)
 p=r/'final_text'/f'pdf_{n:03}.md';put(p,'\n'.join(body)+'\n')
 m.update(body=str(p),body_sha256=sha(p),full_text_verified=False)
 put(r/'final_mapping'/f'pdf_{n:03}_mapping.json',json.dumps(m,ensure_ascii=False,indent=2))
 allbody+=['',f'## PDF {n:03}',('\n'.join(body) if body else '〔编者：本页无新增可确认的手稿正文；现代前附页/页码/封装题记/图背见review及映射。〕')]
 findings += ['',f'## PDF {n:03}',m['finding']]
 cover.append(dict(pdf_page=n,visually_reviewed=True,full_text_verified=False,source_lines=len(m['source_lines']),body_lines=len(body),source_sha256=m['source_sha256'],image_sha256=m['image_sha256'],body_sha256=m['body_sha256'],changes=m['changes']))
put(r/'HAB05_all43_body_final_v3.md','\n'.join(allbody)+'\n')
put(r/'doubts_and_findings_all43_v3.md','\n'.join(findings)+'\n')
put(r/'coverage_all43_method_transfer_v3.json',json.dumps(cover,ensure_ascii=False,indent=2))
put(r/'integrity_check_v3.json',json.dumps(dict(pages=43,all_sources_and_images_unchanged=True,source_physical_lines=sum(x['source_lines'] for x in cover),all_final_bodies_hashed=True,full_text_verified=False),indent=2))
print(r, sum(x['source_lines'] for x in cover))
