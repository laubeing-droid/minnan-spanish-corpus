# M6 释义层只读清点（2026-11-18）

**后续非盲内容修正**：p0286 #3、p0340 #11、p1135 #16/#18，以及 p0086 #5、p0387 #19、p1029 #16、p1137 #17 的主释义已结合原图及论文修订；九份 `codex_M6_preview/nonblind_gloss_fix_receipt*.json` 留存 61 页 81 条不同释义、82 个修订事件的新旧值和来源，其他版本未随之刷新。这不改变下述原有覆盖统计，不构成全书内容验收。

**清点后的确定性修复**：下文记录的是修复前快照。p0102、p0164、p0266 已只添加字符串内引号转义并实际写回第三版；`codex_M6_preview/v3_json_repair_receipt.json` 留有新旧摘要与逐处证据。复验现有第三版 273/273 份可解析、5,560 条位置与封存一致、zh/en 非空；尚缺 830 页，语义未校对。主释义没有因此重产或改动。

范围：读取清册、当前 `blind_read_p*.json` 和释义文件做结构审计；没有读取原图，也没有修改、重产或校对正式释义。清点时仓库 HEAD 为 `df087641d2f33b5e04c8d255c614f8c0c46d60bc`。结构一致不证明译义正确。

## 现状

| 数据层 | 文件 | 可解析 | 缺文件 | 和封存逐页 position 集合 | 已解析条目 |
| --- | ---: | ---: | ---: | --- | ---: |
| `gloss_layer` | 1,103 | 1,103 | 0 | 1,103 页一致；均无重复 | 21,235 |
| `gloss_layer_v2` | 1,103 | 1,103 | 0 | 1,103 页一致；均无重复 | 21,235 |
| `gloss_layer_v3` | 273 | 270 | 830 | 已解析的 270 页一致；均无重复 | 5,499 |

上表三个范围均以清册及当前 1,103 份封存件为准，无页码额外文件；可解析页的 `page` 均匹配，zh/en 均为非空字符串。主释义置信度为 high 9,908 / medium 6,715 / low 4,612；这些是原产物标签，不代表独立验证。v3 已有文件覆盖 p0030–0302，但 `p0102`、`p0164`、`p0266` 无法解析，故实际欠缺完整、可解析第三版共 833 页。主释义结构完整不代表 1,103 页字义已校对，v3 的问题影响第三版及 K≥3 对碰，不应说主释义已缺该三页。仓库当前未见 `COLLISION_LEDGER.json`，不能据此宣称全书三版对碰已完成。

## 三份 v3 损坏文件

均为 JSON 字符串内部双引号未转义：首次解析报错位置分别为 p0102 第 12 行、p0164 第 6 行、p0266 第 9 行；后两份还有更多同类位置。三份均被 Git 跟踪，`git log --all --` 仅见 `66b1a45` 初次加入；其当时、当前 HEAD 与工作区各自的 SHA-256 一致且均不可解析，未找到对应有效历史版本或文件级 v3 清册。

| 页 | 原始 SHA-256 | 需转义引号 | 独立预览条目 |
| --- | --- | ---: | ---: |
| 0102 | `ffb2b0efe21f8ee31ea4da40bbc8557c7c0d57dee958d2b65a90c0ffca1ef220` | 2 | 22 |
| 0164 | `5ba6ca24e49cdce754cb84bd655def973d189d3566ee9355073a629379d772ee` | 64 | 21 |
| 0266 | `b61cb78ebe12881cfcaec16f75d3d764fb2b0f865fc0897c459ffffb7e6efea6` | 44 | 18 |

预览在 `codex_M6_preview/gloss_v3_p0102_syntax_candidate.json`、`gloss_v3_p0164_syntax_candidate.json`、`gloss_v3_p0266_syntax_candidate.json`；`v3_json_repair_preview.json` 逐个记录了原行号、原行 1 基 Unicode 字符列号、字段、原引号、上下文及文件哈希。预览仅在字符串内引号前增加转义反斜杠，去掉这些新增反斜杠后与原始文件逐字节一致；从磁盘重读后均可解析、逐页 position **顺序**与封存一致且无重复、zh/en 非空。预览不修改正式 v3，也不评价词义、读法来源或是否独立。

