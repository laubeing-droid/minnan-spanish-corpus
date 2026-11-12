from pathlib import Path
import json,hashlib,re
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s):
 with p.open('x') as f:f.write(s)
def save(part,n,note,changes=[]):
 b=Path('/workspace/shared/minnan_transcription')/f'hab_91_2_extrav_{part:02}';o=b/'method_transfer_v3'
 for d in ['text','review']:(o/d).mkdir(parents=True,exist_ok=True)
 src=b/'visual_v1'/f'pdf_{n:03}.md'
 if not src.exists():src=b/'page_records'/f'pdf_{n:03}_record.md'
 if not src.exists():src=b/'page_records'/f'pdf_{n:03}.md'
 im=Path('/workspace/shared/minnan_reference_catalog')/f'hab{part:02}_official_max'/f'{n-2:05}.jpg'
 if n<=2:
  poss=[b/'page_records'/f'pdf_{n:03}_render.png',b/'pdf_renders'/f'pdf_{n:03}.png',b/'pdf_renders'/f'pdf-{n:02}.png']
  im=next((p for p in poss if p.exists()),None)
 assert src.exists() and im and im.exists(),(src,im)
 body=[];mapping=[];sec=''
 for i,l in enumerate(src.read_text().splitlines(),1):
  new=l;idx=None
  if l.startswith('## '):sec=l[3:]
  elif n>2 and i>5 and l.strip() and not l.startswith(('摄影','源图','直接高清')):
   editorial=sec in ['方向','痕迹','其他','圈记','图像与疑读说明','来源与方法','方法','来源']
   if not editorial:
    for a,z in changes:new=new.replace(a,z)
    if re.match(r'^(单叶|全叶|整叶|浅灰大片|灰淡|正文倒置|没有|未见|左黑|纸面)',new) and not ('「' in new or '：' in new):editorial=True
   if not editorial:body.append(new);idx=len(body)
  mapping.append({'source_line':i,'source_text':l,'body_line':idx,'new_text':new if idx else None,'disposition':'body_candidate_with_editorial_locator' if idx else 'editorial_legacy'})
 tp=o/'text'/f'pdf_{n:03}_v3.md';put(tp,'\n'.join(body)+'\n')
 m={'pdf_page':n,'source':str(src),'source_sha256':sha(src),'image':str(im),'image_sha256':sha(im),'body':str(tp),'body_sha256':sha(tp),'visually_reviewed':True,'full_text_verified':False,'finding':note,'changes':changes,'source_lines':mapping}
 put(o/'review'/f'pdf_{n:03}_mapping.json',json.dumps(m,ensure_ascii=False,indent=2))
 put(o/'review'/f'pdf_{n:03}_v3.md',f'# PDF {n:03} 原图非盲复核\n\n{note}\n\n旧读→新候选：{changes or "无足够证据改字；保留并非核定"}\n\n全文核定=false。完整旧物理行、原图与旧稿hash见同页mapping；hash仅为完整性校验。\n')
if __name__=='__main__':
 import sys
 for row in json.loads(Path(sys.argv[1]).read_text()):save(**row)
