from pathlib import Path
import re,json,hashlib
B=Path(__file__).resolve().parent.parent; O=B/'method_transfer_v3'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
notes=json.loads((O/'merge_candidate_notes_v3.json').read_text())
notes['168']='右列tJit：新增tzit候选；左列两处Toa新增Zoa候选，未见独立前置小t。'
rows=[];parts=['# 巴黎 BnF Chinois9276 · 全178页方法迁移二校正文 v3\n\n保留原拼写、断行和疑读。PDF页号为本地源文件序号。方括号与校读提示非原文。所有页均有实质原图复核记录；尚非逐字定本。详细校记与方法报告另存review目录。\n']
for n in range(1,179):
 old=B/'visual_v1'/f'pdf_{n:03}.md';t=O/'text'/old.name;r=O/'review'/old.name
 assert t.exists() and r.exists(),n
 im=next((B/'images').glob(f'pdf_{n:03}*300dpi.png'))
 s=t.read_text().split('## 本轮二校定位与疑读')[0]
 s=re.sub(r'^# .*?\n','',s,count=1)
 s=re.sub(r'^(状态：|源：|图：|原图：).*\n','',s,flags=re.M)
 s=re.sub(r'^- (源文件|方法|状态)：.*\n','',s,flags=re.M)
 s=s.replace('../images/','../images/')
 parts.append(f'\n\n---\n\n## PDF {n:03}\n\n原图：[第{n}页](../images/{im.name})\n\n'+s.strip()+'\n')
 if str(n) in notes:parts.append('\n〔二校疑读追加〕'+notes[str(n)]+'\n')
 rows.append({'pdf_page':n,'original_image':str(im.resolve()),'original_sha256':h(im),'prior_text':str(old.resolve()),'prior_sha256':h(old),'v3_page':str(t.resolve()),'v3_page_sha256':h(t),'review':str(r.resolve()),'review_sha256':h(r),'visual_review':True,'full_text_verified':False})
with(O/'Paris_Chinois9276_all178_method_transfer_v3.md').open('x')as f:f.write(''.join(parts))
with(O/'coverage_all178_method_transfer_v3.json').open('x')as f:json.dump({'book':'Paris BnF Chinois9276','pdf_pages':178,'visual_review_pages':178,'nature':'second review with prior text; not blind','full_text_verified':False,'important_addendum':'review/pdf_120_addendum_v3a.md overrides review120 items3,4; not old transcription errors','pages':rows},f,ensure_ascii=False,indent=2)
print('assembled178',h(O/'Paris_Chinois9276_all178_method_transfer_v3.md'))
