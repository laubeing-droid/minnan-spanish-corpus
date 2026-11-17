# 字面音写封存管线只读审计

**后续处理**：原净化器和门禁未改。现行修复器会将净化会改写候选字面的项列为待核；封存驱动器对 raw 全页先做同样检查，并对非 0030–0040 页核对封存基准与批次 old/new，不一致的页延迟。隔离重跑 p0146 全链 PASS；p0181 检出 7 项净化变化而延迟，原 raw 与封存摘要不变。详见 `codex_progress_M2.md`。

审计时间：2026-11-18；仓库起始提交 `4898830b6fd5c0fbf9d91f7398c51fb45fd10ae9`。本审计未看原图，未修改项目脚本、raw、封存件或清册；仅在系统临时目录调用既有管线作隔离试验。raw 与封存的任何差异都不证明哪一份符合墨迹，也不构成数据损坏结论。

## 发现

`literature/tools/zcode_m2_pipeline.py:123–132,149` 在写 `source_M` 前调用 `sanitize_17c_missionary_orthography()`，将净化结果作为字面值；`literature/tools/hokkien_17c_converter.py:38–87` 无论原图如何，规则性替换上置 `ⁿ`、`ts/tsh/chh`、`k/kh`、词尾 `k` 和 U+030D，另有根据汉字触发的特例，最后做 NFC。代码本身不观察墨迹。这与用户“字面忠实禁止音系修正”的要求存在**机制风险**：如任何上述 raw 字形确为清晰墨迹，管线会改变它。

`architect_gatekeeper.py:220–233` 另直接拒绝 `source_M` 中部分上置 `ⁿ`、U+030D、`k/kh` 和 `ts/tsh/chh`，用户禁止修改该文件。**只有在原图证实被禁字形确实清晰时**，才可断定“原样录入该字形、门禁全绿、门禁不改”互相冲突。本次没有核图，不能把 raw 中的相关字符认作已证实墨迹，也不能编造一个能同时满足三项的绕行方法。

以下文件摘要用于固定本次代码与清册范围：

| 文件 | SHA-256 |
| --- | --- |
| `literature/tools/zcode_m2_pipeline.py` | `7e9d814dad6914569dafa37885e0e9be7f87585da70255f5b6c3e3ebb74c2f1a` |
| `literature/tools/hokkien_17c_converter.py` | `6e170ffdfbceaceea466489d81b587f31293a685b10a9efc340811675d58fc35` |
| `architect_gatekeeper.py` | `470339fa4d58dd85e2eaa0c6dd2665419742393b2eddd27d515e085774396e93` |
| `literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json` | `00202ecdcfe0461f19d976601c1a25df6466dc286eb27f74e55b039f659dd3ad` |

## 全量对照及纯函数模拟

清册 1,103 页中，1,065 页存在对应 raw 且 JSON 可解析，原页与封存条目数、position 集合均相同；共 20,346 行可按 position 对照。另有 38 页没有 `raw_part_pXXXX.json`，其中包括 0030–0040；这不代表封存文件缺页，修复器可在其既定条件下从封存件构造 raw。

| 检查项 | 行数 | 页数 | 范围说明 |
| --- | ---: | ---: | --- |
| raw 与封存的 `source_M` 原值不全等 | 2,404 | 674 | 既有阶段差异；不判断对错 |
| 直接对 raw M 执行净化，输出与输入码点不同 | 2,236 | 670 | 剥掉首尾空白后比较 |
| 其中 NFC 后仍不同 | 2,213 | 667 | 不只是 Unicode 等价表示变化 |
| 其中输入有 `ⁿ`，输出中该符号消失 | 1,719 | 528 | 是上一行范围内可重叠子集 |
| 若使用现有 raw 净化，预测 M 与当前封存不同 | 221 | 97 | 只比较该字段，不代表整页能通过 commit |

分别按每条原 raw 的处理顺序调用净化、音写检查、调标归一化、西语展开及音系推导等纯函数，1,065 页中 **863 页**全部纯函数执行成功；**202 页**至少一项失败，其首个失败原因分别为调标 126 页、音写检查 76 页。此统计不调用正式封存，也不把纯函数成功等同整库门禁通过或视觉正确。

在上述 863 页中，504 页的 1,537 个 raw M 输入会被净化改变，其中 1,162 条去掉 `ⁿ`、206 条命中 `k/kh` 声母规则、103 条命中词尾 `k`、90 条命中 `ts/tsh/chh`、3 条替换 U+030D；类别允许交叠。典型输入/纯函数输出：

