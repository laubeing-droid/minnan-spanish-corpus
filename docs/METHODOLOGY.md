# 研究方法论与工程方法 / Methodology

> 本文是本仓库的 canonical 方法论文档（汉语正文）。English summary at §6; versión española prevista tras el cotejo.

---

## 1. DHS 四栏版式的观察层与派生层

以下 L/H/M/R 是 DHS 四栏页的来源角色，不是所有 22 来源通用的固定版式，也不等同于 M1 的六个 `layer_*` 存储对象。历史阅读稿、参考辅助校对、M1 整理层与 M2 盲读封存件须分别说明生成方法，不能统一追认为盲读成果。

按处理职责区分如下：

| 层 | 内容 | 来源 |
| --- | --- | --- |
| L | 西班牙语词头/释义栏照录（缩写展开另属派生层） | 页面视觉 |
| H | 汉字栏（含俗字、[疑:A/B] 存疑标注） | 页面视觉 |
| M | 闽南语原稿音写栏（17 世纪多明我会拼写） | 页面视觉 |
| R | 右栏官话对音 | 页面视觉 |
| 推导层 Ⅰ | 17 世纪漳州音 IPA（历史拟音） | 确定性引擎 `hokkien_17c_converter` |
| 推导层 Ⅱ | 现代教育部台罗对照 | 同上 |

**纪律**：L/H/M/R 四栏是"照所见抄录"的一手层；推导层只读四栏生成，永不回写；MOE 台罗仅作现代参照，
**严禁冒充 17 世纪历史音值**。

## 2. 盲读协议 v3.1（纯视觉铁律）

1. **只依据页面图像转写**。严禁凭音韵知识补写、"修正"或规范化字面；严禁发明音标。
2. **现代拼写禁令**：`source_M` 不得出现现代台罗/白话字特征（k-/kh-/ts-/tsh-/chh-、
   U+030D、ⁿ 上标鼻化符等）；手稿本身的多明我会拼写（c-/qu-/ch-/g-/s-/z-/ttz- 等）照抄所见。
   引擎净化器会把笔误的 ⁿ 归位为元音鼻化，残留者由门禁拦截。
3. **声调几何字典**：手稿声调符按几何形态记录（不是按调值推断）：

   | 代码 | 形态 |
   | --- | --- |
   | T00 | 無標號 |
   | T01 | 升斜 |
   | T02 | 降斜 |
   | T03 | 尖頂帽 |
   | T04 | 凹角 |
   | T05 | 平橫 |
   | T06/T07 | 交叉入聲號 |
   | T99 | 污損難辨 |

4. **栏位标记**：空栏 `[空]`；完全不可辨 `[残]`；汉字难辨抄最可能的字并附 `[疑:A/B]`。
5. **三步施工法**：`slice`（300dpi 横带+纵栏切片）→ 精读员纯视觉转写 `raw_part_pXXXX.json` →
   `commit`（净化、推导、封存）+ `architect_gatekeeper.py` 验收。**严禁直接手写封存件。**

## 3. 盲读封存、完整性校验与不可改门禁

* 每页 `commit` 时：净化正字 → 声调标签规范化 → 西语缩写展开 → IPA/台罗推导 → 写 `blind_read_pXXXX.json`
  → 计算全文件 SHA-256 → 登入 `BLIND_READ_MANIFEST.json`（`status: LOCKED_BEFORE_COLLATION`）。
* `architect_gatekeeper.py` 文件头声明"**STRICTLY FORBIDDEN TO EDIT OR MODIFY**"，任何人（包括施工方自己）
  不得修改。它独立复查：
  * **M1 线**：逐条核对队列 ID、封存批次数、台罗/IPA/依据非空且反模板（同值超限即拒收——防 LLM 批量编造）、
    主卷总条数（5,762）；
  * **M2 线**：逐页 SHA-256 对账、禁用声调代码、`source_M` 现代拼写/鼻化符残留扫描、页条目下限（豁免登记页）。
