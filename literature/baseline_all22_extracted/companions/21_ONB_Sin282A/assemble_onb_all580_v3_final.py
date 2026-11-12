from pathlib import Path
import json,hashlib,re,datetime
O=Path(__file__).resolve().parent;B=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
 with (O/name).open('x',encoding='utf8') as f:
  f.write(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2))
missing=[n for n in range(1,581) if not all((O/k/f'pdf_{n:03}{suffix}').exists() for k,suffix in [('text','.md'),('review','.md'),('review','_mapping.json')])]
assert not missing,missing
baseline=json.loads((O/'prior_text_hash_baseline_v3.json').read_text())
assert len(baseline['files'])==1160
assert all(sha(Path(x['path']))==x['sha256'] for x in baseline['files'])
body=['# ONB Sin282-A · 全580图序正文 v3',''];maps=[];coverage=[];relocated=[];findings=[];errors=[];changes_count=0;changed_pages=0;bodylinecount=0
for n in range(1,581):
 mp=O/'review'/f'pdf_{n:03}_mapping.json';d=json.loads(mp.read_text());old=Path(d['old']);oldlines=old.read_text().splitlines();lines=d['lines']
 assert d['page']==n and d['visual_review'] is True
 assert sha(old)==d['old_sha256'] and sha(Path(d['image']))==d['image_sha256']
 assert len(lines)==len(oldlines) and [x['old_line'] for x in lines]==list(range(1,len(oldlines)+1))
 assert all(x['old_text']==l for x,l in zip(lines,oldlines))
 ot='\n'.join(x['old_text'] for x in lines if x['disposition']=='body');nt='\n'.join(x['new_text'] or '' for x in lines)
 for a,b in d['changes']:assert a in ot and b in nt,(n,a,b)
 changes_count+=len(d['changes']);changed_pages+=bool(d['changes'])
 body.extend([f'## PDF {n:03}',f'原图：{d["image"]}',''])
 outmap=[];nontext=n in [3,5,15,141,142,303,575,576,580]
 for x in lines:
  l=x['new_text'];reason=None;clean=l
  if x['disposition']=='companion':reason='原v2说明/校记；保存在逐页review'
  elif not l or not l.strip():reason='空行'
  elif nontext:reason='无正面可录文字页；图面说明移配套'
  elif l.startswith(('#','```','來源：','来源：','原图：','- 原PDF：','- 原页图：','- 狀態：','- 状态：','- 记号：')):reason='转写层说明/格式'
  elif re.match(r'^(右起 |右起向左|本页右起|下列 C01)',l):reason='读序说明'
  else:
   # Retain readings and uncertainty, move previous-reading editorial history out of body.
   clean=re.sub(r'；旧读[^〕]*','',l)
   clean=re.sub(r'；旧漏','',clean)
   if clean!=l:relocated.append({'page':n,'old_line':x['old_line'],'before':l,'after':clean,'reason':'旧读历史移配套，候选及疑号保留'})
   body.append(clean);bodylinecount+=1
  rec={**x,'final_body_line':len(body) if reason is None else None,'final_text':clean if reason is None else None,'final_disposition':reason or '正文/页定位'}
  outmap.append(rec)
  if reason and reason not in ['空行','原v2说明/校记；保存在逐页review']:relocated.append({'page':n,'old_line':x['old_line'],'text':l,'reason':reason})
 if nontext:body.append('〔本面未见可可靠转写的正面文字；图面说明见配套逐页复核。〕')
 body.append('')
 maps.append({'page':n,'old':d['old'],'old_sha256':d['old_sha256'],'lines':outmap})
 coverage.append({'page':n,'image':d['image'],'image_sha256':d['image_sha256'],'visual_review':True,'review_mode':'可读旧稿的原图方法迁移二校，非盲测','full_text_verified':False,'source_line_mapping_valid':True,'old_line_count':len(lines),'change_records':len(d['changes']),'text':str(O/'text'/f'pdf_{n:03}.md'),'review':str(O/'review'/f'pdf_{n:03}.md'),'mapping':str(mp),'text_sha256':sha(O/'text'/f'pdf_{n:03}.md'),'review_sha256':sha(O/'review'/f'pdf_{n:03}.md'),'mapping_sha256':sha(mp)})
 findings.append(f'## PDF {n:03}\n\n'+(O/'review'/f'pdf_{n:03}.md').read_text().split('## 旧稿说明与校记保全')[0].replace(f'# PDF {n:03} 方法迁移原图复核','').strip())
