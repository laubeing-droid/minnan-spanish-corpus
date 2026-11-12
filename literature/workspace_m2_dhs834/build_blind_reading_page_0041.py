"""
Generate and cryptographically freeze the Double-Blind Initial Diplomatic Transcription
for DHS PDF Page 0041 (Folio 12), the inaugural page of the 17th-century 4-column manuscript.

Strictly conforms to v3.1 Final Approved Blueprint:
- Layer 1 verbatim raw glyphs from 300 DPI image (no PEH-OE-JI / TAI-LO modernisation)
- Diacritics mapped strictly to T01~T07 matrix:
  T01 = / (升斜)
  T02 = \ (降斜)
  T03 = ^ (尖頂帽)
  T04 = v (凹角)
  T05 = — (平橫)
  T06/T07 = 交叉入聲號 / 入聲促調
- Row 11: Hanzi = "息 [膀/嘮]" (unresolved, ⿰月旁 或 ⿰口旁), M = "zoâ là", R = "zē la"
- Rows 12-14: 17th-c. orthography "quêng:", "quêng chìn", "quêng qué"
- Rows 08-09: entering tone marks on "pit" recorded as T06/T07
"""

import json
import hashlib
from pathlib import Path

WORKSPACE_ROOT = Path(r"D:\Codex\2.闽南文史工作区\闽南文献迁移")
OUTPUT_DIR = WORKSPACE_ROOT / "literature" / "workspace_m2_dhs834"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

entries_p0041 = [
    {
        "position": 1,
        "source_L": "Acabar perfectamente -",
        "source_H": "全",
        "source_M": "choān",
        "source_R": "chuên:",
        "tone_marks_M": ["T05 (平橫)"],
        "tone_marks_R": ["T03 (尖頂帽)"]
    },
    {
        "position": 2,
        "source_L": "acabar perficionar -",
        "source_H": "完 全",
        "source_M": "oān choān",
        "source_R": "nguân chuên",
        "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"],
        "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]
    },
    {
        "position": 3,
        "source_L": "acabar perfecta m.te -",
        "source_H": "完",
        "source_M": "oān",
        "source_R": "nguân",
        "tone_marks_M": ["T05 (平橫)"],
        "tone_marks_R": ["T03 (尖頂帽)"]
    },
    {
        "position": 4,
        "source_L": "acabado concluido -",
        "source_H": "完 滿",
        "source_M": "oān moǎⁿ",
        "source_R": "nguân moàn",
        "tone_marks_M": ["T05 (平橫)", "T04 (凹角)+上標n"],
        "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
    },
    {
        "position": 5,
        "source_L": "acabado concluido -",
        "source_H": "完 成",
        "source_M": "oān sēng. oan chīn",
        "source_R": "nguân chêng",
        "tone_marks_M": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)", "T05 (平橫)"],
        "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]
    },
    {
        "position": 6,
        "source_L": "acabar los negocios -",
        "source_H": "完 備",
        "source_M": "oān pȳ.",
        "source_R": "nguân pȳ",
        "tone_marks_M": ["T05 (平橫)", "T05 (平橫)+右點"],
        "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]
    },
    {
        "position": 7,
        "source_L": "acabarse concluirse -",
        "source_H": "完 了",
        "source_M": "oān liàu",
        "source_R": "nguân liào",
        "tone_marks_M": ["T05 (平橫)", "T02 (降斜)"],
        "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
    },
    {
        "position": 8,
        "source_L": "acabar perficionarse -",
        "source_H": "完 畢",
        "source_M": "oān pit",
        "source_R": "nguân piē",
        "tone_marks_M": ["T05 (平橫)", "T06/T07 (交叉入聲號)"],
        "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]
    },
    {
        "position": 9,
        "source_L": "acabado negocio concluido -",
        "source_H": "畢 了",
        "source_M": "pit liàu",
        "source_R": "piē liào",
        "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"],
        "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]
    },
    {
        "position": 10,
        "source_L": "acabar o dejar algo -",
        "source_H": "息",
        "source_M": "zoâ",
        "source_R": "zē",
        "tone_marks_M": ["T03 (尖頂帽) + T02 (降斜)"],
        "tone_marks_R": ["T05 (平橫)+z頂點"]
    },
    {
        "position": 11,
        "source_L": "acabar. acabose ya -",
        "source_H": "息 [膀/嘮]",
        "source_M": "zoâ là",
        "source_R": "zē la",
        "tone_marks_M": ["T03 (尖頂帽) + T02 (降斜)", "T02 (降斜)"],
        "tone_marks_R": ["T05 (平橫)+z頂點", "無號/輕聲"]
    },
    {
        "position": 12,
        "source_L": "acabarse cosa acabada -",
        "source_H": "罄",
        "source_M": "quêng:",
        "source_R": "quēng",
        "tone_marks_M": ["T03 (尖頂帽)"],
        "tone_marks_R": ["T05 (平橫)"]
    },
    {
        "position": 13,
        "source_L": "acabarse todo -",
        "source_H": "罄 盡",
        "source_M": "quêng chìn",
        "source_R": "quēng chīn",
        "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)"],
        "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
    },
    {
        "position": 14,
        "source_L": "acabar se todo lo que ay en casa consumir lo -",
        "source_H": "罄 家",
        "source_M": "quêng qué",
        "source_R": "quēng quiǎ",
        "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"],
        "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
    },
    {
        "position": 15,
        "source_L": "acabar. acabada cosa -",
        "source_H": "遂",
        "source_M": "zuī",
        "source_R": "zuī",
        "tone_marks_M": ["T05 (平橫)"],
        "tone_marks_R": ["T05 (平橫)"]
    },
    {
        "position": 16,
        "source_L": "acabar. acabada cosa. tener efeto la cosa -",
        "source_H": "效",
        "source_M": "hāu",
        "source_R": "hiāu",
        "tone_marks_M": ["T05 (平橫)+下點"],
        "tone_marks_R": ["T05 (平橫)"]
    },
    {
        "position": 17,
        "source_L": "acabarse la cosa, tener efeto -",
        "source_H": "效 驗",
        "source_M": "hāu giām",
        "source_R": "hiāu nguiēn",
        "tone_marks_M": ["T05 (平橫)+下點", "T05 (平橫)"],
        "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
    },
    {
        "position": 18,
        "source_L": "acabada cosa, acabarse -",
        "source_H": "已 果",
        "source_M": "ỳ cò",
        "source_R": "yù cǒ",
        "tone_marks_M": ["T02 (降斜)", "T02 (降斜)"],
        "tone_marks_R": ["T02 (降斜)", "T04 (凹角)"]
    },
    {
        "position": 19,
        "source_L": "acabarse el año de luto -",
        "source_H": "期",
        "source_M": "quý",
        "source_R": "quī : quǐ",
        "tone_marks_M": ["T01 (升斜)"],
        "tone_marks_R": ["T05 (平橫) / T04 (凹角)"]
    },
    {
        "position": 20,
        "source_L": "acabarse el año de luto -",
        "source_H": "期 年",
        "source_M": "quý liên",
        "source_R": "quī niên",
        "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
        "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
    },
    {
        "position": 21,
        "source_L": "acabarse, morir -",
        "source_H": "亡",
        "source_M": "bōng",
        "source_R": "vâng",
        "tone_marks_M": ["T05 (平橫)"],
        "tone_marks_R": ["T03 (尖頂帽)"]
    }
]

