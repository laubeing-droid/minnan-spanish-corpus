# ZCode 施工进度（第一书 DHS，2026-11-19 接手起）

延续 `codex_progress_M1.md` 口径；数字范围有重叠，不可相加。交接基准 `aca823d`。

## 接手核验（2026-11-19，只读）

- `git HEAD = aca823d`，与 `origin/main` 一致；交接书基准吻合。
- `codex_ledgers/verify.py` PASS；台账数字与交接书逐项吻合：唯一匹配 5,480（含墨迹不明 599）、未唯一收集 21,334、逐项 pending 2,528（239 完整键重复 + 2,289 双判级缺失或无效）、缺回执页自 p0283 起；修复账 15 条、互证账 filled 0。
- 全库门禁 1,103/1,103、复扫硬违 3,705 基线复现（3705 为扫查器硬违计数，非已证实错误数）。

## 准备阶段（2026-11-19，用户逐项批准后实施）

1. **声调数组同步口径（RSI 待审批件①，已批准实施）**：`repair_batch_a.py` 新增 `tone_disposition()`——每条 source_M/source_R 修复落地前，回执须提供「原图新数组 / 不变确认 / ≥2 可核查来源依据」三者之一，缺一延迟待核；applied 账目新增 `tone_check/tone_marks_old[/tone_marks_new][/tone_basis]` 字段。`seal_and_verify.py` 的 expected 推演同步调号数组改动（含 None/[] 归一）。`test_repair_batch_a.py` 更新夹具并新增 `tone_sync_test`；**10/10 隔离回归通过**。口径：宽松版+置信度门槛，联网核查只是旁证、不能替代原图墨迹。
2. **释义验收退出码（RSI 待审批件②，已批准实施）**：新增只读工具 `literature/tools/verify_gloss_coverage.py`——按封存库全集核对选层（main/v2/v3）：可解析、page 匹配、逐页 position 集合一致且无重复、zh/en 非空；缺项/损坏退出非零；`--census` 普查模式缺文件只报告。验证：main 全库 1,103/1,103 PASS；v3 普查 273/1,103（缺 830，自 p0303 起）如实报告；selected 模式缺页退出 1。内容语义仍另案审校。
3. **工具链演练**：管线四件套 py_compile 通过；`zcode_m2_pipeline.py` CLI 正常；`literature/tiles/01_DHS/page_0283` 横带/四栏裁片读图确认可用（300dpi、带 SHA-256 清单）。
4. **施工规约**：`zcode_workflow_protocol.md`（授权三层边界、批次工作流 S0–S6、声调同步表、读图纪律、联网检索规范、用户裁决请求格式、提交纪律）。
5. **信息源登记册**：`zcode_source_register.md`——本地自有库 + 晚清闽南语三辞书（甘为霖 1913 GitHub/archive、Douglas 1873、Medhurst 1832，均经 WebSearch 核实入口）+ 同期西语-闽南资料（约 1617《Bocabulario de la Lengua Sangleya》EMHo 数位版等）。Gil 论文本地无存，用时重检。

## 未完成（按交接书口径保留）

- 历史 15 条修复外的历史批次是否还有 p0265 同类错行、p0267 同类调号失同步：**未全量复核**，继续按批抽核。
- M3 两栏重构（p0030–0040）、M4 汉字独立重读、M5 互证填充（0）、官话 R 后段、净化器根本冲突：均按交接书状态保留，未动。
- 队列剩余约 830 页无回执；每批约 20 页推进，从 p0283 起。
