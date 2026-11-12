from pathlib import Path
import json,hashlib,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s):
 with p.open('x') as f:f.write(s)
def save(part,notes,changes={}):
 b=Path('/workspace/shared/minnan_transcription')/f'hab_91_2_extrav_{part:02}'
 o=b/'method_transfer_v3';o.mkdir(exist_ok=True)
 for d in ['text','review']:(o/d).mkdir(exist_ok=True)
 cov=[];maps=[];merged=[f'# HAB 91.2 Extrav {part} 方法迁移复核\n\n〔保留疑读，未全文核定。〕\n']
 for n,note in notes.items():
  candidates=[b/d/f'pdf_{n:03}.md' for d in ['visual_v2','visual_v1','page_records','blind_v1']]
  src=next((p for p in candidates if p.exists()),None)
  if src is None:raise RuntimeError(candidates)
  image=Path('/workspace/shared/minnan_reference_catalog')/f'hab{part:02}_official_max'/f'{n-2:05}.jpg' if n>2 else b/'blind_v1'/f'pdf-{n:02}.png'
  if not image.exists():image=b/'page_records'/f'pdf_{n:03}.png'
  lines=src.read_text().splitlines();out=[f'# HAB {part:02} · PDF {n:03}'];mapping=[];active=False
  if n<=2:out.append('〔现代馆方使用说明页；无古稿正文。〕')
  for i,line in enumerate(lines,1):
   if line.startswith('## '):active=not any(k in line for k in ['来源','方法','摄影','限制','不确定','标签注意'])
   target=None;new=line
   if active and n>2:
    for a,z in changes.get(n,[]):new=new.replace(a,z)
    out.append(new);target=len(out)
   mapping.append({'source_line':i,'source_text':line,'body_line':target,'new_text':new if target else None,'disposition':'body' if target else 'editorial_or_modern_in_source'})
  text='\n'.join(out)+'\n';tp=o/'text'/f'pdf_{n:03}_v3.md';put(tp,text);merged.append(text)
  record={'pdf_page':n,'source':str(src),'source_sha256':sha(src),'image':str(image),'image_sha256':sha(image) if image.exists() else None,'body':str(tp),'body_sha256':sha(tp),'visually_reviewed':True,'full_text_verified':False,'finding':note,'changes':changes.get(n,[])}
  cov.append(record);maps.append({**record,'source_lines':mapping})
  put(o/'review'/f'pdf_{n:03}_v3.md',f'# PDF {n:03} 逐页实核\n\n{note}\n\n旧读→新候选：{changes.get(n,[])}\n\n本次读取原图及旧稿，属于非盲二校。正文古字、数序及疑读保留。图与旧稿路径、哈希和全源行映射见本目录合并JSON。哈希不代表内容准确。\n')
 put(o/f'HAB{part:02}_all{len(notes)}_body_v3.md','\n'.join(merged))
 put(o/f'coverage_all{len(notes)}_v3.json',json.dumps(cov,ensure_ascii=False,indent=2))
 put(o/f'source_line_mapping_all{len(notes)}_v3.json',json.dumps(maps,ensure_ascii=False,indent=2))
 assert all(sha(Path(c['source']))==c['source_sha256'] for c in cov)
 put(o/'FINAL_DELIVERY_v3.md',f'# HAB {part:02} 方法迁移复核\n\n{len(notes)}/{len(notes)}页实际查图并对照旧稿，逐页发现见review。所有源稿保持不变。全文核定标记仍为false。\n\n正文、覆盖及全源物理行映射均在本目录；摄影标识、现代使用说明及方法说明独立在原稿和映射，不混古正文。\n\n{len(changes)}页含新的候选调整，非准确率或确定错误数。草写汉字音写、账目字、圈销与边注不套DHS罗马字调号规则；不能按数值加总或现代词义补字。\n')
 print(part,len(notes),sum(len(m['source_lines']) for m in maps))
if __name__=='__main__':
 notes={1:'现代德文使用说明页；CC许可图与脚注属于馆方层。',2:'现代说明续页，结尾2013-03-01；不当古稿纪年。',3:'覆纸主体无正文，右缘残字仍只有候选；不据露出的窄边补题名。',4:'实际看整图及180度右叶；九带词组与小字关系保留，粗黑涂条下不恢复，末带肉/于尼仍按字形。',5:'实际看顺时针90度两叶；账目数字和斤形不据总数重排。D07迫形增加進候选，字末仍疑。',6:'贴条三行拉丁文与底下草写属不同层；manû上标不当闽南调号。左缘旋转核李頁增貝候选，末字不是确定戈。',7:'右上4与褐纸翻背保留；左缘八行不是正文新页连续八句。頁/貝本页原候选保留。',8:'右上5及空叶实核；孔洞和褐点无文字。',9:'右上6闭合小环实核，不因相邻号补读。',10:'右上带横7；纸褶、孔洞不增字。',11:'右叶淡字样痕实际存在，未能可靠读；不能并入纯空白页。',12:'左右叶旋转局部核对；左字组与右账列是不同布局，右十一月廿七日与数序照留。',13:'两叶旋转核对；右十字销线跨列，左多处连写不强分人名。R10七百五十七仍按原数字记录。',14:'左大弧形销线越过多列，不删掉其下可见字；右糖五四保留未改五十四。',15:'左竖销与侧加字层分离；右又欠酒四十斤形可定位，左大量草字仍不能确读。',16:'右R10四百后字有六状笔而旧作八，增六候选；前后总数不作裁决。左一埕/斤形不混同。',17:'右十二月初二与白布二十八疋可核；R11分分仍保留，左鹽分一五文不据金额改十五。',18:'左八长列原向阅读，与前几页横置方向不同；两组横倒侧字仍不可读，右页15及空叶独立。',19:'棕色外覆纸；左窄边残痕不足以转写题名，右黑摄影背景无正文。',20:'封装书脊曲面隐藏文字未补；本地00018对应eb01不是手稿页18。',21:'封装内面左上倒纸签91可定位，其后出框；补纸损痕非字。',22:'封装内面上部Extravag. 91,2及右上倒签保留缩写，源标签不替代实际页面身份。',23:'封装外面、系带及斑痕实核；无可确认正文，不把污点拼字。'}
 save(1,notes,{5:[('〔一字似迫，疑〕','〔一字似迫／進，疑〕')],6:[('李頁〔疑字，黑重〕','李〔頁／貝；疑字，黑重〕')],16:[('共四百八十五〔斤形〕','共四百〔八／六？〕十五〔斤形〕')]})
