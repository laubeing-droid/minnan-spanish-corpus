from pathlib import Path
import collections, datetime, hashlib, json, re, shutil
import fitz

BASE = Path('/workspace/scratch/3ee2b91a8980/minnan_continuation')
OUT = Path(__file__).resolve().parent
INVENTORY = BASE/'handoff_21sources_20261016_v1/completed21_sources_handoff_inventory_v1.json'
DHS = BASE/'dhs_hispanico_sinicum/delivery_package_v1'
ANG = BASE/'angelica_method_independent_v3'
HAB = BASE/'hab_all14_method_transfer_summary_v3'
TEXT = {'.md','.json','.jsonl','.py','.txt','.csv','.tsv','.yaml','.yml','.toml','.sh'}
created = datetime.datetime.now(datetime.timezone.utc).isoformat()
copies, destination_map, source_map, exclusions = [], {}, {}, []

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(4*1024*1024), b''): h.update(block)
    return h.hexdigest()

def write(name, value):
    p = OUT/name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f: f.write(value if isinstance(value, bytes) else value.encode('utf8'))
    return p

def jbytes(value): return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf8')

def copy(p, dest, role):
    p, dest = Path(p), str(dest)
    assert p.is_file(), str(p)
    assert p.suffix.lower() in TEXT, str(p)
    if dest in destination_map:
        assert destination_map[dest] == str(p), (dest,p)
        return dest
    data = p.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    write(dest, data)
    assert sha(OUT/dest) == digest == sha(p), str(p)
    record = {'path':dest,'role':role,'bytes':len(data),'sha256':digest,
              'original_path':str(p),'original_sha256':digest,'copy_matches_original':True}
    copies.append(record); destination_map[dest] = str(p)
    source_map.setdefault(str(p), []).append(dest)
    return dest

def copy_tree(p, dest, role, skip=None):
    skip = set() if skip is None else skip
    results = []
    for f in sorted(Path(p).rglob('*')):
        if not f.is_file() or f in skip: continue
        if f.suffix.lower() in TEXT: results.append(copy(f,Path(dest)/f.relative_to(p),role))
        else: exclusions.append({'original_path':str(f),'reason':'Non-text file deliberately not copied','bytes':f.stat().st_size})
    return results

def pages(p):
    return [int(m.group(1)) for line in Path(p).read_text().splitlines()
            if (m := re.match(r'^#{1,3}\s+(?:HAB\s*\d+\s*[·.]\s*)?PDF\s+(\d+)\b',line,re.I))]

def source_pdf_info(p, expected):
    p=Path(p)
    with fitz.open(p) as doc: count=len(doc)
    assert count == expected, (p,count,expected)
    return {'filename':p.name,'original_path':str(p),'bytes':p.stat().st_size,
            'sha256_current':sha(p),'physical_page_count_current':count,'included_in_package':False}

inv = json.loads(INVENTORY.read_text())
assert len(inv['entries']) == 21
free_before = shutil.disk_usage(OUT).free
assert free_before > 100*1024*1024, free_before

# Validate every legacy body against the existing handoff, without changing it.
legacy_checks=[]
for e in inv['entries']:
    for r in e['current_body_hashes']:
        digest=sha(r['path'])
        assert digest == r['sha256'], r['path']
        legacy_checks.append({'original_path':r['path'],'sha256_current':digest,'matches_21source_inventory':True})

labels=['02_UB_Ms1027']+[f'{n+2:02}_HAB_91.2_Extrav_{n:02}' for n in range(1,15)]+[
    '17_BNE_MSS6040_Mingxin','18_BNE_R33396_Shilu','19_BnF_Chinois9276_Paris',
    '20_Angelica_Ms60_DSH','21_ONB_Sin282A','22_AUST_Tomo211_fragments']
assert len(labels)==21
entries=[]

