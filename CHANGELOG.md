# 更新日志 / Changelog

> 版本沿革（进度细账与事故记录见 [docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)）。
> 语义化版本：0.x = 施工/校对期；1.0.0 = 首批书卷人工校对完成。

## [0.2.0] — 2026-11-12 · 仓库门面与缺口补读启动

### Added
- 三语 README（汉/英/西）、方法论 METHODOLOGY、实际意义 SIGNIFICANCE（三语）、
  项目历史 PROJECT_HISTORY、使用方法 USAGE（三语）、CC BY-NC-SA 4.0 LICENSE
- `docs/DATA_SCHEMA.md`：M1 主卷七层结构（含 layer_0 视觉锚点与 layer_5 关系标签 TAG-1~5
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
