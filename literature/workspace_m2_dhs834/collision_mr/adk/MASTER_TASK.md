# 字面裁决主任务（Gemini 裁判管线·standing task）

你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的字面裁决员。工作区 `literature/workspace_m2_dhs834/collision_mr/adk/` 下有逐页裁决任务文件 `adk_pXXXX.json`（XXXX 为 PDF 页号，四位）。**逐页处理，直到全部完成。**

## 每页做什么

1. 读任务文件 `adk/adk_pXXXX.json`：`items` 数组每条含 `position / field(M=R闽南音写栏, R=官话对音栏) / v1(第一读法) / rr(重读读法) / kind`。
2. 对照横带切图核验墨迹（M 栏=倒数第二栏，R 栏=最右栏）：
   `literature/tiles/01_DHS/page_XXXX/pdf_XXXX_band_y0_top.png` / `_band_y1_mid.png` / `_band_y2_bot.png`
3. 逐条四选一裁决，写 `adk/adk_verdict_pXXXX.json`：

```json
{"protocol": "ADK_VERDICT_V1", "page": N,
 "verdicts": [{"position": 1, "field": "M", "v1": "…", "rr": "…", "verdict": "V1对", "ink": "", "note": "",
               "letters": "V1", "tone_mark": "一致"}]}
```

## 裁决口径（四选一 + 双填）

- **V1对**：墨迹与 v1 一致（ink 留空）
- **重读对**：墨迹与 rr 一致（ink 留空）
- **两皆误**：两侧都错（ink 写出你所见的忠实字面）
- **墨迹不明**：无法判定（ink 留空，note 一句原因）

**双填字段（防判级噪声——字母差与调符记法差分开）：**
- `"letters"`：剥去声调符后，字母本体与哪边一致 → `"V1" / "rr" / "两皆误" / "等价"`
- `"tone_mark"`：声调符归属层 → `"一致" / "位置差" / "缺失" / "存疑"`

（说明：`cang` vs `cáng` 属声调符位置差、字母等价——判"等价"并标 `tone_mark: 位置差`，
**不得**判"两皆误"。）

## 铁律

1. **照录所见字母**：元音符（û/ā/é/ò/^）戴在哪个字母上就记在哪个字母上；禁止用现代台罗/教会罗马字/词典拼写"纠正"墨迹。
2. **f/v 字形特别提示**：本手稿存在 t/Z/f 三形混淆字形，且闽南语无 /f/ /v/ 声母——但**禁止按音系预判改读**：墨迹像什么就判什么；判不准写 "墨迹不明"。
3. 两读仅为**拼写变体/声调符位置差/标点差**时判 "等价"（ink 留空）。
4. 上标鼻化 n（ⁿ）照录为普通字母 `n`。
5. 反空转纪律：禁止 "hmm/让我想想" 式空转推演，看完墨迹直接逐条写结论；拿不准判 "墨迹不明"。
6. **禁止读取** `blind_read_p*`、`gloss_layer*/`、`reread_mr/` 下任何文件——v1/rr 数值已在任务文件里，你只需要看图。

## 完成判据

`adk/` 下每个 `adk_pXXXX.json` 都有对应的 `adk_verdict_pXXXX.json`。全部完成后汇报：完成页数 / 各裁决计数 / 异常页清单。
