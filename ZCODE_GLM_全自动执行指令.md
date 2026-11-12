# ZCode (GLM5.3FLASH / 国产视觉与文本模型) 全自动执行指令与本地引擎使用手册

> **架构设计原则（针对 GLM5.3FLASH 能力画像定制）**：
> * **你的强项（直接发挥）**：西班牙语殖民文献阅读、马尼拉 Sangley（生理人）背景史、明清闽南社会名物考据、中文手写繁体与异体字识读、拉丁字母与几何符号抄录。
> * **你的短板（已由本地 Python 确定性引擎 100% 接管，严禁手算或硬猜）**：
>   1. 17 世纪多明我会传教士拼写 $\to$ 17 世纪漳州音 IPA 与教育部标准台罗（`tai_lo_standard`）的音韵推导；
>   2. 17 世纪西班牙语手稿上标缩写（`q̃`, `p.ᵃ`, `m.ᵗᵉ`, `sup.ᵒʳ` 等）的规则展开；
>   3. 第 1 层（`source_M`）严禁混入现代白话字/台罗拼写习惯（严禁出现 `k-`, `kh-`, `ts-`, `tsh-`, `chh-`, 阳入竖线 `\u030d` 或鼻化上标 `ⁿ`）。

---

## 一、 首席架构师已为你预装的 3 大本地 Python 确定性武器

在当前工作区 [`literature/tools/`](file:///d:/Codex/2.闽南文史工作区/闽南文献迁移/literature/tools) 下，已部署好 0 Token 消耗、100% 确定性的本地脚本，**你只需要调用它们，不需要自己手算音标或维护 SHA-256 清单**：

1. **[`literature/tools/zcode_m2_pipeline.py`](file:///d:/Codex/2.闽南文史工作区/闽南文献迁移/literature/tools/zcode_m2_pipeline.py)（一站式切片 + 自动音韵转换 + 门禁入库 CLI）**
   * **查看当前 M2 进度**：
     ```bash
     python literature/tools/zcode_m2_pipeline.py status
     ```
   * **批量生成 300 DPI 横带与子列切片**：
     ```bash
     python literature/tools/zcode_m2_pipeline.py slice --start 30 --end 40
     python literature/tools/zcode_m2_pipeline.py slice --start 71 --end 100
     ```
   * **自动净化、展开西语缩写、计算 17c 漳州 IPA 与台罗、并自动计算 SHA-256 写入 `BLIND_READ_MANIFEST.json`**：
     ```bash
     python literature/tools/zcode_m2_pipeline.py commit --input your_raw_pages.json
     ```
2. **[`literature/tools/hokkien_17c_converter.py`](file:///d:/Codex/2.闽南文史工作区/闽南文献迁移/literature/tools/hokkien_17c_converter.py)**：
   * 自动将 `source_M` 净化为纯正 17 世纪多明我会拼写（自动修复误写的 `k-`/`kh-`/`ts-`/`-̍`/`ⁿ`），并根据 `source_M` + `source_H` + `tone_marks_M` 自动算出 `reconstructed_17th_c_hokkien` 与 `tai_lo_standard`。
3. **[`literature/tools/spanish_17c_expander.py`](file:///d:/Codex/2.闽南文史工作区/闽南文献迁移/literature/tools/spanish_17c_expander.py)**：
   * 自动展开 60+ 种 17 世纪西班牙语手稿缩写，并自动识别 `cuxin`（舉人）、`sangley`（生理人）、`parian`（澗內/八連）、`champan`（舢舨）等马尼拉唐人借词。

---

## 二、 你的标准工作流（以每 10 页为一轮，循环推进 M2）

> **注意**：M1 线（`PDF 0835–1140` 共 306 页、5,762 条）已经 100% 完工封盘，**严禁修改 `literature/workspace_m1_dhs306/` 下的任何文件**！你只负责推進 **M2 线（`PDF 0030–0040` 及 `PDF 0071–0834`）**。

### Step 1：运行切片命令
每次切 10～15 页（先做 `30..40`，再做 `71..834`）：
```bash
python literature/tools/zcode_m2_pipeline.py slice --start 30 --end 40
```

### Step 2：看图抄录四栏字面（只做纯视觉抄录，不猜音标！）
读取 `literature/tiles/01_DHS/page_XXXX/` 下的高清横带图（`pdf_XXXX_band_y0_top.png`、`band_y1_mid.png`、`band_y2_bot.png`），按行生成简单的 JSON 文件（支持单页或多页数组），格式如下：
```json
[
  {
    "pdf_page": 71,
    "historical_folio": 38,
    "page_header": "A. ante. G.",
    "page_footer_printed": "- 38 -",
    "entries": [
      {
        "position": 1,
        "source_L": "西语原文字面（保留原缩写如 q̃, p.ᵃ, m.ᵗᵉ）",
        "source_H": "手稿第2栏繁体汉字",
        "source_M": "手稿第3栏17世纪传教士闽南语拼写（严禁用c-/qu-/ch-，禁写现代k-/kh-/ts-）",
        "source_R": "手稿第4栏右栏官话或批注（若空则写 [空]）",
        "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
        "tone_marks_R": []
      }
    ]
  }
]
```
* **声调视觉几何编码唯一合法字典**：
  * `T00 (無標號)`、`T01 (升斜)`、`T02 (降斜)`、`T03 (尖頂帽)`、`T04 (凹角)`、`T05 (平橫)`、`T06/T07 (交叉入聲號)`、`T99 (污損難辨)`。

### Step 3：调用 `zcode_m2_pipeline.py commit` 自动合成音韵与门禁锁
```bash
python literature/tools/zcode_m2_pipeline.py commit --input raw_batch.json
python architect_gatekeeper.py
```
`commit` 命令会自动帮你把西语缩写展开、算出 17 世纪漳州 IPA 与教育部台罗、写入 `literature/workspace_m2_dhs834/blind_read_pXXXX.json` 并更新 `BLIND_READ_MANIFEST.json` 的 SHA-256！
