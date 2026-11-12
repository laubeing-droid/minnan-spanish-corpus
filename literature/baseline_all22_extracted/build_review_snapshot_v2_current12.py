"""Executed assembler: retain v1 planning script unchanged and add latest evidence.

This wrapper applies only in-memory source edits before first execution. It does
not edit the v1 script, source artifacts, or existing delivery files. The builder
uses exclusive creation and is intentionally not rerunnable in a populated dir.
"""
from pathlib import Path

p = Path(__file__).with_name('build_review_snapshot_v1.py')
source = p.read_text()
source = source.replace('八页的部分字段新增原像素外校', '十二页的部分字段新增原像素外校')
source = source.replace('只有八页的部分字段新增外校', '只有十二页的部分字段新增外校')
source = source.replace('parts of only eight pages', 'parts of only twelve pages')
anchor = "assert len(entries)==22\n"
assert source.count(anchor) == 1
addition = '''# Current evidence supplements the immutable 17:49 eight-page package.
supplements=[]
for name in ['C01_C02_C03_C06_postfreeze_native_addendum_v1.md',
             'C_remaining_native_crop_manifest_v1.json',
             'C_remaining_body_hashes_v1.json']:
    supplements.append(copy(BASE/'dhs_hispanico_sinicum/external_collation'/name,
        'companions/01_DHS_Hispanico_Sinicum/research/current12_addendum/'+name,
        'current_twelve_page_partial_collation_addendum'))
supplements.append(copy(BASE/'dhs_hispanico_sinicum/index_structure_acceptance_20261016T175230Z_v1.json',
    'companions/01_DHS_Hispanico_Sinicum/index/index_structure_acceptance_20261016T175230Z_v1.json',
    'DHS_static_index_structure_acceptance'))
entries[0]['companions'].extend(supplements)
entries[0]['current_partial_external_collation_page_count']=12
entries[0]['prior_1749_package_partial_external_collation_page_count']=8
entries[0]['index_structure']={'manuscript_image_pages':1102,'paratext_pages':38,
    'total_physical_pages':1140,'last_page_type':'dictionary entries and numeral table, not back cover',
    'unseen_internal_footer_page_numbers':[725,757,767],
    'warning':'Unseen footer numbers do not mean blank pages; legacy page_type aliases must be reconciled before filtering.'}

'''
source = source.replace(anchor, addition + anchor)
readme_anchor = '## 目录与正文优先级\n'
assert source.count(readme_anchor) == 1
readme_addendum = '''## 当前12页与原8页快照

原DHS小包delivery_package_v1的17:49快照写8页，数值在当时正确，本包保留原文，不覆盖历史。之后PDF051、070、080、293新增四页目标字段，当前累计12个DHS物理页部分字段外校／互参；仍不是12页全字段校定。新增报告在[后校增补](companions/01_DHS_Hispanico_Sinicum/research/current12_addendum/C01_C02_C03_C06_postfreeze_native_addendum_v1.md)，附目标原像素裁片manifest与首稿hash，裁片本身未装包。新后校读过论文答案，非盲测重跑；候选没有写回首稿。当前Skill v1保留原8页历史验证范围，须连同本新增报告阅读，不把12页默认为Skill全部重新验证。

静态索引复核为1102个手稿影像页＋38个副文本页＝1140。书内725／757／767三处是页脚未见，不能当成空白页。历史批次page_type同时有中文／英文别名，不能只筛一个dictionary值而漏算；源索引未改。PDF1140是词条与数表，非封底。见[索引验收](companions/01_DHS_Hispanico_Sinicum/index/index_structure_acceptance_20261016T175230Z_v1.json)。

'''
source = source.replace(readme_anchor, readme_addendum + readme_anchor)
source = source.replace("'source_count':22,'physical_page_positions':3139,'primary_body_files':22,", "'source_count':22,'physical_page_positions':3139,'primary_body_files':22,'DHS_current_partial_collation_page_count':12,")
exec(compile(source, str(p), 'exec'))
