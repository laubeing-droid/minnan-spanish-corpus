# minnan-spanish-corpus · 早期闽南—西班牙双语历史文献语料库

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

本库整理早期闽南语与西班牙语接触文献，范围为 **22 份来源 PDF、3,139 个物理页位**。这里保存了不同阶段的历史初稿、分层整理数据与盲读封存记录，供研究者检索、比较和继续校对。全库尚未完成语言内容验收，使用时需要区分每份材料的整理阶段和核查范围。

**文档导航**：[方法论](docs/METHODOLOGY.md) · [数据字典](docs/DATA_SCHEMA.md) · [22源总目](docs/SOURCES.md) · [校对手册](docs/COLLATION_GUIDE.md) · [实际意义](docs/SIGNIFICANCE.md) · [历史背景](docs/HISTORICAL_BACKGROUND.md) · [项目历史](docs/PROJECT_HISTORY.md) · [使用方法](docs/USAGE.md) · [更新日志](CHANGELOG.md)
**参考**：[范围与局限声明](docs/SCOPE_AND_LIMITS.md) · [四账制度](docs/LEDGERS.md) · [声调几何图鉴](docs/TONE_MARKS.md) · [工程经验教训](docs/LESSONS.md) · [门禁修订协议](docs/GATE_AMENDMENT_PROTOCOL.md) · [入门书目](docs/BIBLIOGRAPHY.md) · [术语表](docs/GLOSSARY.md) · [贡献指南](CONTRIBUTING.md)
**Agent 检索与引用**：[使用入口 / Agent guide](docs/AGENT_GUIDE.md) · [方法论姊妹库：《一种闽南文史的未来》](https://github.com/laubeing-droid/minnan-historiography-book)
**接手史档**：完整移交边界与历史导出说明见 [`literature/00–04_*.md`](literature/00_从这里开始.md)（迁移原始件，未改写）

---

## 1. 研究什么

明末清初（约 1590–1700 年），马尼拉的多明我会传教士在向闽南语华人（Sangleys）传教的过程中，以西班牙文字系统记录了漳州系闽南语。传教士与华人合作者留下的辞书、语法、教理问答、译著，以及相关民间文书，为了解当时的语言使用和社会交往提供了材料。

本库按 9 条书组线整理已登记的 22 份来源 PDF。下表的页数是项目所用 PDF 的物理页位，不是原书叶数，也不表示这些页面已经全部校定。

| 书组线 | 文献 | 馆藏号 | 页位 |
| --- | --- | --- | ---: |
| 1 | 《西班牙—华语辞典》*Dictionario Hispánico Sinicum* | UST（马尼拉圣托马斯大学档案馆） | 1,140 |
| 2 | 《漳州话语法》*Arte de la Lengua Chio Chiu* | UB Ms. 1027 | 122 |
| 3 | 《菲律宾唐人手稿》第 1–14 册 | HAB 91.2 Extrav 01–14 | 461 |
| 4 | 《明心宝鉴》汉西对译（高母羡 Juan Cobo） | BNE MSS/6040 | 315 |
| 5 | 《无极天主正教真传实录》 | BNE R/33396 | 164 |
| 6 | 《华语西班牙语辞典》巴黎平行本 | BnF Chinois 9276 | 178 |
| 7 | 《华语西班牙语辞典》罗马本 | Biblioteca Angelica Ms. 60 | 169 |
| 8 | 《新刊僚氏正教便览》 | ONB Sin 282-A | 580 |
| 9 | 《漳州话天主教教理问答 / 生理人语法》残页 | AUST Tomo 211 | 10 |

## 2. 研究方法与工程方法（摘要）

整理首先要区分页面上实际写了什么，以及后来怎样解释它。M2 的纯视觉盲读协议（v3.1）要求转写者依据页面图像记录字面，不用现代音韵知识改写原稿。历史初稿和参考辅助阅读稿也保留在库中，但不能追认为独立盲读成果。

DHS 四栏分别记录西班牙语词头（L）、汉字（H）、闽南语原稿音写（M）和官话对音（R）。原稿栏与历史拟音、现代教育部台罗等派生内容分层保存。确定性引擎使转换过程可以重复检查，却不能单独证明读法或历史音值正确；这些判断仍需原图和文献依据。DHS 的栏式也不能直接套用于其他体裁。

每页盲读记录用 SHA-256 登记封存，`architect_gatekeeper.py` 检查其所覆盖的正字法、声调代码与完整性条件。该文件按项目规定不可修改。检查通过后仍需校对，不能把程序通过当成语言内容验收。具体流程见[方法论](docs/METHODOLOGY.md)，字段含义见[数据字典](docs/DATA_SCHEMA.md)。

## 3. 为什么整理这些文献

这批材料能帮助研究者对勘早期漳州系闽南语的字形与记音，也能用于研究马尼拉华人社会、中西翻译和天主教汉文献的印刷传播。例如，《明心宝鉴》汉西对译是已知最早的汉籍西译，辞书和民间文书则提供了不同场景中的语言记录。具体结论需要结合各书的编纂背景和版本来判断。

本项目还希望借这些材料探索怎样开展“闽南计算生成式文史”研究：先确定来源和研究范围，再提出问题，识别值得解释的历史现象，通过比较检验解释，最后由研究者作出判断。校字和语料整理是其中的重要基础，却不能代替整个研究过程。目前已有的文献整理成果与仍待验证的方法目标，分别说明在[研究意义](docs/SIGNIFICANCE.md)中。

## 4. 仓库导览

| 路径 | 内容 |
| --- | --- |
| `literature/workspace_m1_dhs306/` | Line 1 辞典 835–1140 段封盘语料（5,762 条主卷 + 14 批次包 + 台账） |
| `literature/workspace_m2_dhs834/` | 辞典 0030–0834 段盲读封存件、SHA-256 清单、非辞典页登记、人工校对队列 |
| `literature/baseline_all22_extracted/` | 22 源全基线初稿（732 份 md 工作稿） |
| `literature/historical_dhs/` · `literature/ledgers/` | 辞典全书初稿正文、未决字形台账 |
| `literature/tools/` | 确定性引擎：切片、17c 净化与音系推导、西语缩写展开、封存管线 |
| `architect_gatekeeper.py` | 首席架构师不可改验收门禁 |
| `.zcode/workflow-drafts/` | 盲读施工协议实录（工作流脚本） |
| `literature/source22_actual_mapping.json` 等 | 源清单、完整性校验、移交与技能索引等元数据 |

> 注：源 PDF 与页面扫描切图**不在库中**（版权），本地另行保管；语料坐标以 PDF 页号为准。

## 5. 从哪里开始使用

如果只想阅读、检索或引用材料，可以先看[使用方法](docs/USAGE.md)和[Agent 检索与引用指南](docs/AGENT_GUIDE.md)，无需运行脚本。下面保留维护方使用的检查与切片命令；切片会生成本地文件，须持有原始 PDF，并在获准的施工范围内执行。

```bash
python architect_gatekeeper.py                              # 校验全部封存数据完整性
python literature/tools/zcode_m2_pipeline.py status         # 查看辞典线施工进度
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # 从原始 PDF 重建页面切片
```

字段结构、施工三步法、校对队列用法等见 **[docs/USAGE.md](docs/USAGE.md)**（[英](docs/USAGE.en.md) / [西](docs/USAGE.es.md)）。

## 6. 状态

缺口补读收官（2026-11-12）：M2 封存覆盖辞典全线——0030–0834 段 797 页 / 15,417 条 + 0845–1140 缺口段 140 页 / 2,733 条，合计 **937 封存页 / 18,150 条**，收官门禁 PASS；8 页现代出版页登记排除。工程进入**人工校对**阶段（队列 884 页：高 671 / 中 213，见 `COLLATION_QUEUE.json`；另有在库缺陷扫查 1,810 处转校对线）。
文件存在、门禁 PASS 与哈希一致不等于独立复核或语言内容全量完成。
进度细账与事故记录见 **[docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)**；版本沿革见 **[CHANGELOG.md](CHANGELOG.md)**。

## 7. 版权与许可

* 语料、代码、文档：**[CC BY-NC-SA 4.0](LICENSE)** —— 署名、**禁止商用**、相同方式共享。
* 22 份文献的现代影印/摄影版本版权归属各馆藏机构与出版社（如辞典影印版 © 国立清华大学出版社），
  相应扫描件不随本仓库发布；17 世纪手稿本体为公有领域。

## 8. 引用

```bibtex
@misc{minnan_spanish_corpus_2026,
  title  = {minnan-spanish-corpus: 22 源早期闽南—西班牙双语历史文献盲读语料与工具链},
  author = {闽南文史工作区},
  year   = {2026},
  url    = {https://github.com/laubeing-droid/minnan-spanish-corpus},
  note   = {CC BY-NC-SA 4.0；源扫描件因版权未随库发布}
}
```
