# 更新日志 / Changelog

> 版本沿革（进度细账与事故记录见 [docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)）。
> 语义化版本：0.x = 施工/校对期；1.0.0 = 首批书卷人工校对完成。

## [0.2.1] — 2026-11-12 · 前任施工方（Gemini）规则溯源、翻车教训补全、140 页悬案解密与西/英双语审校

### Added & Calibrated
- `docs/LESSONS.md`：前任施工方（Gemini）对 L1–L4、L7、L11 补充规则来历溯源，并在 L14（Codex）之后新增 **L15–L21** 共 7 条亲历翻车教训（`p0059–0070` 现代 POJ/台罗穿越污染逼出正字法禁令与净化器、`p0042–0045` 偷看旧初稿冒充盲读逼出前置哈希封存与三步隔离法、`batch_07–14` `"已考定"` 正则洗稿与 `"tsu-tsu"` 假台罗逼出 `architect_gatekeeper.py` 同值频次 `Counter` 门禁、`T06` 循环论证与 `p0051–0055` 私造几何名逼出八代码纯几何字典、`p0030` `quì` 裁断逼出 6% 软重叠与横纵双轨切片、62 批 8 种异构 schema 与 M1 主卷 5,106 条 Core 空壳合龙自白、四账物理分离来历）
- `docs/PROJECT_HISTORY.md`：新增「二、前任施工期：v3.1 定案、反作弊阻击战与 M1 封盘（Gemini，2026-11-05 ~ 11-06）」，完整记录 P-01~P-08 审定补丁、M1 三次反作弊阻击战、M2 起步三大翻车，并**彻底解密 M1 主卷"140 页规律缺块（每 10 页缺 5）"悬案**（28 个批次 `0845.01`/`DHS1080.01` 异构 ID 导致 `^DHS(\d{4})-` 漏检 + `merge_m1_master_5762.py` 对 5,106 条 Core 记录的 `sio-huê` 空壳合龙缺陷披露）
- `docs/METHODOLOGY.md`：校准 v3.1 六层架构（Layer 0–5）与盲读四栏+两推导层的映射关系，补全 `-k` 塞音韵尾禁令、净化器五项逆向还原逻辑、补丁 P-03 外交层视觉独立原则（禁看韵尾定调号）、6% 中缝重叠规格及门禁 `Counter` 阈值与 `31/32` 页（原稿仅 2 条词条）豁免来历；新增完整西班牙文方法论节要（`§7. Resumen en español`）并润色英文节要（`§6. English Summary`）
- `docs/HISTORICAL_BACKGROUND.md` & `docs/BIBLIOGRAPHY.md`：经联网检索扩充大帆船贸易与漳州月港—马尼拉涧内走廊、多明我会先驱（Miguel de Benavides O.P.、Juan Cobo O.P.、Francisco Blancas de San José O.P.、Melchor de Mançano O.P.）与华人刻工龚容（Juan de Vera）史实；补齐 Piet van der Loon（1966–1967, *Asia Major* N.S. 12.1: 1–43 & 13.1–2: 95–186）、刘莉美（2020《汉学研究》38.2: 215–236；2005《中外文学》33.10: 121–131）及 2023 年西班牙索里亚公爵基金会首届国际西班牙语学研讨会首奖官方西文题名；为 `HISTORICAL_BACKGROUND.md` 新增道地西班牙文与英文学术节要（§四、§五）
- `README.es.md`、`README.en.md`、`docs/SIGNIFICANCE.md`、`docs/GLOSSARY.md`、`docs/USAGE.es.md`：全面清理早期机器翻译遗留的西语硬伤（如英文词未译 `"La scholarship moderna"` / `"finales checking"`、伪西语词 `"disambiguación"` → `"desambiguación"`、链接错指等）与英语语法瑕疵，并与中文正本同步收窄后的学术口径（解除 `update pending`）
- `docs/DATA_SCHEMA.md` & `docs/SCOPE_AND_LIMITS.md`：同步标注 M1 主卷三种 `entry_id` 历史命名实测分布与 5,106 条 Core 记录的合龙占位边界
- `docs/METHODOLOGY.md` §6（新，现任）：递归自我改进闭环（RSI）与硬刹车——闭环图、编译步人守门原则（工作流永不自改脚本，经验总结员只写知识不写代码）、九条硬刹车清单（每条均拦过真实事故）、"校对准确"目标锚定（字面忠实性判断一律不得自动化）；英/西节要顺延为 §7/§8 并在英文摘要补第 5 点

## 文档溯源审校 — 2026-11-12

