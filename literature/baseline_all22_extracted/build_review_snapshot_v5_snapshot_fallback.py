"""Final executed version: recover an expired /tmp script by its saved SHA.

No missing body was discovered. The AUST script's original /tmp path expired;
the immutable prior handoff includes an exact 5,043-byte, hash-verified copy.
All previous builder versions remain as a transparent build history.
"""
from pathlib import Path

v4=Path(__file__).with_name('build_review_snapshot_v4_final.py')
wrapper=v4.read_text()
anchor="\nexec(compile(source, str(p), 'exec'))\n'''"
assert wrapper.count(anchor)==1
addition=r'''
target = '            assert p.exists(), p'
fallback = """            if not p.exists() and str(p)=='/tmp/save_aust_v3.py':
                p=BASE/'handoff_21sources_20261016_v1/small_code_snapshots/save_aust_v3.py'
                assert sha(p)=='4a0d344a8ae125651cbd8d97f8efe0240dd5c0f77a46dd9ff2e4dfdac82b1023'
            assert p.exists(), p"""
assert source.count(target)==1
source=source.replace(target,fallback)
source=source.replace("'missing_required_primary_files':[],'source_PDF_total_bytes_not_copied':", "'missing_required_primary_files':[],'recovered_missing_original_script_paths':[{'original_path':'/tmp/save_aust_v3.py','snapshot_path':str(BASE/'handoff_21sources_20261016_v1/small_code_snapshots/save_aust_v3.py'),'sha256':'4a0d344a8ae125651cbd8d97f8efe0240dd5c0f77a46dd9ff2e4dfdac82b1023','snapshot_matches_recorded_original_hash':True}],'source_PDF_total_bytes_not_copied':")
source=source.replace('## 本次核验边界和下一步\n', '## 临时脚本路径恢复\n\n旧清单的/tmp/save_aust_v3.py已不存在；原21源handoff的small_code_snapshots内保留5043-byte同SHA256快照。本包从该已核实快照收录，源代码未丢失，原临时路径仍记为失效，没有重新创建它。\n\n## 本次核验边界和下一步\n')
'''
wrapper=wrapper.replace(anchor,'\n'+addition+anchor)
exec(compile(wrapper,str(v4),'exec'))
