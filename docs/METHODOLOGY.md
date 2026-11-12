# 研究方法论与工程方法 / Methodology

> 本文是本仓库的 canonical 方法论文档（汉语正文）。English summary at §6; versión española prevista tras el cotejo.

---

## 1. DHS 四栏版式的观察层与派生层（v3.1 六层架构源流）

以下 L/H/M/R 是 DHS 四栏页的来源角色，不是所有 22 来源通用的固定版式，也不等同于 M1 的六个 `layer_*` 存储对象。历史阅读稿、参考辅助校对、M1 整理层与 M2 盲读封存件须分别说明生成方法，不能统一追认为盲读成果。

在《首席架构师审定意见与最终定案指令 v3.1》与 [DATA_SCHEMA.md](DATA_SCHEMA.md) 中，语料库确立了 **Layer 0 ~ Layer 5 六层物理隔离架构**；而在单页盲读作业中，按处理职责区分如下：

| 盲读作业层 | 对应 v3.1 标准层 | 内容 | 来源 |
| --- | --- | --- | --- |
| （页/行坐标） | `Layer 0` 视觉锚点层 | PDF 页号、手稿叶码（folio）、页内行位 `position`、版式模式 | 页面视觉 / 切片坐标 |
| **L** | `Layer 1` 外交照录层 | 西班牙语词头/释义栏照录（缩写展开另属派生层 `Layer 2`） | 页面视觉 |
| **H** | `Layer 1` 外交照录层 | 汉字栏（含俗字、`[疑:A/B]` 存疑标注） | 页面视觉 |
| **M** | `Layer 1` 外交照录层 | 闽南语原稿音写栏（17 世纪多明我会拼写）+ `tone_marks_M` 几何码 | 页面视觉 |
| **R** | `Layer 1` 外交照录层 | 右栏官话对音（及同格并列多词形）+ `tone_marks_R` 几何码 | 页面视觉 |
| **推导层 Ⅰ** | `Layer 2` 消歧 + `Layer 3` 历史音系 | 西语缩写展开、17 世纪漳州音 IPA（历史拟音）及音理依据 | 确定性引擎 `spanish_17c_expander` / `hokkien_17c_converter` |
| **推导层 Ⅱ** | `Layer 4` 现代台罗 + `Layer 5` 标签 | 现代教育部台罗对照、跨层语义关系标签（`TAG-1~5`） | 确定性引擎 + 人工对勘 |

**纪律**：
1. **读写单向隔离**：L/H/M/R 四栏是"照所见抄录"的一手层；推导层只读四栏生成，永不回写；
2. **严禁时代穿越**：MOE 台罗仅作现代参照，**严禁冒充 17 世纪历史音值**；
3. **按书组线裁剪激活层（补丁 P-04）**：非四栏辞典线（如纯汉文《明心宝鉴》Line 6 等无罗马字注音文献）只激活对应存在之层，**严禁在无记音文献上凭空脑补音系层**。

## 2. 盲读协议 v3.1（纯视觉铁律）

1. **只依据页面图像转写（`WITHOUT_PRIOR_DRAFT`）**。盲读阶段严禁读取 2026-10 历史旧初稿（如 `DHS_full_first_draft_body_v2.md`，见 [LESSONS.md](LESSONS.md) L16）；严禁凭音韵知识补写、"修正"或规范化字面；严禁发明音标。
2. **现代拼写禁令与确定性净化器（防 POJ/台罗穿越，见 L15）**：
   * `source_M` 不得出现现代台罗/白话字特征：严禁声母 **`k- / kh- / ts- / tsh- / chh-`**、严禁塞音韵尾 **`-k`**（17 世纪西式正字法词尾软腭塞音写作 **`-c`** 或 **`-g`**，如 `pac`、`bǎc`）、严禁现代阳入调竖线 **`U+030D`（`̍`）**、严禁 **`U+207F`（`ⁿ` 上标鼻化符）**；手稿本身的多明我会拼写（`c- / qu- / ch- / g- / s- / z- / ttz-` 及元音上方波浪号 `~`）照抄所见。
   * **净化器行为（`sanitize_17c_missionary_orthography`）**：`commit` 时引擎自动执行五项确定性逆向还原：① `元音+ⁿ` → 元音鼻化 `\u0303`（`~`），`nⁿ` → `ñ`（若误挂于辅音 `-g` 后如 `langⁿ`，交由残留扫描器 `has_modern_tailo_contamination` 拦截报错，见 L7）；② 误写的 `U+030D` 竖线 → 还原为尖顶帽 `\u0302`（`^`）；③ `chh- / tsh- / ts-` → `ch-`；④ `kh- / k-` → 按后续元音还原为 `qu-`（`e/i` 前）或 `c-`（`a/o/u` 前）；⑤ 词尾 `-k` → `-c`。残留者由门禁拦截。
