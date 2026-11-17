# 封存回滚重放可行性审计

审计时间：2026-11-18 06:31（Asia/Shanghai；UTC 为 2026-11-17 22:31）。范围为现行清册中的 1,103 个 DHS 可校页。审计只读取现行封存件和清册，在系统临时目录调用现有管线；未修改正式 raw、封存件、清册、门禁或管线代码。

## 结果

以每页现行封存对象为输入，在隔离目录调用原 `process_and_commit_page_dict`，同时比较原封存文件字节与原清册的该页记录：

| 结果 | 页数 | 含义 |
| --- | ---: | --- |
| 文件字节及清册页项均相同 | 1,062 | 本次隔离环境下可以精确重放 |
| 执行成功但文件字节或清册页项不同 | 28 | 不能当作精确回滚 |
| 执行失败 | 13 | 均因存量非规范调标引发 `ValueError` |

28 页：`0042–0063`、`0065–0070`。`0064` 不在此组。

13 页：`0041`、`0975`、`0985`、`0986`、`0987`、`0988`、`0989`、`0995`、`0996`、`0997`、`0998`、`0999`、`1066`。

失败首个调标字面分别为：p0041 `無號/輕聲`；p0975 `chun=T03 [疑:T03/T04]`；p0985–0989、p0995–0999 为 `T`；p1066 `T06[疑:T07]`。这些是程序读到的现存值，不是对原图调号的裁决。

28 页中，p0046 和 p0049 的六个字面及调标字段可以保持一致，但重放后的 `blind_state` 从 `INDEPENDENT_FIRST_READ_PRE_COLLATION` 变为 `AUDITED_VISUALLY_VERIFIED`，`protocol_version` 也变化；p0042 还有一处 `tone_marks_M` 值发生变化。不能以字段大致相同代替文件和清册页项的精确恢复，也不能把状态变化冒称原有盲读状态。

## 四例真实 CLI 验证

将各页原封存对象写入独立临时回滚 raw，再在隔离仓库调用原 `zcode_m2_pipeline.py commit --input <回滚 raw>`，比较封存文件及该页清册项：

| 页 | CLI 退出码 | 封存字节 | 清册页项 | 结果 |
| --- | ---: | --- | --- | --- |
| 0146 | 0 | 相同 | 相同 | 可精确重放 |
| 0181 | 0 | 相同 | 相同 | 可精确重放 |
| 0046 | 0 | 不同 | 不同 | 不可作为精确回滚 |
| 0988 | 1 | 未写出 | 原项未变 | 非规范调标，不能重放 |

全量函数层临时输出位于 `C:/Users/being/AppData/Local/Temp/codex_rollback_feasibility_all_uy7peg3_`，四例 CLI 临时输出位于 `C:/Users/being/AppData/Local/Temp/codex_rollback_cli_740pogfo`。临时路径仅为本次证据位置，不是正式原件或交付数据。

## 固定范围

| 输入 | SHA-256 |
| --- | --- |
| `literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json` | `00202ecdcfe0461f19d976601c1a25df6466dc286eb27f74e55b039f659dd3ad` |
| `literature/tools/zcode_m2_pipeline.py` | `7e9d814dad6914569dafa37885e0e9be7f87585da70255f5b6c3e3ebb74c2f1a` |
| `literature/tools/hokkien_17c_converter.py` | `6e170ffdfbceaceea466489d81b587f31293a685b10a9efc340811675d58fc35` |
| `literature/tools/minnan_engine.py` | `3b0f9570dfd7d3fecc025dab61a34fa85a28bc5325f961f79a8dd5534cfc684e` |
| `literature/tools/spanish_17c_expander.py` | `61b26ad2c41ca24eae21cfe4637d44e8164d155effa182224201389a5db1369b` |

## 全量复算命令

从仓库根目录运行。它将完整清册复制到新的系统临时目录，把管线输出目录指向该目录；逐页分类并输出临时路径。它不调用正式工作区的 `commit`，也不改写正式封存件或清册。

```powershell
@'
import sys, json, tempfile, copy, contextlib, io, collections
from pathlib import Path

sys.path.insert(0, str(Path('literature/tools').resolve()))
import zcode_m2_pipeline as pipeline

work = Path('literature/workspace_m2_dhs834')
manifest_bytes = (work / 'BLIND_READ_MANIFEST.json').read_bytes()
original_manifest = json.loads(manifest_bytes)
temp = Path(tempfile.mkdtemp(prefix='codex_rollback_replay_'))
(temp / 'BLIND_READ_MANIFEST.json').write_bytes(manifest_bytes)
pipeline.M2_DIR = temp
results = collections.defaultdict(list)

for page in sorted(original_manifest['pages']):
    original = (work / f'blind_read_p{page}.json').read_bytes()
    page_data = json.loads(original)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            pipeline.process_and_commit_page_dict(copy.deepcopy(page_data))
        replayed = (temp / f'blind_read_p{page}.json').read_bytes()
        replay_manifest = json.loads((temp / 'BLIND_READ_MANIFEST.json').read_bytes())
        same = (replayed == original and
                replay_manifest['pages'][page] == original_manifest['pages'][page])
        results['exact' if same else 'different'].append(page)
    except Exception as exc:
        results['error'].append({'page': page, 'type': type(exc).__name__, 'detail': str(exc)})

print(json.dumps({'counts': {k: len(v) for k, v in results.items()},
                  'different': results['different'], 'errors': results['error'],
                  'temporary_output': str(temp)}, ensure_ascii=False, indent=2))
'@ | python -X utf8 -
```

## 影响边界

全量结果是对**审计时这份封存与代码**的函数层重放，不代表原图字面已核准，也不证明正式环境的回滚、并发控制或整批事务已经实现。四例 CLI 只验证了所列四页。若代码、依赖、清册或封存件改变，须重新试算。

实际回滚仍应只通过 `raw → zcode_m2_pipeline.py commit`，在正式修改前保存可追溯的回滚 raw，并先以同一 CLI 在隔离环境验证原文件字节及页项；无法精确重放的页面应逐页延迟。若提交中断或同页出现其他写入，先确认当前状态是本批产物，不能以旧快照覆盖未知的新工作。恢复后还需核对结果并运行门禁及复扫。