write('ONB_Sin282A_all580_body_clean_v3.md','\n'.join(body)+'\n')
write('source_line_mapping_all580_v3.json',maps)
write('editorial_material_relocated_v3.json',relocated)
write('coverage_all580_method_transfer_v3.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'visual_reviewed_pages':580,'source_line_mapping_validated_pages':580,'full_text_verified':False,'change_record_count':changes_count,'pages_with_change_records':changed_pages,'pages':coverage})
write('doubts_and_findings_all580_v3.md','# ONB 全580页逐页疑难与方法迁移记录\n\n改读记录包含明确改错、增加候选、保留旧疑；数量不能换算准确率。\n\n'+'\n\n'.join(findings))
write('README_quality_and_findings_v3.md',f'''# ONB Sin282-A 方法迁移 v3

## 可用交付
- `ONB_Sin282A_all580_body_clean_v3.md`：全580图序合并正文；按原PDF次序，重复叶不去重，现代封签/许可页注明身份，不混当汉字古正文。
- `coverage_all580_method_transfer_v3.json`：580页实际原图复核、图像/正文/复核/映射hash。
- `source_line_mapping_all580_v3.json`：旧v2每一物理行到正文或配套的去向；正文行号是合并文件物理行。
- `doubts_and_findings_all580_v3.md`：逐页改读、依据及未决处。
- `editorial_material_relocated_v3.json`：正文外移的格式/说明/旧读历史，可追溯原行。
- `text/`、`review/`：逐页工作转写和原图复核记录；对读历史在review保留。

## 覆盖与质量必须分开
580/580原图已直接查看；580/580源文本行映射及图像hash已验证。所有页 `full_text_verified=false`。全书存在缺边、模糊、透背及未能读清的汉字音译，不能称无误全文。
本轮{changed_pages}页有{changes_count}组改读/候选记录；一组可能涉及多字或多处，候选不等于确定错误，不能作为准确率或改进率。
旧首稿580件+旧v2共1160件与本轮开始前hash一致；未覆盖。新稿先读旧v2再看原图的二校，可使用研究背景，不称盲测。

## 实际方法收益与边界
1. 可迁移的是分清字形证据、语义支持、编辑层；逐栏短行/旁字/截边与跨页词串要分别保留。汉字宗教连续文本没有辞典逐词西汉对译，DHS/DSH的tz连写与七类调号不适用于本书汉字正文，不为套方法而造音值层。
2. 发现实质旧读错形及拆字：PDF150章次三→二；215不是真→亦是真；225亦人人皆敢→家公公喝；258善的下口被拆成另一个口；259發晉→效昔。详见各页笔形依据，不能从一句通顺倒推全部成立。
3. 多处硅/碓、突/实、兀/瓦音译字仍标候选，逐幅检查后才记，不以相同人名批量归一。小字如213/215汝旁身与原行分层保留。
4. 图像中重复叶及不同裁切均保留原序。正文短栏、封装/空白、黑块或重文钩不当成缺句自行填写。
5. PDF9原日期22与外证12、574跡/所及章次冲突保持可追溯；本轮没有重新逐条核验全部外部来源，不宣称外校全文核定。

## 失败与待核
低对比、纸面磨损与裁边在本轮仍无法恢复；如45/48/78/87/96/102/112/153/155/162/165/167/178/194/205/207/210/212/223/242/252等保留缺字或疑读，后半见逐页记录。局部候选需要更清晰原件或人工复核。本轮为现有300dpi原图的视觉复核，工具预览可能缩小；没有声称每字都已按原像素放大检查。
研究/规约、验收及疑难记录属于配套；最终AgentSkill尚未封装。
''')
files=['ONB_Sin282A_all580_body_clean_v3.md','source_line_mapping_all580_v3.json','editorial_material_relocated_v3.json','coverage_all580_method_transfer_v3.json','doubts_and_findings_all580_v3.md','README_quality_and_findings_v3.md']
write('final_integrity_acceptance_v3.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':580,'prior_files_unchanged':1160,'baseline':str(O/'prior_text_hash_baseline_v3.json'),'source_mapping_all_lines_valid':True,'actual_visual_review_reported_pages':580,'full_text_verified':False,'body_lines_preserved':bodylinecount,'change_records':changes_count,'changed_pages':changed_pages,'files':[{'path':str(O/f),'sha256':sha(O/f)} for f in files]})
print(json.dumps({'pages':580,'changed_pages':changed_pages,'change_records':changes_count,'body_sha256':sha(O/files[0])}))
