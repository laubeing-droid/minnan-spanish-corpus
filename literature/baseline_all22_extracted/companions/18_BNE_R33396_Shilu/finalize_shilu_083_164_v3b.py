from pathlib import Path
import json,hashlib,sys
from save_shilu_transfer_v3b import save
O=Path(__file__).resolve().parent;B=O.parent
save(163,'独立查看整页素纸及四边，左折装订与右边纸层可见；本面无页码、正文、印章。不能因与162相似而省略本页，影像水印不算原件文字。')
save(164,'最后页标签分三枚：3／34104与1／66848都有划销线；黄签377-2，末2折线可见。左上R后短笔仍不定，33396逐位对照。标签属于实物附加记号，与底部现代水印区分。')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
allowed={'頁題、號','正文','手写页码','逐行转写','正面试笔，按位置','主文逐行转写','左缘题署','题头','印记'}
manifest=[]
for n in range(83,165):
 p=B/'collation_v1'/f'pdf_{n:03}_visual_v2.md';lines=p.read_text().splitlines();initial=json.loads((O/'review'/f'pdf_{n:03}_mapping.json').read_text())
 assert initial['old_sha256']==sha(p) and initial['image_sha256']==sha(B/f'pdf_{n:03}.png')
 assert [x['old_text'] for x in initial['lines']]==lines
 changes=[] if n==113 else initial['changes'];keep=False;out=[];mapping=[];comp=[]
 for i,l in enumerate(lines,1):
  if l.startswith('## '):
   h=l[3:];keep=h in allowed
   if n in [83,86,89]:keep=h not in ['頁面與圖形','難辨處與版面','影像水印','第二視覺校記','外校限度']
   if n in [159,161,164]:keep=h=='可見文字與記錄'
   if n==151:keep=h=='可見文字與記錄'
  k=keep
  if n==151 and ('鏡向' in l):k=False
  if l.startswith('原图自上往下排列'):k=False
  new=l
  if k:
   for a,b in changes:new=new.replace(a,b)
   out.append(new)
  else:comp.append(l)
  mapping.append({'old_line':i,'old_text':l,'disposition':'body' if k else 'companion','new_text':new if k else None})
 body=O/'text'/f'pdf_{n:03}_adopted.md';mp=O/'review'/f'pdf_{n:03}_adopted_mapping.json';cp=O/'review'/f'pdf_{n:03}_adopted_companion.md'
 with body.open('x') as f:f.write(f'# BNE R33396 · PDF {n:03}\n\n'+'\n'.join(out).strip()+'\n')
 with cp.open('x') as f:f.write(f'# PDF{n:03} 正文分层附记\n\n逐页新复核意见见 pdf_{n:03}.md。本文件保全不属于转写正文的全部旧物理行。113采用暴雹，撤回電候选。\n\n'+'\n'.join(comp)+'\n')
 result={**initial,'changes':changes,'lines':mapping,'canonical_text':str(body),'companion':str(cp),'review':str(O/'review'/f'pdf_{n:03}.md'),'text_sha256':sha(body)}
 with mp.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 manifest.append({'page':n,'text':str(body),'mapping':str(mp),'review':result['review'],'companion':str(cp),'old_lines':len(lines),'body_lines':sum(x['disposition']=='body' for x in mapping),'full_text_verified':False,'changes':changes})
with (O/'shilu_083_164_manifest_v3b.json').open('x') as f:json.dump({'pages':manifest,'page_count':len(manifest),'all_source_lines_mapped':True,'all_source_and_image_hashes_verified':True,'canonical_suffix':'_adopted','full_text_verified':False},f,ensure_ascii=False,indent=2)
print('VERIFIED',len(manifest),'pages',sum(x['old_lines'] for x in manifest),'physical source lines')
