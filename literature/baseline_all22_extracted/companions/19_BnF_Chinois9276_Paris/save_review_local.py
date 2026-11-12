from pathlib import Path
import re,json,hashlib
B=Path(__file__).resolve().parent.parent
O=B/'method_transfer_v3'
def save(n,note,changes=()):
 old=B/'visual_v1'/f'pdf_{n:03}.md';images=list((B/'images').glob(f'pdf_{n:03}*png'));im=next((p for p in images if '300dpi' in p.name),images[0]);s=old.read_text()
 s=re.sub(r'^# .*?\n',f'# 巴黎 Chinois9276 · PDF {n:03} 方法迁移二校\n',s,count=1)
 s=re.sub(r'^- (方法|状态)：.*\n','',s,flags=re.M)
 if '仅巴黎原页，不与罗马稿合并；未全文核定。' in s:s=f'# 巴黎 Chinois9276 · PDF {n:03} 方法迁移二校\n\n'+s.split('仅巴黎原页，不与罗马稿合并；未全文核定。',1)[1].strip()+'\n'
 for a,b in changes:
  assert a in s,(n,a);s=s.replace(a,b,1)
 with (O/'text'/old.name).open('x') as f:f.write(s)
 r=f'# PDF {n:03} 原图实质复核\n\n原图：../../images/{im.name}\n旧稿：../../visual_v1/{old.name}\n状态：逐页直接看原图及旧稿，方法迁移二校，非盲测。\n\n{note}\n\n'
 r+='\n'.join('旧读 '+a+' → 新读/候选 '+b for a,b in changes) if changes else '旧读→新读：保留；上列实质检查不等于全部疑读已解决。'
 with (O/'review'/old.name).open('x') as f:f.write(r+'\n')
