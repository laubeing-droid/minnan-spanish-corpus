import fitz
from pathlib import Path

pdf_path = Path("literature/history_and_sources/01_丛刊一_西班牙-华语辞典_Dictionario_Hispánico_Sinicum.pdf")
doc = fitz.open(pdf_path)

print("Total pages in DHS:", len(doc))

# Check pages 35 to 50
for p_num in range(38, 55):
    page = doc[p_num - 1]
    text = page.get_text()
    first_line = text.splitlines()[0] if text.splitlines() else "(no text/image only)"
    # sample pixmap color: check if orange grid is present
    # orange grid has high red, medium green, low blue
    pix = page.get_pixmap(dpi=72)
    # count pixels with orange tint (R > 180, G between 80 and 150, B < 80)
    samples = pix.samples
    # pix.width, pix.height, pix.n (channels)
    w, h, n = pix.width, pix.height, pix.n
    orange_count = 0
    total_pixels = w * h
    for i in range(0, len(samples), n * 10): # sample every 10th pixel
        r = samples[i]
        g = samples[i+1]
        b = samples[i+2]
        if r > 160 and 60 < g < 140 and b < 80:
            orange_count += 1
    has_grid = orange_count > 50
    print(f"PDF {p_num:04d}: text_sample='{first_line[:40]}', orange_pixels_sampled={orange_count}, has_orange_grid={has_grid}")