# DHS first draft and its existing small-text package.
dhs_body=DHS/'body/DHS_full_first_draft_body_v2.md'
dhs_label='01_DHS_Hispanico_Sinicum'
dhs_dest=copy(dhs_body,f'body/{dhs_label}__{dhs_body.name}','primary_body')
assert pages(dhs_body)==list(range(1,1141))
anchors=re.findall(r'<a id="pdf-(\d+)"></a>',dhs_body.read_text())
assert [int(x) for x in anchors]==list(range(1,1141))
dhs_comp=copy_tree(DHS,f'companions/{dhs_label}','DHS_evidence_method_code_history',{dhs_body})
entries.append({'source_id':dhs_label,'source_pdf':source_pdf_info(inv['pending_source']['source_pdf'],1140),
    'primary_body':dhs_dest,'primary_body_original':str(dhs_body),'primary_body_sha256':sha(dhs_body),
    'primary_body_file_count':1,'physical_page_sequence':{'first':1,'last':1140,'count':1140,'exact_contiguous_sequence':True,'missing':[],'duplicates':[]},
    'related_group':'DHS; separate work from DSH, cross-references are research only',
    'status':'1140物理页合并首稿；并非全书校定或全部严格盲测',
    'full_text_verified':False,'complete_text_pages_claimed':None,
    'unresolved':'仅八页的部分字段新增原像素外校；另有DSH016互参和五页跨21源定点复验。正文保留首稿，后校单列，尚未外校的页及字段仍大量存在。',
    'companions':dhs_comp,'page_order_note':'PDF 0001–1140及pdf-0001至pdf-1140锚点；原书页号不等于PDF序号。'})

for e,label in zip(inv['entries'], labels):
    original_body=Path(e['body_files'][0])
    angelica='Angelica' in e['source_file']
    primary=ANG/'merged_release_v1/Angelica_Ms60_all169_method_independent_v3.md' if angelica else original_body
    pgs=pages(primary)
    assert pgs==list(range(1,e['expected_pdf_pages']+1)), (label,len(pgs))
    dest=copy(primary,f'body/{label}__{primary.name}','primary_body')
    entry={'source_id':label,'source_pdf':source_pdf_info(e['source_pdf'],e['expected_pdf_pages']),
        'primary_body':dest,'primary_body_original':str(primary),'primary_body_sha256':sha(primary),'primary_body_file_count':1,
        'physical_page_sequence':{'first':1,'last':e['expected_pdf_pages'],'count':len(pgs),'exact_contiguous_sequence':True,'missing':[],'duplicates':[]},
        'related_group':e['group'],'status':e['status'],'full_text_verified':False,'complete_text_pages_claimed':None,
        'unresolved':e['unresolved'],'legacy_note':e.get('legacy'),
        'page_order_note':'原PDF顺序；不按推测刊页重新排序。封面、空白、装帧或未读清页均占页位。',
        'companions':[]}
    if angelica:
        entry['unresolved']='字母及调号细笔仍未定；9/21/52有旧见、33有教学暴露。165–168为书信题记，169封底。169冻结页已合并且逐字节保留，不再缺合并MD；独立稿没有虚构的旧稿逐行替换映射。'
        entry['status']='169冻结逐页独立方法稿及纯连接合本；非全部严格盲测、非全书校定'
        entry['companions'] += copy_tree(ANG/'merged_release_v1',f'companions/{label}/merged_release_evidence','Angelica_merge_evidence',{primary})
        entry['frozen_page_input_files']=[copy(p,f'companions/{label}/frozen_page_inputs/{Path(p).name}','frozen_page_input') for p in e['body_files']]
        mapj=json.loads((ANG/'merged_release_v1/coverage_and_source_mapping_all169_v1.json').read_text())
        assert mapj['body_sha256']==sha(primary)
        mb=primary.read_bytes()
        for row in mapj['pages']:
            pb=Path(row['source_md']).read_bytes()
            assert hashlib.sha256(pb).hexdigest()==row['source_sha256']
            assert mb[row['merged_byte_start_inclusive']:row['merged_byte_end_exclusive']]==pb
        entry['all169_original_frozen_inputs_and_merged_byte_spans_verified']=True
    if label.startswith('22_'):
        entry['complete_text_pages_claimed']=0
        entry['status']='仅10个公开残页页位；完整正文识读0页'
        entry['unresolved']='007/009有较多部分识读且大量疑读，属于初读而非校定；008/010仅候选。公开残页不构成完整教理问答或语法全书。'
    if 'part' in e: entry['hab_part']=e['part']
    method_root=ANG if angelica else next(p for p in primary.parents if p.name=='method_transfer_v3')
    for category in ['coverage_files','mapping_files','issue_files','scripts']:
        for path in e.get(category,[]):
            p=Path(path)
            assert p.exists(), p
            if p.is_relative_to(HAB):
                # Copied once in the group evidence tree below.
                continue
            if p.is_relative_to(method_root): rel=p.relative_to(method_root)
            else: rel=Path('external_references')/p.parent.name/p.name
            target=Path('companions')/label/rel
            copied = copy_tree(p,target,category) if p.is_dir() else [copy(p,target,category)]
            entry['companions'].extend(x for x in copied if x not in entry['companions'])
    entries.append(entry)

