from pathlib import Path
import json,hashlib,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s):
 with p.open('x') as f:f.write(s)
def save(part,notes,changes={}):
 b=Path('/workspace/shared/minnan_transcription')/f'hab_91_2_extrav_{part:02}'
 o=b/'method_transfer_v3';o.mkdir(exist_ok=True)
 for d in ['text','review']:(o/d).mkdir(exist_ok=True)
 cov=[];maps=[];merged=[f'# HAB 91.2 Extrav {part} 方法迁移复核\n\n〔保留疑读，未全文核定。〕\n']
 for n,note in notes.items():
  candidates=[b/d/f'pdf_{n:03}.md' for d in ['visual_v2','visual_v1','page_records','blind_v1']]
  src=next((p for p in candidates if p.exists()),None)
  if src is None:src=b/'page_records'/f'pdf_{n:03}_record.md'
  if not src.exists():raise RuntimeError(candidates)
  image=Path('/workspace/shared/minnan_reference_catalog')/f'hab{part:02}_official_max'/f'{n-2:05}.jpg' if n>2 else b/'blind_v1'/f'pdf-{n:02}.png'
  if not image.exists():image=b/'page_records'/f'pdf_{n:03}_record_render_100dpi.png'
  lines=src.read_text().splitlines();out=[f'# HAB {part:02} · PDF {n:03}'];mapping=[];active=False
  if n<=2:out.append('〔现代馆方使用说明页；无古稿正文。〕')
  for i,line in enumerate(lines,1):
   if line.startswith('## '):active=not any(k in line for k in ['来源','方法','摄影','限制','不确定','标签注意','图像与疑读'])
   if line.startswith(('右上页码：','封装外侧','封装内侧','封装另一内侧')):active=True
   target=None;new=line
   if active and n>2 and not line.startswith(('摄影','Herzog','来源：','源图：')):
    for a,z in changes.get(n,[]):new=new.replace(a,z)
    out.append(new);target=len(out)
   mapping.append({'source_line':i,'source_text':line,'body_line':target,'new_text':new if target else None,'disposition':'body' if target else 'editorial_or_modern_in_source'})
  text='\n'.join(out)+'\n';tp=o/'text'/f'pdf_{n:03}_v3.md';put(tp,text);merged.append(text)
  record={'pdf_page':n,'source':str(src),'source_sha256':sha(src),'image':str(image),'image_sha256':sha(image) if image.exists() else None,'body':str(tp),'body_sha256':sha(tp),'visually_reviewed':True,'full_text_verified':False,'finding':note,'changes':changes.get(n,[])}
  cov.append(record);maps.append({**record,'source_lines':mapping})
  put(o/'review'/f'pdf_{n:03}_v3.md',f'# PDF {n:03} 逐页实核\n\n{note}\n\n旧读→新候选：{changes.get(n,[])}\n\n本次读取原图及旧稿，属于非盲二校。正文古字、数序及疑读保留。图与旧稿路径、哈希和全源行映射见本目录合并JSON。哈希不代表内容准确。\n')
 put(o/f'HAB{part:02}_all{len(notes)}_body_v3.md','\n'.join(merged))
 put(o/f'coverage_all{len(notes)}_v3.json',json.dumps(cov,ensure_ascii=False,indent=2))
 put(o/f'source_line_mapping_all{len(notes)}_v3.json',json.dumps(maps,ensure_ascii=False,indent=2))
 assert all(sha(Path(c['source']))==c['source_sha256'] for c in cov)
 put(o/'FINAL_DELIVERY_v3.md',f'# HAB {part:02} 方法迁移复核\n\n{len(notes)}/{len(notes)}页实际查图并对照旧稿，逐页发现见review。所有源稿保持不变。全文核定标记仍为false。\n\n正文、覆盖及全源物理行映射均在本目录；摄影标识、现代使用说明及方法说明独立在原稿和映射，不混古正文。\n\n{len(changes)}页含新的候选调整，非准确率或确定错误数。草写汉字音写、账目字、圈销与边注不套DHS罗马字调号规则；不能按数值加总或现代词义补字。\n')
 print(part,len(notes),sum(len(m['source_lines']) for m in maps))
