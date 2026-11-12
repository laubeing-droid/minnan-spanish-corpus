from pathlib import Path
import json,hashlib,re,datetime,shutil
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
ROOT=BASE.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def write_json(name,obj):
    with (OUT/name).open('x',encoding='utf8') as f: json.dump(obj,f,ensure_ascii=False,indent=2)
records=[]
for f in sorted(BASE.glob('freeze*.json')):
    if not re.fullmatch(r'freeze_(?:pdf)?\d{3}_\d{3}\.json',f.name): continue
    data=json.loads(f.read_text()); rows=data if isinstance(data,list) else data['pages']
    for row in rows:
        n=row['pdf_page']; p=Path(row.get('transcription',str(BASE/row.get('file',''))))
        b=p.read_bytes(); assert sha(b)==row['sha256'], (n,'freeze mismatch')
        records.append((n,p,b,row,f))
records.sort(key=lambda r:r[0]); assert [r[0] for r in records]==list(range(1,170))
assert len({r[1] for r in records})==169
images=json.loads((ROOT/'blind_calibration_20261016_v1/DSH_Angelica_all169_images_only_v2.json').read_text())['pages']
images={r['pdf_page']:r['image'] for r in images}
merged=bytearray(); mapping=[]
for n,p,b,old,freeze in records:
    if merged: merged.extend(b'\n\n')
    start=len(merged); line_start=merged.count(b'\n')+1
    merged.extend(b)
    image=Path(images[n]); imagehash=sha(image.read_bytes())
    if old.get('source_sha256'): assert imagehash==old['source_sha256'], (n,'image mismatch')
    mapping.append({'pdf_page':n,'source_md':str(p),'source_sha256':sha(b),'freeze_file':str(freeze),'freeze_sha256':sha(freeze.read_bytes()),'matches_frozen_sha256':True,'image':str(image),'image_sha256_current':imagehash,'image_hash_matches_freeze':True if old.get('source_sha256') else None,'merged_byte_start_inclusive':start,'merged_byte_end_exclusive':len(merged),'merged_line_start_1based':line_start,'merged_source_line_count':len(b.splitlines()),'body_bytes_preserved':True})
body=OUT/'Angelica_Ms60_all169_method_independent_v3.md'
with body.open('xb') as f:f.write(merged)
check=body.read_bytes()
for r in mapping:
    p=Path(r['source_md']); assert sha(p.read_bytes())==r['source_sha256']
    assert check[r['merged_byte_start_inclusive']:r['merged_byte_end_exclusive']]==p.read_bytes()
inv=json.loads((ROOT/'handoff_21sources_20261016_v1/completed21_sources_handoff_inventory_v1.json').read_text())
entry=next(x for x in inv['entries'] if 'angelica_method_independent_v3' in str(x['body_files']))
pdf=Path(entry['source_pdf'])
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation':'Byte-preserving concatenation in PDF order; separator only two LF bytes between files','body_file':str(body),'body_sha256':sha(check),'source_pdf':str(pdf),'source_pdf_sha256_current':sha(pdf.read_bytes()),'page_count':169,'missing_pages':[],'duplicate_pages':[],'all169_match_prior_freeze':True,'all169_embedded_byte_segments_match_source':True,'old_files_unchanged':True,'full_text_verified':False,'image_hash_note':'1–85 compare recorded freeze source hashes;86–169 current image hashes only, no prior image-hash assertion','disk_free_bytes':shutil.disk_usage(OUT).free,'pages':mapping}
write_json('coverage_and_source_mapping_all169_v1.json',report)
print(json.dumps({k:v for k,v in report.items() if k!='pages'},ensure_ascii=False,indent=2))