# HAB combined reader is redundant with, not a substitute for, its 14 source segments.
hab_body=HAB/'HAB_all14_461pages_body_v3.md'
hab_dest=copy(hab_body,f'body/90_HAB_all14_sources03-16__{hab_body.name}','group_combined_body')
hab_text=hab_body.read_text()
parts=re.split(r'\n# 分册 (\d{2})\n',hab_text)
assert [int(parts[n]) for n in range(1,len(parts),2)]==list(range(1,15))
hab_checks=[]
for n in range(14):
    e=inv['entries'][n+1]
    current=Path(e['body_files'][0]).read_text()
    assert parts[2*n+2].strip()==current.strip(), n+1
    hab_checks.append({'part':n+1,'primary_source_id':labels[n+1],'section_equals_current_final_body_except_outer_separator_whitespace':True})
hab_comp=copy_tree(HAB,'companions/90_HAB_group','HAB_group_evidence_and_actual_code',{hab_body})
for e in entries:
    if 'hab_part' in e: e['shared_group_companions']='companions/90_HAB_group'

copy_tree(BASE/'handoff_21sources_20261016_v1','companions/92_prior21_handoff_history','historical_handoff')
copy_tree(BASE/'blind_calibration_20261016_v1','companions/91_historical_method_research','historical_method_research_and_test_keys')

assert len(entries)==22
assert sum(e['physical_page_sequence']['count'] for e in entries)==3139
assert len([r for r in copies if r['role']=='primary_body'])==22
assert not any(Path(r['path']).suffix.lower() not in TEXT for r in copies)

verification={'created_utc':created,'scope':'File integrity, final-entry selection and page-order audit only; not a new visual or textual accuracy review',
    'source_count':22,'physical_page_positions':3139,'primary_body_files':22,'additional_HAB_group_combined_file':hab_dest,
    'legacy_body_hash_checks':legacy_checks,'HAB_group_final_segment_checks':hab_checks,
    'source_PDF_page_counts_and_SHA256_recomputed':True,'missing_primary_bodies':[],'page_gaps':[],'duplicate_page_positions_within_source':[],
    'Angelica169_input_bytes_preserved_in_merge':True,'DHS1140_headings_and_anchors_exact_sequence':True,
    'copied_files_byte_identical_at_copy_and_verification':True,'content_accuracy_certified':False,
    'full_text_verified_for_all_sources':False,'AUST_complete_text_pages':0,'no_PDF_or_image_copied':True,
    'compressed':False,'uploaded':False,'published':False,'old_files_overwritten_or_deleted':False}
write('VERIFICATION_REPORT_v1.json',jbytes(verification))

lines=['# 全22来源文本预审清单','',f'生成时间：{created}','',
       '22是来源PDF数量，不是22部独立书。页数为物理页位。全部全文核定状态均为false。',
       '每源一个首要正文入口；HAB另有同书组合本；Angelica169份冻结输入在配套证据中，不重复计为来源。','']
for e in entries:
    p=e['source_pdf']; seq=e['physical_page_sequence']
    lines.extend([f"## {e['source_id']}",'',f"- 原来源：{p['filename']}",f"- 原PDF：{p['original_path']}",
      f"- 原PDF SHA256（本次重算）：{p['sha256_current']}",f"- 首要正文：[打开]({e['primary_body']})",
      f"- 正文原路径：{e['primary_body_original']}",f"- 正文SHA256：{e['primary_body_sha256']}",
      f"- 份数和页序：1份首要MD，PDF {seq['first']:04}–{seq['last']:04}，{seq['count']}个连续页位；无缺页号、无重复页号。",
      f"- 状态：{e['status']}",f"- 缺口／疑难：{e['unresolved']}",
      f"- 配套：companions/{e['source_id']}/（逐文件见manifest）",''])
lines.extend(['## HAB同书组附加合本','',f'- [14分段461页合本]({hab_dest})',
              '- 依原分册01–14、各自PDF序号连接；14源分段仍保留。没有对原卷叶序、重复装帧或缺叶作推测性重排。',''])
write('SOURCE_INVENTORY_ALL22_v1.md','\n'.join(lines))

