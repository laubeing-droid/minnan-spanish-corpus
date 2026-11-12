# 数据字典 / Data Schema（双 schema 对照）

> [中文 canonical]。解析数据前必读。所有 JSON 均为 UTF-8（`ensure_ascii=False`）。
> 本文档由实测字段并集生成（M1 主卷 5,762 条全字段核查；统计见文末）。

---

## A. M1 主卷七层结构

文件：`literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json`
顶层：`{ "entries": [ ... ] }`，共 5,762 条。每条 `entry_id` 形如 `DHS0835-01`（`DHS` + PDF 四位页码 + 页内序号）。

| 层 | 字段 | 含义 |
| --- | --- | --- |
| `layer_0_visual_anchor` | `page_pdf` / `page_folio` / `position_in_page` / `bounding_box_hint` | 视觉锚点：PDF 页号、手稿叶码、页内行位、行版式提示（如 "row 01, 4-column layout"） |
| `layer_1_diplomatic_raw` | `source_L` / `source_H` / `source_M` / `source_R` | **照录层**：西语词头（含圈线等版面记号照录）、汉字、闽南语原稿音写、官话对音。允许为空字符串 |
| `layer_2_disambiguation` | `spanish_disambiguated` / `abbreviations_expanded` / `zh_disambiguated` / `en_disambiguated` / `syntactic_notes` | 消歧层：西语缩写展开与词头定形；中/英释义；句法备注 |
| `layer_3_historical_phonology` | `dhs_tone_class` / `reconstructed_17th_c_hokkien` / `phonological_basis` | 历史音系层：声调类（几何代码数组）、17 世纪漳州音重构、逐条音理依据 |
| `layer_4_modern_tai_lo` | `tai_lo_standard` / `moe_code` / `hanzi_standard` | 现代参照层：教育部台罗标准形、MOE 编码、标准字形 |
| `layer_5_relationship_tag` | `tag` / `definition` / `rationale` | 关系标签层：词条与 handoff 基线的对勘关系 + 逐条理由 |

### layer_5 标签体系（全库实测分布）

| 标签 | 定义（原文） | 条数 | 占比 |
| --- | --- | ---: | ---: |
| TAG-1 | Direct lexical/semantic or cultural institutional calque（直接词汇/语义或文化直承） | 5,552 | 96.4% |
| TAG-4 | Institutional calque / paraphrastic cultural gloss（机构承借/释译性文化注） | 146 | 2.5% |
| TAG-2 | Near synonym / register or stylistic differentiation（近义/语域风格分化） | 50 | 0.9% |
| TAG-3 | Contextual extension / polysemic gloss（语境引申/多义注） | 10 | 0.2% |
| TAG-5 | Divergent / asymmetric translation（歧异/非对称翻译） | 4 | 0.1% |

### 示例（`DHS0835-01`，截取）

```jsonc
{
  "entry_id": "DHS0835-01",
  "layer_0_visual_anchor": { "page_pdf": 835, "page_folio": 797,
    "position_in_page": 1, "bounding_box_hint": "row 01, 4-column layout" },
  "layer_1_diplomatic_raw": { "source_L": "preguntar〔L01–02圈線相接，01下另有橫弧〕",
    "source_H": "", "source_M": "", "source_R": "" },
  "layer_2_disambiguation": { "spanish_disambiguated": "preguntar〔…〕",
    "abbreviations_expanded": [], "zh_disambiguated": "問、詢問",
    "en_disambiguated": "Ask; inquire.", "syntactic_notes": "…" },
  "layer_3_historical_phonology": { "dhs_tone_class": ["T01 (升斜)", "T05 (平橫)"],
    "reconstructed_17th_c_hokkien": "sio¹ hue⁵", "phonological_basis": "…" },
  "layer_4_modern_tai_lo": { "tai_lo_standard": "sio-huê", "moe_code": "", "hanzi_standard": "" },
  "layer_5_relationship_tag": { "tag": "TAG-1", "definition": "…", "rationale": "…" }
}
```

## B. M2 逐页封存件

文件：`literature/workspace_m2_dhs834/blind_read_pXXXX.json`（每 PDF 页一份，由 `commit` 管线生成，**禁止手写**）。

| 字段 | 含义 |
| --- | --- |
| `protocol_version` | 固定 `v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT` |
| `pdf_page` / `historical_folio` | PDF 页号 / 印刷页脚叶码（缺损时估算并在原始件 notes 注明） |
| `layout_mode` | `DHS_4COL_BILINGUAL`（正编）/ `DHS_2COL_SUPPLEMENT_NO_HANZI`（补充本） |
| `image_source` | 本页 300dpi 整页图路径（图不入库，可由 PDF 重建） |
| `total_positions_recorded` | 条目数 |
| `blind_state` | `AUDITED_VISUALLY_VERIFIED` |
| `page_class` | 空串=辞典页；`MODERN_FRONT_MATTER` / `BLANK` = 非辞典页（登记排除） |
| `entries[]` | `position` + 四栏 `source_L/H/M/R` + `tone_marks_M/R` + `auto_precomputed` |

`tone_marks` 只允许八个几何代码字面（见 [TONE_MARKS.md](TONE_MARKS.md)）；`source_*` 栏标记 `[空]`/`[残]`/`[疑:A/B]`。

`auto_precomputed`（推导层，与四栏物理隔离）：`spanish_disambiguated`、`abbreviations_expanded`、
`loanwords_detected`、`reconstructed_17th_c_hokkien`、`tai_lo_standard`、`phonological_basis`。

## C. 清单与队列

* **`BLIND_READ_MANIFEST.json`**：`pages{ "XXXX": { pdf_page, file, entries_count, blind_first_read_sha256, status:"LOCKED_BEFORE_COLLATION" } }` ——SHA-256 对账入口（gatekeeper 逐页复核）。
* **`COLLATION_QUEUE.json`**：`[{ page, can, yi, t99, estimated, severity(high/medium/low), notes }]`——人工校对工作清单，用法见 [COLLATION_GUIDE.md](COLLATION_GUIDE.md)。
* **`non_lexicographic_pages.json`**：被排除的现代出版页登记（现 8 页：396–399、769–772）。
* **四本证据台账**（`literature/evidence_ledger/`）：结构 `{ledger_type, description, entries[]}`，见 [LEDGERS.md](LEDGERS.md)。

## D. 统计快照（本文档生成时）

* M1 主卷：5,762 条；7 层字段在抽样并集中无缺位。
* M2 封存：827 页 / 声调标记 47,720 个（频次见 [TONE_MARKS.md](TONE_MARKS.md)）；数字随缺口补读实时增长。
