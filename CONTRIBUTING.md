# 贡献指南 / Contributing

> 语言：中文为主，Issue 可用中文、English 或 Español。

---

## 1. 这个仓库接受什么贡献

| 类型 | 方式 |
| --- | --- |
| **盲读校对**（最需要） | 按 [docs/COLLATION_GUIDE.md](docs/COLLATION_GUIDE.md) 领取 `COLLATION_QUEUE.json` 中的页，给出逐条裁决 |
| 转写勘误 | Issue 附 PDF 页号 + position + 栏位 + 目视值；须以原图为证 |
| 台账销账证据 | 对 [docs/LEDGERS.md](docs/LEDGERS.md) 四账中的条目提供图证或平行本对勘依据 |
| 音系学讨论 | 对 `layer_3` 历史拟音的依据提出商榷（附文献依据） |
| 工程改进 | `literature/tools/` 的确定性引擎 bug 或改进（不得改变既有封存数据的字节） |

## 2. 硬边界

1. **禁止商用**：本库为 CC BY-NC-SA 4.0，任何贡献一经合并即同协议发布；
2. **不可改门禁**：`architect_gatekeeper.py` 不接受任何修改建议（包括"改进"）；
3. **冻结区**：`literature/workspace_m1_dhs306/` 只读；问题走 `evidence_ledger/` 入账；
4. **纯视觉纪律**：转写贡献不得以现代拼音/音韵知识"纠正"17 世纪字面；
5. **扫描件不上传**：不要在 Issue/PR 中粘贴原书扫描图——引用 PDF 页号与行位即可。

## 3. Issue 规范

标题格式：`[页号] 一句话`，如 `[p0627 pos21] langⁿ 鼻化符归属`。
正文须含：PDF 页号、条目 position、栏位、现状、你的依据（图上所见/文献）。

## 4. 校对贡献流程

1. 从 `COLLATION_QUEUE.json` 选页（high 优先），在 Issue 报备避免撞车；
2. 按 [COLLATION_GUIDE.md](docs/COLLATION_GUIDE.md) §2 程式逐条裁决；
3. 以文本形式提交结论（不要求改数据文件——数据回写由维护方经 commit 管线统一执行）；
4. 维护方复核后合入并重封存，贡献者进入致谢名单。

## 5. 致谢

实质性贡献者（校对、勘误、音理商榷、工程修复）将记入 README 致谢节与
`docs/PROJECT_HISTORY.md`。
