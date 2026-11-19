# ZCode 可核查信息源登记册（2026-11-19 建档）

用途见 `zcode_workflow_protocol.md` 第五节。所有外部来源在**引用时**须按实际访问版本核对页码（L52/L64）；本登记册记录的是入口，不是引文本身。

## 一、项目自有（本地，权威层）

| 资源 | 路径 | 说明 |
| --- | --- | --- |
| DHS 底本影印 | `literature/history_and_sources/01_丛刊一_西班牙-华语辞典_Dictionario_Hispánico_Sinicum.pdf` | 第一书本体；字面层唯一权威是页面墨迹 |
| 丛刊诸册影印 | `literature/original_sources/*.pdf` | 漳州话语法、菲律宾唐人手稿、明心宝鉴等 22 个 PDF |
| 已核实书目 | `docs/BIBLIOGRAPHY.md` | Klöter 2011、van der Loon 1966/67、連金發 2023、周振鹤 2018 论文集、丛刊各册 ISBN/链接 |
| Klöter/李导读文本 | `literature/reference_bibliography/REF-02_Kloten_and_Li_introductions_dhs_p23_p29.txt` | 丛刊一导读 p23–p29 |

## 二、晚清–民国闽南语辞书（音值/词义旁证层）

⚠️ 这些是厦门腔后期资料，比 DHS 晚 200–300 年；只能佐证「该音节/词在闽南语中的存在与通常拼读」，**不能证明 17 世纪墨迹、也不能按其拼写改写历史字面**。

