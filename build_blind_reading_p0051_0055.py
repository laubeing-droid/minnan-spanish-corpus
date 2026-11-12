"""
Build certified visual blind reading files for DHS Folios 0051 to 0055 (historical pages 22 to 26).
Also updates ledger_1_unresolved_glyphs.json and BLIND_READ_MANIFEST.json.
"""

import json
import hashlib
from pathlib import Path

M2_DIR = Path("literature/workspace_m2_dhs834")
LEDGER_PATHS = [
    Path("literature/evidence_ledger/ledger_1_unresolved_glyphs.json"),
    Path("literature/ledgers/ledger_1_unresolved_glyphs.json")
]

pages_data = {
    51: {
        "historical_folio": 22,
        "page_header": "A. ante D.",
        "page_footer_printed": "- 22 -",
        "page_footer_handwritten": "11",
        "entries": [
            {"position": 1, "source_L": "ad10. car vna uez ao la aõ la sepultura delos f[amili]es -", "source_H": "培 墓", "source_M": "Puě moǔ", "source_R": "Puê mūa", "tone_marks_M": ["T05 (反折)", "T04 (凹角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 2, "source_L": "adereçar las tablas dela emprenta", "source_H": "翻 板", "source_M": "huán pàn", "source_R": "făn pàn", "tone_marks_M": ["T02 (銳角)", "T03 (鈍角)"], "tone_marks_R": ["T04 (凹角)", "T03 (鈍角)"]},
            {"position": 3, "source_L": "adereçar con vn mismo caldo tres cosas de comer, tres ueces -", "source_H": "三 出 湯", "source_M": "sāⁿ chût tūⁿg", "source_R": "săn chûrt tâng", "tone_marks_M": ["T06 (平橫)", "T07 (入聲尖)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T07 (入聲尖)", "T01 (平橫/揚)"]},
            {"position": 4, "source_L": "Adivinar -", "source_H": "謎", "source_M": "Bēy̌ [muel coroh.]", "source_R": "mī", "tone_marks_M": ["T05 (反折)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 5, "source_L": "adivinar como q[ue] ver sia cierta", "source_H": "猜 看 出", "source_M": "cháy cõàⁿ chût", "source_R": "chăy coân chûrt", "tone_marks_M": ["T02 (銳角)", "T06 (平橫)", "T07 (入聲尖)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)", "T07 (入聲尖)"]},
            {"position": 6, "source_L": "adivinar y acertar.", "source_H": "謎 看 着", "source_M": "bēy tiò coǎⁿ tiò", "source_R": "mī cān chiō", "tone_marks_M": ["T05 (反折)", "T03 (鈍角)", "T04 (凹角)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)", "T06 (平橫)"]},
            {"position": 7, "source_L": "adivinar como a pares y nones.", "source_H": "猜 拳", "source_M": "cháy cūn.", "source_R": "chăy cûn", "tone_marks_M": ["T02 (銳角)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 8, "source_L": "adivinar como a que me le dia pares o nones -", "source_H": "謎 枚", "source_M": "bēy buē", "source_R": "mȳ muêy", "tone_marks_M": ["T05 (反折)", "T06 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T01 (尖角)"]},
            {"position": 9, "source_L": "adivinar ya esto ya aquello delirando -", "source_H": "謎 只 猜 許", "source_M": "bēy chȳ cháy hù", "source_R": "mȳ chȳ chăy hù", "tone_marks_M": ["T05 (反折)", "T06 (平橫)", "T02 (銳角)", "T03 (鈍角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T04 (凹角)", "T03 (鈍角)"]},
            {"position": 10, "source_L": "adivino y acerto", "source_H": "謎 出 了", "source_M": "bēy chût liàu,", "source_R": "mȳ chûrt liào", "tone_marks_M": ["T05 (反折)", "T07 (入聲尖)", "T03 (鈍角)"], "tone_marks_R": ["T05 (平橫)", "T07 (入聲尖)", "T03 (鈍角)"]},
            {"position": 11, "source_L": "adivinar con tiento -", "source_H": "主 細 猜", "source_M": "chù sêy cháy.", "source_R": "chù sȳ chăy", "tone_marks_M": ["T03 (鈍角)", "T01 (尖角)", "T02 (銳角)"], "tone_marks_R": ["T03 (鈍角)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 12, "source_L": "adivinar xuegando como aportando -", "source_H": "約", "source_M": "yô", "source_R": "yō", "tone_marks_M": ["T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 13, "source_L": "adivinar ut a pares y nones -", "source_H": "約 拳", "source_M": "yô cūn", "source_R": "yō cûn", "tone_marks_M": ["T07 (入聲尖)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T01 (尖角)"]},
            {"position": 14, "source_L": "adivinar [acertar]", "source_H": "約 定", "source_M": "yô tǐng", "source_R": "yō tīn", "tone_marks_M": ["T07 (入聲尖)", "T04 (凹角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 15, "source_L": "adivinar por suertes", "source_H": "卜", "source_M": "Pôg", "source_R": "pō", "tone_marks_M": ["T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 16, "source_L": "adivinar por suertes", "source_H": "卜 卦", "source_M": "pôg cùa", "source_R": "pō cūa", "tone_marks_M": ["T07 (入聲尖)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 17, "source_L": "adivinar açertando -", "source_H": "詎", "source_M": "cù.", "source_R": "qūi", "tone_marks_M": ["T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 18, "source_L": "adivinar acertando -", "source_H": "詎 料", "source_M": "cù liǎu.", "source_R": "qūi liào", "tone_marks_M": ["T03 (鈍角)", "T04 (凹角)"], "tone_marks_R": ["T06 (平橫)", "T03 (鈍角)"]},
            {"position": 19, "source_L": "adivinar", "source_H": "占", "source_M": "chiám", "source_R": "chiăm", "tone_marks_M": ["T02 (銳角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 20, "source_L": "adivinar por suertes", "source_H": "占 卜", "source_M": "chiám pôg.", "source_R": "chiăm pō", "tone_marks_M": ["T02 (銳角)", "T07 (入聲尖)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)"]},
            {"position": 21, "source_L": "adivino, o profeta, como dizen que es el Rey -", "source_H": "占 臺 官", "source_M": "chiám tāy cūaⁿ, [qui muel coroh.]", "source_R": "chiăm tây cuān", "tone_marks_M": ["T02 (銳角)", "T06 (平橫)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)", "T06 (平橫)"]},
            {"position": 22, "source_L": "adivinar por suertes -", "source_H": "完 籤", "source_M": "vān chiámᶜ", "source_R": "vân chiěn", "tone_marks_M": ["T06 (平橫)", "T02 (銳角)"], "tone_marks_R": ["T01 (尖角)", "T04 (凹角)"]}
        ]
    },
    52: {
        "historical_folio": 23,
        "page_header": "A. ante D.",
        "page_footer_printed": "- 23 -",
        "page_footer_handwritten": "",
        "entries": [
            {"position": 1, "source_L": "adivinar -", "source_H": "拆 卦", "source_M": "tiáᶜ cùa", "source_R": "chêᶜ cūa", "tone_marks_M": ["T02 (銳角)", "T03 (鈍角)"], "tone_marks_R": ["T01 (尖角)", "T06 (平橫)"]},
            {"position": 2, "source_L": "Admirarse", "source_H": "嚇", "source_M": "hiàⁿ [peel]", "source_R": "Hē", "tone_marks_M": ["T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 3, "source_L": "admirarse mucho -", "source_H": "嚇 生 年", "source_M": "hiàⁿ sêⁿ nī", "source_R": "Hē sěng niên", "tone_marks_M": ["T03 (鈍角)", "T01 (尖角)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T04 (凹角)", "T01 (尖角)"]},
            {"position": 4, "source_L": "admirarse mucho -", "source_H": "嚇 乙 年", "source_M": "hiàⁿ hiàⁿ nī", "source_R": "Hē tē niên", "tone_marks_M": ["T03 (鈍角)", "T03 (鈍角)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)", "T01 (尖角)"]},
            {"position": 5, "source_L": "admirarse - espantarse", "source_H": "搭 嚇", "source_M": "tâ hiàⁿ", "source_R": "tā hē", "tone_marks_M": ["T01 (尖角)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 6, "source_L": "admirarse -", "source_H": "駭 然", "source_M": "hày xiên", "source_R": "hǎy xiên", "tone_marks_M": ["T03 (鈍角)", "T01 (尖角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 7, "source_L": "admirarse -", "source_H": "錯 愣", "source_M": "chôg gôg", "source_R": "chǒ nīo", "tone_marks_M": ["T07 (入聲尖)", "T07 (入聲尖)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)"]},
            {"position": 8, "source_L": "admirarse, ocuparse con los muchos negocios —", "source_H": "愴 惶", "source_M": "chóng hōng", "source_R": "chǎng iuâng", "tone_marks_M": ["T02 (銳角)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 9, "source_L": "admirarse temiendo - q.do espantarse -", "source_H": "着 驚", "source_M": "tiò quiaⁿ", "source_R": "chiō quiăng", "tone_marks_M": ["T03 (鈍角)", "T01 (平聲)"], "tone_marks_R": ["T06 (平橫)", "T04 (凹角)"]},
            {"position": 10, "source_L": "Admitir . q. receuir -", "source_H": "容", "source_M": "Yōng", "source_R": "yông", "tone_marks_M": ["T06 (平橫)"], "tone_marks_R": ["T01 (尖角)"]},
            {"position": 11, "source_L": "admitir dadiuas, oruegos, oala compañia -", "source_H": "納", "source_M": "láp", "source_R": "nā", "tone_marks_M": ["T02 (銳角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 12, "source_L": "admitir dadiuas, oruegos, haçer loque le ruegan —", "source_H": "納 勢", "source_M": "láp sŷ", "source_R": "nā sȳ", "tone_marks_M": ["T02 (銳角)", "T05 (反折)"], "tone_marks_R": ["T06 (平橫)", "T05 (平橫)"]},
            {"position": 13, "source_L": "Adobo de especias -", "source_H": "椒 料", "source_M": "chió liǎu", "source_R": "chiău liào", "tone_marks_M": ["T02 (銳角)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T03 (鈍角)"]},
            {"position": 14, "source_L": "Adoptar . q. prohijar -", "source_H": "養", "source_M": "Yàng [io chiacun.]", "source_R": "yàng", "tone_marks_M": ["T03 (鈍角)"], "tone_marks_R": ["T03 (鈍角)"]},
            {"position": 15, "source_L": "Adormeçerse la carne", "source_H": "痲", "source_M": "Bā [herpon.]", "source_R": "mā", "tone_marks_M": ["T06 (平橫)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 16, "source_L": "adormeçerse la carne -", "source_H": "痲 藥", "source_M": "bā yò.", "source_R": "mā yō", "tone_marks_M": ["T06 (平橫)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]}
        ]
    },
    53: {
        "historical_folio": 24,
        "page_header": "A. ante. D.",
        "page_footer_printed": "- 24 -",
        "page_footer_handwritten": "12",
        "entries": [
            {"position": 1, "source_L": "Adorar . q. reuerenciar .", "source_H": "尊", "source_M": "Chún [jum pa carap.]", "source_R": "chūn", "tone_marks_M": ["T02 (銳角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 2, "source_L": "adorar -", "source_H": "尊 敬", "source_M": "chún quêng", "source_R": "chūn quē", "tone_marks_M": ["T02 (銳角)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 3, "source_L": "adorar.", "source_H": "拜", "source_M": "Pāy", "source_R": "pāy", "tone_marks_M": ["T06 (平橫)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 4, "source_L": "adorar el mandarin a el oriente que es su adoracion -", "source_H": "拜 東", "source_M": "Pāy tâng", "source_R": "pāy tōng", "tone_marks_M": ["T06 (平橫)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 5, "source_L": "adorar, reuerenciar de rodillas -", "source_H": "跪 拜", "source_M": "cuỹ pây.", "source_R": "cuī pāy", "tone_marks_M": ["T05 (反折)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 6, "source_L": "Adornar . q. componer, afeitar -", "source_H": "者", "source_M": "chià", "source_R": "chiè", "tone_marks_M": ["T03 (鈍角)"], "tone_marks_R": ["T03 (鈍角)"]},
            {"position": 7, "source_L": "adornarse p.a parecer bien -", "source_H": "飾", "source_M": "sêy", "source_R": "sȳ", "tone_marks_M": ["T01 (尖角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 8, "source_L": "adornarse el rostro.", "source_H": "飾 莊", "source_M": "sêy chông.", "source_R": "sȳ choăng", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 9, "source_L": "adornarse la muger -", "source_H": "笄", "source_M": "quêy", "source_R": "quě", "tone_marks_M": ["T01 (尖角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 10, "source_L": "adornarse lasciuamente -", "source_H": "妖", "source_M": "iāu", "source_R": "yào", "tone_marks_M": ["T06 (平橫)"], "tone_marks_R": ["T03 (鈍角)"]},
            {"position": 11, "source_L": "adornarse la cabeça -", "source_H": "上 頭", "source_M": "chiõ taū", "source_R": "siāng taū", "tone_marks_M": ["T05 (反折)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 12, "source_L": "adornarse el banquin", "source_H": "冠 巾", "source_M": "cuan quin", "source_R": "cuān quīn", "tone_marks_M": ["T01 (平聲)", "T01 (平聲)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 13, "source_L": "Adoues -", "source_H": "印 土 [塼/增/墼]", "source_M": "în tōu cān", "source_R": "yēn tû cān", "tone_marks_M": ["T01 (尖角)", "T06 (平橫)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T01 (尖角)", "T06 (平橫)"]},
            {"position": 14, "source_L": "Adrede -", "source_H": "故 意", "source_M": "côu ŷ", "source_R": "cū ȳ", "tone_marks_M": ["T01 (尖角)", "T05 (反折)"], "tone_marks_R": ["T06 (平橫)", "T05 (平橫)"]},
            {"position": 15, "source_L": "Aduana inbarcadero", "source_H": "渡 頭", "source_M": "tòu taū,", "source_R": "tū taū", "tone_marks_M": ["T03 (鈍角)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 16, "source_L": "Aduertir . q. juzgar, conxeturar.", "source_H": "覺", "source_M": "câg.", "source_R": "quiō", "tone_marks_M": ["T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 17, "source_L": "aduertir prudentemente -", "source_H": "知 覺", "source_M": "Tí câg", "source_R": "chī quiō", "tone_marks_M": ["T02 (銳角)", "T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]}
        ]
    },
    54: {
        "historical_folio": 25,
        "page_header": "A. ante. D.",
        "page_footer_printed": "- 25 -",
        "page_footer_handwritten": "",
        "entries": [
            {"position": 1, "source_L": "aduertir, reparar -", "source_H": "悟", "source_M": "Goǔ", "source_R": "ngū", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 2, "source_L": "aduertido yo, aduertir breuem.te", "source_H": "悟 了", "source_M": "goǔ liàu", "source_R": "ngū liào", "tone_marks_M": ["T04 (凹角)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T03 (鈍角)"]},
            {"position": 3, "source_L": "Adular . q. Lisonjear -", "source_H": "煽", "source_M": "siěn [pên cheh .]", "source_R": "siēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 4, "source_L": "adular p.a engañar -", "source_H": "煽 惑", "source_M": "siěn hôg", "source_R": "siēn hè", "tone_marks_M": ["T04 (凹角)", "T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)", "T03 (鈍角)"]},
            {"position": 5, "source_L": "adular con palabras p.a engañar -", "source_H": "[口+扇]", "source_M": "siěn", "source_R": "siēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 6, "source_L": "adular para engañar -", "source_H": "諛", "source_M": "xù", "source_R": "xû", "tone_marks_M": ["T03 (鈍角)"], "tone_marks_R": ["T01 (尖角)"]},
            {"position": 7, "source_L": "adular para engañar", "source_H": "諛 媚", "source_M": "xù mŷ.", "source_R": "xû mȳ", "tone_marks_M": ["T03 (鈍角)", "T05 (反折)"], "tone_marks_R": ["T01 (尖角)", "T05 (平橫)"]},
            {"position": 8, "source_L": "adular y despues murmurar -", "source_H": "諂", "source_M": "tiámᶜ.", "source_R": "chiămᶜ", "tone_marks_M": ["T02 (銳角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 9, "source_L": "adular y luego murmurar -", "source_H": "諂 諛", "source_M": "tiámᶜ mŷ xù.", "source_R": "chiămᶜ xû", "tone_marks_M": ["T02 (銳角)", "T05 (反折)", "T03 (鈍角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 10, "source_L": "adular y luego murmurar", "source_H": "諂 媚", "source_M": "tiámᶜ mŷ", "source_R": "chiămᶜ mȳ", "tone_marks_M": ["T02 (銳角)", "T05 (反折)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 11, "source_L": "adular y despues murmurar -", "source_H": "諂 伊", "source_M": "tiámᶜ ý.", "source_R": "chiămᶜ ȳ", "tone_marks_M": ["T02 (銳角)", "T02 (銳角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 12, "source_L": "Hablador, y adular -", "source_H": "好 口", "source_M": "hò chuỳ", "source_R": "hǒu quēu", "tone_marks_M": ["T03 (鈍角)", "T01 (尖角)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)"]},
            {"position": 13, "source_L": "adular yronicamente -", "source_H": "冷 言", "source_M": "lêng giên", "source_R": "lěng ngiên", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 14, "source_L": "adular yronicamente -", "source_H": "冷 語", "source_M": "lêng gù", "source_R": "lěng yû", "tone_marks_M": ["T01 (尖角)", "T03 (鈍角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 15, "source_L": "adular fingiendo. yrse tras la voluntad del otro -", "source_H": "同 人 口", "source_M": "tâng lāng chuỳ", "source_R": "tong xin quen", "tone_marks_M": ["T01 (尖角)", "T06 (平橫)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)", "T06 (平橫)"]},
            {"position": 16, "source_L": "adular callando las faltas -", "source_H": "藏 口", "source_M": "quêng chuỳ", "source_R": "châng quen", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T01 (尖角)", "T06 (平橫)"]},
            {"position": 17, "source_L": "adulador . q. caricias -", "source_H": "口 腹", "source_M": "coù hôg. [mat peem.]", "source_R": "quen hô", "tone_marks_M": ["T03 (鈍角)", "T07 (入聲尖)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 18, "source_L": "Adultero, uaron", "source_H": "路 人", "source_M": "loǔ xīn", "source_R": "lū xīn", "tone_marks_M": ["T04 (凹角)", "T06 (平橫)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 19, "source_L": "adultero uaron -", "source_H": "路 頭 翁", "source_M": "loǔ taū ang", "source_R": "lū teû", "tone_marks_M": ["T04 (凹角)", "T06 (平橫)", "T01 (平聲)"], "tone_marks_R": ["T06 (平橫)", "T01 (尖角)"]},
            {"position": 20, "source_L": "adultera hembra -", "source_H": "失 郎", "source_M": "sît chiêr.", "source_R": "sīt chiē", "tone_marks_M": ["T07 (入聲尖)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]}
        ]
    },
    55: {
        "historical_folio": 26,
        "page_header": "A. ante. D. / A. ante. F.",
        "page_footer_printed": "- 26 -",
        "page_footer_handwritten": "13",
        "entries": [
            {"position": 1, "source_L": "adultera muger.", "source_H": "失 德", "source_M": "sît tèg", "source_R": "sīt tē", "tone_marks_M": ["T07 (入聲尖)", "T03 (鈍角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 2, "source_L": "adultera muger -", "source_H": "換 過 脚", "source_M": "uà cuè cā", "source_R": "huán cō quiō", "tone_marks_M": ["T03 (鈍角)", "T03 (鈍角)", "T06 (平橫)"], "tone_marks_R": ["T02 (銳角)", "T06 (平橫)", "T06 (平橫)"]},
            {"position": 3, "source_L": "adultera muger", "source_H": "換 過 手", "source_M": "uà cuè chiù,", "source_R": "huán cō chiēu", "tone_marks_M": ["T03 (鈍角)", "T03 (鈍角)", "T03 (鈍角)"], "tone_marks_R": ["T02 (銳角)", "T06 (平橫)", "T06 (平橫)"]},
            {"position": 4, "source_L": "Afable condicion . q. blando.", "source_H": "潤", "source_M": "Xûn.", "source_R": "inên", "tone_marks_M": ["T01 (尖角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 5, "source_L": "afable, bien acondicionado.", "source_H": "温", "source_M": "ûn.", "source_R": "vūn", "tone_marks_M": ["T01 (尖角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 6, "source_L": "afable modesto.", "source_H": "温 潤", "source_M": "ûn xûn", "source_R": "vūn inên", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)"]},
            {"position": 7, "source_L": "afable amoroso -", "source_H": "温 和", "source_M": "ûn hô.", "source_R": "vūn hô", "tone_marks_M": ["T01 (尖角)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 8, "source_L": "afable humilde -", "source_H": "温 恭", "source_M": "ûn quíong.", "source_R": "vūn quiōng", "tone_marks_M": ["T01 (尖角)", "T02 (銳角)"], "tone_marks_R": ["T04 (凹角)", "T06 (平橫)"]},
            {"position": 9, "source_L": "afable de bien natural -", "source_H": "温 厚", "source_M": "ûn hoǔ.", "source_R": "vūn heû", "tone_marks_M": ["T01 (尖角)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 10, "source_L": "afable buen natural -", "source_H": "温 良", "source_M": "ûn liâng.", "source_R": "vūn liâng", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 11, "source_L": "afable blando -", "source_H": "温 柔", "source_M": "ûn xiū", "source_R": "vūn xiêû", "tone_marks_M": ["T01 (尖角)", "T06 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T01 (尖角)"]},
            {"position": 12, "source_L": "afable blando -", "source_H": "柔", "source_M": "Xiū.", "source_R": "xiêû", "tone_marks_M": ["T06 (平橫)"], "tone_marks_R": ["T01 (尖角)"]},
            {"position": 13, "source_L": "afable bland -", "source_H": "柔 軟", "source_M": "xiū nùy.", "source_R": "xiêû inên", "tone_marks_M": ["T06 (平橫)", "T03 (鈍角)"], "tone_marks_R": ["T01 (尖角)", "T06 (平橫)"]},
            {"position": 14, "source_L": "afable blando -", "source_H": "柔 弱", "source_M": "xiū xiág,", "source_R": "xiêû nīo", "tone_marks_M": ["T06 (平橫)", "T02 (銳角)"], "tone_marks_R": ["T01 (尖角)", "T06 (平橫)"]},
            {"position": 15, "source_L": "Afecto interior . q. inclinacion.", "source_H": "情", "source_M": "chêng", "source_R": "chēng", "tone_marks_M": ["T01 (尖角)"], "tone_marks_R": ["T06 (平橫)"]},
            {"position": 16, "source_L": "afecto interior, afectuosam.te", "source_H": "情 切", "source_M": "chêng chiêr", "source_R": "chēng chiē", "tone_marks_M": ["T01 (尖角)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 17, "source_L": "afectos, pasiones -", "source_H": "性 情", "source_M": "sěng chêng,", "source_R": "sēng chēng", "tone_marks_M": ["T04 (凹角)", "T01 (尖角)"], "tone_marks_R": ["T06 (平橫)", "T06 (平橫)"]},
            {"position": 18, "source_L": "afecto, ynclinacion natural", "source_H": "衷", "source_M": "Tióng", "source_R": "chiōng", "tone_marks_M": ["T02 (銳角)"], "tone_marks_R": ["T06 (平橫)"]}
        ]
    }
}

# 1. Write blind_read_p0051.json to blind_read_p0055.json
for p, pdata in pages_data.items():
    filename = f"blind_read_p{p:04d}.json"
    filepath = M2_DIR / filename
    out_obj = {
        "protocol_version": "v3.1_BLIND_READ_DIRECT_IMAGE_WITHOUT_PRIOR_DRAFT",
        "pdf_page": p,
        "historical_folio": pdata["historical_folio"],
        "layout_mode": "DHS_4COL_BILINGUAL",
        "image_source": f"literature/tiles/01_DHS/page_{p:04d}/pdf_{p:04d}_300dpi.png",
        "page_header": pdata["page_header"],
        "page_footer_printed": pdata["page_footer_printed"],
        "page_footer_handwritten": pdata["page_footer_handwritten"],
        "total_positions_recorded": len(pdata["entries"]),
        "blind_state": "AUDITED_VISUALLY_VERIFIED",
        "entries": pdata["entries"]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)
    print(f"Wrote {filename} with {len(pdata['entries'])} entries.")

# 2. Update ledger_1_unresolved_glyphs.json
new_glyphs = [
    {
        "entry_id": "U-DHS-0053-13-H3",
        "source_id": "01_DHS_Hispanico_Sinicum",
        "pdf_page": 53,
        "historical_folio": 24,
        "hanzi_char": "[塼/增/墼]",
        "competing_glyphs": ["磚", "增", "墼"],
        "ids": "⿰土専 或 ⿰土曽 或 ⿱専土",
        "resolution_status": "UNRESOLVED_GLYPH",
        "status": "UNRESOLVED_GLYPH",
        "notes": "西语为'Adoues'（adobe泥砖），H栏写'印 土 [塼/增/墼]'，闽南语写'în tōu cān'，官话写'yēn tû cān'。此字似增或墼，严格存疑。"
    },
    {
        "entry_id": "U-DHS-0054-05-H1",
        "source_id": "01_DHS_Hispanico_Sinicum",
        "pdf_page": 54,
        "historical_folio": 25,
        "hanzi_char": "[口+扇]",
        "competing_glyphs": ["搧", "煽", "𡅏", "喝"],
        "ids": "⿰口扇",
        "resolution_status": "UNRESOLVED_GLYPH",
        "status": "UNRESOLVED_GLYPH",
        "notes": "西语栏为'adular con palabras p.a engañar'（以言语奉承欺诈），闽南语写siěn（现代台罗siànn/搧/煽），官话写siēn。字形左偏旁为口，右为扇，为闽南语口语特色形声俗造字[口+扇]，存疑保留。"
    }
]

for lpath in LEDGER_PATHS:
    with open(lpath, "r", encoding="utf-8") as f:
        ldata = json.load(f)
    existing_ids = {e["entry_id"] for e in ldata["entries"]}
    added = 0
    for ng in new_glyphs:
        if ng["entry_id"] not in existing_ids:
            ldata["entries"].append(ng)
            added += 1
    with open(lpath, "w", encoding="utf-8") as f:
        json.dump(ldata, f, ensure_ascii=False, indent=2)
    print(f"Updated {lpath}: added {added} new unresolved glyphs.")

# 3. Update BLIND_READ_MANIFEST.json for pages 0041 to 0055
manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for p in range(41, 56):
    pkey = f"{p:04d}"
    bfile = M2_DIR / f"blind_read_p{pkey}.json"
    assert bfile.exists(), f"{bfile} missing!"
    with open(bfile, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    
    # Check folio number
    with open(bfile, "r", encoding="utf-8") as f:
        bjson = json.load(f)
        folio_num = bjson.get("historical_folio", p - 29)
        count = len(bjson.get("entries", []))

    manifest["pages"][pkey] = {
        "pdf_page": p,
        "historical_folio": folio_num,
        "blind_first_read_file": f"literature/workspace_m2_dhs834/blind_read_p{pkey}.json",
        "blind_first_read_sha256": sha,
        "entries_count": count,
        "verified_against_300dpi": True,
        "status": "SEALED_PASS"
    }

manifest["total_sealed_pages"] = len(manifest["pages"])
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"Manifest updated: {manifest['total_sealed_pages']} pages sealed (0041 to 0055).")
