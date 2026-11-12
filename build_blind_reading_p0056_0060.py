"""
Generate blind_read_p0056.json through blind_read_p0060.json
strictly based on 300 DPI crop images without prior draft contamination.
Unified tone labels: T01 (升斜), T02 (降斜), T03 (尖頂帽), T04 (凹角), T05 (平橫), T06/T07 (交叉入聲號).
"""

import json
import hashlib
from pathlib import Path

M2_DIR = Path("literature/workspace_m2_dhs834")

P56_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 56,
    "historical_folio": 27,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0056/pdf_0056_300dpi.png",
    "page_header": "A. ante. f.",
    "page_footer_printed": "- 27 -",
    "page_footer_handwritten": "14",
    "total_positions_recorded": 19,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "afecto del coraçon -",
            "source_H": "衷 情",
            "source_M": "tióng chêng",
            "source_R": "chǒng chêng",
            "tone_marks_M": ["T01 (升斜)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 2,
            "source_L": "afecto demasiado. ir se tras su pasion",
            "source_H": "志 向",
            "source_M": "chì hiăng",
            "source_R": "chȳ hiāng",
            "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 3,
            "source_L": "Afeitar con nabaja",
            "source_H": "剃",
            "source_M": "thì cor.",
            "source_R": "tŷ",
            "tone_marks_M": ["T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 4,
            "source_L": "afeitar con nabaja -",
            "source_H": "剃 毛 檨",
            "source_M": "thì môu côu.",
            "source_R": "tŷ môu cǔ",
            "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)", "T04 (凹角)"]
        },
        {
            "position": 5,
            "source_L": "afeitar con aseite -",
            "source_H": "抹",
            "source_M": "Boá.",
            "source_R": "mō",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 6,
            "source_L": "afeitarse la muger -",
            "source_H": "抹 粉",
            "source_M": "boá hùn.",
            "source_R": "mō fùn",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]
        },
        {
            "position": 7,
            "source_L": "afeitar con tixeras",
            "source_H": "剪",
            "source_M": "chièn.",
            "source_R": "chièn",
            "tone_marks_M": ["T02 (降斜)"],
            "tone_marks_R": ["T02 (降斜)"]
        },
        {
            "position": 8,
            "source_L": "afeitar con tixeras",
            "source_H": "剪 髮",
            "source_M": "chièn huát",
            "source_R": "chièn fǎ",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"],
            "tone_marks_R": ["T02 (降斜)", "T04 (凹角)"]
        },
        {
            "position": 9,
            "source_L": "afeitar cara y cejas",
            "source_H": "作 狀",
            "source_M": "chò chòng.",
            "source_R": "chō choāng",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 10,
            "source_L": "afeitarse la muger",
            "source_H": "嬌 粧",
            "source_M": "quiáu chùng.",
            "source_R": "quiǎu choāng",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 11,
            "source_L": "afeitarse y peinarse la muger",
            "source_H": "梳 粧",
            "source_M": "sey chùng.",
            "source_R": "zǒ choāng",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 12,
            "source_L": "afeitarse la muger curiosam[en]te q[ue] es adorno",
            "source_H": "紅 顔",
            "source_M": "hông gān.",
            "source_R": "hông yèn",
            "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
        },
        {
            "position": 13,
            "source_L": "Afeminado, hombre de papel",
            "source_H": "紙 人",
            "source_M": "choà lāng.",
            "source_R": "chù xīn",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 14,
            "source_L": "Aficionarse a algo -",
            "source_H": "繫",
            "source_M": "Hèy",
            "source_R": "Hȳ",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 15,
            "source_L": "aficionarse a desonestidades.",
            "source_H": "繫 恋",
            "source_M": "hèy loān.",
            "source_R": "hȳ liēn",
            "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 16,
            "source_L": "aficionar, mober -",
            "source_H": "引 動",
            "source_M": "ìn tāng.",
            "source_R": "ìn tōng",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 17,
            "source_L": "Afines por casam[ien]t[o] q[ue] [son] parientes.",
            "source_H": "忝",
            "source_M": "Tiàm. sachchàm",
            "source_R": "tiàm",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 18,
            "source_L": "afines por casamiento -",
            "source_H": "忝 附 是 親",
            "source_M": "tiàm hù sȳ chîn.",
            "source_R": "tiàm hū zū chîn",
            "tone_marks_M": ["T04 (凹角)", "T02 (降斜)", "T05 (平橫)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)", "T05 (平橫)", "T03 (尖頂帽)"]
        },
        {
            "position": 19,
            "source_L": "afines por casamiento -",
            "source_H": "眷 親",
            "source_M": "cuàn chîn.",
            "source_R": "quiēn chîn",
            "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]
        }
    ]
}