* 门禁 `[PASS]` 只表示该批满足检查器实际覆盖的工程入库条件，不表示逐字正确、历史拟音已证成、独立复核完成或全量学术验收。盲读封存、人工校对与语言内容验收分别记账。
* 哈希证明字节一致，不证明读者未看旧稿。未有两名互不知结果的独立读者及过程证据，不把封存称为“双盲”。
* raw 原读与净化／规范化结果须分辨，转换可追溯；确定性转换不证明疑字、历史音值或词义正确，证据不足仍保留未决。

## 4. 施工管线与质量机制

```
PDF 原件 ──slice──▶ 300dpi 横带+纵栏 ──▶ 精读员并行盲读 ──▶ merge(现代页过滤)
   ──▶ commit(净化+推导+封存) ──▶ gatekeeper ──▶ 入库登记 ──▶ 人工校对队列
```

* **并行精读 + 修复环**：每 10 页一批并行盲读；入库失败自动派校订员，批次外问题即停即报。
* **缺页大声记账**：两轮派发均失败的页以 high 级 finding 公示，绝不静默缺页。
* **现代出版页登记**：影印版中穿插的现代书名页/版权页/致谢页判定为 `MODERN_FRONT_MATTER`，
  从辞典语料排除并登记于 `non_lexicographic_pages.json`（现登记 8 页：396–399、769–772）。
* **页面覆盖审计**：按页码 ID 扫描各封存账，杜绝"总数对但页面缺块"的隐性缺口
  （本次施工即由此发现 M1 主卷 140 页规律缺块，见 PROJECT_HISTORY）。
* **冷读抽检**：独立子代理对照横带图与封存件 diff，出 clean/minor/major 判定。
* **防循环与一次通过纪律**：读图次数上限、写后禁改——既防模型空转，也防止"越改越像想象"。

## 5. 封存数据模式（schema）

```jsonc
// literature/workspace_m2_dhs834/blind_read_p0621.json（节选）
{
  "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
  "pdf_page": 621,
  "historical_folio": 587,            // 印刷页脚；缺损时估算并注明
  "layout_mode": "DHS_4COL_BILINGUAL",
  "total_positions_recorded": 19,
  "blind_state": "AUDITED_VISUALLY_VERIFIED",
  "entries": [
    {
      "position": 1,
      "source_L": "luna Uena ~ [疑:Uena/llena]",   // 西语栏照录
      "source_H": "月 望",                          // 汉字栏
      "source_M": "güě bǒng",                      // 17c 原稿音写（净化后）
      "source_R": "yũe juáng [疑:juang/vuang]",    // 官话对音栏
      "tone_marks_M": ["T04 (凹角)", "T04 (凹角)"],
      "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"],
      "auto_precomputed": {                        // 确定性推导层（与四栏隔离）
        "reconstructed_17th_c_hokkien": "...",
        "tai_lo_standard": "...",
        "spanish_disambiguated": "...", "abbreviations_expanded": [...],
        "phonological_basis": "..."
      }
    }
  ]
}
```

## 6. English summary

The repository preserves different stages, including reference-assisted drafts and M2 blind-read records. These must not be retrospectively treated as one blind-read corpus. The M2 protocol specifies: transcription follows the page image only
(no phonological "corrections"), the four manuscript columns (Spanish head, Chinese characters,
Hokkien manuscript spelling, Mandarin gloss) are kept verbatim in isolated layers, tone marks are
recorded as **geometric shapes** (T00–T07, T99) rather than inferred tone values, and every page is
SHA-256-sealed at commit. An explicitly immutable gatekeeper re-verifies orthographic purity,
tone codes and seal integrity with anti-template rules that reject batch-fabricated content.
Derivations (17th-c. Zhangzhou IPA, modern MOE Tâi-lô) are computed by deterministic engines into
separate layers and never written back into the source layers. Page-level coverage audits exist to
catch "totals match but pages missing" gaps; non-lexicographic modern publisher pages are excluded
by registration. Limitations: blind reads are single-pass and require the human collation stage
that follows; the MOE layer is a modern reference only.

> Versión española: pendiente del cotejo; el texto chino es canónico.
