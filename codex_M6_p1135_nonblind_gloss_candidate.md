# p1135 #18 释义候选（非盲，已另复核并写回）

范围：在读过现有字面层和释义后，对照原图及已发表文献；这不是独立盲读、人工验真或 M0 放行。下文保留原始候选；随后结合另一位非盲复核者对第 16、18 条的意见，已采用更审慎的表述修正主释义，详见 `codex_M6_preview/nonblind_gloss_fix_receipt.json`。未更改字面、音写或其他释义版本。

## 精确位置与现值

- 正式文件：`literature/workspace_m2_dhs834/gloss_layer/gloss_p1135.json`，`entries` 中 `position = 18`。
- 当前 `zh`：`僧家；僧众、佛门（出家人一门）`
- 当前 `en`：`the monastic order; monks as a class`
- 当前 `confidence`：`medium`
- 当前 `notes`：`词头'escriuimiento'有[疑:escriuiendo]标记，词头义依赖推断；释义以汉字栏僧、家为准。`
- 对应封存字面：`source_H = 僧 家`；`source_L = yo el Sacerdote escrivimiento [疑:escriuiendo]`。这里引用现值仅为可重复定位，非新的原图逐笔判读。

## 证据和判断

1. [原图下横带](literature/tiles/01_DHS/page_1135/pdf_1135_band_y2_bot.png)：页脚印刷页码 1097；下部圈出的西文 `yo el sacerdote ...` 行，与汉字「僧 家」和右侧圈出的音写处于同一视觉行。上一条另有「僧」，中间隔着「予 也」，不能将两条合成一条。
2. 劉莉美，〈馬尼拉閩南語文獻《西班牙—華語辭典》與西班牙傳教士高母羡〉，《漢學研究》38 卷 2 期（2020），[第 226 页表三及第 227 页](https://ccs.ncl.edu.tw/files/current_chinese_studies/01_038_002_01_06.pdf)：表三将该辞典 1097 页例子排印为 `Yo el saçerdote escriviendo` 对 `僧／僧家`；下页讨论早期天主教教士以「僧」自称。文献合列两项，未对本项目位置 16 和 18 分别建立逐笔真值。
3. [中等] (50-80%) 西文首段的第一人称和教士语境，与将本行仅释为「僧众、佛门／monks as a class」不相符。将「僧家」解释为教士在此处的自称，是基于相同行及论文背景的语境判断；论文不单独证明「僧家」在所有语境中的一般词义。

## 最小候选

以下是初始候选而非最终写回值；最终将第 18 条置信度降为 low，并保留具体用法待核：

```json
{
  "position": 18,
  "zh": "僧家；此处可理解为教士的自称。",
  "en": "a cleric's self-reference; ‘I, the priest’ in the Spanish context",
  "confidence": "medium",
  "notes": "西文首段为 yo el Sacerdote，封存末词读法存疑。刘莉美（2020）第 226 页将该辞典词例排印为 Yo el saçerdote escriviendo，第 227 页讨论天主教教士以‘僧’自称；末词及逐笔字形仍待核。"
}
```

当前 `gloss_layer_v2/gloss_p1135.json` 的第 18 条也将「僧家」释为佛门；本候选不覆盖 v2。第 16 条后经另一位非盲复核者单独比对，也已谨慎修正主释义；第二版仍待后续核查。原图西文末词具体拼写、是否为缩写及墨迹状态仍待具备资格的复核者核实，不能把论文排印直接写成盲读字面。
