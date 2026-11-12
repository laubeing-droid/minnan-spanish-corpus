# minnan-spanish-corpus · 早期闽南—西班牙双语历史文献语料库

[简体中文](README.md) | [English](README.en.md) | [Español](README.es.md)

> 17 世纪马尼拉多明我会与华人（Sangley）社群遗留的 **22 份闽南语—西班牙语双语历史文献**：
> 以可复现的工程方法完成的全文盲读转写、历史音系推导与校对语料库。

**文档导航**：[研究方法论](docs/METHODOLOGY.md) · [实际意义](docs/SIGNIFICANCE.md) · [项目历史](docs/PROJECT_HISTORY.md) · [使用方法](docs/USAGE.md) · [更新日志](CHANGELOG.md)

---

## 1. 研究什么

明末清初（约 1590–1700 年），多明我会传教士在马尼拉为向闽南语华人（Sangleys）传教，
以西班牙文字系统记录了漳州系闽南语，并留下辞书、语法、教理问答、译著与民间文书。
本工程对现存的 **22 份原件（合计 3,139 个物理页位，分 9 条书组线）** 进行工业化语料整理：

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

* **纯视觉盲读协议（v3.1）**：转写只依据页面图像，严禁以音韵知识"修正"字面——保证语料是 17 世纪书手的独立证据，而非现代人的重构。
* **六层数据隔离**：西语词头（L）、汉字（H）、闽南语原稿音写（M）、官话对音（R）四栏照录；再由确定性引擎推导 17 世纪漳州音 IPA 与现代教育部台罗对照，推导航与原始栏物理隔离，互不污染。
* **双盲哈希封存 + 不可改门禁**：每页转写落盘即记 SHA-256；`architect_gatekeeper.py`（声明不可修改）独立校验正字法纯度、声调代码合法性与封存一致性，反模板、反伪造。
* 全部细节见 **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)**。

## 3. 实际意义（摘要）

为 17 世纪漳州闽南语提供最早、最大规模的**共时字形—字音对勘语料**；为马尼拉华人社会史、
中西翻译史（含已知最早的汉籍西译《明心宝鉴》）、天主教汉文献传播史提供结构化一手材料；
同时示范一套**濒危手稿可复现数据化**的工程范式。详见 **[docs/SIGNIFICANCE.md](docs/SIGNIFICANCE.md)**。

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

## 5. 快速上手

```bash
python architect_gatekeeper.py                              # 校验全部封存数据完整性
python literature/tools/zcode_m2_pipeline.py status         # 查看辞典线施工进度
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849   # 从原始 PDF 重建页面切片
```

字段结构、施工三步法、校对队列用法等见 **[docs/USAGE.md](docs/USAGE.md)**（[英](docs/USAGE.en.md) / [西](docs/USAGE.es.md)）。

## 6. 状态

工程进行中：盲读封存已覆盖辞典全线，现处**人工校对**阶段。
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
