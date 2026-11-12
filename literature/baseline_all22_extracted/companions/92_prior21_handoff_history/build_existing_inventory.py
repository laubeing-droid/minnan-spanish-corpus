from pathlib import Path
import json,hashlib,shutil,datetime
B=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation');S=Path('/workspace/shared/minnan_transcription');O=B/'handoff_21sources_20261016_v1';R=B/'blind_calibration_20261016_v1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(name,t):(O/name).open('x').write(t)
def paths(xs):return [str(x) for x in xs]
srcs=json.loads((R/'all22_method_migration_inventory_v1.json').read_text())['sources'];hab=json.loads((B/'hab_all14_method_transfer_summary_v3/coverage_HAB_all14_461pages_v3.json').read_text())
entries=[]
configs={
'UB_Ms1027':('grammar','Arte_Grammar_all122_body_clean_v3.md',['coverage_all122_method_transfer_v3.json'],['source_line_mapping_all122_v3.json','final_body_line_mapping_v3.json'],['doubts_and_findings_all122_v3.md','README_quality_and_findings_v3.md'],'复合上标、缩写、细字、字母调号边界仍疑；037/038已补实看。','旧首稿/二校保留；映射是两级，应先源行后净正文行。'),
'MSS6040':('bne_mss6040','Mingxin_all315_body_final_v3.md',['coverage_all315_method_transfer_v3.json'],['source_line_mapping_all315_final_v3.json'],['doubts_and_findings_all315_v3.md','FINAL_DELIVERY_v3.md'],'淡西语、缩记、人名、裁边仍未定；195 malicia候选撤回。','630首稿/v2文件保持；以最终正文为准。'),
'R33396':('bne_r33396','Shilu_all164_body_final_v3.md',['coverage_all164_method_transfer_v3.json'],['source_line_mapping_all164_final_v3.json'],['doubts_and_findings_all164_v3.md','FINAL_DELIVERY_v3.md'],'009草写西文、淡汉字长串、图表仍疑；113電撤回采用暴雹。','328首稿/v2保留；083–164 adopted映射优先。'),
'Chinois9276':('paris_chinois9276','Paris_Chinois9276_all178_method_transfer_v3.md',['coverage_all178_method_transfer_v3.json'],['review'],['README_quality_and_findings_v3.md','report_001_089_findings_v3.md','review/pdf_120_addendum_v3a.md'],'g/q、n/u/m、i点与调号、边注仍疑；120两条旧错指控撤回。','旧visual_v1/旧二校保留；review提供旧读对应，不声称统一全物理行映射。'),
'Sin282-A':('onb_sin282_a','ONB_Sin282A_all580_body_final_v3.md',['coverage_all580_method_transfer_v3.json'],['source_line_mapping_all580_final_v3.json'],['doubts_and_findings_all580_v3.md','FINAL_DELIVERY_v3.md'],'古字、跨栏和淡笔仍疑；不同日期/章次不静默调和；279组修改/候选非279确定错。','1160首稿/v2文件保持。'),
'AUST_':('aust_tomo211_fragments','AUST_all10_partial_body_v3.md',['coverage_all10_v3.json'],['source_line_mapping_all10_v3.json'],['FINAL_DELIVERY_v3.md','review'],'10幅仅公开残页；完整正文识读0页；007/009较多部分识读，008/010仅候选。','旧MD保留；不能称完整AUST全书。')}
for src in srcs:
 name=src['source_file'];n=src['pdf_pages'];e={'source_file':name,'source_pdf':src['source_path'],'source_pdf_exists':Path(src['source_path']).exists(),'expected_pdf_pages':n,'full_text_verified':False}
 if 'Hispánico' in name:
  e.update(status='待接入：另一组继续1140页主稿；本清单不冻结或包装其动态正文',image_review_pages_in_this_completed_set=0,body_files=[],coverage_files=[],mapping_files=[],unresolved='待协调者交最终冻结、范围和疑难；已有局部不能冒充全1140完成',scripts=[]);pending=e;continue
 if 'Extrav_' in name:
  part=int(name.rsplit('_',1)[1].split('.')[0]);p=hab['parts'][part-1];d=Path(p['companion_directory']);root=d.parent if d.name=='release' else d
  cover=list(d.glob('coverage_all*.json'));maps=[d/'final_mapping'] if (d/'final_mapping').exists() else list(d.glob('source_line_mapping_all*.json'))
  reports=[root/'FINAL_DELIVERY_v3.md',d/'review',*d.glob('doubts*.md')];reports=[x for x in reports if x.exists()]
  scripts=list((B/'hab_all14_method_transfer_summary_v3/scripts').glob('*.py'));e.update(group='HAB14分册同书组；保持分册/PDF序，未静默重排',part=part,body_files=[p['body']],coverage_files=paths(cover),mapping_files=paths(maps),unresolved='草写音写、账目重墨、细注、截边仍未定；空白/透背/装帧也计图像覆盖。14册低分辨率限制未解决。',issue_files=paths(reports),legacy='旧逐页首稿与映射中source/old指向文件均保留；release优先于中间text',scripts=paths(scripts))
 elif 'Angelica' in name:
  d=B/'angelica_method_independent_v3';files=[d/f'pdf_{i:03}.md' for i in range(1,86)]+[d/f'pdf{i:03}.md' for i in range(86,170)]
  freeze=[]
  for p in sorted(d.glob('freeze*.json')):
   j=json.loads(p.read_text());rs=j if isinstance(j,list) else j.get('pages',[])
   for r in rs:
    path=Path(r.get('transcription',str(d/r.get('file',''))));freeze.append({'pdf_page':r['pdf_page'],'file':str(path),'hash_matches_freeze':path.exists() and sha(path)==r['sha256']})
  assert len(freeze)==169 and all(r['hash_matches_freeze'] for r in freeze)
  put('Angelica169_frozen_body_recheck.json',json.dumps(freeze,ensure_ascii=False,indent=2))
  e.update(group='DSH Angelica；与Paris平行本分别保留',body_files=paths(files),coverage_files=paths([d/'coverage_001_085_verified.json',d/'reader_pdf086_169_completion.json']),mapping_files=paths([R/'DSH_Angelica_all169_images_only_v2.json',*sorted(d.glob('freeze*.json'))]),unresolved='字母/调号细笔未定；9/21/52旧见、33教学暴露；165–168书信题记、169封底。169冻结页已复核hash，尚无此方法版合并MD。独立新读不生成旧稿逐行替换映射。',issue_files=paths([d/'reader_exposure_and_method.md',d/'work_record_001_085.md',d/'reader_pdf086_169_learning.json',R/'DSH_newmethod_reference_and_crossdictionary_stage_v1.md',R/'DSH_newmethod_086169_reference_addendum_v1.md']),legacy=f'旧稿保留于{B}/angelica_ms60及{S}/angelica_ms60；不把旧二校覆盖独立冻结新稿',scripts=paths(list((B/'angelica_ms60').glob('audit*.py'))),script_scope='所列为旧稿审计脚本；此独立169稿保存脚本未定位到，不能冒称这些脚本生成了新稿。',packaging_gap='后续可另建合并MD；本次仅核现有成果，未合并、未改冻稿。')
 else:
  key=next(k for k in configs if k in name);folder,body,cov,mp,issues,unres,legacy=configs[key];d=B/folder/'method_transfer_v3';scripts=list(d.glob('*.py'))
  if key=='AUST_':scripts=[Path('/tmp/save_aust_v3.py')]
  e.update(group=src['book_group'],body_files=[str(d/body)],coverage_files=paths([d/x for x in cov]),mapping_files=paths([d/x for x in mp]),issue_files=paths([d/x for x in issues]),unresolved=unres,legacy=legacy,scripts=paths(scripts))
 e.update(status='已完成逐页方法新读/迁移复核，部分正文候选可交接',image_review_pages_in_this_completed_set=n)
 e['current_body_hashes']=[{'path':p,'exists':Path(p).exists(),'sha256':sha(p) if Path(p).is_file() else None} for p in e['body_files']]
 refs=e['coverage_files']+e['mapping_files']+e['issue_files']+e['scripts'];e['missing_referenced_paths']=[p for p in refs if not Path(p).exists()]
 assert not e['missing_referenced_paths'],e
 entries.append(e)