| 页/position | raw `source_M` | 净化输出 |
| --- | --- | --- |
| 0077/6 | `hioⁿ sia` | `hiõ sia` |
| 0083/6 | `tng chheng` | `tng cheng` |
| 0119/5 | `kiap` | `quiap` |
| 0171/8 | `to̍k chǔi chià` | `tôc chǔi chià` |

其中 `kiap` 与 `quiap` 等仅是现有原始记录和函数输出；是否是书写者所见，须另外核图。

以这 863 页的现行 raw **整页**模拟输出，再与现行封存六字段逐项比较，四页存在变化：

| 页 | L | H | M | R | 调标 M | 调标 R |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0181 | 8 | 1 | 15 | 8 | 11 | 6 |
| 0184 | 8 | 5 | 17 | 13 | 12 | 12 |
| 0185 | 13 | 15 | 17 | 16 | 13 | 12 |
| 0188 | 13 | 6 | 20 | 18 | 19 | 15 |

这些数是字段差异数，同一条可计多次；可能属于不同工作阶段，不能判定哪个版本正确。修复器已有全页 raw/封存比较保护；但直接调用封存驱动器 `--pages` 时应注意它以既有 raw 为输入，须保证不会把未指定字段退回旧值。

## 隔离管线实跑

将管线输出目录仅在独立 Python 进程中指向 `C:/Users/being/AppData/Local/Temp/codex_literal_audit_s35njsq9`，调用原 `cmd_commit` 读取现有 raw：

- p0181 成功生成临时封存件，与现行封存的六字段差异依次为 L 8、H 1、M 15、R 8、调标 M 11、调标 R 6，与纯函数模拟一致。
- p0119 成功生成临时封存件，六字段与现行封存相同；其中 raw 的 `kiap` 经净化为 `quiap` 后与现行封存相同。
- p0074 因第 4 条残留上置 `ⁿ` 被音写检查拒绝；临时封存件未写出。

以上结果仅属隔离技术试验，未提交到正式封存，不证明字面读法正确。

## 当前修复器的覆盖边界

按现行 `repair_batch_a.py` 的 `same_entries()` 和 `nonstandard_tones()` 原规则，对上述 1,065 页只读计算：357 页 raw 与封存六字段全等且调标规范；570 页六字段不同但调标规范；137 页六字段不同且调标非规范；1 页六字段全等但调标非规范。38 页无 raw 单列，不直接归为失败。

950 个尚无裁决回执的队列页中，分别有 289 页属于“相同且规范”、524 页属于“不同但规范”、137 页属于“不同且非规范”。若后续这些页确需修复，现行保护会使后两类共 661 页进入延迟；这不是说 661 页最终都需要修复。

## RSI 最小建议

1. 不改 `architect_gatekeeper.py`、不手改 `blind_read_p*.json`。在正式修复前，将 raw 与封存差异分为能够逐字段证明仅由现有管线净化造成的情况，以及存在其他差异、旧工作的情况；后者继续保护、单页入账，不能拿旧 raw 直接覆盖现封存。
2. 如需减少可证明的非语义漂移造成的大面积延迟，提出小范围补丁：以现行封存为基准保留完整六字段，在隔离副本中逐页经原 `raw → commit` 计算，验证非目标字段完全相同、目标与回执及旧值一致，再决定是否提交；不可仅凭 raw/封存相似就覆盖。原 raw 应保留。
3. 对原图**实际证实**的门禁禁字符，忠实保存墨迹与来源并列待核，不能仅因音系将其替换成合法字母，也不能对清楚字形伪记 `[残]`；如确与不可修改门禁发生冲突，应记录具体页、位置、字形及两项条件，提请用户裁定。尚未出现这样的视觉实证，不能现在宣称全书有多少处冲突。
4. 对音系映射只在派生字段使用的方案，连同门禁和旧数据影响另写 RSI 编译提案；不能自行改写门禁或冒称已解决。全库门禁通过仅证其既有规则检查通过，不代替原图校对。

## 复算范围

