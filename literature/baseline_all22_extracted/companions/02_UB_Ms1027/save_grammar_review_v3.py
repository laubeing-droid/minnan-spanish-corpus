from pathlib import Path
import json,re,hashlib
O=Path(__file__).resolve().parent;B=O.parent
M=json.loads((B/'grammar_stage_coverage_001_122_v3.json').read_text())['pages']
def save(n,note,changes=()):
 d=M[n-1]['stage_files'];old=Path(d['collated_v3']['path'] if d['collated_v3']['exists'] else d['visual_v2']['path']);im=Path(d['image']['path'])
 s=old.read_text().split('# 随页校记')[0].strip()
 # Preserve only original transcription and local uncertainty; methodology remains outside body.
 lines=s.splitlines(); start=next((i for i,l in enumerate(lines) if l.startswith('## ') or re.match(r'^(原页码|L\d\d |R\d\d |A\d\d )',l)),2)
 s='\n'.join(lines[start:]).strip().rstrip('-').strip()
 for a,b in changes:
  assert a in s,(n,a);s=s.replace(a,b,1)
 with(O/'text'/f'pdf_{n:03}.md').open('x')as f:f.write(f'# Arte/Grammar · PDF {n:03} 方法迁移二校正文\n\n原图：{im}\n\n'+s+'\n')
 with(O/'review'/f'pdf_{n:03}.md').open('x')as f:
  f.write(f'# PDF {n:03} 方法迁移实质原图复核\n\n原图：{im}\n旧稿：{old}\n性质：逐页直接看图对照旧稿，非盲测；full_text_verified=false。\n\n'+note+'\n\n')
  f.write('\n'.join('旧读 '+a+' → 新读/候选 '+b for a,b in changes) if changes else '旧读→新读：本页保留；上述检查不代表所有字形已定。')
