# M2 修复器上置字符审计（只读与隔离重放）

审计时间：2026-11-18。数据为 `literature/workspace_m2_dhs834/collision_mr/ADK_ADJUDICATION_LEDGER.json` 中 4,732 条唯一匹配记录，不把旧裁决当成已证实的墨迹真值。正式账及源数据未修改。账 SHA-256：`598eb965f917d4244abd42f86bd04c45a24bd9efa03e1ac6aba5026e09ef2a15`；修复器 `literature/tools/repair_batch_a.py` SHA-256：`96d49f08e118f0ebf0976f957b1c7501a86d3e072430f87fa893cb296741446d`。

## 实存范围

`soup()` 的第 29–32 行把 `ⁿ` 映为普通 `n`，遗漏名称不以 `LATIN ` 开头的上置或修饰字符 `ᶜ`、`ᵛ`，也遗漏名称为 `COMBINING LATIN ...` 的组合字母。排印符号的历史功能仍需核图，不能预先把它们都断言为字母、声调或正确读法。

4,732 条唯一匹配记录中，3,370 条判为“重读对”或“两皆误”。其中 **22 条**“两皆误”记录的 V1 与 ink 按现有 soup 相等，但按保留修饰字母及组合上置拉丁字母的比较法不同，涉及 10 页。以当前队列、回执、封存及 raw 条件只读筛查，10 条满足进入字母汤比较的前置条件；另 12 条因目标重复或 raw 与封存不一致先被延迟，两类原因有重叠。

对 0046、0047、0054、0082、0182 的冻结队列、账、回执及相关封存/raw 复制到临时目录，复制修复脚本，仅在 `old == v1 and soup(old) == soup(ink)` 跳过分支插入一行打印，不改条件，在副本运行 5 页。实际共打印 23 条整栏字母汤跳过，其中以下 **10 条**存在上置字母差异：

| 页 | position | 栏 | 数量说明 |
|---|---:|---|---|
| 0046 | 4、6 | R | 各 1 |
| 0047 | 20 | M | 1 |
| 0054 | 15、16、19 | M/R | position 15 M/R、16 M/R、19 R，共 5 |
| 0082 | 15 | source_R | 1 |
| 0182 | 5 | R | 1 |

复现的临时目录为 `C:/Users/being/AppData/Local/Temp/codex_m2_modifier_audit_dku7zoqt`；运行在副本中产生的批次账和 5 页 raw 仅属测试，不得误认作正式修复。本次重放不会证明十条 ink 正确，也不证明它们都应直接写回；它只证明现行工具会把这些差异作为等价跳过，未逐条记为待核。

## 三个可追溯样例

| 页/position/栏 | V1 原文 | 回执 ink 原文 | 回执定位 |
|---|---|---|---|
| 0046/4/R | `chûi taý` | `chûiᶜ tay̌` | `adk/adk_verdict_p0046.json` 第 3 项 |
| 0054/15/R | `tong xin quen` | `tôngᶜ xīn quěnᶜ` | `adk/adk_verdict_p0054.json` 第 25 项 |
| 0182/5/R | `eù tū` | `eù tūᶜ` | `adk/adk_verdict_p0182.json` 第 14 项 |

三例均为“两皆误”，当前 V1 与 ink 的普通字母汤相同，而 ink 含 V1 所无的 `ᶜ`。回执由历史模型产生，相关上置记号性质及 ink 是否忠实仍待独立核图。

## `重读对` 分支的边界

现有 151 条“重读对”中，**未发现**非空 ink 和 rr 同汤但上置字母不同的实例。另有 24 条“两皆误”的 ink 与 rr 满足该现象；两皆误本来允许另给 ink，因此这些记录本身不是误应用证据。

修复器第 295 行仅用 soup 检查“重读对”的 ink 与 rr：未来若出现 `rr=chúi`、`ink=chûiᶜ`，该检查会把它们当相同；这是基于代码的可复现理论例，**不是已发生误写回**。如果真实字段含被 soup 丢弃的上置字符，又有其他普通字母差而通过第 323 行的跳过判断，是否实际写回还受重复目标、raw/封存、调标及音系门禁约束，不能直接推断。

## 最小处置建议

继续保留既有 soup 作为既定“仅普通字母差自动修复”边界；在同汤跳过及 `重读对` 的 ink/rr 一致性判断前，检测两侧上置或修饰字母原码差异，转 `deferred` 并留存原值、位置及回执；不自动转为 applied、不把符号归为声调。覆盖上述真实样例及无上置差异的现有回归。Unicode `Lm` 同时可能包括某些标音符号，统一列为待核比预断其历史功能更稳妥。最终修复仍须经用户要求的 raw → commit → 门禁 → 复扫，并保留 provenance。

## 只读复算 22 条

在仓库根目录将以下 Python 送入 `python -X utf8 -` 即可复算 22 条；这只读账与修复器，不运行修复主程序：

```python
from pathlib import Path
import json, sys, unicodedata
sys.path.insert(0, str(Path("literature/tools").resolve()))
from repair_batch_a import soup

def strict(text):
    text = unicodedata.normalize("NFD", text or "").lower()
    return "".join(c if unicodedata.category(c) == "Lm" or
                   unicodedata.name(c, "").startswith("COMBINING LATIN") else soup(c)
                   for c in text)

path = Path("literature/workspace_m2_dhs834/collision_mr/ADK_ADJUDICATION_LEDGER.json")
rows = json.loads(path.read_text(encoding="utf-8-sig"))["rows"]
risks = [r for r in rows if r.get("verdict") in ("两皆误", "重读对")
         and r.get("v1") and r.get("ink")
         and soup(r["v1"]) == soup(r["ink"])
         and strict(r["v1"]) != strict(r["ink"])]
print(len(risks), len({r["page"] for r in risks}))
```
