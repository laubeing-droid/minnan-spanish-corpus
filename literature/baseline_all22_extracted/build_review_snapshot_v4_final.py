"""Final builder with source-specific page parsing and no-overwrite resume.

v2 stopped because Angelica086-169 have plain PDF086 labels; v3 broadened
all sources and correctly stopped on DHS's repeated interior location labels.
This version accepts plain labels only in the Angelica merged body. Existing
partial copies are verified byte-for-byte and reused, never overwritten.
"""
from pathlib import Path

v2 = Path(__file__).with_name('build_review_snapshot_v2_current12.py')
wrapper = v2.read_text()
old = "exec(compile(source, str(p), 'exec'))"
assert wrapper.count(old) == 1
patch = r'''
start = source.index('def pages(p):')
end = source.index('def source_pdf_info', start)
replacement = """def pages(p):
    pattern = r'^#{1,3}\\s+(?:HAB\\s*\\d+\\s*[·.]\\s*)?PDF\\s+(\\d+)\\b'
    if Path(p).name == 'Angelica_Ms60_all169_method_independent_v3.md':
        pattern = r'^(?:#{1,3}\\s+)?PDF\\s*(\\d+)\\b'
    return [int(m.group(1)) for line in Path(p).read_text().splitlines()
            if (m := re.match(pattern, line, re.I))]

"""
source = source[:start] + replacement + source[end:]
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
