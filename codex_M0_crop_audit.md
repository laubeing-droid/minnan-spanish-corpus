# M0 B 裁片截断核查（仅几何）

2026-11-18。只核对图像尺寸、几何映射与可见笔画边界；未读取既有转写或判卷答案，未改原图、判卷标准或任何数据。

| 原图/裁片 | 像素尺寸 | SHA-256 |
| --- | --- | --- |
| `_scratch_p0257/calib_p0257_mcol_y1.png` | 960 × 2434 | `d2944f17f3b345526b7c0a443cdf750de44838b81c40277ac1a8832993eb64d6` |
| `literature/tiles/01_DHS/page_0257/pdf_0257_band_y1_mid.png` | 2041 × 1217 | `8c3a125273d76a80302ab2d104f4a1574d760bc637094c981b6404bb7babfed1` |
| 同页 300 dpi 整页 | 2171 × 3380 | `2c8aadba48f527a07ebdbc4c53ac0cf5985a16db707047bd2b314357eb11f3cf` |

B 裁片与中横带的 `[950, 0, 1430, 1217]` 像素框经 Pillow LANCZOS 放大 2 倍所得图像 **逐像素相同**；框采用左上含、右下不含的 `(x1, y1, x2, y2)`。中横带的宽度为 2041，故其右边界 x=1430 是裁片边界，并非原横带边界。依原图清册，中横带从整页 `(x=43, y=1081)` 开始，该裁片对应整页 `[993, 1081, 1473, 2298]`。

## 第六视觉行右边缘

交接口径所称 B 第六视觉行的连写末段横跨裁片右边界。对中横带 `[1100, 800, 1530, 1010]` 原像素检查，行内下延连笔及其上方记号越过 x=1430，右侧约 x=1430–1455 仍有同一行的墨迹；原裁片最后一个可见横向源像素是 x=1429。中横带框 `[1430, 835, 1460, 900]` 中有 57 个灰度低于 150 的像素，可重复确认裁片外存在较深笔画；这是像素量化，不自动区分每一笔的字母或功能。

因此，**仅凭该 B 裁片不能完整看见这一行的末段**。原横带提供了裁片右侧的上下文，但增加横带范围会改变原试卷可见内容；不能在不披露此差异的情况下把扩大裁片的成绩当作原裁片盲测成绩，也不能只凭图像边缘外推字母。该观察不判定具体字母、音系、真值或整体分数；正式题数、真值和门槛仍按已有争议记录处理。

## 可复验命令（只读）

```powershell
@'
from pathlib import Path
from PIL import Image
import hashlib
import numpy as np

crop = Path('_scratch_p0257/calib_p0257_mcol_y1.png')
band = Path('literature/tiles/01_DHS/page_0257/pdf_0257_band_y1_mid.png')
a = Image.open(crop).convert('RGB')
b = Image.open(band).convert('RGB')
r = b.crop((950, 0, 1430, 1217)).resize((960, 2434), Image.Resampling.LANCZOS)
print('crop', a.size, hashlib.sha256(crop.read_bytes()).hexdigest())
print('band', b.size, hashlib.sha256(band.read_bytes()).hexdigest())
print('exact_pixels', np.array_equal(np.asarray(a), np.asarray(r)))
gray = np.asarray(b.convert('L'))[835:900, 1430:1460]
print('right_of_edge_dark_lt150', int((gray < 150).sum()))
'@ | python -X utf8 -
```