doc_record = {
    "protocol_version": "v3.1 Final Approved Blueprint",
    "pdf_page": 41,
    "historical_folio": 12,
    "layout_mode": "4_COLUMN_STANDARD",
    "image_source": "literature/tiles/01_DHS/page_0041/pdf_0041_300dpi.png",
    "page_header": "A. ante. C.",
    "page_footer_printed": "- 12 -",
    "page_footer_handwritten": "6",
    "total_positions_recorded": len(entries_p0041),
    "blind_state": "INDEPENDENT_FIRST_READ_PRE_COLLATION",
    "entries": entries_p0041
}

raw_json_str = json.dumps(doc_record, ensure_ascii=False, indent=2)
file_sha256 = hashlib.sha256(raw_json_str.encode("utf-8")).hexdigest()

doc_record["blind_first_read_sha256"] = file_sha256

out_json_path = OUTPUT_DIR / "blind_read_p0041.json"
with open(out_json_path, "w", encoding="utf-8") as f:
    json.dump(doc_record, f, ensure_ascii=False, indent=2)

print(f"Blind First Read for Page 0041 saved to: {out_json_path}")
print(f"Cryptographic Hash (blind_first_read_sha256): {file_sha256}")

# Update Blind Read Manifest
manifest_file = OUTPUT_DIR / "BLIND_READ_MANIFEST.json"
manifest = {}
if manifest_file.exists():
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

manifest["pages"] = manifest.get("pages", {})
manifest["pages"]["0041"] = {
    "pdf_page": 41,
    "historical_folio": 12,
    "positions_count": len(entries_p0041),
    "blind_first_read_file": "literature/workspace_m2_dhs834/blind_read_p0041.json",
    "blind_first_read_sha256": file_sha256,
    "status": "LOCKED_PRE_COLLATION"
}

with open(manifest_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Updated BLIND_READ_MANIFEST.json successfully.")
