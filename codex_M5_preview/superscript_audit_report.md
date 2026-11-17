# 同书互证预览：上置字符风险

旧预览快照为提交 `7c38bb8310f4fd5aa16adaee5f88488dccf8749d` 中的 `candidate_sources.json` 和 `candidate_targets.json`；文件 SHA-256 已记入 `superscript_audit_report.json`。复算命令 `python -X utf8 codex_M5_preview/superscript_audit.py` 依赖相同输入快照，只生成本审查报告，不修改原始数据或预览输入。

6,813 条候选来源中，101 条含 Unicode 上置或修饰字母（M 55、R 46）；99 条的 V1 与重读此类字符集合不同。字符集合不比较重复次数。29 个唯一音节组目标引用了这些来源，均在 R 栏；其中 21 个目标的候选来源全部带此风险。目标间的数字基于旧索引，并非已确认的可填或不可填数量。

| 来源 | V1 原文 | 重读原文 | 旧字母汤 | 待核事项 |
| --- | --- | --- | --- | --- |
| p0046/3 R，隨 | `chûiᶜ` | `chúi` | `chui` | 旧字母汤去掉 `ᶜ`，需判定上置笔画的性质。 |
| p0164/8 R，片 | `piēⁿ` | `pien` | `pien` | 旧字母汤将 `ⁿ` 映射为 `n`，是否可等同需核。 |
| p0043/14 M | `ngòu chaûᶜ.` | `ngoû chāù.` | `ngouchau` | 旧字母汤丢掉 `ᶜ`；韵部、记号与声调需分别判断。 |

逐来源原文、文件路径、position、重读数组序号、字符集合及受影响目标见 `superscript_audit_report.json`。Unicode 码点仅是筛查线索：上置字符可能是字母、鼻化信息或标记，原图未裁定前不能宣称差异是错误，也不能静默归作声调差。三条核图候选的源图坐标及细节另见 `review_alignment_sample.json`。
