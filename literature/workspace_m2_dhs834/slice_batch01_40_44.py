import sys
from pathlib import Path
sys.path.insert(0, "literature/tools")
from minnan_engine import MinnanEngine

engine = MinnanEngine(Path("literature"))
pdf_path = engine.get_source_pdf_path("01_DHS_Hispanico_Sinicum")
print(f"Slicing DHS Batch 01 (PDF 0041-0044) from {pdf_path}...")

for p in [41, 42, 43, 44]:
    out_dir = Path(f"literature/tiles/01_DHS/page_{p:04d}")
    manifest = engine.extract_4column_tiles(pdf_path, p, out_dir)
    print(f"Page {p:04d}: Sliced into 3 bands and 4 sub-columns ({manifest['page_type']}). SHA={manifest['full_page_sha256'][:8]}...")
print("Batch 01 (PDF 0040-0044) slicing complete.")