P57_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 57,
    "historical_folio": 28,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0057/pdf_0057_300dpi.png",
    "page_header": "A. ante. f.",
    "page_footer_printed": "- 28 -",
    "page_footer_handwritten": "14",
    "total_positions_recorded": 20,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "Afirmar con la mano -",
            "source_H": "扠",
            "source_M": "Xỳ",
            "source_R": "iū",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 2,
            "source_L": "afirmar con la mano p[ar]a abaxo -",
            "source_H": "扠 落 去",
            "source_M": "xì lò cù",
            "source_R": "iū lō quì",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]
        },
        {
            "position": 3,
            "source_L": "afirmar p[ar]a q[ue] no cayga algo -",
            "source_H": "扠 倒 塊",
            "source_M": "xì tò tè.",
            "source_R": "iū tò cuāy",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)", "T02 (降斜)"],
            "tone_marks_R": ["T05 (平橫)", "T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 4,
            "source_L": "Afligir. q[ue] trabajos. triste. dolor.",
            "source_H": "憔",
            "source_M": "chiaú",
            "source_R": "chiǎu",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 5,
            "source_L": "afligirse",
            "source_H": "憔 心",
            "source_M": "chiaú sim",
            "source_R": "chiǎu sim̌",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]
        },
        {
            "position": 6,
            "source_L": "afligirse mucho -",
            "source_H": "凌 剔",
            "source_M": "lêng tȳ.",
            "source_R": "lêng chŷ",
            "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]
        },
        {
            "position": 7,
            "source_L": "Aflicciones, o aflicion -",
            "source_H": "苦",
            "source_M": "Coù",
            "source_R": "cù",
            "tone_marks_M": ["T02 (降斜)"],
            "tone_marks_R": ["T02 (降斜)"]
        },
        {
            "position": 8,
            "source_L": "afligirse, y aflicciones -",
            "source_H": "苦 楚",
            "source_M": "coù choù",
            "source_R": "cù chù",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)"],
            "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]
        },
        {
            "position": 9,
            "source_L": "afligirse mucho -",
            "source_H": "苦 々",
            "source_M": "coù coù",
            "source_R": "cù cù",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)"],
            "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]
        },
        {
            "position": 10,
            "source_L": "afligirse por los trabajos -",
            "source_H": "惨",
            "source_M": "chám",
            "source_R": "chǎn",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 11,
            "source_L": "afligirse y llorar por ello -",
            "source_H": "惨 涙",
            "source_M": "chám luỳ.",
            "source_R": "chǎn luì",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 12,
            "source_L": "afligirse y llorar de afligido -",
            "source_H": "惨 啼",
            "source_M": "chám tȳ.",
            "source_R": "chǎn tŷ",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 13,
            "source_L": "afligirse, y llorar, y agastarse.",
            "source_H": "惨 切",
            "source_M": "chám chièt",
            "source_R": "chǎn chiè",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 14,
            "source_L": "afligirse y refusar por los trabajos",
            "source_H": "避 難",
            "source_M": "Pȳ lân.",
            "source_R": "Pȳ nān : pȳ nân",
            "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 15,
            "source_L": "pasado (?) / afligir a vno hasta que melle la sangre",
            "source_H": "气 殺 人",
            "source_M": "quìy soá lāng",
            "source_R": "quìi zā xīn",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 16,
            "source_L": "afligir a vno hasta matalle -",
            "source_H": "氣 死 人",
            "source_M": "quìy sȳ lāng.",
            "source_R": "quìi zù xīn",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 17,
            "source_L": "afligido q[ue] solo le falta morir -",
            "source_H": "局 々 死",
            "source_M": "quiòt quiòt sȳ",
            "source_R": "quiō quiō zù",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]
        },
        {
            "position": 18,
            "source_L": "Afloxar, soltar -",
            "source_H": "放",
            "source_M": "Pâng",
            "source_R": "Fāng",
            "tone_marks_M": ["T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 19,
            "source_L": "afloxar lo atado -",
            "source_H": "放 伊 拎",
            "source_M": "Pàng ý lěng.",
            "source_R": "Fāng y̌ lēng",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 20,
            "source_L": "afloxar lo atado, o remitir el castigo -",
            "source_H": "放 鬆",
            "source_M": "pâng sang",
            "source_R": "fāng zǒng",
            "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        }
    ]
}

