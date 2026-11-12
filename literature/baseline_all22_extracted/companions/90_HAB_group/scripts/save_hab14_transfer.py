from pathlib import Path
import hashlib,json
b=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_91_2_extrav_14');o=b/'method_transfer_v3';o.mkdir(exist_ok=True)
for d in ['text','review']:(o/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,t):p.open('x').write(t)
notes={1:'现代许可首面实看。',2:'现代许可续面实看，与古稿正文分离。',3:'单叶十列草写，整叶淡墨及左缘破损。词串无可靠连续释读，保留已有逐字候选；不以音韵主题补齐。',4:'刻本二十列含短标题和段尾。首列診三、吐/虛首字与輩等细笔仍未清；旧补记已有疑号现纳入正文，非新证实改字。',5:'右刻本二十列、左淡镜背。手經、叫胃氣等不依医书通句校成顺文；旧补记疑位入正文。旁注可见字补入定位，其他仍缺。',6:'灰色单叶无正文，不能以纸纤维和色差拟字。',7:'外封左曲面书脊小字、下签仍不全，系带非字；不据架号补。',8:'内封左上残倒签与胶痕分层，数字不能全定。',9:'内封上部铅笔号及倒签可见但未细定，仍原疑；不由其他分册补全。',10:'外封左斑密集、中央纵纹右四缝结，无正文。'}
changes={4:[('診三經','［診?］［三?］經'),('按靈樞','［按?］靈樞'),('吐舌出口齧齒咬人','［虛／吐?］舌出口［齧?］齒咬人'),('脈氣輩至','脈氣［輩?］至'),('齧頰','齧［頰?］'),('齧唇','齧［唇?］'),('魚口氣急','［魚?］口氣急'),('蛔虫','［蛔?］虫')],5:[('疾診尺','［疾?］診尺'),('顖','［顖?］'),('抑熱','［抑?］熱'),('于額','于［額?］'),('過睛','過［睛?］'),('經手經','經［手?］經'),('自腋','自［腋?］'),('大叫胃氣挾痰','大［叫?］胃氣［挾?］［痰?］'),('直視觀','直視［觀?］')]}
cov=[];maps=[];merge=['# HAB14 方法迁移正文\n\n〔部分识读；未全文核定。〕\n']
for n in range(1,11):
 src=b/f'page-{n:02}.md';im=b/f'page-{n:02}.png';lines=src.read_text().splitlines();out=[f'# HAB14 · PDF {n:03}'];mp=[];active=False
 if n<=2:out+=['〔现代使用说明页；无古稿正文。〕']
 for i,l in enumerate(lines,1):
  if l=='## 实录':active=True;target=None
  elif l=='## 校记':active=False;target=None
  elif active and n>2:
   z=l
   for a,v in changes.get(n,[]):z=z.replace(a,v)
   out.append(z);target=len(out)
  else:target=None
  mp.append({'source_line':i,'source_text':l,'body_line':target,'new_text':out[-1] if target else None,'disposition':'body' if target else 'editorial_or_modern'})
 if n==5:out+=['〔C01旁注〕經筋篇謂太〔未辨〕陽為目上綱','〔C02旁注〕經筋篇謂陽〔未辨〕明為目下綱']
 t='\n'.join(out)+'\n';tp=o/'text'/f'pdf_{n:03}_v3.md';put(tp,t);merge.append(t)
 r={'pdf_page':n,'source':str(src),'source_sha256':sha(src),'image':str(im),'image_sha256':sha(im),'body':str(tp),'body_sha256':sha(tp),'visually_reviewed':True,'full_text_verified':False,'finding':notes[n],'changes':changes.get(n,[])}
 cov.append(r);maps.append({**r,'source_lines':mp});put(o/'review'/f'pdf_{n:03}_v3.md',f'# PDF {n:03}\n\n{notes[n]}\n\n非盲二校。改变详见映射；本册目前原图仅1024像素级正文，低分辨率限制尚在。\n')
put(o/'HAB14_all10_body_v3.md','\n'.join(merge));put(o/'coverage_all10_v3.json',json.dumps(cov,ensure_ascii=False,indent=2));put(o/'source_line_mapping_all10_v3.json',json.dumps(maps,ensure_ascii=False,indent=2))
put(o/'prior_addendum_mapping_v3.json',json.dumps({'source':str(b/'doubt-addendum.md'),'sha256':sha(b/'doubt-addendum.md'),'source_lines':[{'line':i,'text':l,'disposition':'prior_uncertainty_adopted_on_PDF004_005_or_editorial'} for i,l in enumerate((b/'doubt-addendum.md').read_text().splitlines(),1)]},ensure_ascii=False,indent=2))
assert all(sha(Path(r['source']))==r['source_sha256'] for r in cov)
put(o/'FINAL_DELIVERY_v3.md','# HAB14 方法迁移复核\n\n10/10原图实际查看，部分正文层、逐页实核、全旧物理行映射同目录。004/005旧补记疑号纳入正文，不能计作本轮新确定纠错；005两旁注从旧校记回归定位正文。003草写与004/005细字仍多未能读清。现有低分辨率原稿图未被放大充作新高清证据。全书核定为false。\n')
print('14',sum(len(m['source_lines']) for m in maps))
