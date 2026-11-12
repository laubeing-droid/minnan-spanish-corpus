from pathlib import Path
import json,hashlib,re,datetime
O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,t):
 with (O/n).open('x') as f:f.write(t)
def js(n,o):put(n,json.dumps(o,ensure_ascii=False,indent=2))
body=['# 天主正教真傳實錄 BNE R33396 · 164頁方法遷移照錄 v3',''];mapping=[];coverage=[];findings=['# 逐頁復核與疑難記錄',''];errors=[]
for n in range(1,165):
 p=O/'review'/(f'pdf_{n:03}_adopted_mapping.json' if n>=83 else f'pdf_{n:03}_mapping.json');d=json.loads(p.read_text());old=Path(d['old']);src=old.read_text().splitlines();assert len(src)==len(d['lines'])
 assert sha(old)==d['old_sha256'];assert sha(Path(d['image']))==d['image_sha256']
 body.extend([f'## PDF {n:03}',f'原圖：{d["image"]}','']);skip=False;cnt=0
 for x in d['lines']:
  assert src[x['old_line']-1]==x['old_text']
  l=x['new_text'];reason='old_companion';final=None
  if l is not None:
   if l.startswith('## '):skip=bool(re.search('非正文|页面类别与阅读次序|難辨|影像水印|轉寫限制|轉寫處理|本面判讀|視覺記錄|版面$',l))
   meta=l.startswith(('源：','- 源：','- 原页图：','- 类别：','- 状态：','原图：','方向：','僅本頁原圖視讀' ))
   if not skip and not meta and not l.startswith('# '):
    final=l;reason='body'
    if n==113:final=final.replace('暴〔疑讀：雹／電〕','暴雹')
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
put('Shilu_all164_body_final_v3.md','\n'.join(body))
js('source_line_mapping_all164_final_v3.json',mapping)
js('coverage_all164_method_transfer_v3.json',coverage)
findings.append((O/'review/pdf_113_addendum.md').read_text());put('doubts_and_findings_all164_v3.md','\n'.join(findings))
changes=[(d['page'],c) for d in coverage for c in d['change_candidates']]
js('final_delivery_acceptance_v3.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':164,'source_lines':len(mapping),'baseline_files_unchanged':len(base['files']),'baseline_errors':errors,'pages_with_change_candidates':len({p for p,c in changes}),'change_candidates':len(changes),'full_text_verified':False,'final_body_sha256':sha(O/'Shilu_all164_body_final_v3.md'),'candidate_113_withdrawn':True})

put('FINAL_DELIVERY_v3.md',f'''# Shilu 164頁方法遷移交付

原圖實核164/164，非盲二校。舊首稿及v2共{len(base['files'])}檔未改；全源物理行{len(mapping)}條均映射。圖像覆蓋與來源驗證不等於全文核定。

- 正文 Shilu_all164_body_final_v3.md
- 覆蓋 coverage_all164_method_transfer_v3.json
- 映射 source_line_mapping_all164_final_v3.json
- 逐頁疑難 doubts_and_findings_all164_v3.md
- 驗收 final_delivery_acceptance_v3.json

{len({p for p,c in changes})}頁、{len(changes)}項改寫或候選；不當錯字計數。092宜→宣、122嗇→極具字形支持；146補漏字位置而字仍未辨。113電候選已撤回，採用暴雹。083–164採用adopted映射，最初工作稿保留變更軌跡。

成功：分清正向正文、反向透背、圖環字、重文號、旁補小字和現代鉛筆號。章題頁眉不同、數字及異體原樣保留。失敗：009草體西文與多頁漢字淡筆長串仍不能可靠裁定；表述通順與熟悉經典不能替代原字。55疑漏柔等新增候選未定。圖背和空白也計圖像實核，不能算正文完整轉寫。

本書無DHS逐條羅馬注音，調號規約不可硬套。圖版、宗教漢文、書前後西語分別處理。所有頁full_text_verified=false，不估準確率。最終AgentSkill未封裝。
''')
print((O/'final_delivery_acceptance_v3.json').read_text())
