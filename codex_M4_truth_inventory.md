# M4 汉字十行校准真值清点

日期：2026-11-18。范围为本仓库的校准标准、DHS 历史工作记录、相关 Git 提交、图像定位和现有 H 复核附件；未读取其他会话，未改既有转写、源图或校准标准。

## 结果

目前**不能组出符合 M4 要求的十行人验真值卷**。唯一找到的逐行用户核验记载为 p0257 两条视觉行，且其人验出处是标准中的项目记录，未找到独立的用户原话或人验回执。它们可作为已登记的两条候选，不应伪称有十条或把其他机器复核充作人验。M4 仍未启动，十行卷没有固定、交卷或判分。

| 视觉行 | 项目记录中的字面 | 人验来源及限度 | 原图定位 |
| --- | --- | --- | --- |
| p0257，校准裁片 D 汉字栏第 1 行 | `割 皮` | `literature/workspace_m2_dhs834/collision_mr/calibration/CALIBRATION_STANDARD_V1.json:57` 记“用户+主会话双验”；未定位用户原话或独立回执。 | `literature/workspace_m2_dhs834/collision_mr/calibration/p0257_pos10_circuncidar.png`，D 图自上而下第 1 汉字行。 |
| p0257，校准裁片 D 汉字栏第 2 行 | `割玉脛皮` | 同标准 `:58–59` 记“用户眼验坐实”；未定位用户原话或独立回执。 | 同一 D 图自上而下第 2 汉字行。 |

D 图为 2535 × 574 PNG，SHA-256 `efcb99cf23aee502b9ad5c17d3c76a5eaacf981597729227c36087615fdc88bb`；`_scratch_p0257/p0257_pos10_circuncidar.png` 是相同字节的本地副本。整页汉字列位于 `literature/tiles/01_DHS/page_0257/pdf_0257_subcol2_hanzi_full.png`，SHA-256 `8219d0d43054bf5e0610ee4de0f516d906c60705e27db1812d6cd3d2bbda2eb5`。两条为同裁片的两个视觉行，不能重复拆字凑题数；且已用于本轮 M0，不视为本会话未见的新答案。后续独立读者只接收预先固定的图片和行定位，不接触标准、此报告或已有转写。

`CODEX_BRIEF.md:95–98` 要求主会话提供已验真值裁片、十行至少 8/10 才放全量。对上述两条，标准 `:4` 自称用户审批并声称具体眼验，但这仅能证明项目记录**作出过该声明**。两条之外还需至少 8 条有同等级或更强的可追溯人工核验证据；若要求直接用户原话，则这两条也仍需补齐原始凭据。

## 排除：已有 H 复核材料不是已证人验

- `literature/assets/H_NONAUTHOR_BATCH_REVIEW_1100_1104_20261028T041452Z.json` 的 `reviewer` 为 `/root/review_h_literal_remaining`；记录五页 87 个物理 H 位置，其中 54 条为有限字面释义提案，其他包括局部、组件和未定项。该文件 SHA-256 `ae341262c51545e4aef8635f9ce779c8b53d03d52362a18bb3c3326362657414`。
- `literature/assets/DHS1100_1104_H_LITERAL_REVIEWED_INCREMENT_20261028T041419Z.zip` 的 `independent_review/h_nonauthor_review_1101_20261028T041010Z.json` 明列 reviewer `/root/review_h_literal_remaining`、author `/root/resolve_literature_execution_scope`，并绑定当时图像和逐条意见。它可以作为带定位和边界的代理复核线索；回执未声明用户或人工核验，不升级为 M4 人验真值。ZIP SHA-256 `605658bdb0a044247b094de889438cacdc7553c1eb5b7fd3f3ee469d4829776c`。
- `literature/assets/DHS1130_1134_H_LITERAL_REVIEWED_INCREMENT_20261028T035900Z.zip` 同样含图像和非作者复核回执；其中 p1133/p1134 审者为 `/root/review_h_literal_remaining`，未声明用户或人工核验。ZIP SHA-256 `b4199f55fc347bf20a160bfb3652f4278552b2f0d4aedc9e12a363f7b553ea2a`。
- `literature/baseline_all22_extracted/companions/91_historical_method_research/DHS_calibration_worklog_snapshot_06.md:7` 记录用户实体观察两部辞典的总体详略，并未提供 DHS 汉字逐行真值。`66b1a45` 的提交说明记载 p0257 的 `cûa` 经用户眼验，属于罗马字，不构成额外汉字题。

## 继续执行的边界

保留上述两条及代理复核线索，继续查找能定位图像、视觉行和人工核验者的历史记录。确有十行且标准固定后，让**未见答案**的读者从原图独立作答并先封卷，再以字符原样比较与逐项留存，达到 8/10 方按原计划扩量；不能用 2/2 变相折算 8/10，也不能把 H 释义提案当作字形真值。若在 M4 时间盒内找不到足够记录，则如执行书所述入待办，不把 M4 写成通过。