readme='''# 全22来源文本交付预审包

这是2026-10-16建立的本地文本预审快照。未压缩、未上传、未发布、未安装；原文件均不删除、不覆盖。正文照原字节复制，未借包装新增正文校改。

## 先读这几项

1. [逐源入口与状态](SOURCE_INVENTORY_ALL22_v1.md)：22份来源各自的最终正文、原PDF身份、SHA256、份数、页序和缺口。
2. [完整manifest](manifest_all22_v1.json)：逐来源资料、所有配套文件的包内路径／原路径／SHA256、实际字节总数及明确未含内容。
3. [本轮核验报告](VERIFICATION_REPORT_v1.json)：最终入口、旧清单正文hash、页号连续性、Angelica合并字节及HAB分段一致性；这些不等于文字准确率。
4. SHA256SUMS.txt校验除它自身外的每个交付文件；在本目录运行 `sha256sum -c SHA256SUMS.txt` 可复验文本包。

## 数量与状态必须这样理解

- 22份是来源PDF，不是22部独立书。HAB十四分册是同书组；DSH Angelica与Paris为两套底本；AUST是公开残页组合。
- 共有3139个PDF物理页位：既有21源1999，加DHS1140。封面、空白、装帧、现代出版说明和未读清页均计页位。不能说3139页完整正文或全文校定。
- body/有22个逐来源首要MD，加1个HAB十四分册合本，共23个直接阅读入口。Angelica另外169份冻结页稿在companions/20_Angelica_Ms60_DSH/frozen_page_inputs/，是合并依据，不再算169份新来源。
- 所有来源full_text_verified仍为false。疑读、未辨和未决均保留；没有全书准确率、全量独立复验或全部严格盲测声明。
- AUST仅10个公开残页页位，完整正文识读0页。007/009较多部分识读仍带大量疑读，属于初读；008/010仅候选。不能包装成教理问答或语法全本。
- DHS首稿页号及锚点0001–1140连续；本轮只有八页的部分字段新增外校，另有DSH016互参及五页跨21源定点复验。这些校读在research配套中，未写回首稿，不代表全1140页或其他21源全部重新核读。

## 目录与正文优先级

- body/：按编号排列的最终入口。Grammar选clean_v3；Mingxin／Shilu／ONB选final_v3；HAB05、06、13选release最终层；其余用既有21源清单指定版本。HAB合本按01–14保留原分段，不自行去重或重排。
- companions/01_DHS_Hispanico_Sinicum/：DHS索引、审计、research、工作记录、实际代码、当前方法Skill。它是原delivery_package_v1的小文本快照，原有相对正文入口应改由本包body/对应文件进入。
- companions/02…22/：各源覆盖、映射、疑难、工作记录和实际脚本。来源原路径保留在manifest，不在旧记录内进行全局替换。
- companions/90_HAB_group/：HAB组覆盖、最终逐行映射增补、验收、实际脚本及历史Skill候选材料。
- companions/91_historical_method_research/：本轮方法、一手研究学习、小样本对照和答案键的历史记录。REFERENCE_ONLY、比对结果和已知答案不得交给要求新隔离识读的读者；只有明确method_only材料适合纯方法准备。这是用途区分，不是权限硬隔离。
- companions/92_prior21_handoff_history/：原21源交接快照，保持原字节。其“DHS待接入”“Angelica合并尚缺”等文字只描述旧时点，现由本README、Angelica合并证据和逐源清单更新。旧“Skill尚待封装”亦为历史阶段，当前方法材料在DHS/skill/，验证范围仍受限且未安装。

## 已知难点与撤回必须保留

Paris120两条旧错字指控已撤回，以addendum优先；Mingxin195 malicia候选撤回；Shilu113電候选撤回，最终采用暴雹。不得从旧工作记录反向覆盖本包最终正文。ONB日期和章次原层矛盾不静默调和。HAB草写音写、账目重墨、细注与裁边疑难及低分辨率限制仍在。

Angelica169合本仅连接169份冻结输入，逐字节核验通过。9／21／52有旧见、33有教学暴露；165–168是书信／题记，169封底，不能当同类词项计分。原清单中“尚无合本”的包装缺口已经补齐，文字疑难没有因此解决。

## 可携带范围与复现限制

本包只含文本；原PDF、原图、截图、参考PDF、图像裁片、大型图像审计对象及旧稿全集均不在包内。原22份PDF的名称、位置、实际页数和本次SHA256都有记录；它们共约1.2GB但未复制。旧coverage或脚本中的绝对路径仍指原环境，离开该环境不能直接看图或完整重跑原项目。须另取得相同SHA的原件以及所需图像／依赖，并审查路径与输出目标。不要未经检查直接运行历史保存脚本。

可以脱离聊天读取正文、当前状态、方法及现有校读结论；不能仅凭此小包独立重现全部看图证据。SHA只证明文件一致性，不证明识读正确。

## 本次核验边界和下一步

本次重算22份PDF的SHA256及真实页数；核验22份首要正文页序无缺口／重复；与21源旧清单核对当前正文hash；核验Angelica169输入在合本中的字节区间；核验HAB合本十四分段对应最终分册。所有复制件与原文本逐字节一致。本次没有重新逐页看3139幅图。

当前停在本地预审。先由主协调审查本包数量、状态与范围，再决定是否制作压缩包或向指定接收方交付。本包没有执行压缩或上传。后续校订须另建版本，并区分已确认、优先候选、未定，不能无痕改首稿。
'''
write('README_START_HERE.md',readme)

