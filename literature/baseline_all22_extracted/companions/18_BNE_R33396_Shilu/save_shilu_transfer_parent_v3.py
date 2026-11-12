from pathlib import Path
import hashlib,json,re
O=Path(__file__).resolve().parent;B=O.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,note,changes=()):
 old=B/'collation_v1'/f'pdf_{n:03}_visual_v2.md';im=B/f'pdf_{n:03}.png';lines=old.read_text().splitlines();out=[];mapping=[];comment=False
 for i,l in enumerate(lines,1):
  if re.match(r'^## .*?(校记|校記|疑读|疑讀|限度)',l):comment=True
  keep=not comment and not (l.startswith(('第二獨立','- 方法：','- 状态：','来源：')) or l.startswith('# '))
  new=l
  if keep:
   for a,b in changes:
    if a in new:new=new.replace(a,b,1)
   out.append(new)
  mapping.append({'old_line':i,'old_text':l,'disposition':'body' if keep else 'companion','new_text':new if keep else None})
 with(O/'text'/f'pdf_{n:03}.md').open('x') as f:f.write(f'# BNE R33396 · PDF {n:03}\n\n原图：{im}\n\n'+'\n'.join(out).strip()+'\n')
 with(O/'review'/f'pdf_{n:03}.md').open('x') as f:
  f.write(f'# PDF {n:03} 方法迁移原图复核\n\n{note}\n\n性质：可读旧稿的非盲二校；已直接查看本页原图，full_text_verified=false。\n')
  for a,b in changes:f.write(f'\n旧读：{a}\n新读/候选：{b}\n')
  f.write('\n## 旧稿说明与校记保全\n'+ '\n'.join(x['old_text'] for x in mapping if x['disposition']=='companion')+'\n')
 with(O/'review'/f'pdf_{n:03}_mapping.json').open('x') as f:json.dump({'page':n,'image':str(im),'image_sha256':sha(im),'old':str(old),'old_sha256':sha(old),'visual_review':True,'changes':list(changes),'lines':mapping},f,ensure_ascii=False,indent=2)
