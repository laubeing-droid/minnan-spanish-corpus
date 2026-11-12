from pathlib import Path
import json,re,hashlib,datetime
b=Path('/workspace/scratch/3ee2b91a8980/minnan_continuation/dhs_hispanico_sinicum')
pat=re.compile(r'^transcripts/pdf_(\d{4})_visual_first_v1\.md$')
rows=[]; manifest_summary=[]
def walk(x):
 if isinstance(x,dict):
  if 'transcript' in x and 'transcript_sha256' in x:yield x['transcript'],x['transcript_sha256']
  if 'path' in x and 'sha256' in x:yield x['path'],x['sha256']
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for p in sorted(b.glob('manifest_pdf_*_visual_first_v1.json')):
 d=json.loads(p.read_text()); refs={}
 for path,h in walk(d):
  m=pat.fullmatch(path)
  if m:refs[path]=h
 for path,h in refs.items():
  f=b/path; actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
  rows.append({'pdf_page':int(pat.fullmatch(path)[1]),'transcript':path,'manifest':p.name,'expected_sha256':h,'actual_sha256':actual,'sha256_matches':h==actual})
 manifest_summary.append({'manifest':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'body_md_reference_count':len(refs)})
verified=sorted({r['pdf_page'] for r in rows if r['sha256_matches']}); frozen={r['pdf_page'] for r in rows}
allmd={int(pat.fullmatch(str(p.relative_to(b)))[1]):p for p in (b/'transcripts').glob('pdf_*_visual_first_v1.md') if pat.fullmatch(str(p.relative_to(b)))}
def ranges(nums):
 out=[]
 for n in sorted(nums):
  if out and n==out[-1][1]+1:out[-1][1]=n
  else:out.append([n,n])
 return out
now=datetime.datetime.now(datetime.timezone.utc); stamp=now.strftime('%Y%m%dT%H%M%SZ')
result={'snapshot_at':now.isoformat(),'total_source_pdf_pages':1140,'scope':'Page body MD references recursively discovered across entries/transcript_sha256, artifacts, files and pages. Tone sidecars excluded. SHA match proves immutability, not transcription accuracy. Includes front matter and duplicated source leaves. Concurrent unfinished work may advance after snapshot.','manifest_count':len(manifest_summary),'frozen_unique_pdf_pages':len(frozen),'verified_unique_pdf_pages':len(verified),'verified_ranges':ranges(verified),'hash_mismatches_or_missing':[r for r in rows if not r['sha256_matches']],'duplicate_page_references':sorted(n for n in frozen if sum(r['pdf_page']==n for r in rows)>1),'unfrozen_draft_count':len(set(allmd)-frozen),'unfrozen_draft_pages':sorted(set(allmd)-frozen),'unfrozen_drafts':[{'pdf_page':n,'path':str(allmd[n].relative_to(b)),'sha256_at_snapshot':hashlib.sha256(allmd[n].read_bytes()).hexdigest()} for n in sorted(set(allmd)-frozen)],'manifests':manifest_summary,'verified_body_records':rows}
p=b/f'coverage_snapshot_{stamp}_v1.json'
with p.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(p);print(json.dumps({k:v for k,v in result.items() if k not in ['manifests','verified_body_records','unfrozen_drafts']},ensure_ascii=False))