# Verify source copies again immediately before the manifest snapshot.
for r in copies:
    assert sha(OUT/r['path'])==r['sha256']==sha(r['original_path']), r['path']
payloads=sorted(p for p in OUT.rglob('*') if p.is_file())
copy_lookup={r['path']:r for r in copies}
files=[copy_lookup.get(str(p.relative_to(OUT)),{'path':str(p.relative_to(OUT)),'role':'generated_review_document_or_builder',
       'bytes':p.stat().st_size,'sha256':sha(p),'original_path':None,'original_sha256':None}) for p in payloads]
payload_bytes=sum(f['bytes'] for f in files)
manifest_name='manifest_all22_v1.json'
checksum_name='SHA256SUMS.txt'
checksum_paths=sorted([r['path'] for r in files]+[manifest_name])
checksum_bytes=sum(len(('0'*64+'  '+p+'\n').encode('utf8')) for p in checksum_paths)
manifest={'created_utc':created,'package_name':OUT.name,'delivery_stage':'local_review_only',
    'source_count':22,'independent_book_count_asserted':False,'physical_page_positions':3139,
    'primary_body_file_count':22,'additional_group_combined_file_count':1,'frozen_Angelica_input_file_count':169,
    'full_text_verified':False,'source_entries':entries,
    'HAB_group_combined':{'body':hab_dest,'sha256':sha(hab_body),'parts':14,'physical_page_positions':461,'companions':hab_comp},
    'files':files,'excluded_non_text_files_encountered':exclusions,
    'exclusion_policy':'No PDF, image, archive, original-image tree or old-draft corpus. Exclusions list records only encountered non-text files, not every omitted original-image file.',
    'content_gaps':['AUST: 10 public page positions; 0 complete text pages; 007/009 partial uncertain first readings.',
       'All source texts remain unverified in full; many uncertain readings remain.',
       'DHS new external collation covers parts of only eight pages, plus DSH016 and five targeted cross-source pages.',
       'Original PDFs and images must be supplied separately for visual evidence reproduction.',
       'Legacy absolute paths and historical progress statements retained unchanged; current package README takes precedence for delivery state.',
       'Angelica independent-reading production script was not located in the old handoff; actual merge and other located scripts are included.'],
    'missing_required_primary_files':[],'source_PDF_total_bytes_not_copied':sum(e['source_pdf']['bytes'] for e in entries),
    'disk_free_bytes_before':free_before,'file_count_including_manifest_and_checksums':len(files)+2,
    'payload_bytes_excluding_manifest_and_checksums':payload_bytes,
    'manifest_self_bytes':0,'checksums_file_bytes':checksum_bytes,'package_total_bytes_including_manifest_and_checksums':0,
    'manifest_hash_location':checksum_name,'checksum_file_self_hash':'Omitted to avoid recursive checksum dependency',
    'compressed':False,'uploaded':False,'published':False,'original_files_changed':False}
for _ in range(20):
    mb=jbytes(manifest)
    if manifest['manifest_self_bytes']==len(mb) and manifest['package_total_bytes_including_manifest_and_checksums']==payload_bytes+len(mb)+checksum_bytes: break
    manifest['manifest_self_bytes']=len(mb)
    manifest['package_total_bytes_including_manifest_and_checksums']=payload_bytes+len(mb)+checksum_bytes
else: raise AssertionError('Manifest size did not stabilize')
write(manifest_name,mb)
checksums=''.join(sha(OUT/p)+'  '+p+'\n' for p in checksum_paths)
assert len(checksums.encode('utf8'))==checksum_bytes
write(checksum_name,checksums)
actual_files=[p for p in OUT.rglob('*') if p.is_file()]
actual_bytes=sum(p.stat().st_size for p in actual_files)
assert actual_bytes==manifest['package_total_bytes_including_manifest_and_checksums']
assert len(actual_files)==manifest['file_count_including_manifest_and_checksums']
print(json.dumps({'directory':str(OUT),'file_count':len(actual_files),'total_bytes':actual_bytes,
    'manifest':str(OUT/manifest_name),'README':str(OUT/'README_START_HERE.md'),
    'source_count':22,'primary_body_files':22,'additional_HAB_combined':1,'page_positions':3139,
    'copied_files':len(copies),'missing_required_primary_files':[],'disk_free_bytes_after':shutil.disk_usage(OUT).free},ensure_ascii=False,indent=2))
