"""
Generate blind_read_p0061.json strictly from 300 DPI crop images without prior draft.
Unified tone labels: T01 (升斜), T02 (降斜), T03 (尖頂帽), T04 (凹角), T05 (平橫), T06/T07 (交叉入聲號).
"""

import json
import hashlib
from pathlib import Path

M2_DIR = Path("literature/workspace_m2_dhs834")

P61_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 61,
    "historical_folio": 32,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0061/pdf_0061_300dpi.png",
    "page_header": "A. ante. G.",
    "page_footer_printed": "- 32 -",
    "page_footer_handwritten": "16",
    "total_positions_recorded": 22,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "Agrauiar",
            "source_H": "欺",
            "source_M": "qúy",
            "source_R": "qǔi",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 2,
            "source_L": "agrauiar",
            "source_H": "欺 負",
            "source_M": "qúy hũ",
            "source_R": "qǔi hū",
            "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 3,
            "source_L": "agrauiar, escarneçer",
            "source_H": "欺 凌",
            "source_M": "qúy lēng",
            "source_R": "qǔi lêng",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 4,
            "source_L": "agrauiar, oprimir",
            "source_H": "欺 壓",
            "source_M": "qúy a̍h",
            "source_R": "qǔi ār",
            "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 5,
            "source_L": "agrauiar el maior al menor -",
            "source_H": "欺 謀",
            "source_M": "qúy bōu",
            "source_R": "qǔi mēu",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 6,
            "source_L": "agrauiar, afrentar -",
            "source_H": "凌",
            "source_M": "lêng",
            "source_R": "lêng",
            "tone_marks_M": ["T03 (尖頂帽)"],
            "tone_marks_R": ["T03 (尖頂帽)"]
        },
        {
            "position": 7,
            "source_L": "agrauiome -",
            "source_H": "開 我",
            "source_M": "khúy gùa",
            "source_R": "cǎy ngò",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 8,
            "source_L": "agrauiar, leuantar falso -",
            "source_H": "虧 心 事",
            "source_M": "khúy sim sū",
            "source_R": "khǔi sǐm zū",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 9,
            "source_L": "agrauiar",
            "source_H": "虧 失",
            "source_M": "khúy sit",
            "source_R": "khǔi sǐt",
            "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]
        },
        {
            "position": 10,
            "source_L": "agrauiome -",
            "source_H": "虧 我",
            "source_M": "khúy gùa",
            "source_R": "khǔi ngò",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 11,
            "source_L": "agrauiar",
            "source_H": "毆",
            "source_M": "àu",
            "source_R": "èu",
            "tone_marks_M": ["T02 (降斜)"],
            "tone_marks_R": ["T02 (降斜)"]
        },
        {
            "position": 12,
            "source_L": "agrauiar, afrentar",
            "source_H": "毆 辱",
            "source_M": "àu xiǒg",
            "source_R": "èu xiō",
            "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 13,
            "source_L": "agrauiar, ofender -",
            "source_H": "毆 蠻",
            "source_M": "àu bān",
            "source_R": "èu mân",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T03 (尖頂帽)"]
        },
        {
            "position": 14,
            "source_L": "agrauiar",
            "source_H": "害",
            "source_M": "hãy",
            "source_R": "hāy",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 15,
            "source_L": "agrauiome",
            "source_H": "歆 我",
            "source_M": "hím gùa",
            "source_R": "hǐm ngò",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 16,
            "source_L": "agrauiar -",
            "source_H": "歪",
            "source_M": "uǎy",
            "source_R": "uǎy",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 17,
            "source_L": "agrauiar con injusticia -",
            "source_H": "枉 屈",
            "source_M": "òng khút",
            "source_R": "vàng cǔ",
            "tone_marks_M": ["T02 (降斜)", "T06/T07 (交叉入聲號)"],
            "tone_marks_R": ["T02 (降斜)", "T04 (凹角)"]
        },
        {
            "position": 18,
            "source_L": "agrauiar",
            "source_H": "枉 人",
            "source_M": "òng lāng",
            "source_R": "vàng xīn",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 19,
            "source_L": "agrauiar",
            "source_H": "負",
            "source_M": "hũ",
            "source_R": "hū",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 20,
            "source_L": "agrauiar, descomediedose con ingratitud -",
            "source_H": "負 義",
            "source_M": "hũ gỹ",
            "source_R": "hū guī",
            "tone_marks_M": ["T04 (凹角)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 21,
            "source_L": "agrauiar tomando por fuerça -",
            "source_H": "強",
            "source_M": "quiāng",
            "source_R": "quiâng",
            "tone_marks_M": ["T05 (平橫)"],
            "tone_marks_R": ["T03 (尖頂帽)"]
        },
        {
            "position": 22,
            "source_L": "agrauiar tomando por fuerça",
            "source_H": "強 挾 人",
            "source_M": "quiāng hiáp lāng",
            "source_R": "quiâng hiā xīn",
            "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)", "T05 (平橫)"]
        }
    ]
}

manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

out_file = M2_DIR / "blind_read_p0061.json"
raw_bytes = json.dumps(P61_DATA, ensure_ascii=False, indent=2).encode("utf-8")
out_file.write_bytes(raw_bytes)
sha = hashlib.sha256(out_file.read_bytes()).hexdigest()

manifest["pages"]["0061"] = {
    "pdf_page": 61,
    "historical_folio": 32,
    "blind_first_read_file": "literature/workspace_m2_dhs834/blind_read_p0061.json",
    "blind_first_read_sha256": sha,
    "entries_count": len(P61_DATA["entries"]),
    "verified_against_300dpi": True,
    "status": "SEALED_PASS"
}

manifest["total_sealed_pages"] = len(manifest["pages"])
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[SUCCESS] Updated BLIND_READ_MANIFEST.json with page 0061 (Total: {manifest['total_sealed_pages']} pages).")