## 可复用工具与限制

- `.zcode/workflow-drafts/D2D3-释义层生产第一书-937-页.dwf.ts:142` 的 `glossAsk(page)` 给出原有生成口径及 JSON 格式；需要让释义员读最新封存件产出逐页中英释义，没有发现现成的单页确定性释义刷新 CLI。不能以机械复制现有释义冒充重产。
- 同文件 `:98` 的 `GLOSS_VALIDATE_PY` 只比较 position 集合，且 `:245–250` 的外层只检查脚本运行退出码：有缺页或不齐时也可能退出 0 并仅报告统计。它不检查重复位置、非空译义或语义正确性。
- `python literature/tools/build_gloss_review_packets.py` 按现有 `GLOSS_REVIEW_QUEUE.json` **生成抽样中文复核包**，不是刷新器；脚本会覆盖 `gloss_review_workbench/`，本次未运行。`en` 不在该包复核范围。
- `.zcode/workflow-drafts/对碰V3-第一书盲产加对碰-937页.dwf.ts:299` 含三版预筛与后续矩阵裁决草案，但要求完整 v1/v2/v3，且会写工作产物；本次未运行。版本数据或封存件变化后，旧对碰结果不能直接继承。

## 受影响页清单

1. M2 修复账 `applied` 行记录页、位置、字段与 old/new，但当前修复器的 `READY_FOR_SEAL` 只表示 raw 待重封，不能直接视为封存已成功；结合 `seal_and_verify.py` 的实际输入、`deferredTonePages` 和 `commitErrors`、退出结果，逐页对照重封前后封存内容。
2. M3 11 页行重构须按视觉行重新建立释义。即使新旧 position 数或集合相同，position 所代表的视觉行也可能已改变，不能仅凭集合相等沿用旧释义。
3. M5 只从互证台账中计入实际写回并成功重封的页；保留目标页、位置、字段、old/new、来源页和互证标识。预览候选与 deferred 不算实际修改。
4. 以修改前封存快照与重封后封存件逐页比较 position 和 `source_L/H/M/R`、`tone_marks_M/R`；页内增删行或任一字面字段改变均加入 M6 刷新集合。SHA 变化可作提示，但单凭哈希不能断定字面改变；原批 A 账上 `applied` 曾出现未落盘，不能仅以账面数量推断。刷新后逐页记录输入封存版本、输出文件及验证结果；若执行三版终检，相应 v2/v3 和对碰结论的过期范围也要明示。

## 主释义结构复验命令

以下只读命令已实跑：`pages=1103, entries=21235, bad=[]`，退出码 0。失败时列出页码并返回非零；其范围仅为结构和非空，不构成词义验真。

```powershell
@'
import json,sys
from pathlib import Path
m=Path('literature/workspace_m2_dhs834')
pages=sorted(json.loads((m/'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))['pages'])
bad=[];count=0
for p in pages:
 try:
  sealed=json.loads((m/f'blind_read_p{p}.json').read_text(encoding='utf-8'))
  gloss=json.loads((m/'gloss_layer'/f'gloss_p{p}.json').read_text(encoding='utf-8'))
  a=[e['position'] for e in sealed['entries']];b=[e['position'] for e in gloss['entries']]
  if gloss['page']!=int(p) or len(b)!=len(set(b)) or set(a)!=set(b) or any(not isinstance(e.get(k),str) or not e[k].strip() for e in gloss['entries'] for k in ('zh','en')):bad.append(p)
  count+=len(b)
 except (OSError,ValueError,KeyError,TypeError) as e:bad.append(f'{p}:{e}')
print(json.dumps({'pages':len(pages),'entries':count,'bad':bad},ensure_ascii=False))
sys.exit(bool(bad))
'@ | python -X utf8 -
```
