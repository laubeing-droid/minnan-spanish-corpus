# 最终 AgentSkill 待封装材料清单（过程清单，尚未封装）

2026-10-16。当前HAB05/06尚在逐页复核，DHS主稿亦仍推进；本清单不构成全批完成或全文校定声明。

## 已有可纳入的材料

以下研究目录为 ../blind_calibration_20261016_v1/：

1. 学者明说、实例归纳、自拟规则分层：DHS_scholarly_transcription_method_evidence_v1.md；DHS_historical_to_modern_minnan_layers_v1.md。原字母照录、历史音值解释和现代闽南各地参照分别保存，不冻结统一台罗映射。
2. 教学页及纯方法：DHS_seven_tone_symbols_learning_sheet_v1.md、tone_learning_source_manifest_v1.json、DHS_reader_method_only_v1.md、DSH_reader_method_only_v1.md、DSH_tz_letter_learning_addendum_v1.md。七类符号有教学例，不等于七类皆经独立测试掌握。
3. 冻结盲读及失败：DHS_roundA_frozen_comparison_v1.md、DHS_roundB_frozen_comparison_v1.md、DHS_roundC_same_images_comparison_v1.md、DHS_roundD_taught_comparison_v1.md、DHS_roundD_supplement_comparison_v1.md、DHS_roundD_exposure_correction_addendum_v1.md、DSH_roundS_published_comparison_v1.md。附各REFERENCE_ONLY键及图像清单，但参考键绝不进入读者方法包。
4. 双书互参：DHS_DSH_first_crossdictionary_check_v1.md、DSH_newmethod_reference_and_crossdictionary_stage_v1.md、DSH_newmethod_086169_reference_addendum_v1.md。语义对齐不等于同音同词，独立照录封存后再做互校。
5. 复合记号迁移：Arte_composite_notation_teaching_preparation_v1.md、Arte_EMHo_method_addendum_v1.md、EMHo_TEI2026_actual_method_reading_v1.md。BL Add25317项目规则不能冒充DHS底本专属规约。
6. 工作记录：DHS_calibration_worklog_snapshot_01.md至10.md，范围修订及分辨率/暴露追加说明；各书method_transfer_v3中的逐页review、coverage、全源行映射、最终入口。正文与这些配套材料分别打包。
7. 实际代码：DHS目录match_five_crops_v1.py与后续新版本、scripts目录中已有图像/定位说明；本轮save_hab_transfer_v3系列只负责已看图后的保存和映射，绝非自动识读。必须注明模板高分假阳性、尺度敏感和原图人工确认要求。

## 本轮迁移可教的具体条件

- HAB账页：金额字需原像素笔画核验，禁止用加总校成顺数。02/028廿六→十二、03/004六分→二分、07/006一千五→一十五有本轮局部图支持。
- HAB词书：汉字音写未必字义，不能套DHS罗马调号。12/021原上分下貝支持貧，不能因新旧成对把它读成舊。
- 透背：深色也可镜反；先核偏旁方向和纸层。12/013仅镜层辅助读法，12/014才正面，不能都算独立正文。
- 小字与边注：能确认的旧校记旁注应回归定位正文，同时保留来源映射；14/005两旁注这样处理。其余细字不能被整页覆盖数隐去。
- 医书/宗教连续文本：通行语义只作候选支持，原刻笔画和版本差异独立；Mingxin195与Shilu113已有撤回候选，不删除失败记录。

## 必须附的限制与尚缺项

- 上下文隔离没有文件权限硬隔离；学习后重读暴露页不可称项目全新留出。
- C两读者同图比较仍有读者差异，不能证明提示因果提升。四题两类符号的教学实测不可外推全书、其他调类或汉字音写。
- 参考论文仅覆盖部分字段；未覆盖罗马字、调号不能判通过。公开未人工校对数据库只作定位线索。
- 原图覆盖、文本映射完整、正文读清是三个不同指标。所有疑字和整段未辨仍须随正文交付。
- HAB14原图正文仅1024像素级，图像放大不增加原扫描细节；AUST10仅部分识读，不能因逐页查看而称十页全文完成。
- 最终封装应等待DHS现行主稿冻结及家长确认整体交付状态；现有draft-v1保持过程草案身份，不安装、不更改已有技能。
