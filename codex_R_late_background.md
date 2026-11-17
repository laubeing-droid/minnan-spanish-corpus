# 官话栏后段：文献线索与随机核图（进行中）

[Henning Klöter，《The Dictionario Hispanico Sinicum: Some remarks on its historical contexts and lexicographical peculiarities》](https://www.academia.edu/45452702/The_Dictionario_Hispanico_Sinicum_Some_remarks_on_its_historical_contexts_and_lexicographical_peculiarities)指出，手稿的官话音写在 folio 210v 的 `escriuir` 子条目后停止，后续仍留有第四栏空位。该论断为研究者对本手稿的观察；folio 与本地 PDF 页码尚未从外部目录独立核定，不能直接把 210v 当 PDF 页号。

先对一页原图独立盲读：`codex_R_p0455_blind.json` 记录，第 11 视觉行是该图最后一行可辨的右栏罗马字母，下方有空白、碎痕和两个疑似汉字状记号，不能据此称后面毫无笔迹。读图后才对照当前封存：该行的西语为 `escriuir en abreviatura`、下一行为 `escriuir en el libro`，右栏现值分别为罗马字及 `[空]`。这是图像与文献线索的对应候选，不证明任意其他页面的所有右栏都空。

对清册中的 PDF 0456 及以后页做只读盘点：12,820 个条目中，当前 `source_R` 为空或 `[空]` 11,536 条、单独 `[残]` 275 条、其他 1,009 条（316 页）。这些是既有模型封存字段的内容分类，不是认定 1,009 条均有错误；其中可能有边注、跨栏文字、残疑标记或其他情况。

在看盲读之前，以固定种子 20261118 从 1,009 条中抽出 5 个不同页的目标，登记见 `codex_R_late_sample_plan.json`；各读者只看源图、先交卷，再与封存对照，结果见 `codex_R_late_sample_comparison.json`。p0943/1 的两个独立模型读者在候选行右栏均未见可辨文字，但同页中栏有上下相邻字串和被划文字，条目合并或错栏仍待核；p1026/2 的候选图像与封存 H/M/R 字段有疑似整体错位；p0611/13 右侧有跨栏西文；p1086/2 外缘笔迹归属不明；p0743/9 的视觉行与结构位置不符，不能比较。这些都是候选，不作人审真值，不直接删除或搬移正文。

用户允许对 `[空]`/`[残]` 使用同书互证，但若空栏原本就是手稿未填写，补出的音写只能标作有来源的推定，不能冒充该行原墨迹。上述资料不覆盖已冻结的 `adk/` 队列，也不证明已经完成官话栏校对。
