"""Final executed builder; verifies and reuses identical partial copies only.

The first run stopped at a page-label format check: Angelica pages 086-169
use plain PDF086 labels rather than Markdown '# PDF 086'. No text was changed.
This run recognizes both existing label formats and never overwrites files.
"""
from pathlib import Path

v2 = Path(__file__).with_name('build_review_snapshot_v2_current12.py')
wrapper = v2.read_text()
old = "exec(compile(source, str(p), 'exec'))"
assert wrapper.count(old) == 1
patch = r'''
old_pattern = r"r'^#{1,3}\s+(?:HAB\s*\d+\s*[·.]\s*)?PDF\s+(\d+)\b'"
new_pattern = r"r'^(?:#{1,3}\s+)?(?:HAB\s*\d+\s*[·.]\s*)?PDF\s*(\d+)\b'"
assert source.count(old_pattern) == 1
source = source.replace(old_pattern, new_pattern)
old_write = "    with p.open('xb') as f: f.write(value if isinstance(value, bytes) else value.encode('utf8'))"
new_write = """    data = value if isinstance(value, bytes) else value.encode('utf8')
    if p.exists():
        assert p.read_bytes() == data, ('Existing output differs; refusing overwrite', str(p))
        return p
    with p.open('xb') as f: f.write(data)"""
assert source.count(old_write) == 1
source = source.replace(old_write, new_write)
exec(compile(source, str(p), 'exec'))
'''
exec(compile(wrapper.replace(old, patch), str(v2), 'exec'))
