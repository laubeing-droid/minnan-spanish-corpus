# 术语表 / Glossary / Glosario

> 三语对照术语表。按拼音/字母排序。

| 术语 (汉) | English | Español | 释义 |
| --- | --- | --- | --- |
| 盲读 | blind read | lectura ciega | 只依据页面图像的转写，禁止音韵推断补写；本库核心协议（v3.1） |
| 版面/行版式 | layout | disposición | 手稿页面版式：四栏正编 `4COL`、双栏补充本 `2COL` |
| 波浪符鼻化 | tilde nasalization | nasalización con tilde | 手稿 ⁿ 鼻化符的净化目标形态（元音上加鼻化符），如 piēⁿ → piēñ |
| 不可改门禁 | immutable gate | puerta inmutable | `architect_gatekeeper.py`，声明禁止修改的验收器，反伪造+反模板 |
| 物理页位 | physical page position | posición física de página | PDF 中的绝对页序（含封面/空白页），全库共 3,139 个 |
 | 多明我会拼写 | Dominican (Dominican mission) orthography | ortografía dominica | 17 世纪西班牙传教士记录闽南语的拼写系统：c-/qu-/ch-/g-/s-/z-/ttz- 等 |
| 官话对音（R 栏） | Mandarin gloss column | glosa mandarín | 手稿第四栏的官话读音对照 |
| 后设数据/清单 | manifest | manifiesto | `BLIND_READ_MANIFEST.json` 等 SHA-256 对账总账 |
| 基线初稿 | baseline first draft | borrador base | 22 源既有全文初稿（`baseline_all22_extracted/`） |
| 几何调码 | geometric tone codes | códigos tonales geométricos | 按调符形态记录的 T00–T07/T99（非调值），见 [TONE_MARKS.md](TONE_MARKS.md) |
| 交叉入声号 | entering-tone cross | cruz de entrada | T06/T07：两条短线交叉的入声标记 |
| 九条书组线 | nine book lines | nueve líneas de obra | 22 源按文献分组形成的 9 条执行线（见 [SOURCES.md](SOURCES.md)） |
| 静默缺页 | silent page gap | laguna silenciosa | 总数达标但个别页面缺失——须由页面覆盖审计发现并逐项处理 |
| 冻结区 | frozen zone | zona congelada | `workspace_m1_dhs306/`，封盘后只读，问题入台账 |
| 灾备 | disaster recovery | recuperación ante desastres | 远端数据、合法持有的原始 PDF、匹配版本的工具及可用依赖经恢复验证后接续施工的能力 |
| 四账分离 | four-ledger separation | separación de cuatro libros | 未决字形/缺证音值/词义未定/未执行工序四本台账（[LEDGERS.md](LEDGERS.md)） |
| 台罗（MOE） | Tâi-lô (MOE) | Tâi-lô (MOE) | 台湾教育部推荐闽南语拼音方案；本库仅作现代参照层 |
| 提交封存 | commit sealing | sellado por commit | 净化→推导→写盘→SHA-256 入清单的确定性流程 |
| 页面覆盖审计 | page-coverage audit | auditoría de cobertura de páginas | 按页码 ID 核对各封存账，防"总数对但缺页" |
| 一次性产出 | single-pass output | salida de una pasada | 盲读为单遍产出，仍须下游逐条人工校对，单遍产出本身不保证忠实性 |
| 生理人 Sangley | Sangley | sangley | 17 世纪马尼拉的闽南语华人（生理人）；本库文献的主要使用者群体 |
| 原稿音写（M 栏） | manuscript spelling (column M) | grafía del manuscrito | 手稿第三栏：多明我会式闽南语音写 |
| 照录层 | diplomatic (verbatim) layer | capa diplomática | source_L/H/M/R 四栏"照所见抄录"，不规范化 |
