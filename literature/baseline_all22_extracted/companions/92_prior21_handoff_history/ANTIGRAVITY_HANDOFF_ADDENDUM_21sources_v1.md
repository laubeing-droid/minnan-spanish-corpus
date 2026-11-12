# Antigravity独立交接增补：21份来源，DHS待接入

日期：2026-10-16。无需聊天上下文即可按本页定位。此为本地交付准备，未上传、发布或安装。旧稿、原图与旧报告保留不变。

## 1. 范围与当前结论

已完成阶段：21份PDF来源、1999幅PDF页的方法新读或方法迁移复核。14份HAB归为同书组但保留各册PDF定位；Angelica与Paris为两套底本，分别保存。页数包含现代封面/许可、空白、透背、装帧和未能读清页，不是完整正文页数。

尚未完成接入：DHS《西班牙—华语辞典》1140页，主稿由另一组继续。不要将局部产物算全书完成，不在本次清单中冻结或重打包其正文。全部来源共22份，当前没有全批完成声明。

所有书的全文核定状态仍为false。没有全书准确率、模型训练权重更新或零误保证。

## 2. 从这里读取

- 人读逐书清单：/workspace/scratch/3ee2b91a8980/minnan_continuation/handoff_21sources_20261016_v1/completed21_sources_handoff_inventory_v1.md
- 机器清单及当前正文SHA256：/workspace/scratch/3ee2b91a8980/minnan_continuation/handoff_21sources_20261016_v1/completed21_sources_handoff_inventory_v1.json
- 本次Angelica169冻结稿复验：/workspace/scratch/3ee2b91a8980/minnan_continuation/handoff_21sources_20261016_v1/Angelica169_frozen_body_recheck.json
- HAB同书组正文：/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_all14_method_transfer_summary_v3/HAB_all14_461pages_body_v3.md
- HAB总入口：/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_all14_method_transfer_summary_v3/FINAL_DELIVERY_HAB_all14_v3.md

正文阅读优先顺序：Grammar采用body_clean_v3；ONB/Mingxin/Shilu采用body_final_v3；HAB05/06/13采用release最终层；其他册采用清单指向正文。旧text、中间clean或method版本仅作追溯，不自动替代最终入口。

Angelica当前交付为169份冻结逐页MD：001–085文件名pdf_001.md样式，086–169为pdf086.md样式。尚未存在本方法版合并MD。包装时如另建合并，应只连接冻稿并保留PDF边界，另记合并hash，不覆盖或顺文改写原冻稿。165–168为书信/题记，169为封底，不能当同类词典词项评分。

## 3. 五类交付怎样分

1. 正文MD：使用清单body_files；古拼写、汉字异体、物理续行及必要疑读保留。阅读候选是当前可用成果，不能删去未辨标记制造完整稿。
2. Antigravity交接：本页＋逐书清单＋覆盖/映射链接；旧交接记录作为历史层并存。
3. 自身工作记录：本次WORK_RECORD_existing_artifact_verification_v1.md；各书逐页review、doubts文件；研究目录工作日志snapshot01–10和各追加说明。不要把过程报告粘进正文。
4. AgentSkill：仅候选材料，见/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_all14_method_transfer_summary_v3/skill_packaging_materials_PROVISIONAL_v1.md及completion_and_skill_materials_addendum_v2.md。已有transcribe-historical-minnan-draft-v1是草案，未最终封装/安装。最终封装等待整体接入与确认。
5. 实际代码：各条scripts指向真实文件，另见本次actual_code_index_v1.json。这些代码主要保存、渲染/定位、映射和验收；不能冒称自动完成识读。Angelica旧审计脚本不等于本轮独立新稿生成脚本；后者未定位到，明确留缺。

## 4. 映射及证据的解释

PDF序号从1起；它不等于刊页，偏移不保证恒定。原图路径和hash见每书coverage；源行映射、逐页校记或freeze各有作用。Grammar净正文为两级映射；Paris现有逐页旧读/新候选review与coverage，不冒称统一全源物理行表；Angelica独立新稿用原图清单与freeze定位，不生成对旧稿逐行替换的虚构映射。

本次只重新核已存路径和正文文件hash，Angelica169与先前冻结hash逐一相等；没有重新看1999幅图，也没有重复hash大型PDF/原图。逐页视觉阅读由此前各书实核记录支持。本次文件核验不能替代字形核验。

## 5. 必须继承的未决和已撤回项

- Paris120两条校记把转义换行n当原字母，已追加撤回，原正确拼写保留；review/pdf_120_addendum_v3a.md优先。
- Mingxin195 malicia候选撤回；Shilu113電候选撤回，最终用暴雹。不要拿旧工作候选覆盖最终正文。
- ONB日期、章次原层矛盾保留；修改组数不等于确定错字数。
- AUST10只覆盖公开残页，完整正文识读0页；低分辨率放大不能称新高清证据。
- HAB大量草写音写、账目重墨、边缘细注未解；HAB14刻页/草写图分辨率限制仍在。HAB13第一版hash审计选错层，后v2按final_text_sha256复验通过，失败轨迹保留。
- DHS七类调号规约不能硬套HAB汉字注西语、宗教汉文或Arte复合上标。原笔照录、作者符号编码、音值解释、现代闽南各地参照是分开的层。

## 6. 盲读与互校材料隔离

读者纯方法在/workspace/scratch/3ee2b91a8980/minnan_continuation/blind_calibration_20261016_v1/DHS_reader_method_only_v1.md、DSH_reader_method_only_v1.md。REFERENCE_ONLY、既有盲稿及比对结果不能交给新隔离读者。上下文隔离不等于权限硬隔离。Angelica9/21/52旧见、33教学暴露不可称新留出。

用户流程保留：先学一手研究方法→两本带方法独立照录并冻结→各自公开参照纠错→两本同词义条目互参→其余各书迁移复核总结边界→最后封装。语义支持用于校读，不能压过笔画；两词典同义也不必同词同音同长度。

## 7. 交接操作边界与磁盘

检查时同一32GB卷已用约28GB，剩约2.5GB（92%）。本次仅新增小型JSON/MD和少量实际代码快照，没有复制大图/PDF，也未建ZIP。接手先检查磁盘；不要默认制作包含所有图像的整包，不删除或覆盖旧稿，不安装依赖或改配置。发布/上传仍暂停。

DHS接入时应取得最终freeze、逐页覆盖、正文入口、原图定位、未决及实际脚本，再另建清单增补；这不是现在授权停止或修改其转写。
