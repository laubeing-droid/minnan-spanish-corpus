# 使用方法 / Usage

> [中文](USAGE.md) | [English](USAGE.en.md) | [Español](USAGE.es.md)
> 环境要求：Python ≥ 3.10，**零第三方依赖**（全部标准库）。所有命令在仓库根目录执行。

---

## 1. 数据在哪里

| 你想看什么 | 去哪里 |
| --- | --- |
| 辞典 835–1140 段封盘语料（含消歧/音系/台罗六层） | `literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json` |
| 辞典 0030–0834 段逐页盲读封存件 | `literature/workspace_m2_dhs834/blind_read_pXXXX.json` |
| 全库封存总账（SHA-256 对账） | `literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json` |
| 人工校对工作清单（按严重度排序） | `literature/workspace_m2_dhs834/COLLATION_QUEUE.json` |
| 非辞典页（现代书名页等）登记 | `literature/workspace_m2_dhs834/non_lexicographic_pages.json` |
| 22 源基线初稿 | `literature/baseline_all22_extracted/body/` |

## 2. 验证数据完整性

```bash
python architect_gatekeeper.py
```

输出 `[PASS] M1 ...` 与 `[PASS] M2 Gate: N blind-read pages verified`，表示检查器所覆盖的一致性条件通过。这不等于原图读法、历史音值或全库语言内容已经验收，具体检查范围见 [方法论](METHODOLOGY.md) 第 3 节。

`architect_gatekeeper.py` **声明不可修改**。它也承担反伪造检查；不能通过修改验收器使数据通过。

## 3. 查看施工进度

```bash
python literature/tools/zcode_m2_pipeline.py status
```

## 4. 从原始 PDF 重建页面切片

扫描切图（tiles）因版权不入库，但可由你合法持有的原件 PDF **确定性重建**：

```bash
python literature/tools/zcode_m2_pipeline.py slice --start 845 --end 849
# 产出 literature/tiles/01_DHS/page_XXXX/ 下每页 3 张横带 + 4 张纵栏 + 整页 300dpi
```

## 5. 盲读施工三步法（新增/修复页面时）

1. `slice --start X --end Y` 切片；
2. **纯视觉**转写：只看切图，写入 `literature/workspace_m2_dhs834/raw_blind/raw_part_pXXXX.json`，
   结构 `{"pages":[{ ... 仅本页 ... }]}`，页面字段 `pdf_page / historical_folio / page_header /
   page_footer_printed / page_footer_handwritten / entries`；每条 entry 为
   `{position, source_L, source_H, source_M, source_R, tone_marks_M, tone_marks_R}`；
3. 入库并过门禁：

```bash
python literature/tools/zcode_m2_pipeline.py commit --input literature/workspace_m2_dhs834/raw_blind/<你的合并文件>.json
python architect_gatekeeper.py
```

**铁律**：source_M 只许 17 世纪多明我会拼写（c-/qu-/ch-/g-/s-/z-/ttz-），
禁现代 k-/kh-/ts-/tsh-/chh-；tone_marks 只许
`T00 (無標號) / T01 (升斜) / T02 (降斜) / T03 (尖頂帽) / T04 (凹角) / T05 (平橫) /
T06/T07 (交叉入聲號) / T99 (污損難辨)`；空栏 `[空]`、不可辨 `[残]`、存疑 `[疑:A/B]`；
**严禁手写 `blind_read_pXXXX.json`**（封存件只能由 commit 生成）。

## 6. 校对队列用法

`COLLATION_QUEUE.json` 为按严重度排序的页清单：

```json
{"page": 621, "can": 2, "yi": 3, "t99": 1, "estimated": true,
 "severity": "high", "notes": "..."}
```

* `can`/`yi`/`t99` = 该页 [残]/[疑:]/T99 计数；`estimated` = 页码为估算或 notes 含待人工标记。
* 推荐顺序：`high` → `medium`；`page ≥ 835` 的条目为缺口补读新页，优先与相邻页并读。

## 7. 禁止事项

* 修改 `architect_gatekeeper.py`（验收器自我修改 = 验收失效）；
* 手写/直改 `blind_read_pXXXX.json`（只能经 commit 管线生成）；
* 跨书组线混用数据口径（各线完成度分账独立，严禁相加）；
* 在 `source_M` 写入现代拼音或推测音值。

## 8. 常见问题

* **为什么没有 PDF/图片？** 版权：现代影印版归出版社/馆藏所有。语料坐标均以 PDF 页号为准，
  持有合法原件即可按 §4 重建全部切片。
* **encodings 报错？** 本库 JSON 均为 UTF-8（`ensure_ascii=False`），读取请显式 `encoding="utf-8"`。
* **换行/CRLF 警告？** 本仓库**以字节为准**：`.gitattributes` 设 `* -text`，严禁任何自动换行转换——
  换行转换会改写 SHA-256 封存字节并使门禁失配（0.2.3 实测事故：git eol 转换导致 p0905/p0041 失配，
  按清册逆向重建 937 页方恢复）。克隆本仓库后请勿开启 `core.autocrlf`。
