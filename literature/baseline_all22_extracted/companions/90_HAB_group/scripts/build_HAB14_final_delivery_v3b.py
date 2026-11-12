from pathlib import Path
import json,hashlib
base=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation');shared=Path('/workspace/shared/minnan_transcription');out=base/'hab_all14_method_transfer_summary_v3'
counts=[23,34,20,11,43,45,24,17,12,14,12,28,168,10]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s):p.open('x').write(s)
parts=[];pages=[];merged=['# HAB 菲律宾唐人手稿 · 14分册461页方法迁移候选正文\n\n〔分册保持文件次序，各页PDF号独立；同书归组不证明原卷叶序无缺。疑读及未辨保留，非全文核定本。〕\n']
for n,count in enumerate(counts,1):
 b=(shared if n<13 else base)/f'hab_91_2_extrav_{n:02}'/'method_transfer_v3'
 r=b/'release' if n in [5,6,13] else b
 body=next(r.glob(f'HAB{n:02}_all{count}_body*.md'))
 if n in [5,6,13]:maps=[json.loads(p.read_text()) for p in sorted((r/'final_mapping').glob('*json'))]
 else:maps=json.loads(next(r.glob('source_line_mapping_all*_v3.json')).read_text())
 assert len(maps)==count,(n,len(maps),count)
 pc=[]
 for j in maps:
  pg=j.get('page',j.get('pdf_page'));ls=j.get('lines',j.get('source_lines'));src=Path(j.get('old',j.get('source')));srcsha=j.get('old_sha256',j.get('source_sha256'))
  tp=Path(j.get('body',str(r/'final_text'/f'pdf_{pg:03}.md')));th=j.get('final_text_sha256',j.get('body_sha256'))
  assert sha(src)==srcsha,(n,pg,'source');assert sha(tp)==th,(n,pg,'body');assert sha(Path(j['image']))==j['image_sha256'],(n,pg,'image')
  assert [l.get('old_line',l.get('source_line')) for l in ls]==list(range(1,len(src.read_text().splitlines())+1)),(n,pg,'mapping')
  rec={'part':n,'pdf_page':pg,'image':j['image'],'image_sha256':j['image_sha256'],'source':str(src),'source_sha256':srcsha,'body':str(tp),'body_sha256':th,'visually_reviewed':j.get('visual_review',j.get('visually_reviewed')),'full_text_verified':False,'physical_source_lines':len(ls),'finding':j.get('observation',j.get('finding')),'changes':j['changes']}
  assert rec['visually_reviewed'] is True
  pc.append(rec);pages.append(rec)
 merged.extend([f'\n# 分册 {n:02}\n',body.read_text()]);parts.append({'part':n,'pages':count,'body':str(body),'body_sha256':sha(body),'companion_directory':str(r),'physical_source_lines':sum(p['physical_source_lines'] for p in pc),'changes_page_count':sum(bool(p['changes']) for p in pc)})
assert len(pages)==461
put(out/'HAB_all14_461pages_body_v3.md','\n'.join(merged))
cover={'source_files':14,'pages_visually_reviewed':461,'missing_pages':[],'full_text_verified':False,'physical_source_lines':sum(p['physical_source_lines'] for p in pages),'all_source_body_image_hashes_and_mapping_sequences_pass':True,'parts':parts,'pages':pages,'hashes_do_not_imply_accuracy':True}
put(out/'coverage_HAB_all14_461pages_v3.json',json.dumps(cover,ensure_ascii=False,indent=2))
report=['# HAB 全14分册方法迁移交付\n\n461/461页实际看图，保存各页观察与旧读→新候选。正文仍是部分识读候选，不是全文校定。各分册馆藏、透背、空白、封装的记录也占覆盖页数，不能换算识字准确率。\n','## 正文与定位\n\n合并正文：HAB_all14_461pages_body_v3.md。分册维持01–14文件次序、PDF页定位；源文件之间可能包含重复装帧图和跨分册叶序，未静默去重或重排。\n\n覆盖：coverage_HAB_all14_461pages_v3.json，含每页图、源稿、最终正文hash与完整分册映射入口。所有源稿与原图未变。HAB13最终正文逐行准确字符串补映射见 HAB13_exact_final_body_line_mapping_supplement_v3.json。\n','## 有据改进与未解决\n\n- 02/028 L09廿六担→十二担、03/004 R01六分→二分、04/006 R09余目→余日、06/014金额三→二、07/006 L04b一千五→一十五、12/021 R07旧主读舊→貧，系本轮可见笔画支持。仍不宣称全页其余文字正确。\n- 01三处、05/038六→八疑、09/006肯→肯／肖疑、13九处等均只是候选；13另两处七栏→八栏为版面修正，08补154/155为页号。不得合并当确定错字数。\n- 10、11未找到可确定新改字，保持疑读本身就是本轮结果。\n- 12镜反层与正面词书分别保存，不能把透背当第二份正文。14/004–005旧疑号进入新正文，005旧校记两旁注回归定位，不计新发现字符。\n- 账目销线下、草写汉字音写、细小边注、破边截字仍大量未能读清。14正文图1024像素级限制尚未克服。\n','## 失败与迁移边界\n\n数目加总、熟悉词义及新旧/亲属成对结构可提示候选，不能代替笔画。账页的圈、销线、单位记号与DHS罗马调号无直接映射。字形看似漢字也可能音写西语，不擅改成现代汉语顺文。医学刻页不按通行医书倒填。\n\nHAB13验收第一版误将旧提取层hash对最终层，随后按final_text_sha256重验全部通过；过程文件保留，不掩去失败。保存脚本只记录人工已看原图之后的决定，不能充作图像识读程序。\n\nAgentSkill暂仅材料清单 skill_packaging_materials_PROVISIONAL_v1.md，不最终封装；DHS主稿进度须由主协调确认。\n','## 分册入口\n']
for p in parts:report.append(f"- {p['part']:02}: {p['pages']}页，{p['companion_directory']}\n")
put(out/'FINAL_DELIVERY_HAB_all14_v3.md','\n'.join(report))
print(json.dumps({'pages':461,'physical_lines':cover['physical_source_lines'],'merged_sha256':sha(out/'HAB_all14_461pages_body_v3.md')},ensure_ascii=False))
