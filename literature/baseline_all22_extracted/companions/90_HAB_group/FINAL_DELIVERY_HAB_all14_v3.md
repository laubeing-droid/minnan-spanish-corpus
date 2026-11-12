# HAB 全14分册方法迁移交付

461/461页实际看图，保存各页观察与旧读→新候选。正文仍是部分识读候选，不是全文校定。各分册馆藏、透背、空白、封装的记录也占覆盖页数，不能换算识字准确率。

## 正文与定位

合并正文：HAB_all14_461pages_body_v3.md。分册维持01–14文件次序、PDF页定位；源文件之间可能包含重复装帧图和跨分册叶序，未静默去重或重排。

覆盖：coverage_HAB_all14_461pages_v3.json，含每页图、源稿、最终正文hash与完整分册映射入口。所有源稿与原图未变。HAB13最终正文逐行准确字符串补映射见 HAB13_exact_final_body_line_mapping_supplement_v3.json。

## 有据改进与未解决

- 02/028 L09廿六担→十二担、03/004 R01六分→二分、04/006 R09余目→余日、06/014金额三→二、07/006 L04b一千五→一十五、12/021 R07旧主读舊→貧，系本轮可见笔画支持。仍不宣称全页其余文字正确。
- 01三处、05/038六→八疑、09/006肯→肯／肖疑、13九处等均只是候选；13另两处七栏→八栏为版面修正，08补154/155为页号。不得合并当确定错字数。
- 10、11未找到可确定新改字，保持疑读本身就是本轮结果。
- 12镜反层与正面词书分别保存，不能把透背当第二份正文。14/004–005旧疑号进入新正文，005旧校记两旁注回归定位，不计新发现字符。
- 账目销线下、草写汉字音写、细小边注、破边截字仍大量未能读清。14正文图1024像素级限制尚未克服。

## 失败与迁移边界

数目加总、熟悉词义及新旧/亲属成对结构可提示候选，不能代替笔画。账页的圈、销线、单位记号与DHS罗马调号无直接映射。字形看似漢字也可能音写西语，不擅改成现代汉语顺文。医学刻页不按通行医书倒填。

HAB13验收第一版误将旧提取层hash对最终层，随后按final_text_sha256重验全部通过；过程文件保留，不掩去失败。保存脚本只记录人工已看原图之后的决定，不能充作图像识读程序。

AgentSkill暂仅材料清单 skill_packaging_materials_PROVISIONAL_v1.md，不最终封装；DHS主稿进度须由主协调确认。

## 分册入口

- 01: 23页，/workspace/shared/minnan_transcription/hab_91_2_extrav_01/method_transfer_v3

- 02: 34页，/workspace/shared/minnan_transcription/hab_91_2_extrav_02/method_transfer_v3

- 03: 20页，/workspace/shared/minnan_transcription/hab_91_2_extrav_03/method_transfer_v3

- 04: 11页，/workspace/shared/minnan_transcription/hab_91_2_extrav_04/method_transfer_v3

- 05: 43页，/workspace/shared/minnan_transcription/hab_91_2_extrav_05/method_transfer_v3/release

- 06: 45页，/workspace/shared/minnan_transcription/hab_91_2_extrav_06/method_transfer_v3/release

- 07: 24页，/workspace/shared/minnan_transcription/hab_91_2_extrav_07/method_transfer_v3

- 08: 17页，/workspace/shared/minnan_transcription/hab_91_2_extrav_08/method_transfer_v3

- 09: 12页，/workspace/shared/minnan_transcription/hab_91_2_extrav_09/method_transfer_v3

- 10: 14页，/workspace/shared/minnan_transcription/hab_91_2_extrav_10/method_transfer_v3

- 11: 12页，/workspace/shared/minnan_transcription/hab_91_2_extrav_11/method_transfer_v3

- 12: 28页，/workspace/shared/minnan_transcription/hab_91_2_extrav_12/method_transfer_v3

- 13: 168页，/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_91_2_extrav_13/method_transfer_v3/release

- 14: 10页，/workspace/scratch/3ee2b91a8980/minnan_continuation/hab_91_2_extrav_14/method_transfer_v3
