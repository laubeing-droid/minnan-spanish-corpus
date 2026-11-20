#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一页的汉字/闽南/官话三栏裁片按高度切成拼条（只读源图，输出到 scratch）。

用法: python literature/tools/make_page_strips.py 283 [284 ...]
每页输出若干条 _scratch_zcode_strips/pXXXX_stripY.png：
三栏横向拼接（原 300dpi 原生分辨率，条高默认 1050px、重叠 150px），
便于读图时跨栏对齐行锚。
"""
import sys
from pathlib import Path
from PIL import Image

TILES = Path("literature/tiles/01_DHS")
OUT = Path("_scratch_zcode_strips")
COLS = ("subcol2_hanzi_full", "subcol3_minnan", "subcol4_mandarin_right")
STRIP_H, OVERLAP = 1050, 150


def main(pages):
    OUT.mkdir(exist_ok=True)
    for pg in pages:
        pk = f"{pg:04d}"
        imgs = []
        for s in COLS:
            p = TILES / f"page_{pk}" / f"pdf_{pk}_{s}.png"
            if not p.exists():
                raise SystemExit(f"缺裁片: {p}")
            imgs.append(Image.open(p))
        height = min(im.height for im in imgs)
        y, n = 0, 0
        while y < height:
            box = (0, y, 0, min(y + STRIP_H, height))
            pieces = [im.crop((0, box[1], im.width, box[3])) for im in imgs]
            total_w = sum(p.width for p in pieces) + 8 * (len(pieces) - 1)
            canvas = Image.new("RGB", (total_w, pieces[0].height), (255, 255, 255))
            x = 0
            for p in pieces:
                canvas.paste(p, (x, 0))
                x += p.width + 8
            n += 1
            out = OUT / f"p{pk}_strip{n}.png"
            canvas.save(out)
            print(f"{out}  y=[{y},{box[3]}) 尺寸={canvas.size}")
            if box[3] >= height:
                break
            y += STRIP_H - OVERLAP


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
