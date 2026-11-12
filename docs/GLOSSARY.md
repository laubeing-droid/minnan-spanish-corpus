# 术语表 / Glossary / Glosario

本表提供汉语、英语和西班牙语术语对照，帮助读者理解仓库中的材料、字段和操作名称。字段与代码保留原样；涉及具体规则时，请继续查阅所链接的手册。

| 术语 (汉) | English | Español | 释义 |
| --- | --- | --- | --- |
| 版面/行版式 | page layout / column mode | disposición de página / formato de columnas | 手稿页面版式：四栏正编 `DHS_4COL_BILINGUAL`、双栏无汉字补抄本 `DHS_2COL_SUPPLEMENT_NO_HANZI` |
| 波浪符鼻化 | tilde nasalization | nasalización con tilde (`~`) | 手稿元音鼻化符的目标形态（元音上叠加 `\u0303`），引擎自动将误写的现代 POJ 上标 `ⁿ` 归位 |
| 不可改门禁 | immutable acceptance gate | puerta de aceptación inmutable | `architect_gatekeeper.py`，声明禁止修改的验收器，含正字法黑名单与反模板 `Counter` 频次检查 |
| 多明我会拼写 | Hispano-Dominican missionary orthography | ortografía misionera hispano-dominica | 17 世纪西班牙多明我会士记录闽南语的拼写系统：`c-/qu-/ch-/g-/s-/z-/ttz-` 及 `-p/-t/-c/-h` 等 |
| 冻结区 | frozen zone | zona congelada (solo lectura) | `workspace_m1_dhs306/`，M1 封盘后只读，发现问题一律入四账，严禁就地修改 |
| 官话对音（R 栏） | Mandarin gloss column (Column R) | glosa en mandarín (columna R) | 手稿第四栏的早期官话罗马字读音对照（及同格并列多词形） |
| 后设数据/封存清单 | seal manifest | manifiesto de sellado SHA-256 | `BLIND_READ_MANIFEST.json` 等前置 SHA-256 对账总账 |
| 基线初稿 | baseline first draft | borrador base de referencia | 22 源既有初稿（`baseline_all22_extracted/`），含参考辅助校对稿，严禁在盲读阶段偷读 |
| 几何调码 | geometric tone codes | códigos tonales geométricos | 按手稿调符纯几何形态记录的八个代码 `T00–T07 / T99`（非调值推论），见 [TONE_MARKS.md](TONE_MARKS.md) |
| 交叉入声号 | entering-tone cross mark | cruz de tono de entrada (*rùshēng*) | `T06/T07`：两条短线交叉的入声几何标记 |
| 静默缺页 | silent page gap | laguna de páginas silenciosa | 总条目数达标但个别页面缺失或因异构 ID 漏检——须由页面覆盖审计发现并逐项处理 |
| 九条书组线 | nine document lines | nueve líneas documentales (líneas de obra) | 22 份源 PDF 按文献性质分组形成的 9 条执行线（见 [SOURCES.md](SOURCES.md)） |
| 盲读 | pure visual blind read | lectura ciega puramente visual | 只依据页面切片图像的转写，禁止读取旧稿或凭音韵先验"修正"字面；本库核心协议（v3.1） |
| 生理人 Sangley | Sangley (Manila Hokkien Chinese) | sangley (chino minnan de Manila) | 16–17 世纪旅居马尼拉的闽南语华人（源自闽南语「生理人」*seng-lí-lâng*）；本库文献的核心社群 |
| 四账分离 | four-ledger separation | separación en cuatro libros de registro (*ledgers*) | 未决字形 / 缺证音值 / 词义未定 / 未执行工序四本独立台账（见 [LEDGERS.md](LEDGERS.md)） |
| 台罗（MOE） | Tâi-lô (MOE Romanization) | romanización Tâi-lô (MOE) | 台湾教育部台湾台语罗马字拼音方案；本库仅作 `Layer 4` 现代参照，严禁冒充 17 世纪历史音值 |
| 提交封存 | commit & seal | confirmación y sellado (*commit*) | 正字法净化 → 音系推导 → 写盘 → SHA-256 锁入清单的确定性管线流程 |
| 物理页位 | physical page position | posición física de página (pág. PDF) | 源 PDF 中的绝对页序（含封面/空白/现代分册页），22 源合计 3,139 个物理页位 |
| 页面覆盖审计 | page-coverage audit | auditoría de cobertura de páginas | 按页码核对各封存账，防"总数达标但页面缺块" |
| 一次性产出 | single-pass transcription | transcripción de una sola pasada | 盲读为单遍视觉产出，写盘即冻结，必须经下游人工校对（`COLLATION_GUIDE.md`）逐条核验忠实性 |
| 原稿音写（M 栏） | manuscript Hokkien spelling (Column M) | grafía hokkien del manuscrito (columna M) | 手稿第三栏：17 世纪多明我会式漳州系闽南语音写 |
| 灾备 | deterministic disaster recovery | recuperación determinista ante desastres | 远端封存数据 + 本地合法持有的原始 PDF + 确定性切片/推导工具链可完整重建施工现场的能力 |
| 照录层 | diplomatic (verbatim) layer | capa diplomática (transcripción literal) | `source_L/H/M/R` 四栏"照所见抄录"，与派生音系层物理隔离 |
