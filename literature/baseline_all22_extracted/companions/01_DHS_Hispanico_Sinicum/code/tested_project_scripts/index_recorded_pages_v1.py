from pathlib import Path
import json,datetime,hashlib
b=Path(__file__).resolve().parent.parent
records={}
for p in sorted(b.glob('manifest_pdf_*_visual_first_v1.json')):
 d=json.loads(p.read_text())
 for e in d.get('entries',d.get('pages',[])):
  n=e.get('pdf_page')
  if n is not None and 'printed_page' in e:records[n]=dict(pdf_page=n,printed_page_label=e['printed_page'],page_number_basis=p.name+' per-page entry',page_type=e.get('page_type','manuscript_dictionary'),manifest=p.name)
 if 'printed_pages' in d:
  for n,v in zip(d['pdf_pages'],d['printed_pages']):records[n]=dict(pdf_page=n,printed_page_label=v,page_number_basis=p.name+' observed printed_pages list',page_type='manuscript_dictionary',manifest=p.name)
early=json.loads((b/'index_pdf_0011_0040_printed_pages_types_from_frozen_v1.json').read_text())
for r in early['records']:
 n=r['pdf_page'];records[n]=dict(pdf_page=n,printed_page_label=r['printed_page_label'],page_number_basis='index_pdf_0011_0040_printed_pages_types_from_frozen_v1.json; frozen transcript header, not new visual check',page_type=r['page_type'])
for n in range(1,11):
 labels={4:'i',5:'ii',6:'iii',7:'iv',8:'v',9:'vi',10:'vii'}
 records[n]=dict(pdf_page=n,printed_page_label=labels.get(n),page_number_basis='frozen transcript explicit printed-page sentence; no offset inference',page_type={1:'title_page',2:'funding_and_permissions',3:'contents'}.get(n,'modern_foreword'))
for n,t in {396:'part1_publication_imprint',397:'part2_cover',398:'part2_title',399:'funding_and_permissions',400:'contents',769:'part3_cover',770:'part3_title',771:'funding_and_permissions',772:'contents'}.items():records[n]['page_type']=t
records[1140]['page_type']='manuscript_dictionary_and_Contar_numeral_table'
correction='metadata_correction_reader_0011_0040_printed_page_reading_v1.json'
affected=set(n for a,z in [(601,620),(681,700),(781,800),(861,880),(941,960),(1021,1040),(1101,1120)] for n in range(a,z+1))
for n,r in records.items():
 p=b/f'transcripts/pdf_{n:04d}_visual_first_v1.md';r['transcript']=str(p.relative_to(b));r['transcript_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 if n in affected:r['metadata_correction']=correction;r['ignore_field']='batch printed_page_reading narrative; use per-page entry above'
 if n in [30,37]:r['observed_duplicate_pair']=[30,37]
 if n in [725,757,767]:r['page_number_note']='Footer unseen/unread; null preserved, never filled by arithmetic'
now=datetime.datetime.now(datetime.timezone.utc);d=dict(at=now.isoformat(),scope='Index of already recorded page labels and classifications, not fresh palaeographic verification. No fixed-offset interpolation. Batch narrative typo superseded by per-page entries and linked correction sidecar.',source_pdf_pages=1140,indexed_pages=len(records),missing_pages=sorted(set(range(1,1141))-set(records)),records=[records[n] for n in sorted(records)],observed_breakpoints=[dict(pdf_page=30,printed_page=1),dict(pdf_page=396,printed_page=None),dict(pdf_page=401,printed_page=367),dict(pdf_page=769,printed_page=None),dict(pdf_page=773,printed_page=735),dict(pdf_page=1140,printed_page=1102)])
p=b/('page_index_'+now.strftime('%Y%m%dT%H%M%SZ')+'_v1.json')
with p.open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(p);print('indexed',len(records),'missing',d['missing_pages'])