统计按 `BLIND_READ_MANIFEST.json` 中 1,103 个页键定位 `raw_blind/raw_part_pXXXX.json` 与 `blind_read_pXXXX.json`；raw 可为单页对象或 `pages` 数组。相同 position 才比较六个字段，调用的都是上述管线原有纯函数，未调用 `process_and_commit_page_dict`。纯函数单页失败以遇到的第一项分类；多个条件可在同页同时存在。来源随修复而变化时必须重算，不能将本次数字视为永久基线。

以下命令可复现 1,065 页原值、净化、全页纯函数及四页差异统计，不写任何项目文件：

```powershell
@'
import json,sys,unicodedata,collections
from pathlib import Path
sys.path.insert(0,str(Path('literature/tools').resolve()))
import zcode_m2_pipeline as p, repair_batch_a as a
w=Path('literature/workspace_m2_dhs834')
manifest=json.loads((w/'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8-sig'))['pages']
c=collections.Counter(); page_sets=collections.defaultdict(set); changed_pages={}
for key in sorted(manifest):
    rawpath=w/'raw_blind'/f'raw_part_p{key}.json'
    sealed=json.loads((w/f'blind_read_p{key}.json').read_text(encoding='utf-8-sig'))['entries']
    if not rawpath.exists():
        c['missing_raw']+=1
        continue
    data=json.loads(rawpath.read_text(encoding='utf-8-sig'))
    pages=data.get('pages') if isinstance(data.get('pages'),list) else [data]
    raw=next(x for x in pages if x.get('pdf_page')==int(key))['entries']
    sr={e['position']:e for e in sealed}
    same=a.same_entries(sealed,raw)
    tone=a.nonstandard_tones(sealed) or a.nonstandard_tones(raw)
    c[('same' if same else 'different')+('_nonstandard' if tone else '_standard')]+=1
    failure=None; diffs=collections.Counter()
    for idx,e in enumerate(raw,1):
        pos=e.get('position',idx); old=sr[pos]
        l=(e.get('source_L') or '').strip(); h=(e.get('source_H') or '').strip()
        m0=(e.get('source_M') or '').strip(); r=(e.get('source_R') or '').strip()
        m=p.sanitize_17c_missionary_orthography(m0,h); c['matched_rows']+=1
        if e.get('source_M')!=old.get('source_M'): c['raw_seal_M_diff']+=1
        if m0!=m:
            c['sanitize_diff']+=1;page_sets['sanitize_diff'].add(key)
            if unicodedata.normalize('NFC',m0)!=unicodedata.normalize('NFC',m): c['sanitize_non_nfc']+=1
            if 'ⁿ' in m0 and 'ⁿ' not in m: c['superscript_n_removed']+=1
        if m!=old.get('source_M'): c['predicted_M_diff']+=1
        try:
            if p.has_modern_tailo_contamination(m): raise ValueError('orthography')
            tm=p.normalize_tone_list(e.get('tone_marks_M',[]))
            tr=p.normalize_tone_list(e.get('tone_marks_R',[]))
            p.expand_spanish_entry(l);p.missionary_to_17c_ipa_and_tailo(m,h,tm)
            values={'source_L':l,'source_H':h,'source_M':m,'source_R':r,
                    'tone_marks_M':tm,'tone_marks_R':tr}
            for field,val in values.items():
                if old.get(field)!=val: diffs[field]+=1
        except Exception as exc:
            if failure is None:
                failure=('orthography' if str(exc)=='orthography' else
                         'tone' if '非规范调标' in str(exc) else type(exc).__name__)
    if failure:
        c['would_fail']+=1;c['first_failure_'+failure]+=1
    else:
        c['pure_functions_pass']+=1
        if diffs: changed_pages[key]=dict(diffs)
c['sanitize_diff_pages']=len(page_sets['sanitize_diff'])
print(json.dumps({'counts':dict(c),'passed_pages_with_field_differences':changed_pages},ensure_ascii=False,indent=2))
'@ | python -X utf8 -
```

## 原图盲读定位补充

`codex_pipeline_ink_blind.json` 与 `codex_pipeline_ink_blind2.json` 为先写盘的独立模型盲读，均非正式裁决。p0119/5 的汉字及邻行与目标相符，两次候选均读 `hiap`，上方记号未明；旧 raw 为 `kiap`，现封存为 `quiap`，尚不能据此认定哪一份忠实。p0077 首份盲读的鄉村实际对应 position 8，而非审计中的 position 6；第二份对鄉社的独立盲读将上方及部分字母记残，不能证明上置 n 是清晰墨迹。逐项对照见 `codex_pipeline_ink_comparison.json`。
