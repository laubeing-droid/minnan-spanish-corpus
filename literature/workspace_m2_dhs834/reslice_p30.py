import sys
from pathlib import Path
sys.path.insert(0, 'literature/tools')
from minnan_engine import MinnanEngine

engine = MinnanEngine(Path('literature'))
pdf = engine.get_source_pdf_path('01_DHS_Hispanico_Sinicum')
out_dir = Path('literature/tiles/01_DHS/page_0030')
manifest = engine.extract_4column_tiles(pdf, 30, out_dir)
print('Page 30 sliced:', manifest['page_type'])
for col in manifest['columns']:
    print(' ', col['name'], col['bbox'], col['tile_path'])
