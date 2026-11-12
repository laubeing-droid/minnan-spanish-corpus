from pathlib import Path
import json,re,hashlib,datetime
O=Path(__file__).resolve().parent; G=O.parent
M=json.loads((G/'grammar_stage_coverage_001_122_v3.json').read_text())['pages']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,s):
 with p.open('x') as f:f.write(s)
merged=['# Arte de la lengua chio chiu · 122 PDF页方法迁移复核正文','', '〔保留原拼写、原符号及疑读；PDF编号是影像定位。校记索引见 accompanying_historical_notes_v3.md。〕','']
notes=['# 历史校记与正文分离记录','', '编号与合并正文对应。候选为未定读法；这里保存历次说明，不代表本轮全部确认。','']
coverage=[]; mapping=[]; note_i=0
skipstarts=('仅第二','仅应用','本稿只应用','来源：','源 grammar','范围：','记法：','已独立核看','本轮','原文中所有','状态：','〔本页无正文行ID','〔本面无正文ID','所有表格区域','未据邻页','未读参考','首稿','---')
for n in range(1,123):
 d=M[n-1]['stage_files']; old=Path(d['collated_v3']['path'] if d['collated_v3']['exists'] else d['visual_v2']['path']); src=O/'text'/f'pdf_{n:03}.md'; review=O/'review'/f'pdf_{n:03}.md'; im=Path(d['image']['path']); raw=src.read_text().splitlines()
 merged.extend([f'## PDF {n:03}', '',f'原图：{im}','']); startline=len(merged)+1
 skip_current=False; pageout=[]; permap=[]
 for k,l in enumerate(raw,1):
  out=l; reason='body_retained'
  if l.startswith('## 当前整合'):skip_current=True
  if l.startswith('## 原v2') or l.startswith('## 原visual'):skip_current=False
  if skip_current or l.startswith(('# Arte/Grammar','# 《','## 原v2','## 原visual','## 整合正文','原图：')) or l.startswith(skipstarts):out='';reason='workflow_or_duplicate_metadata_to_mapping'
  if l.startswith('## 图像与疑读记录'):out='';reason='notes_section_to_mapping'
  # Retain page numbers, but remove historical method declarations after the first sentence.
  if re.match(r'^(原页码|原叶码|叶码)',out):out=re.split(r'。',out,1)[0]+'。'
  if l.startswith('## 不确定') or l.startswith('## 原图'):out='';reason='notes_heading_to_mapping'
  # Nested bracket-aware relocation of historical commentary only.
  if out:
   cursor=0; pieces=[]
   while cursor<len(out):
    b=out.find('〔',cursor)
    if b<0:pieces.append(out[cursor:]);break
    pieces.append(out[cursor:b]);j=b+1;depth=1
    while j<len(out) and depth:
     if out[j]=='〔':depth+=1
     elif out[j]=='〕':depth-=1
     j+=1
    block=out[b:j]
    if re.match(r'〔(?:第二视觉复核校|二复校|二复疑读|校\d|v3裁决|本轮整合候选)',block):
     note_i+=1;key=f'P{n:03}-N{note_i:04}';notes.extend([f'## {key}',f'来源：{src.name}，行{k}',block,'']);pieces.append(f'〔校记 {key}；相关旧读/候选未必定〕');reason='body_with_commentary_relocated'
    else:pieces.append(block)
    cursor=j
   out=''.join(pieces)
  # Drop pure process sentences, retaining full source in mapping and historical per-page layer.
  if out and not re.match(r'^[A-Z]\d|^\s+|^#|^〔',out) and any(w in out for w in ['未查参考','未读答案','未联网','未读参考答案','首稿封存','本轮实际','详见同页']):
   if any(w in out for w in ['页码','叶码','右上','页顶']):out=out.split('。')[0]+'。'
   else:out='';reason='process_sentence_to_mapping'
  target=None
  if out:
   target=len(merged)+len(pageout)+1;pageout.append(out)
  elif not l.strip() and pageout and pageout[-1]!='':pageout.append('')
  permap.append({'source_line':k,'source_text':l,'disposition':reason if out else 'relocated_to_source_mapping','merged_line':target,'merged_text':out or None})
 # Supplement genuinely missing folio metadata reviewed in this round.
 folios={27:'2',29:'3',31:'4',33:'5',35:'6',39:'8',41:'9',43:'10',45:'11',47:'12',49:'〔疑读13/19〕',51:'14',53:'〔疑读15/5；本轮见左淡竖〕'}
 if n in folios and not any(('页码' in x or '叶码' in x or '右上' in x) for x in pageout):pageout.insert(0,'〔右上叶码：'+folios[n]+'〕')
 # Mapping line positions recomputed below; exact text matching retained for supplements.
 merged+=pageout+['']; endline=len(merged)
 for x in permap:
  if x['merged_text']:
   matches=[i+1 for i in range(startline-1,endline) if merged[i]==x['merged_text']]
   x['merged_line_candidates']=matches;x.pop('merged_line',None)
 mapping.append({'page':n,'source':str(src),'sha256':sha(src),'lines':permap,'prior_source':str(old),'prior_source_sha256':sha(old),'prior_source_lines':[{'line':i,'text':t} for i,t in enumerate(old.read_text().splitlines(),1)]})
 coverage.append({'page':n,'original_image_viewed':True,'full_text_verified':False,'image':str(im),'image_sha256':sha(im),'prior_text':str(old),'prior_text_sha256':sha(old),'text':str(src),'text_sha256':sha(src),'review':str(review),'review_sha256':sha(review),'merged_line_range':[startline,endline],'nature':'nonblind_method_transfer_visual_review'})
write(O/'Arte_Grammar_all122_method_transfer_v3.md','\n'.join(merged)+'\n')
write(O/'accompanying_historical_notes_v3.md','\n'.join(notes)+'\n')
write(O/'source_line_mapping_all122_v3.json',json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
write(O/'coverage_all122_method_transfer_v3.json',json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'image_review_pages':122,'full_text_verified':False,'old_blocked_037_038_now_reviewed':True,'same_leaf_images':[25,122],'distinct_number_tables':[56,57],'pages':coverage},ensure_ascii=False,indent=2)+'\n')
print('pages',len(coverage),'relocated historical notes',note_i,'merged lines',len(merged))
