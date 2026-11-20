#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 y 区间从整页 300dpi 原图裁行放大（只读源图，输出到 scratch）。

用法: python literature/tools/zoom_rows.py 283 M 340 580 460 700 ...
即 page、栏(M/R/H 对应 subcol3/4/2)、之后每两个数一个裁剪区间 y0 y1。
输出 _scratch_zcode_strips/zoom_pXXXX_<col>_<y0>.png（2x 放大）。
"""
import sys
from pathlib import Path
from PIL import Image

TILES = Path("literature/tiles/01_DHS")
OUT = Path("_scratch_zcode_strips")
COL = {"M": "subcol3_minnan", "R": "subcol4_mandarin_right", "H": "subcol2_hanzi_full"}
SCALE = 2


def main():
    pg, col, *rest = sys.argv[1:]
    pk = f"{int(pg):04d}"
    im = Image.open(TILES / f"page_{pk}" / f"pdf_{pk}_{COL[col]}.png")
    pairs = [(int(rest[i]), int(rest[i + 1])) for i in range(0, len(rest) - 1, 2)]
    OUT.mkdir(exist_ok=True)
    for y0, y1 in pairs:
        crop = im.crop((0, max(0, y0), im.width, min(im.height, y1)))
        crop = crop.resize((crop.width * SCALE, crop.height * SCALE), Image.LANCZOS)
        out = OUT / f"zoom_p{pk}_{col}_{y0}.png"
        crop.save(out)
        print(f"{out} y=[{y0},{y1}) 尺寸={crop.size}")


if __name__ == "__main__":
    main()
