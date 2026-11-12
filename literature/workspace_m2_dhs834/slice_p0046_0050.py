import sys
from pathlib import Path
sys.path.insert(0, 'literature/tools')
from minnan_engine import MinnanEngine

engine = MinnanEngine(Path('literature'))
pdf_path = engine.get_source_pdf_path('01_DHS_Hispanico_Sinicum')

for p in range(46, 51):
    out_dir = Path(f'literature/tiles/01_DHS/page_{p:04d}')
    manifest = engine.extract_4column_tiles(pdf_path, p, out_dir)
    print(f"Page {p:04d} sliced: {manifest['page_type']}")