| 辞书 | 年份 | 可核查入口（2026-11-19 核实） |
| --- | --- | --- |
| 甘为霖《厦门音新字典》（甘字典，约 15,000 字头） | 1913 | GitHub 数据库 [TongUanLab/CampbellAmoyDict](https://github.com/TongUanLab/CampbellAmoyDict)（信望爱仓库校订版 fork）、[ChhoeTaigi/ChhoeTaigiDatabase](https://github.com/ChhoeTaigi/ChhoeTaigiDatabase)（台语数位典藏）；原书扫描 [archive.org dictionaryofamoy00camp](https://archive.org/details/dictionaryofamoy00camp) |
| Douglas《厦门方言英汉辞典》（漳泉腔变体并收） | 1873 | [archive.org chineseenglish00doug](https://archive.org/details/chineseenglish00doug)、[另一扫描本](https://archive.org/details/chineseenglishdi00doug) |
| Medhurst《Hok-këèn 方言辞典》（约 12,000 字） | 1832 | [archive.org dictionaryofhokk00medhrich](https://archive.org/details/dictionaryofhokk00medhrich)、[全文文本](https://archive.org/stream/dictionaryofhokk00medhrich/dictionaryofhokk00medhrich_djvu.txt) |

## 三、同期（16–17 世纪）西语–闽南资料（同期参照层，最贴近 DHS）

| 资料 | 年代 | 可核查入口（2026-11-19 核实） |
| --- | --- | --- |
| **Bocabulario de la Lengua Sangleya**（马尼拉匿名教士手稿辞典） | 约 1617 | 奥地利格拉茨大学 Early Manila Hokkien (EMHo) 数位学术版（GAMS 平台）；项目介绍 [Zenodo 记录](https://zenodo.org/records/16023787)；Döhla 专著 2024 由 John Benjamins 出版（[书目页](https://benjamins.com/catalog/hl.00170.doh)） |
| Arte de la lengua chio chiu（现存最早闽南语语法手稿） | 17 世纪 | 见 Klöter 2011 *The Language of the Sangleys*（Brill，本地无全文；按 BIBLIOGRAPHY 途径获取） |
| 高田時雄〈SANGLEY 語研究的一種資料〉 | 2009 | [作者公开全文](https://www.zinbun.kyoto-u.ac.jp/~takata/sangley.pdf) |
| van der Loon "The Manila Incunabula and Early Hokkien Studies" | 1966/67 | *Asia Major* 12(1) 1–43、13(1-2) 95–186；JSTOR/图书馆途径 |
| 連金發 "In Search for the Dialectal Variants of Hokkien…" | 2023 | Harrassowitz 文集（ISBN 9783447120654）；图书馆途径 |
| 周振鹤编《中欧语言接触的先声》 | 2018 | 复旦版（ISBN 978-7-309-13164-2），含 Klöter、洪惟仁诸篇 |

## 四、Gil 论文（M6 释义引用曾用）

本地**未存档**（Codex 时为临时下载）。使用前须重新检索并按实际版本核页码；引文页码与辞典影印页分别记录（L52/L64 事故教训）。

## 五、使用规则摘要

1. 字面层：墨迹唯一权威；外部资料只是旁证（协议第三节三层置信度表）。
2. 声调几何码（T01–T05/T99）与任何现代调类体系**不互相折算**；甘/Douglas/Medhurst 的调值记法只作「该音节存在、通常读法」的旁证。
3. 每条引用入库时记：来源名 + 版本/印页 + URL/路径 + 访问日期；释义刷新回执带引用字段。
4. 每批 S0 步骤按需深挖本册入口；新来源先核可访问性再入库本册。

## 六、独立把门专用（2026-11-19 增设）

| 资源 | 位置 | 纪律 |
| --- | --- | --- |
| 甘为霖《厦门音新字典》本地库 | `_external_refs/campbell_amoy/main.csv`（[TongUanLab/CampbellAmoyDict](https://github.com/TongUanLab/CampbellAmoyDict) 深克隆，MIT 许可，24,387 条：白话字/汉字/文读/台罗/页码） | **未提交仓库**（本地参照）；检索工具 `literature/tools/campbell_lookup.py`；页码按 1961 年第 8 版/2006 年第 19 版 8 刷，**非 1913 原版页码**；台罗/白话字风格经库方校订，引用时注明「甘字典（TongUanLab 校订版）」 |
| 《汇集雅俗通十五音》漳州版数位库 | [thothit/ngeesiokthong](https://github.com/thothit/ngeesiokthong)（同源 TongUanLab 维护；整理方注明：**现只出文读音**、系多源参校，可能与原书有出入；白读音待公开） | **备用**；正式判定以本地韵书原件为主；⚠️ 同名潮州版（1915《十五音全本》/《击木知音》，潮汕音系）严禁混入 |

## 七、用户供料（2026-11-19 就位，参照专用）

- **本地韵书库** `D:\Codex\2.闽南文史工作区\清代民初閩方言韻書整理及研究叢書`（侧线会话按用户指示剥离，主目录仅闽南 4 卷）：
  1. 《八音定訣》整理及研究.pdf（**葉開溫，1894 年觉梦氏序本**——整理本核实；此前登记「1875 叶开恩」系误，2026-11-19 晚经摘要子代理以页码证据更正；兼漳泉二腔、近厦门远郊及同安"古同安音"）
  2. 《增補彙音》整理及研究.pdf（1820 漳州）
  3. 《彙集雅俗通十五音》整理及研究.pdf（1818 漳州，漳浦音系）——⚠️ 同名潮州版（击木知音/潮声十五音/潮语十五音/潮声十七音）已剥至子目录，严禁混用
  4. 《渡江書十五音》整理及研究.pdf（漳州）
  - **铁律（用户明令）**：只作参照，不得反推明末读音（协议第五节 4）。
  - **知识摘要**：`knowledge_briefs/`（八音定訣已完成：含检索方法【整理本无检字表，按部→声母→八音翻页，●有字○空栏】、工作示例、对照 apparatus；另三册在途）
- 《汇音妙悟》（泉州 1800）暂未在本地库；网络扫描未获可靠入口，继续等供料。
- MacGowan《厦英辞典》1883：[archive.org Cornell 扫描](https://archive.org/details/cu31924023550878)已核实，用时下载。

## 变更记录
- 2026-11-19：建档；甘/Douglas/Medhurst/Sangley 辞书四处入口经 WebSearch 核实。
- 2026-11-19（二）：增设独立把门专用区——甘字典本地库（TongUanLab 校订版，MIT）+ 检索工具；收录 MacGowan 1883、漳州版十五音数位库（备用）；《汇音妙悟》《十五音》漳州版原件待用户供料；潮州同名版警示入库。台日大辞典经 [ChhoeTaigi](https://github.com/ChhoeTaigi/ChhoeTaigi)（47 库）可查，用时取用。
