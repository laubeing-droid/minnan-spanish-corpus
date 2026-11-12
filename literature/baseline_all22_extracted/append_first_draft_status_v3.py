"""Append the resumed FIRST_DRAFT decision without changing prior files."""
from pathlib import Path
import datetime, hashlib, json

ROOT=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def put(name,data):
    if isinstance(data,str):data=data.encode('utf8')
    with (ROOT/name).open('xb') as f:f.write(data)
def jb(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf8')

old=json.loads((ROOT/'manifest_all22_CURRENT_v2.json').read_text())
for r in old['files']:assert sha(ROOT/r['path'])==r['sha256'],r['path']
for e in old['source_entries']:assert sha(ROOT/e['primary_body'])==e['primary_body_sha256'],e['source_id']

status={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'FIRST_DRAFT_PENDING_SYMBOL_NORMALIZATION',
 'delivery_stage':'LOCAL_COMPLETE_TEXT_REVIEW_CANDIDATE_NOT_PUBLISHED',
 'scope':'All 22 source first-draft texts, with current final-layer selection preserved byte-for-byte.',
 'supersedes_operational_hold':'DELIVERY_HOLD_READABILITY_v1.json',
 'historical_hold_retained':True,'hold_issue_resolved':False,
 'hold_disposition':'Resume first-draft assembly with prominent qualification; defer shorthand and symbol normalization to later source-supported proofreading.',
 'specific_pending_example':'DHS PDF259 L116: cheng升斜小c／song降斜等速记式说明仍在原首稿；未改写为确定调号。',
 'future_editorial_method':'Broaden relevant literature reading before choosing evidence-backed transcription conventions. Do not invent a normalization convention during packaging.',
 'body_files_changed':False,'skill_status':'METHOD_DRAFT_NOT_FINAL_NOT_INSTALLED',
 'permission_boundary':'No compression or upload until the root coordinator reviews this candidate.'}
put('DELIVERY_STATUS_FIRST_DRAFT_v2.json',jb(status))

readme=(ROOT/'00_README_CURRENT_v2.md').read_text()
readme=readme.replace('# 全22来源文本交付预审包','# FIRST_DRAFT：全22来源文本预审包，待符号规范校对',1)
readme=readme.replace('00_README_CURRENT_v2.md','00_FIRST_DRAFT_README_CURRENT_v3.md').replace('manifest_all22_CURRENT_v2.json','manifest_all22_FIRST_DRAFT_CURRENT_v3.json').replace('SHA256SUMS_CURRENT_v2.txt','SHA256SUMS_FIRST_DRAFT_CURRENT_v3.txt')
insertion='''
## 当前交付定位：FIRST_DRAFT / 待符号规范校对

本包恢复为全22来源首稿的完整文本预审候选，可以审阅与逐源定位；未成为校定本。全部原首稿字节保留。正文中的速记式说明、字形描述、调号编码和疑读待后续统一校对，不能直接当作规范读法。DHS PDF259 L116的“cheng升斜小c／song降斜”等是当前明确例子，尚未解决，未改写原稿。

后续先广读相关文献和一手材料，再采用有证据支持的转写惯例；包装过程不自造统一符号规则。文件名中既存final、clean、release仅指各历史工作层的最终入口，不表示全书最终学术定稿。

Skill仍为METHOD_DRAFT（方法草案），不得最终封版或视为已经安装的成熟技能。当前12页部分字段外校及此前实验的验证范围仍有限；把首稿集中交付不扩大这些结论。

DELIVERY_HOLD_READABILITY_v1.json是此前暂停通知，现由DELIVERY_STATUS_FIRST_DRAFT_v2.json承接：只解除首稿整理暂停，没有宣布可读性问题已解决。原通知、旧README、旧manifest和旧校验清单均保留为历史快照；当前完整清单是manifest_all22_FIRST_DRAFT_CURRENT_v3.json。继续禁止压缩／上传，等待根协调审阅。

'''
readme=readme.replace('## 当前入口及版本说明',insertion+'## 当前入口及版本说明',1)
readme=readme.replace('本包没有执行压缩或上传。后续校订须另建版本', '本包没有执行压缩或上传。可读性问题改列后续校对，不通过无痕更改首稿解决。后续校订须另建版本')
put('00_FIRST_DRAFT_README_CURRENT_v3.md',readme)

lookup={r['path']:r for r in old['files']}
rows=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=str(p.relative_to(ROOT))
    r=dict(lookup.get(rel,{'path':rel,'role':'generated_review_status_or_inventory_snapshot','original_path':None,'original_sha256':None}),bytes=p.stat().st_size,sha256=sha(p))
    if rel.startswith('body/'):
        r['editorial_status']='FIRST_DRAFT_PENDING_SYMBOL_NORMALIZATION'
    if '/skill/' in rel:
        r['method_status']='METHOD_DRAFT_NOT_FINAL'
    rows.append(r)

new=dict(old)
new.update({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'inventory_version':'FIRST_DRAFT_CURRENT_v3','editorial_status':'FIRST_DRAFT_PENDING_SYMBOL_NORMALIZATION',
 'skill_status':'METHOD_DRAFT_NOT_FINAL_NOT_INSTALLED',
 'readme':'00_FIRST_DRAFT_README_CURRENT_v3.md',
 'current_decision':'DELIVERY_STATUS_FIRST_DRAFT_v2.json',
 'historical_hold':'DELIVERY_HOLD_READABILITY_v1.json',
 'operational_hold_on_assembly_lifted':True,'readability_issue_resolved':False,
 'previous_inventory_snapshot':'manifest_all22_CURRENT_v2.json',
 'delivery_stage':'complete_text_first_draft_local_review_candidate',
 'files':rows,'file_count_including_manifest_and_checksums':len(rows)+2,
 'payload_bytes_excluding_manifest_and_checksums':sum(r['bytes'] for r in rows),
 'manifest_self_bytes':0,'checksums_file_bytes':0,'package_total_bytes_including_manifest_and_checksums':0,
 'manifest_hash_location':'SHA256SUMS_FIRST_DRAFT_CURRENT_v3.txt'})
new['source_entries']=[dict(e,editorial_status='FIRST_DRAFT_PENDING_SYMBOL_NORMALIZATION') for e in old['source_entries']]
new['content_gaps']=list(old['content_gaps'])+[
 'Symbol shorthand and notation remain pending literature-informed normalization, including DHS259 L116; the frozen first drafts are unchanged.',
 'Skill is still a method draft, not a finalized or installed skill.']
manifest='manifest_all22_FIRST_DRAFT_CURRENT_v3.json'
checks='SHA256SUMS_FIRST_DRAFT_CURRENT_v3.txt'
paths=sorted([r['path'] for r in rows]+[manifest])
new['checksums_file_bytes']=sum(len(('0'*64+'  '+p+'\n').encode('utf8')) for p in paths)
for _ in range(20):
    data=jb(new)
    total=new['payload_bytes_excluding_manifest_and_checksums']+len(data)+new['checksums_file_bytes']
    if new['manifest_self_bytes']==len(data) and new['package_total_bytes_including_manifest_and_checksums']==total:break
    new['manifest_self_bytes']=len(data);new['package_total_bytes_including_manifest_and_checksums']=total
else:raise AssertionError('manifest size convergence')
put(manifest,data)
put(checks,''.join(sha(ROOT/p)+'  '+p+'\n' for p in paths))
actual=[p for p in ROOT.rglob('*') if p.is_file()]
assert len(actual)==new['file_count_including_manifest_and_checksums']
assert sum(p.stat().st_size for p in actual)==new['package_total_bytes_including_manifest_and_checksums']
for e in new['source_entries']:assert sha(ROOT/e['primary_body'])==e['primary_body_sha256']
print(json.dumps({'status':new['editorial_status'],'README':str(ROOT/new['readme']),
 'manifest':str(ROOT/manifest),'checksums':str(ROOT/checks),
 'actual_files':len(actual),'actual_total_bytes':new['package_total_bytes_including_manifest_and_checksums'],
 'source_count':22,'direct_body_MD':23,'physical_page_positions':3139,
 'body_files_changed':False,'skill_status':new['skill_status'],
 'compressed':False,'uploaded':False,'missing_required_primary_files':[]},ensure_ascii=False,indent=2))