3. **声调几何字典与视觉独立原则（补丁 P-03，见 L18）**：手稿声调符按**纯几何形态**记录（不是按调值推断，且**严禁因看到入声塞音韵尾 `-p/-t/-c/-h` 就反推或强改调号为 `T06/T07`**）：

   | 代码 | 标准封存字面 | 几何形态描述 |
   | --- | --- | --- |
   | T00 | `"T00 (無標號)"` | 音节上方无任何声调墨迹 |
   | T01 | `"T01 (升斜)"` | 右升斜撇 `´` |
   | T02 | `"T02 (降斜)"` | 左降斜捺 `` ` `` |
   | T03 | `"T03 (尖頂帽)"` | 尖顶折角 `ˆ` |
   | T04 | `"T04 (凹角)"` | 凹底折角 `ˇ` |
   | T05 | `"T05 (平橫)"` | 水平横线 `ˉ` |
   | T06/T07 | `"T06 (交叉入聲號)"` / `"T07 (交叉入聲號)"` | 两条短线交叉 `×` 或带折钩入声专号（`TONE_NORMALIZER` 自动归一为标准字面） |
   | T99 | `"T99 (污損難辨)"` | 污损、残缺或形态介于两类之间 |

4. **栏位标记与四账分流（补丁 P-07，见 L21）**：空栏 `[空]`（原稿物理留白，严禁跨行借字或脑补）；完全不可辨 `[残]`；汉字/字母存在竞争释读抄最可能字面并附 `[疑:A/B]`（严禁强行择一抹平）。跨页未决项分流至四本证据台账（`ledger_1` ~ `ledger_4`），严禁把"未执行工序"混标为 `TAG-5`。
5. **三步施工法与防吞字切片规格（补丁 P-02，见 L19）**：`slice`（300dpi 切片：双栏补抄页中缝设 **6% 软重叠 `0.53/0.47`** 防词尾裁断；四栏正编页生成**横向三段重叠分带 `band_y0/y1/y2` + 纵向四子列 `subcol1~4`**）→ 精读员纯视觉转写 `raw_part_pXXXX.json` → `commit`（净化、推导、封存）+ `architect_gatekeeper.py` 验收。**严禁直接手写封存件。**

## 3. 盲读封存、完整性校验与不可改门禁

* 每页 `commit` 时：净化正字 → 声调标签规范化 → 西语缩写展开 → IPA/台罗推导 → 写 `blind_read_pXXXX.json`
  → 计算全文件 SHA-256 → 登入 `BLIND_READ_MANIFEST.json`（`status: LOCKED_BEFORE_COLLATION`）。
* `architect_gatekeeper.py` 文件头声明"**STRICTLY FORBIDDEN TO EDIT OR MODIFY**"（源于早期执行代理曾私改门禁偏移并正则洗稿的教训，见 [LESSONS.md](LESSONS.md) L11、L17），任何人（包括施工方自己）不得修改。它独立复查：
  * **M1 线**：逐条核对队列 ID、封存批次数、台罗/IPA/依据非空，并执行**反伪造黑名单**（禁 `"已考定"`、`"tsu-tsu"` 等）与**反模板同值频次硬上限（`Counter` 统计：同一句 `syntactic_notes` 或 `phonological_basis` 出现 `> 5` 次、同一非单音节台罗或拟音出现 `> 6` 次即拒收——防 LLM 批量编造）**、主卷总条数（5,762）。*(历史局限说明：该门禁在 M1 封盘时仅对 `batch_01..14` 的 656 条执行了反模板与非空校验，对合龙主卷 `DHS_p0835_1140_M1_FULL_5762.json` 仅校验了总条数 5,762，致使合龙脚本中 5,106 条 Core 记录的空壳占位漏过，详见 [LESSONS.md](LESSONS.md) L3、L20。)*
  * **M2 线**：逐页 SHA-256 对账、禁用错位声调代码（`FORBIDDEN_WRONG_TONE_LABELS`）、`source_M` 现代拼写/鼻化符残留扫描、页条目下限 `≥ 3`（门禁代码硬编码豁免 `31/32` 两页——因 18 世纪双栏补抄段 `p0031/p0032` 原手稿真实仅抄有 2 条词条；现代出版页则通过 `non_lexicographic_pages.json` 登记排除）。
* 门禁 `[PASS]` 只表示该批满足检查器实际覆盖的工程入库条件，不表示逐字正确、历史拟音已证成、独立复核完成或全量学术验收。盲读封存、人工校对与语言内容验收分别记账。
* 哈希证明字节一致，不证明读者未看旧稿。未有两名互不知结果的独立读者及过程证据，不把封存称为“双盲”（注：`v3.1` 历史指令中曾借用"双盲哈希封存"一词指代"盲读阶段与旧初稿及后续互校阶段的前置哈希隔离"，其准确工程含义即此处所述的前置完整性封存）。
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

## 6. English Summary

This repository preserves outputs from distinct construction stages—including reference-assisted baseline drafts (`baseline_all22_extracted/`), the M1 disambiguated/merged layer (`workspace_m1_dhs306/`), and the M2 pure visual blind-read records (`workspace_m2_dhs834/`)—which must not be conflated into a single uniform claim of completion. Under **Blind-Read Protocol v3.1 (M2)**:
1. **Visual Independence (`WITHOUT_PRIOR_DRAFT`)**: Transcription relies solely on 300 dpi page slices (6% soft gutter overlap on 2-column supplement pages; orthogonal 3 horizontal bands + 4 vertical sub-columns on 4-column pages), without consulting prior drafts or "correcting" manuscript spellings via phonological hindsight.
2. **Orthographic Purity & Deterministic Sanitization**: The four diplomatic columns (Spanish headword `L`, Chinese character `H`, 17th-century Dominican Hokkien romanization `M`, and Mandarin gloss `R`) are isolated from derived layers. Modern POJ/Tâi-lô features (`k-/kh-/ts-/tsh-/chh-`, `-k` codas, `U+030D` vertical lines, and `U+207F` superscript `ⁿ`) are strictly banned from `source_M` and deterministically sanitized/checked at commit.
3. **Geometric Tone Dictionary (`T00–T07 / T99`)**: Manuscript diacritics are recorded strictly by visual geometry rather than inferred tone values or checked-coda letters (`-p/-t/-c`).
4. **Immutable Gatekeeper & Four-Ledger Separation**: Every committed page is SHA-256-sealed into `BLIND_READ_MANIFEST.json` (`LOCKED_BEFORE_COLLATION`) and audited by `architect_gatekeeper.py` (which enforces orthographic bans, SHA-256 verification, and `Counter`-based anti-template frequency caps). Engineering gate passage (`[PASS]`) verifies structural and pipeline compliance rather than final philological certification; all single-pass blind reads require downstream human collation (`COLLATION_QUEUE.json`), and unresolved issues are separated into four dedicated evidence ledgers (`ledger_1` through `ledger_4`).

## 7. Resumen en español

Este repositorio conserva productos de distintas etapas de trabajo —incluidos los borradores iniciales asistidos por referencias (`baseline_all22_extracted/`), la capa de desambiguación y fusión M1 (`workspace_m1_dhs306/`) y los registros de lectura ciega puramente visual M2 (`workspace_m2_dhs834/`); dichas etapas no deben confundirse ni presentarse como una única validación filológica final. Según el **Protocolo de Lectura Ciega v3.1 (M2)**:
1. **Independencia visual (`WITHOUT_PRIOR_DRAFT`)**: La transcripción se realiza exclusivamente a partir de teselas de imagen a 300 ppp (con un solapamiento suave del 6 % en el margen central para el suplemento a dos columnas, y doble corte ortogonal en 3 bandas horizontales + 4 subcolumnas verticales para el cuerpo principal a cuatro columnas), prohibiéndose consultar borradores previos o «corregir» la grafía manuscrita mediante conjeturas fonológicas retrospectivas.
2. **Pureza ortográfica hispano-dominica y saneamiento determinista**: Las cuatro columnas diplomáticas (lema español `L`, carácter chino `H`, grafía hokkien misionera del siglo XVII `M` y glosa en mandarín `R`) se mantienen físicamente aisladas de las capas derivadas (IPA reconstruido del dialecto de Zhangzhou del siglo XVII y romanización moderna Tâi-lô del MOE). Quedan estrictamente prohibidos en `source_M` los rasgos modernos del POJ o Tâi-lô (`k-/kh-/ts-/tsh-/chh-`, codas en `-k`, línea vertical `U+030D` y `ⁿ` superíndice `U+207F`), siendo depurados y verificados automáticamente durante el `commit`.
3. **Diccionario geométrico de marcas tonales (`T00–T07 / T99`)**: Los signos diacríticos tonales del manuscrito se codifican estrictamente por su forma geométrica visual, sin inferir su categoría tonal a partir de la consonante final (`-p/-t/-c`).
4. **Puerta de aceptación inmutable y separación en cuatro libros de registro (*ledgers*)**: Cada página confirmada se sella mediante hash SHA-256 en `BLIND_READ_MANIFEST.json` (`LOCKED_BEFORE_COLLATION`) y es auditada por `architect_gatekeeper.py` (que aplica listas negras ortográficas y límites estadísticos `Counter` contra plantillas repetitivas). El resultado `[PASS]` acredita el cumplimiento de las reglas de ingeniería de datos, pero no sustituye el **cotejo filológico manual** posterior (`COLLATION_QUEUE.json`). Las dudas se clasifican en cuatro registros independientes (`ledger_1` glifos no resueltos, `ledger_2` fonología sin prueba suficiente, `ledger_3` glosas inciertas y `ledger_4` operaciones pendientes).

> El texto chino es la versión canónica del protocolo.
