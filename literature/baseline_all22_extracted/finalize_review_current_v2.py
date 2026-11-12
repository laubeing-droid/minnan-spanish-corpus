"""Append runtime-provenance clarification and a new complete inventory.

All earlier files and inventory snapshots remain unchanged. No archive, upload,
deletion, overwrite, or historical project-script execution is performed.
"""
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
def jb(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8')

old=json.loads((ROOT/'manifest_all22_v1.json').read_text())
for row in old['files']:
    assert sha(ROOT/row['path'])==row['sha256'],row['path']

code_status={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'script':'save_aust_v3.py','original_path':'/tmp/save_aust_v3.py',
 'original_path_currently_exists':Path('/tmp/save_aust_v3.py').exists(),
 'snapshot_original_path':'/workspace/scratch/3ee2b91a8980/minnan_continuation/handoff_21sources_20261016_v1/small_code_snapshots/save_aust_v3.py',
 'snapshot_package_paths':[r['path'] for r in old['files'] if r['path'].endswith('/save_aust_v3.py')],
 'bytes':5043,'sha256':'4a0d344a8ae125651cbd8d97f8efe0240dd5c0f77a46dd9ff2e4dfdac82b1023',
 'matches_prior_recorded_original_SHA256':True,
 'evidence_of_copy_and_static_integrity':'companions/92_prior21_handoff_history/WORK_RECORD_existing_artifact_verification_v1.md and actual_code_index_v1.json',
 'runtime_status':'Unverified execution; retained as historical source-code evidence, not a validated executable tool.',
 'runtime_evidence_found_in_checked_handoff_records':None,
 'historical_script_executed_during_packaging':False,
 'scope_note':'File presence, hash agreement, and matching output artifact names are not proof of an observed successful runtime.'}
for p in code_status['snapshot_package_paths']:assert sha(ROOT/p)==code_status['sha256']
put('CODE_PROVENANCE_AND_RUNTIME_v1.json',jb(code_status))
put('CODE_PROVENANCE_AND_RUNTIME_v1.md','''# 代码来源与运行验证边界

AUST的原临时路径/tmp/save_aust_v3.py当前失效。原21源handoff内small_code_snapshots/save_aust_v3.py仍在，5043 bytes，SHA256为4a0d344a8ae125651cbd8d97f8efe0240dd5c0f77a46dd9ff2e4dfdac82b1023，与既存代码索引记录完全相同。本包从此快照复制，未创建或改写原临时路径。

已核查的WORK_RECORD_existing_artifact_verification_v1.md只证明当时保存快照和文件核验；actual_code_index_v1.json提供路径、用途、大小及SHA。未定位到足以核验该脚本实际成功运行的日志。因此AUST保存脚本在本包中定为“历史源代码资料，运行未核”，不得列为已验证可执行工具。本次没有运行它。

所有历史项目脚本均保留原文和路径；本次对它们的SHA检查不是运行验证。DHS原包所述tested_project_scripts仅继承该包的既有声明，本次未重跑。真正本轮运行的装配脚本为build_review_snapshot_v2_current12.py、v3、v4及最终成功的v5；早期尝试因页标格式或过期临时路径主动停止，原文件均未覆盖，最后只复用已逐字节核对的部分复制件。finalize_review_current_v2.py生成本运行边界说明和当前清单。

不要直接在新的工作目录运行历史保存／合并脚本；应先审查其中的绝对路径、输入和输出行为。原PDF、图像和依赖不随本包提供，不能把文本打包成功理解为全套项目可直接复现。
''')
current=(ROOT/'README_START_HERE.md').read_text().replace('manifest_all22_v1.json','manifest_all22_CURRENT_v2.json').replace('SHA256SUMS.txt','SHA256SUMS_CURRENT_v2.txt')
current=current.replace('## 先读这几项','''## 当前入口及版本说明

本页00_README_CURRENT_v2.md为当前入口，完整文件清单为manifest_all22_CURRENT_v2.json，完整校验清单为SHA256SUMS_CURRENT_v2.txt。原README_START_HERE.md、manifest_all22_v1.json及SHA256SUMS.txt保持不变，作为初次装配快照；它们不统计随后追加的代码运行边界文件及当前清单。精确总bytes以当前manifest为准。

[代码来源及运行边界](CODE_PROVENANCE_AND_RUNTIME_v1.md)明确：AUST临时脚本由同SHA快照恢复交付，但没有可核实际运行日志，因此仅为历史源代码资料、运行未核，不当作已验证工具。本次不会运行这些历史脚本。

## 先读这几项''')
put('00_README_CURRENT_v2.md',current)

filelist=sorted(p for p in ROOT.rglob('*') if p.is_file())
lookup={r['path']:r for r in old['files']}
rows=[]
for p in filelist:
    rel=str(p.relative_to(ROOT))
    r=lookup.get(rel,{'path':rel,'role':'generated_review_document_or_inventory_snapshot',
                    'original_path':None,'original_sha256':None})
    r=dict(r,bytes=p.stat().st_size,sha256=sha(p))
    if rel.endswith('/save_aust_v3.py'):
        r['role']='historical_source_code_runtime_unverified'
        r['runtime_status']='Unverified; see CODE_PROVENANCE_AND_RUNTIME_v1.json'
        r['expired_original_path']='/tmp/save_aust_v3.py'
    rows.append(r)
new=dict(old)
new.update({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'inventory_version':'CURRENT_v2','readme':'00_README_CURRENT_v2.md',
 'previous_inventory_snapshot':'manifest_all22_v1.json',
 'code_runtime_provenance':'CODE_PROVENANCE_AND_RUNTIME_v1.json',
 'files':rows,'file_count_including_manifest_and_checksums':len(rows)+2,
 'payload_bytes_excluding_manifest_and_checksums':sum(r['bytes'] for r in rows),
 'manifest_self_bytes':0,'checksums_file_bytes':0,
 'package_total_bytes_including_manifest_and_checksums':0,
 'manifest_hash_location':'SHA256SUMS_CURRENT_v2.txt'})
new['content_gaps']=list(old['content_gaps'])+['AUST saved-script execution has not been verified; it is historical code evidence, not a validated runnable tool.']
manifest='manifest_all22_CURRENT_v2.json'
checkfile='SHA256SUMS_CURRENT_v2.txt'
paths=sorted([r['path'] for r in rows]+[manifest])
new['checksums_file_bytes']=sum(len(('0'*64+'  '+p+'\n').encode('utf8')) for p in paths)
for _ in range(20):
    data=jb(new)
    total=new['payload_bytes_excluding_manifest_and_checksums']+len(data)+new['checksums_file_bytes']
    if new['manifest_self_bytes']==len(data) and new['package_total_bytes_including_manifest_and_checksums']==total:break
    new['manifest_self_bytes']=len(data);new['package_total_bytes_including_manifest_and_checksums']=total
else:raise AssertionError('manifest size')
put(manifest,data)
put(checkfile,''.join(sha(ROOT/p)+'  '+p+'\n' for p in paths))
actual=[p for p in ROOT.rglob('*') if p.is_file()]
assert len(actual)==new['file_count_including_manifest_and_checksums']
assert sum(p.stat().st_size for p in actual)==new['package_total_bytes_including_manifest_and_checksums']
print(json.dumps({'manifest':str(ROOT/manifest),'README':str(ROOT/'00_README_CURRENT_v2.md'),
  'total_files':len(actual),'total_bytes':new['package_total_bytes_including_manifest_and_checksums'],
  'body_files':23,'sources':22,'PDF_physical_page_positions':3139,
  'AUST_complete_text_pages':0,'DHS_partial_collation_page_count':12,
  'source_PDF_total_bytes_not_copied':new['source_PDF_total_bytes_not_copied'],
  'copied_binary_files':0,'primary_file_gaps':[],'AUST_code_runtime':'unverified'},ensure_ascii=False,indent=2))
