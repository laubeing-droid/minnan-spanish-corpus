#!/usr/bin/env python3
"""Render source pages only; no OCR or text extraction; never overwrite a file."""
from pathlib import Path
import argparse, fitz
p=argparse.ArgumentParser();p.add_argument('start',type=int);p.add_argument('end',type=int);p.add_argument('--columns',action='store_true');a=p.parse_args()
b=Path(__file__).resolve().parent.parent
source=next((b/'source').glob('*.pdf'))
d=fitz.open(source)
for n in range(a.start,a.end+1):
 page=d[n-1];r=page.rect
 dest=b/'images'/f'pdf_{n:04}.png'
 with dest.open('xb') as f:f.write(page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).tobytes('png'))
 if a.columns:
  for tag,clip in [('left',fitz.Rect(25,25,r.width/2+15,r.height-25)),('right',fitz.Rect(r.width/2-15,25,r.width-15,r.height-25))]:
   with (b/'images'/f'pdf_{n:04}_crop_{tag}_v1.png').open('xb') as f:f.write(page.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip).tobytes('png'))
print(f'Rendered PDF pages {a.start}–{a.end}; total source pages {len(d)}')