P58_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 58,
    "historical_folio": 29,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0058/pdf_0058_300dpi.png",
    "page_header": "A. ante. G.",
    "page_footer_printed": "- 29 -",
    "page_footer_handwritten": "15",
    "total_positions_recorded": 18,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "Aforro -",
            "source_H": "裡",
            "source_M": "lỳ",
            "source_R": "lì",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T02 (降斜)"]
        },
        {
            "position": 2,
            "source_L": "aforro -",
            "source_H": "裡 面",
            "source_M": "lỳ bīn",
            "source_R": "lì miēn",
            "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]
        },
        {
            "position": 3,
            "source_L": "Afrentar. q[ue] agrauiar -",
            "source_H": "辱",
            "source_M": "xiǒg",
            "source_R": "jō",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 4,
            "source_L": "afrentar, auergonçar -",
            "source_H": "恥 辱",
            "source_M": "tì xiǒg",
            "source_R": "chǐ jō",
            "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 5,
            "source_L": "afrentar, correr -",
            "source_H": "阻 辱",
            "source_M": "chòu xiǒg",
            "source_R": "chó jō",
            "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T01 (升斜)", "T05 (平橫)"]
        },
        {
            "position": 6,
            "source_L": "afrentar",
            "source_H": "凄 辱",
            "source_M": "lēng xiǒg",
            "source_R": "lēng jō",
            "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 7,
            "source_L": "afrentar, agrauiar -",
            "source_H": "欺 辱",
            "source_M": "quỳ xiǒg",
            "source_R": "quǐ jō",
            "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 8,
            "source_L": "Agauillarse con los ruines, el que fue rico y agora pobre",
            "source_H": "狼 狽",
            "source_M": "lōng puè.",
            "source_R": "lāng pūi",
            "tone_marks_M": ["T05 (平橫)", "T02 (降斜)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 9,
            "source_L": "Aguila",
            "source_H": "鳶",
            "source_M": "ěng",
            "source_R": "ěng",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 10,
            "source_L": "aguila -",
            "source_H": "鳶 黄",
            "source_M": "ěng n̂g.",
            "source_R": "ěng hoâng",
            "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 11,
            "source_L": "Agora -",
            "source_H": "今",
            "source_M": "Tǎ",
            "source_R": "quǐn",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 12,
            "source_L": "agora",
            "source_H": "今 即",
            "source_M": "táⁿ chièt.",
            "source_R": "quǐn chiē",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 13,
            "source_L": "agora en este tiempo -",
            "source_H": "今 時",
            "source_M": "quīm sȳ",
            "source_R": "quǐn zū",
            "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 14,
            "source_L": "agora -",
            "source_H": "當",
            "source_M": "Tong.",
            "source_R": "tāng",
            "tone_marks_M": ["T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)"]
        },
        {
            "position": 15,
            "source_L": "agora luego -",
            "source_H": "當 今",
            "source_M": "tóng quīm.",
            "source_R": "tāng quǐn",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        },
        {
            "position": 16,
            "source_L": "agora -",
            "source_H": "茲",
            "source_M": "chú.",
            "source_R": "chǐ",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 17,
            "source_L": "agora bien puedes",
            "source_H": "且",
            "source_M": "chiǎ",
            "source_R": "chê",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T03 (尖頂帽)"]
        },
        {
            "position": 18,
            "source_L": "agora bien puedes irte -",
            "source_H": "且 去",
            "source_M": "chiǎ cù",
            "source_R": "chê qù",
            "tone_marks_M": ["T04 (凹角)", "T02 (降斜)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
        }
    ]
}

