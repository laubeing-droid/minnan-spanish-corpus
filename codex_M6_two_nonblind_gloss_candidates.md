# p0286 #3、p0340 #11 释义候选（非盲，已另复核并写回）

先读过现有字面层和释义，再核原图及文献；不是独立盲读、人验或 M0 放行。下文保留原始候选；另一位非盲复核者核对原图和论文后，已以更简洁的保守表述修正主释义，最终 old/new 见 `codex_M6_preview/nonblind_gloss_fix_receipt.json`。未改字面、音写或其他版本。

## p0286 #3：可食之蚶

- 文件：`literature/workspace_m2_dhs834/gloss_layer/gloss_p0286.json`，`entries` 的 `position = 3`。
- 原值：`zh = 蚶（大型贝类，血蚶、泥蚶）`；`en = large shells; cockles (blood cockle, Arca type)`；`confidence = high`；`notes = 西栏尾词 pajamer 难解（疑为原稿转写之讹），不影响四栏互证之主释义。`
- 封存 `source_L = conchas grandes pájamer.`、`source_H = 蚶`；引用现值只为定位。
- [原图上横带](literature/tiles/01_DHS/page_0286/pdf_0286_band_y0_top.png)第三行「蚶」对应西文末段，可见类似 `p` 上置小字后接 `comer` 的形状；这是看过答案后的观察，不是逐笔定稿。
- 劉莉美（2020），[《漢學研究》38 卷 2 期第 226 页表三](https://ccs.ncl.edu.tw/files/current_chinese_studies/01_038_002_01_06.pdf)，将本辞典出版物第 257 页该行排印为 `conchas grandes para comer`。另一份[西班牙文古文字研究](https://iealbacetenses.dipualba.es/high.raw?attachment=0000021571.pdf&id=0000021571&name=00000001.original.pdf)讨论特定文书中的 `pa=para` 缩写，只能作时代和书写习惯的旁证，不证明本笔迹必然如此。
- [中等] (50-80%) 论文读法提示「供食用」比把尾段猜为不明词更有依据；仅凭本条不能确定蚶具体物种。候选在释义里注明论文读法，保留字面层待核。

```json
{
  "position": 3,
  "zh": "蚶；供食用的大型贝类。",
  "en": "large edible shellfish, glossed as han (an ark shell)",
  "confidence": "medium",
  "notes": "刘莉美（2020）第 226 页表三将本辞典该行排印为 conchas grandes para comer。原图末段疑含 para 的缩写，须另核手稿字形；不据此改写封存字面。"
}
```

## p0340 #11：轮子回转

- 文件：`literature/workspace_m2_dhs834/gloss_layer/gloss_p0340.json`，`entries` 的 `position = 11`。
- 原值：`zh = 轮回：车轮回转、轮转不息；亦指轮回转世`；`en = the wheel turns round; the round of transmigration (samsara)`；`confidence = high`；`notes` 为空。
- [原图中横带](literature/tiles/01_DHS/page_0340/pdf_0340_band_y1_mid.png)中，`dar bueltas la rueda` 与「輪 迴」同一行；相邻还有「輪轉」等独立行。
- 劉莉美（2020），[同文第 225 页表二及其后文字、注 16](https://ccs.ncl.edu.tw/files/current_chinese_studies/01_038_002_01_06.pdf)，将该行与《明心寶鑑》对应翻译并列，并讨论「命运之轮」的关联。这是学者对相关用例的阐释，不能据此断言本条唯一意义。
- [中等] (50-80%) 本行可先释为轮子回转；现有「转世 / samsara」并无本行上下文支持，至少不宜作为已确定的本条释义。

```json
{
  "position": 11,
  "zh": "轮回：车轮回转；轮转、循环。",
  "en": "the wheel turns; revolving or cyclical movement",
  "confidence": "medium",
  "notes": "刘莉美（2020）第 225 页将此例与《明心寶鑑》译文对照，并讨论命运之轮的联想；本行未提供明确转世语境。"
}
```

以上代码块为初始候选，实际写回以回执为准。p0286 的论文展开读法不可直接替换手稿字母和上标；未验笔画与缩写时不得冒充已确认字面。
