# M0 原卷跨裁片核查（2026-11-18）

【修改位置】此前将 B 第六行称为原卷整体无法完整看见。

【修改内容】B 单图右边确有截断；原卷 D 四栏图同时展示相同两行及 B 右边界以外的续笔。原提示要求 D 输出汉字栏，但未说明能否利用 D 的 M 栏补看 B 题，因此旧卷是否可以跨图评分仍待按原口径裁定；不能笼统说四张原图都缺少行末。此前八题对照的诊断数字保留，不作为正式分数或证明该题一定读错。

【修正原因】对 B、D 以 SIFT 匹配并用 RANSAC 拟合仿射变换：552 个匹配点中 470 个内点，B→D 约为 x'=0.6999x+1007.8138、y'=0.6999y−881.9538。B 坐标 (995,1792) 在 B 图右界 960 外，映射到 D 中约 (1704.2,372.3)，落在 D 图内部；原图目视也能看到 D 上 M 栏对应两行。B 尺寸 960×2434，D 尺寸 2535×574。这只核对图像对应与覆盖，不判字母、声调或试卷解释。

C 难题裁片可由 p0030 300dpi 图 `[608,219,1048,399]` 按 LANCZOS 放大至 1760×720 逐像素重建；源图在左右相邻边界分别有 10、2 个同 y 深色像素跨边（阈值灰度小于 150）。C 不入核心门槛，裁片边缘墨迹不应被当成完整行能力评估；像素计数不自行判读字符。

图像 SHA-256（本机切图与试卷不入仓）：
- `_scratch_p0257/calib_p0257_mcol_y1.png`：`d2944f17f3b345526b7c0a443cdf750de44838b81c40277ac1a8832993eb64d6`
- `_scratch_p0257/p0257_pos10_circuncidar.png`：`efcb99cf23aee502b9ad5c17d3c76a5eaacf981597729227c36087615fdc88bb`
- `_scratch_p0257/calib_p0030_m_lines12_4x.png`：`7be0d6ae8b833154cfeb78144647336e09e0a0bb8f8f0bf2511059f58bec040c`
- `literature/tiles/01_DHS/page_0030/pdf_0030_300dpi.png`：`9d1dba76f0a273cae4353197352011e80a77b0793367322d9745b46556302d2a`

## 重算命令（只读）

```python
from PIL import Image
import cv2, numpy as np
b = np.asarray(Image.open('_scratch_p0257/calib_p0257_mcol_y1.png').convert('L'))
d = np.asarray(Image.open('_scratch_p0257/p0257_pos10_circuncidar.png').convert('L'))
s = cv2.SIFT_create()
bk, bd = s.detectAndCompute(b, None)
dk, dd = s.detectAndCompute(d, None)
pairs = cv2.BFMatcher().knnMatch(bd, dd, k=2)
good = [m for m, n in pairs if m.distance < 0.75*n.distance]
x = np.float32([bk[m.queryIdx].pt for m in good])
y = np.float32([dk[m.trainIdx].pt for m in good])
mat, keep = cv2.estimateAffinePartial2D(x, y, method=cv2.RANSAC, ransacReprojThreshold=3)
print(len(good), int(keep.sum()), mat, mat @ np.array([995,1792,1]))
c = Image.open('_scratch_p0257/calib_p0030_m_lines12_4x.png').convert('RGB')
src = Image.open('literature/tiles/01_DHS/page_0030/pdf_0030_300dpi.png').convert('RGB')
print(np.array_equal(np.asarray(c), np.asarray(src.crop((608,219,1048,399)).resize(c.size,Image.Resampling.LANCZOS))))
g = np.asarray(src.convert('L'))
print(int(np.sum((g[219:399,607]<150)&(g[219:399,608]<150))), int(np.sum((g[219:399,1047]<150)&(g[219:399,1048]<150))))
```