assert len(entries)==21 and sum(e['expected_pdf_pages'] for e in entries)==1999
u=shutil.disk_usage(O);data={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed_source_count':21,'completed_image_review_pages':1999,'pending_source':pending,'full_text_verified':False,'body_hash_scope':'当前主正文文件重算hash；Angelica169另与冻结值逐一比对；其他书既有验收另链接，本次未重复逐页看图或重算大图/PDFhash。','disk_free_bytes_after':u.free,'entries':entries}
put('completed21_sources_handoff_inventory_v1.json',json.dumps(data,ensure_ascii=False,indent=2))
md=['# 21份来源交接清单\n\n21份来源、1999幅PDF页已完成各自方法新读或迁移复核；包含封面、现代说明、空页及透背，不能称1999页正文读清。DHS1140仍待接入。仅轻量核验及清单，不复制图片/PDF，不建ZIP。\n\n本清单中的路径是当前本地路径；交接环境迁移时须保持相对关系或做显式路径重定位。\n']
for i,e in enumerate(entries,1):
 md.append(f"## {i:02}. {e['source_file']}\n\n- 原PDF：{e['source_pdf']}\n- 视觉覆盖：{e['expected_pdf_pages']}/{e['expected_pdf_pages']}，全文核定否。\n")
 if 'Angelica' in e['source_file']:md.append(f"- 正文169个冻结MD：{B}/angelica_method_independent_v3/pdf_001.md–pdf_085.md；pdf086.md–pdf169.md。尚无方法版合并MD。\n")
 else:md.append('- 正文：'+e['body_files'][0]+'\n')
 for label,key in [('覆盖与原页定位','coverage_files'),('映射/冻稿定位','mapping_files'),('疑难与工作记录','issue_files')]:
  xs=e[key];md.append('- '+label+'：'+ ('；'.join(xs[:4])+('；其余逐项见JSON' if len(xs)>4 else ''))+'\n')
 md.append('- 未决：'+e['unresolved']+'\n- 旧稿：'+e['legacy']+'\n- 实际代码：'+('；'.join(e['scripts'][:3]) or '未定位到独立脚本')+('；更多见JSON' if len(e['scripts'])>3 else '')+'\n')
 if e.get('script_scope'):md.append('- 脚本范围：'+e['script_scope']+'\n')
md.append('\n## 待接入\n\n'+pending['source_file']+'，1140页，由另一组继续；此处不宣布完成、不改动态正文。\n')
put('completed21_sources_handoff_inventory_v1.md','\n'.join(md))
print('21 sources,1999 pages; body files checked',sum(len(e['body_files']) for e in entries),'free GB',round(u.free/1e9,2))
