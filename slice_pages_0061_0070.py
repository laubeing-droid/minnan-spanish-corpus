"""
Slice pages 0061 to 0070 into 300 DPI, 3 horizontal bands, and 4 functional sub-columns.
"""

from pathlib import Path
from literature.tools.minnan_engine import MinnanEngine

engine = MinnanEngine(Path("literature"))
pdf_path = Path("literature/history_and_sources/01_丛刊一_西班牙-华语辞典_Dictionario_Hispánico_Sinicum.pdf")
print("Resolved DHS PDF Path:", pdf_path)
assert pdf_path and pdf_path.exists(), "DHS PDF not found!"

for p in range(61, 71):
    out_dir = Path("literature/tiles/01_DHS") / f"page_{p:04d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = engine.extract_4column_tiles(pdf_path, p, out_dir)
    print(f"Sliced page {p:04d} -> {out_dir} (SHA: {manifest['full_page_sha256'][:16]}...)")

print("Successfully sliced pages 0061 to 0070!")