- 核对 22 源公开登记的页位与哈希锚；区分来源 PDF、独立书、物理页位与语言完成数量。
- 修正 M1 六个 layer 对象、混合 ID 格式及 TAG-1～5 的语义关系口径；不改任何封盘数据。
- 补 52 ZIP 的迁移史、DHS v107 与独立盲读的区别；收窄门禁 PASS、覆盖、复核与全量完成的宣称。
- 补高田時雄、Regalado Trota José、連金發的可核书目；修正丛刊九册与系列编号混淆及 Cobo 会籍。
- 保留不确定书目、原图与完整主卷未重核事项。外文更新待同步处明确标记。
- 本轮只改文档，未运行学术管线或修改受限文件；具体范围见 [审校记录](docs/DOCUMENTATION_AUDIT.md)。

## [0.2.0] — 2026-11-12 · 仓库门面与缺口补读启动

### Added
- `docs/HISTORICAL_BACKGROUND.md`：历史背景——涧内（Parián）与 Sangley 社会场景、1593 圣加布里埃尔
  印刷（龚容 Juan de Vera）、高母羡 Juan Cobo 与《明心宝鉴》、1603 涧内之变、北台湾时期定年证据
  （鸡笼淡水词条）、「Vale muy poco」注记、现代学术接力（van der Loon → 韩可龙 Klöter →
  周振鹤《中欧语言接触的先声》→ 李毓中团队丛刊 9 册与 2023 索里亚公爵奖）及历史/当代人物双表
- 三语 README（汉/英/西）、方法论 METHODOLOGY、实际意义 SIGNIFICANCE（三语）、
  项目历史 PROJECT_HISTORY、使用方法 USAGE（三语）、CC BY-NC-SA 4.0 LICENSE
- `docs/DATA_SCHEMA.md`：M1 主卷结构（旧文称七层；本轮澄清为六个 layer 对象）（含 layer_0 视觉锚点与 layer_5 关系标签 TAG-1~5
  全库实测分布）与 M2 封存件 schema 的对照数据字典
- `docs/SOURCES.md`：22 源总目（馆藏号 / 页位 / SHA-256 锚 / body 初稿映射 / 线状态）
- `docs/COLLATION_GUIDE.md`：人工校对手册（裁决规范、p0621 双版本案、p0041 非规范调标专案）
- `docs/LEDGERS.md`：四账制度（未决字形 8 / 缺证音值 0 / 词义未定 1 / 未执行工序 3，入账销账规则）
- `docs/SCOPE_AND_LIMITS.md`：范围与局限声明（"文件搬迁不增加学术完成数量"）
- `docs/TONE_MARKS.md`：声调几何图鉴 + 全库 47,720 调号频次实测（827 封存页）
- `docs/BIBLIOGRAPHY.md`（只收可确证条目）、`docs/GLOSSARY.md`（三语术语表）、`CONTRIBUTING.md`
- `docs/LESSONS.md`：工程经验教训 13 条（模型施工/确定性管线/编排成本/发布版权四类，
  事故→根因→对策→可迁移性）+ 未解决事项诚实清单
- `docs/`：校对队列与封存 schema 说明
- 缺口补读工作流：M1 主卷页面覆盖审计发现的 140 页缺块（845–849、855–859…）按 M2 协议补读，
  实时进度见 `BLIND_READ_MANIFEST.json`

### Verified
- M2 封存线 0030–0834 全量过门禁：797 页 / 15,417 条；8 页现代出版页登记排除

## [0.1.0] — 2026-11-12 · 首次公开备份

### Added
- M1 封盘语料 `workspace_m1_dhs306/`（5,762 条主卷 + 14 批次包 + 台账，2026-11-06 封盘通过）
- M2 盲读封存件 `workspace_m2_dhs834/`（0030–0834）+ `BLIND_READ_MANIFEST.json` + 校对队列
- `baseline_all22_extracted/`（22 源基线初稿，732 md）、`historical_dhs/` 全书初稿、`ledgers/`
- 确定性工具链 `literature/tools/`（切片 / 17c 净化与音系推导 / 西语缩写展开 / 封存管线）
- 首席架构师门禁 `architect_gatekeeper.py` 与顶层构建脚本
- 元数据：source22 映射、归档完整性、移交清单、技能索引、锁定基线登记

### Excluded（版权/隐私，仅存本地）
- 22 份源 PDF、`tiles/` 扫描切图、读者员裁片（tmp_*/scratch_*）、52 个资产 ZIP、
  参考书目扫描页、slack 交接史

### Fixed（施工期间事故，详见 PROJECT_HISTORY）
- 批次 0621–0630：p0621 原始件尾部截断修复后重入库（189 条）；p0627 一处 `langⁿ` 按引擎规则归位 `lãng`
- 现代出版页门禁墙：396–399（PART 2）与 769–772（PART 3）登记为 `MODERN_FRONT_MATTER` 排除
- M1 主卷页面级覆盖审计：发现 140 页规律缺块（总数达标但页面缺失），转入缺口补读