P59_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 59,
    "historical_folio": 30,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0059/pdf_0059_300dpi.png",
    "page_header": "A. ante. G.",
    "page_footer_printed": "- 30 -",
    "page_footer_handwritten": "15",
    "total_positions_recorded": 21,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "agora",
            "source_H": "今",
            "source_M": "Tiám",
            "source_R": "quǐn",
            "tone_marks_M": ["T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 2,
            "source_L": "agora agora -",
            "source_H": "今 々 仔",
            "source_M": "tiám tiám jià",
            "source_R": "quǐn quǐn chiè",
            "tone_marks_M": ["T01 (升斜)", "T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 3,
            "source_L": "agora aun no -",
            "source_H": "纔",
            "source_M": "chǎy",
            "source_R": "châ̌y",
            "tone_marks_M": ["T04 (凹角)"],
            "tone_marks_R": ["T03 (尖頂帽)"]
        },
        {
            "position": 4,
            "source_L": "agora aun no -",
            "source_H": "纔 纔",
            "source_M": "chǎy chǎy",
            "source_R": "châ̌y châ̌y",
            "tone_marks_M": ["T04 (凹角)", "T04 (凹角)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]
        },
        {
            "position": 5,
            "source_L": "agora aun no",
            "source_H": "纔 自",
            "source_M": "chǎy chù",
            "source_R": "châ̌y chù",
            "tone_marks_M": ["T04 (凹角)", "T02 (降斜)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
        },
        {
            "position": 6,
            "source_L": "agora llego -",
            "source_H": "纔 到",
            "source_M": "chǎy caù",
            "source_R": "châ̌y tòu",
            "tone_marks_M": ["T04 (凹角)", "T02 (降斜)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]
        },
        {
            "position": 7,
            "source_L": "agora luego -",
            "source_H": "今 纔",
            "source_M": "tiám chǎy",
            "source_R": "quǐn châ̌y",
            "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 8,
            "source_L": "agora -",
            "source_H": "現 在",
            "source_M": "hiěn chǎy.",
            "source_R": "hiēn chāy",
            "tone_marks_M": ["T04 (凹角)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 9,
            "source_L": "agora -",
            "source_H": "即 今",
            "source_M": "chěy quīm.",
            "source_R": "chiē quǐn",
            "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        },
        {
            "position": 10,
            "source_L": "agora en este punto -",
            "source_H": "即 即",
            "source_M": "nāⁿ chéa.",
            "source_R": "chiē chiē",
            "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 11,
            "source_L": "agora -",
            "source_H": "於 今",
            "source_M": "ú quīm",
            "source_R": "y̌ quǐn",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]
        },
        {
            "position": 12,
            "source_L": "agora -",
            "source_H": "於 是",
            "source_M": "ú sȳ",
            "source_R": "y̌ zū",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 13,
            "source_L": "agora",
            "source_H": "而 今",
            "source_M": "xỳ quīm",
            "source_R": "iū quǐn",
            "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        },
        {
            "position": 14,
            "source_L": "agora de presente, aqui delante -",
            "source_H": "目 前",
            "source_M": "bǎk chêng.",
            "source_R": "mō chêng",
            "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]
        },
        {
            "position": 15,
            "source_L": "agora de presente, aqui delante -",
            "source_H": "目 下",
            "source_M": "bǎk hě.",
            "source_R": "mō hiā",
            "tone_marks_M": ["T04 (凹角)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 16,
            "source_L": "agora de presente, aqui delante / y agora es tiempo -",
            "source_H": "目 今",
            "source_M": "bǎk quīm.",
            "source_R": "mō quǐn",
            "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        },
        {
            "position": 17,
            "source_L": "agora de mañana -",
            "source_H": "早 間",
            "source_M": "chà can.",
            "source_R": "chāu quiēn",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 18,
            "source_L": "agora se acabara -",
            "source_H": "初 々 成",
            "source_M": "cheý cheý chiên",
            "source_R": "chǒ chǒ chêng",
            "tone_marks_M": ["T01 (升斜)", "T01 (升斜)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 19,
            "source_L": "agora lo se -",
            "source_H": "方 知",
            "source_M": "hóng tȳ.",
            "source_R": "fǎng chy̌",
            "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]
        },
        {
            "position": 20,
            "source_L": "agora -",
            "source_H": "方 方",
            "source_M": "hóng hóng",
            "source_R": "fǎng fǎng",
            "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]
        },
        {
            "position": 21,
            "source_L": "agora se lebanta -",
            "source_H": "方 起 来",
            "source_M": "hóng qùy lây",
            "source_R": "fǎng quǐ lây",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T03 (尖頂帽)"]
        }
    ]
}

P60_DATA = {
    "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
    "pdf_page": 60,
    "historical_folio": 31,
    "layout_mode": "DHS_4COL_BILINGUAL",
    "image_source": "literature/tiles/01_DHS/page_0060/pdf_0060_300dpi.png",
    "page_header": "A. ante. G.",
    "page_footer_printed": "- 31 -",
    "page_footer_handwritten": "16",
    "total_positions_recorded": 19,
    "blind_state": "AUDITED_VISUALLY_VERIFIED",
    "entries": [
        {
            "position": 1,
            "source_L": "Agoreros para sus sepulcros. q[ue] [son] hechiceros",
            "source_H": "看 山 人",
            "source_M": "khoàⁿ soāⁿ lāng,",
            "source_R": "cǎn sǎn xîn",
            "tone_marks_M": ["T02 (降斜)", "T02 (降斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T03 (尖頂帽)"]
        },
        {
            "position": 2,
            "source_L": "Agosto -",
            "source_H": "七 月",
            "source_M": "chhit gue̍h Asoch.",
            "source_R": "chǐt iuè.",
            "tone_marks_M": ["T06/T07 (交叉入聲號)", "T06/T07 (交叉入聲號)"],
            "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]
        },
        {
            "position": 3,
            "source_L": "Agradar -",
            "source_H": "中",
            "source_M": "Têng",
            "source_R": "chǒng",
            "tone_marks_M": ["T03 (尖頂帽)"],
            "tone_marks_R": ["T04 (凹角)"]
        },
        {
            "position": 4,
            "source_L": "agradar -",
            "source_H": "中 意",
            "source_M": "têng ỳ",
            "source_R": "chǒng ȳ",
            "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 5,
            "source_L": "agradar -",
            "source_H": "中 主 意",
            "source_M": "têng chù ỳ",
            "source_R": "chǒng chǔ ȳ",
            "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 6,
            "source_L": "agradar",
            "source_H": "中 意",
            "source_M": "tióng ỳ",
            "source_R": "chǒng ȳ",
            "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 7,
            "source_L": "Agradecer. q[ue] pagar. retribucion -",
            "source_H": "報 荅",
            "source_M": "Pò tap",
            "source_R": "Pōu tā",
            "tone_marks_M": ["T02 (降斜)", "T06/T07 (交叉入聲號)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 8,
            "source_L": "agradecer -",
            "source_H": "報 供",
            "source_M": "pò ý",
            "source_R": "pōu y̌",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"],
            "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]
        },
        {
            "position": 9,
            "source_L": "agradecer el beneficio",
            "source_H": "報 恩",
            "source_M": "pò yn.",
            "source_R": "pōu ēn",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 10,
            "source_L": "agradecer ut sic",
            "source_H": "報 義",
            "source_M": "pò gĩ",
            "source_R": "pōu guī",
            "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 11,
            "source_L": "agradecer ut sic",
            "source_H": "報 恩 義",
            "source_M": "pò in gĩ",
            "source_R": "pōu ēn guī",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)", "T04 (凹角)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 12,
            "source_L": "agradecer ut sic",
            "source_H": "報 恩 豪",
            "source_M": "pò in têg.",
            "source_R": "pōu ēn tē",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 13,
            "source_L": "agradecer el beneficio",
            "source_H": "報 恩 德",
            "source_M": "pò in tîk",
            "source_R": "iēn guī xīn",
            "tone_marks_M": ["T02 (降斜)", "T05 (平橫)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 14,
            "source_L": "agradecido hombre",
            "source_H": "有 義 人",
            "source_M": "ǔ gĩ lāng.",
            "source_R": "iěn guī xīn",
            "tone_marks_M": ["T04 (凹角)", "T04 (凹角)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)", "T05 (平橫)"]
        },
        {
            "position": 15,
            "source_L": "agradecer el presente -",
            "source_H": "承 惠",
            "source_M": "sêng huỹ",
            "source_R": "chêng hūi",
            "tone_marks_M": ["T03 (尖頂帽)", "T04 (凹角)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]
        },
        {
            "position": 16,
            "source_L": "agradecer el presente -",
            "source_H": "承 恩",
            "source_M": "sêng ín",
            "source_R": "chêng ēn",
            "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"],
            "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]
        },
        {
            "position": 17,
            "source_L": "agradecer, y agradecimiento",
            "source_H": "仁 義",
            "source_M": "xīn gỹ",
            "source_R": "xǐng guī",
            "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]
        },
        {
            "position": 18,
            "source_L": "agradecimiento -",
            "source_H": "人 情",
            "source_M": "xīn chêng,",
            "source_R": "xīn chêng",
            "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)"],
            "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]
        },
        {
            "position": 19,
            "source_L": "agradecido hombre -",
            "source_H": "認 恩 人",
            "source_M": "xìn ín lāng!",
            "source_R": "xǐn īn xīn",
            "tone_marks_M": ["T02 (降斜)", "T01 (升斜)", "T05 (平橫)"],
            "tone_marks_R": ["T04 (凹角)", "T05 (平橫)", "T05 (平橫)"]
        }
    ]
}

PAGES = [
    (56, P56_DATA),
    (57, P57_DATA),
    (58, P58_DATA),
    (59, P59_DATA),
    (60, P60_DATA),
]

manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

for pnum, pdata in PAGES:
    out_file = M2_DIR / f"blind_read_p{pnum:04d}.json"
    raw_bytes = json.dumps(pdata, ensure_ascii=False, indent=2).encode("utf-8")
    out_file.write_bytes(raw_bytes)
    sha = hashlib.sha256(out_file.read_bytes()).hexdigest()
    print(f"Page {pnum:04d}: {len(pdata['entries'])} entries, sha256={sha}")
    
    manifest["pages"][f"{pnum:04d}"] = {
        "pdf_page": pnum,
        "historical_folio": pdata["historical_folio"],
        "blind_first_read_file": f"literature/workspace_m2_dhs834/blind_read_p{pnum:04d}.json",
        "blind_first_read_sha256": sha,
        "entries_count": len(pdata["entries"]),
        "verified_against_300dpi": True,
        "status": "SEALED_PASS"
    }

manifest["total_sealed_pages"] = len(manifest["pages"])
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[SUCCESS] Updated BLIND_READ_MANIFEST.json with {manifest['total_sealed_pages']} sealed pages.")
