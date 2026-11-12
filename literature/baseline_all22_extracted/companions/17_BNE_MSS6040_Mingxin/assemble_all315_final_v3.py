from pathlib import Path
import json,hashlib,re,datetime
O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,t):
 with (O/n).open('x') as f:f.write(t)
def js(n,o):put(n,json.dumps(o,ensure_ascii=False,indent=2))
body=['# 明心寶鑑 BNE MSS6040 · 315頁方法遷移照錄 v3',''];mapping=[];coverage=[];findings=['# 逐頁復核與疑難記錄',''];errors=[]
for n in range(1,316):
 p=O/'review'/f'pdf_{n:03}_mapping.json';d=json.loads(p.read_text());old=Path(d['old']);src=old.read_text().splitlines();assert len(src)==len(d['lines'])
 assert sha(old)==d['old_sha256'];assert sha(Path(d['image']))==d['image_sha256']
 body.extend([f'## PDF {n:03}',f'原圖：{d["image"]}','']);skip=False;cnt=0
 for x in d['lines']:
  assert src[x['old_line']-1]==x['old_text']
  l=x['new_text'];reason='old_companion';final=None
  if l is not None:
   if l.startswith('## '):skip=bool(re.search('非正文|页面类别与阅读次序',l))
   meta=l.startswith(('源：','- 源：','- 原页图：','- 类别：','- 状态：','原图：','方向：'))
   if not skip and not meta and not l.startswith('# '):
    final=l;reason='body'
    if n==195:final=final.replace('malicia〔暂读〕','〔未定；malicia候選已撤回〕')
    body.append(final);cnt+=1
   else:reason='page_metadata_or_nonbody'
  mapping.append({'page':n,**x,'final_disposition':reason,'final_text':final,'final_line':len(body) if final is not None else None})
 body.append('')
 coverage.append({'page':n,'visual_review':d['visual_review'],'full_text_verified':False,'image':d['image'],'image_sha256':d['image_sha256'],'old_sha256':d['old_sha256'],'body_lines':cnt,'change_candidates':d['changes']})
 findings.extend([(O/'review'/f'pdf_{n:03}.md').read_text(),''])
base=json.loads((O/'prior_text_hash_baseline_v3.json').read_text())
for a in base['files']:
 if sha(Path(a['path']))!=a['sha256']:errors.append(a['path'])
assert not errors
put('Mingxin_all315_body_final_v3.md','\n'.join(body))
js('source_line_mapping_all315_final_v3.json',mapping)
js('coverage_all315_method_transfer_v3.json',coverage)
findings.append((O/'review/pdf_195_candidate_caution.md').read_text());put('doubts_and_findings_all315_v3.md','\n'.join(findings))
changes=[(d['page'],c) for d in coverage for c in d['change_candidates']]
js('final_delivery_acceptance_v3.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':315,'source_lines':len(mapping),'baseline_files_unchanged':len(base['files']),'baseline_errors':errors,'pages_with_change_candidates':len({p for p,c in changes}),'change_candidates':len(changes),'full_text_verified':False,'final_body_sha256':sha(O/'Mingxin_all315_body_final_v3.md'),'candidate_195_withdrawn':True})
put('FINAL_DELIVERY_v3.md',f'''# Mingxin 315頁方法遷移交付\n\n原圖逐頁復核315/315；非盲二校。首稿與v2共{len(base['files'])}檔哈希未變。全源物理行映射{len(mapping)}行；這是來源完整性，不等於全文校定。\n\n- 正文：Mingxin_all315_body_final_v3.md\n- 覆蓋：coverage_all315_method_transfer_v3.json\n- 源行映射：source_line_mapping_all315_final_v3.json\n- 逐頁疑難與校記：doubts_and_findings_all315_v3.md\n- 驗收：final_delivery_acceptance_v3.json\n\n{len({p for p,c in changes})}頁有{len(changes)}項改寫或候選，不是已證錯字數。195 malicia優先候選已撤回；最終正文改回未定並明示撤回，逐頁工作稿保留軌跡。\n\n適用：漢字偏旁、重字、小字層、跨頁連續、西語古拼寫和縮記、漢西語義旁證。不能套DHS聲調規約，也不能用常見訓誡名句補原稿。105縮記及多處湏／須候選屬實際改進；54缺不、120怨與119amistad等原層不一致保留。\n\n失敗／未解：淡色同方向西文多頁未讀全，不能一概當鏡向透背；人名音寫、重墨、裁邊、近形字仍疑。195候選撤回顯示語義期待會造成誤判。所有頁full_text_verified=false；不給準確率。研究規則與報告另存，不將水印或工具說明混入正文。\n''')
print((O/'final_delivery_acceptance_v3.json').read_text())
