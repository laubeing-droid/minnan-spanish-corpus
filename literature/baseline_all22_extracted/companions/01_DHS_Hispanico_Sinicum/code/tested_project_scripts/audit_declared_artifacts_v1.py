from pathlib import Path
import json,hashlib,datetime
b=Path(__file__).resolve().parent.parent
refs={}; conflicts=[]
def walk(x):
 if isinstance(x,dict):
  for pk,hk in [('path','sha256'),('transcript','transcript_sha256'),('image','image_sha256')]:
   if pk in x and hk in x and isinstance(x[pk],str):yield x[pk],x[hk]
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
manifests=list(sorted(b.glob('manifest_pdf_*_visual_first_v1.json')))
for p in manifests:
 for path,h in walk(json.loads(p.read_text())):
  if path in refs and refs[path]!=h:conflicts.append(dict(path=path,previous=refs[path],new=h))
  refs[path]=h
bad=[];total=0
for path,h in refs.items():
 p=b/path
 if not p.is_file():bad.append(dict(path=path,error='missing'));continue
 a=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):a.update(chunk);total+=len(chunk)
 if a.hexdigest()!=h:bad.append(dict(path=path,expected=h,actual=a.hexdigest()))
now=datetime.datetime.now(datetime.timezone.utc)
d=dict(at=now.isoformat(),scope='All declared path/sha256, transcript and image references recursively found in batch manifests at process start; excludes unreferenced files. No transcription-accuracy inference.',manifest_count=len(manifests),unique_file_count=len(refs),bytes_hashed=total,conflicts=conflicts,mismatches_or_missing=bad,files=refs)
p=b/('all_declared_artifacts_audit_'+now.strftime('%Y%m%dT%H%M%SZ')+'_v1.json')
with p.open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(p);print({k:v for k,v in d.items() if k!='files'})
