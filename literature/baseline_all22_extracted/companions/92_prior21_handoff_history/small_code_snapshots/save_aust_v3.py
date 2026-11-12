from pathlib import Path
import hashlib,json,re
b=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation/aust_tomo211_fragments'); o=b/'method_transfer_v3';o.mkdir(exist_ok=True)
for d in ['text','review']: (o/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):
 with p.open('x') as f:f.write(s)
notes={1:'分类题签而非手稿正文；ROLL 113末笔仍不强定。馆藏水印从正文分离。',2:'左右叶行骨架与图对应；顶部墨污、下半长曲线不当调号。低清细字仍未读，不能按祷文补齐。',3:'教会诫命、圣事等分段标题与右叶14数码可定位；反复lang字形不能代替每行识读。',4:'左叶Primero/Segundo与右叶Tercero/Quarto分段；右上6、7是延续编号，不因PDF相邻调整原顺序。',5:'右上12–17与下部新题分段保留；下部多行长条目不并成单行。中缝墨损未补。',6:'左右叶均为密集罗马字；左中内缩题与右上浓黑横笔分别记录，黑笔覆盖字未恢复。低清仍不能逐行转全。',7:'逐行对照整页及右上/右中局部。208据原图；R08–09 Salimos/entierra跨行，R12–14拉丁祷式不按熟悉文本校正；右上n状附标与声调笔分开保留。',8:'左叶Diminutivo及下部forma plural可定位；旧Delgentivo疑读新增Despectivo候选，仍未裁定。上下长笔相交不可一概当调号。',9:'逐行对照及右下局部。Estando/Estando para/Forte大题分段；原行23接词es bien独立；R13复合附标不能只按现代重音理解。',10:'Vide or及下半拉丁引文题行重新看局部；S后的上标仍不展开。Serm.后更像11，保留候选。下部正文不按常见奥古斯丁引文补全。'}
changes={8:[('⟦… Delgentivo? …⟧','⟦… Delgentivo／Despectivo? …⟧')],10:[('⟦11…?⟧','⟦11?⟧')]}
coverage=[];mapping=[];merged=['# AUST Tomo 211：10幅公开残页，方法迁移复核 v3\n\n〔仅部分识读；不代表全书；正文未全文核定。〕\n']
baseline={str(p):sha(p) for p in b.rglob('*.md') if o not in p.parents}
for n in range(1,11):
 p=b/'visual_v1'/f'pdf_{n:03}.md'; src=p.read_text();lines=src.splitlines(); out=[f'# PDF {n:03}\n']; dest={}; active=False
 for i,line in enumerate(lines,1):
  if line.startswith('## '): active=any(x in line for x in ['左叶','右叶'])
  if active:
   updated=line
   for a,z in changes.get(n,[]):updated=updated.replace(a,z)
   out.append(updated);dest[i]=len(out)
 body='\n'.join(out)+'\n';tp=o/'text'/f'pdf_{n:03}_v3.md';write(tp,body);merged.append(body)
 mp=[]
 for i,line in enumerate(lines,1):mp.append({'source_line':i,'source_text':line,'destination_line':dest.get(i),'disposition':'body_retained_or_candidate' if i in dest else 'editorial_metadata_in_source_and_review'})
 mapping.append({'pdf_page':n,'source':str(p),'source_sha256':sha(p),'body':str(tp),'body_sha256':sha(tp),'lines':mp})
 review=f'# PDF {n:03} 方法迁移复核\n\n{notes[n]}\n\n图像实核：images/pdf_{n:03}_render.png。001–005前段已查看，006–010本段查看；007/009/010另看既有局部，008另看左叶。\n\n新增候选：{changes.get(n,[])}\n\n未能完成：音写细字、附标及遮损仍按原稿疑读；本页不标全文核定。非盲测。\n'
 write(o/'review'/f'pdf_{n:03}_review.md',review)
 coverage.append({'pdf_page':n,'image':str(b/'images'/f'pdf_{n:03}_render.png'),'image_sha256':sha(b/'images'/f'pdf_{n:03}_render.png'),'visually_reviewed':True,'full_text_verified':False,'status':'classification_label' if n==1 else 'partial_transcription_with_unread_body','finding':notes[n],'changes':changes.get(n,[])})
write(o/'AUST_all10_partial_body_v3.md','\n'.join(merged))
for name,obj in [('coverage_all10_v3.json',coverage),('source_line_mapping_all10_v3.json',mapping),('prior_text_hash_baseline_v3.json',baseline)]:write(o/name,json.dumps(obj,ensure_ascii=False,indent=2))
assert all(sha(Path(p))==h for p,h in baseline.items())
write(o/'FINAL_DELIVERY_v3.md','# AUST 10幅公开残页方法迁移复核\n\n10/10原图实际查看；1分类题签，9手稿双叶。完整正文识读仍为0页，全文核定0页。007、009有较多逐行部分识读，其余多为定位及片段；不能把10/10覆盖称全书转写完成。\n\n正文：AUST_all10_partial_body_v3.md。逐页正文text/；逐页实核review/；覆盖coverage_all10_v3.json；源物理行映射source_line_mapping_all10_v3.json。\n\n实际增补仅008术语Despectivo疑读候选、010引文题号11候选，均非确定改错。馆藏现代水印和旧工作说明从正文抽离保存在源稿与报告映射。\n\n失败经验：低分辨率放大并未恢复细节；语义/熟悉祷文或拉丁引文不能替代笔画；复合上标尚不能逐一分解编码。DHS调号编码不能直接套本稿，不能据标题Catecismo认定图内全是教理。本轮读取旧稿，不是盲测。所有既有MD哈希保持不变。\n')
print(len(mapping),sum(len(x['lines']) for x in mapping),sha(o/'AUST_all10_partial_body_v3.md'))
