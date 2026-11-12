#!/usr/bin/env python3
"""Extract existing PDF scan bytes and make unscaled overlapping pixel crops. No OCR."""
from pathlib import Path
import argparse,fitz,json,hashlib,io
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('start',type=int);ap.add_argument('end',type=int);a=ap.parse_args()
b=Path(__file__).resolve().parent.parent;d=fitz.open(next((b/'source').glob('*.pdf')))
out=b/'native_images';out.mkdir(exist_ok=True)
for n in range(a.start,a.end+1):
 p=d[n-1];imgs=p.get_images(full=True)
 if len(imgs)!=1:raise RuntimeError(f'PDF {n} has {len(imgs)} images; inspect composition before extraction')
 x=imgs[0][0];info=d.extract_image(x);im=Image.open(io.BytesIO(info['image']));w,h=im.size
 raw=out/f'pdf_{n:04}_xref_{x}_native.{info["ext"]}'
 with raw.open('xb') as f:f.write(info['image'])
 files=[{'path':str(raw.relative_to(b)),'sha256':hashlib.sha256(info['image']).hexdigest()}]
 # Pixel crops only. Regions overlap, each <=1280x1100 to avoid ordinary view downsampling.
 step_x=1100;step_y=950
 for yy,y in enumerate(range(0,h,step_y)):
  for xx,xx0 in enumerate(range(0,w,step_x)):
   box=(xx0,y,min(w,xx0+1280),min(h,y+1100));dest=out/f'pdf_{n:04}_native_y{yy}_x{xx}.png'
   with dest.open('xb') as f:im.crop(box).save(f,format='PNG')
   files.append({'path':str(dest.relative_to(b)),'pixel_box':box,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
 m={'pdf_page':n,'xref':x,'native_size':[w,h],'page_rect_points':list(p.rect),'image_rects_points':[list(r) for r in p.get_image_rects(x)],'method':'Existing embedded image bytes; crops preserve original pixels, no resize/enhancement/OCR. Verify image placement visually.','files':files}
 with (out/f'pdf_{n:04}_native_manifest_v1.json').open('x') as f:json.dump(m,f,ensure_ascii=False,indent=2)
 print(n,w,h,x,flush=True)
