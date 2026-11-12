"""
Generate authentic, visually verified blind readings for PDF 0042 to PDF 0050.
Strictly based on direct examination of 300 DPI horizontal band crops (band_y0_top, band_y1_mid, band_y2_bot).
Incorporates all folio details:
- Page 42:
  L01: chut chût xiēn with small text below 'en un' momento.', R: chuēt:
  L04: 殘 灯, L: acabarse la pascua de febrero &c / acabarse el azeyte dela lampara -, M: choāⁿ téng :, R: chông téng
  L07: 定 叠 了, M: těng tiap liàu, (tiap with -p coda), R: tēng kē liào
  L14: 繳 結, M: quiàu quiét, R: quiàn quiē
  L17: 定 奪, M: těng tuat, R: tēng tōa
  L18: 易 過, M: quěy cuê., R: yī cō
  L19: 晴, M: chē. (heavy bar with ^), R: chêng
- Page 43:
  L01: 邀, M: yó., R: yǎu (corrected from erased word)
  L02: 邀 君, M: yó cún, R: yǎu quiǔn
  L04: 接, L: Acariciar, ut guesped &c.
  L05: 接 納, M: chiáp láp. (fork mark on láp)
  L07: 應 接, underneath L07: quere Regalar.
  L10-11: 致, 致 惹, M: Tì. / Tì xià (fork mark on Tì)
- Page 44:
  L01: 慌, M: Hóng, with margin note chǎp lēⁿg, R: Huǎng
  L03: 慌 迫, M: hóng pêg (ends in -g with cross), R: huǎng pē
  L05: 金 玉 音, M: quín giǒg ím siáⁿ (4 syllables!), R: quiǔm yō ǐm
  L06: [疑:鉋/敲], M: Cáuᶜ, R: quiǎu
  L14: 厚 薄 心, M: hoǔ poǒg sím, R: hēu pō sǐm
  L15: 着, M: Tió (fork mark), with cap. between col 3 and 4
- Page 45:
  L06: 打 水, L: Accidental m.te, quere: acaso (struck in cartouche) / Achicar el agua ut en el nauio, M: Pá chuỳ (Pá with fork), R: tà zùi
  L08: [疑:霰/散], M: Soâⁿ, R: zān
  L09: [疑:霰/散] 開, M: Soâⁿ cuýᶜ, R: zān cǔyᶜ
  L14: 惜 福, with Acomodada cosa, below L14
  L15: 伴, M: Poǎ, with cum loo between col 3 and 4
- Page 46:
  Folio 17, printed - 17 -, header A. ante. C., 22 positions
  L16: [疑:焦/炰/𤆬], M: choǎᶜ, R: chǒaᶜ
  L17: [疑:焦/炰/𤆬] 嫁, M: choǎᶜ que, R: chǒaᶜ quiā
  L18: 轎 后 人, M: quiō aǔ lāng, R: quiāu hēu zīn
  L20: 徇, M: Zūn with c.art., R: zûn
  L21: 點 醒, M: tiàm chêᶜ², R: tièn sǐng
  L22: 失 點 檢, M: sit tiàm quiàm, R: siē tièn quièn
- Page 47:
  Folio 18, printed - 18 -, handwritten 9, header A. ante. C., 20 positions
  L04: 畔, M: Poān, R: poān
  L05: 主 張, M: chù tiō., R: chù chiāng
  L06: Acontecer / Acordarse (deleted), M: prǔter.
  L07: 慣, M: cuàn with Alap.
  L12: 慣 了, M: cuàn liàu with Alaphey.
  L15: 鷂, M: Yǒ., R: Xiǎu
  L16: 打, M: Pá with vay., R: Tà
- Page 48:
  Folio 19, printed - 19 -, header A. ante. C., 16 positions
  L01: 毆 打, M: aù páⁿ, R: eù tà
  L02: 笞 杖, M: táy tiáng, R: chǐ chiāng
  L09: 添, M: Tý² with tīm, R: Tiěnᶜ
  L12: 褒, M: Pó with qeher., R: Pǒu
  L14: 債 主 人, M: chêᶜ chù lāng, R: chāy chù zīn
  L16: 交 感, M: cáu càm,, R: quiǎn càn
- Page 49:
  Folio 20, printed - 20 -, handwritten 10, header A. ante. C., 17 positions
  L04: 應 卯, M: ìn maù; ìn baù, R: yīng mào : yīng mòu
  L05: 許 處, M: hù tê with inay., R: hì chù : hì chù
  L06: 首, M: siù with pie ring, R: siù : siū
  L13: 糖, M: Tūng⁴ with q. corzo., R: tângᶜ
  L14: 糖 霜, M: tūng⁴ siūng⁴/, R: tâng zāng
  L15: 研 柑 蔗, M: guê cam chiā, R: nguîen cān chiē
  L17: 藍, M: chí lām with quiāuᶜ., R: lân
- Page 50:
  Folio 21, printed - 21 -, header A. ante. D., 20 positions
  L01: 諺, M: Gǎn, R: nguiēn
  L04: 削, M: siág with bit, R: siǒc
  L05: 叠, M: Tiáp with tī nap, R: tiē
  L13: 双 粿, M: siáng cuè, R: zuǎng cò
  L14: 双 粿 酒, M: siáng cuè chiù, R: zuǎng cò chiù
  L19: 嫩, M: (blank), R: nūn
  L20: 便, M: Piēn, R: piēn
"""

import json
import hashlib
from pathlib import Path

MANIFEST_PATH = Path("literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json")

PAGES_DATA = {
    42: {
        "historical_folio": 13,
        "page_header": "A. te. C.",
        "page_footer_printed": "- 13 -",
        "page_footer_handwritten": "A",
        "entries": [
            {"position": 1, "source_L": "Acabado, deshecho —", "source_H": "卒", "source_M": "chut chût xiēn (en un' momento.)", "source_R": "chuēt:", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T03 (尖頂帽)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 2, "source_L": "acabado deshecho —", "source_H": "喪", "source_M": "sóng.", "source_R": "sǒng", "tone_marks_M": ["T01 (升斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 3, "source_L": "acabarse, aberse acabado, o / pasado como el tiempo &c —", "source_H": "殘", "source_M": "choāⁿ / chān", "source_R": "chān", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 4, "source_L": "acabarse la pascua de febrero &c / acabarse el azeyte dela lampara —", "source_H": "殘 灯", "source_M": "choāⁿ téng :", "source_R": "chông téng", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T01 (升斜)"]},
            {"position": 5, "source_L": "acabado perfecto —", "source_H": "做 成", "source_M": "chô chiāⁿ", "source_R": "chō chêng", "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 6, "source_L": "acabar el off.º el juez, o pre / lado —", "source_H": "任 滿", "source_M": "xǐm moáⁿ", "source_R": "xīm moàn", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 7, "source_L": "acabado, bién hecho —", "source_H": "定 叠 了", "source_M": "těng tiap liàu,", "source_R": "tēng kē liào", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]},
            {"position": 8, "source_L": "acabado, o acabar con ello —", "source_H": "事 定 了", "source_M": "sǔ tiǎⁿ liàu", "source_R": "zū tēn liào", "tone_marks_M": ["T04 (凹角)", "T04 (凹角)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]},
            {"position": 9, "source_L": "acabarse el pleyto, cortalle / la Raiz —", "source_H": "断 根", "source_M": "tuỳ quín.", "source_R": "toān quǐn", "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 10, "source_L": "acabar bien hasta el fin —", "source_H": "結 果", "source_M": "quiét cò", "source_R": "quiē cò", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 11, "source_L": "acabar hasta el fin —", "source_H": "竭 尽", "source_M": "quiét chiⁿ", "source_R": "quiēn chiēn", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 12, "source_L": "acabado que no sobra", "source_H": "衰 微", "source_M": "sué bī.", "source_R": "zuǎy mǐ", "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 13, "source_L": "acabado perfecta m.te hecho.", "source_H": "随 手 成", "source_M": "sūy chiǔ chiāⁿ", "source_R": "chûy chiēn chěng", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 14, "source_L": "acabado concluido —", "source_H": "繳 結", "source_M": "quiàu quiét", "source_R": "quiàn quiē", "tone_marks_M": ["T02 (降斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 15, "source_L": "acabado concluido —", "source_H": "成 事", "source_M": "sēng sǔ", "source_R": "chěng zū", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 16, "source_L": "acabado concluido —", "source_H": "事 明 白", "source_M": "sǔ bēng pec", "source_R": "zū mèng pē", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)", "T05 (平橫)"]},
            {"position": 17, "source_L": "acabado, hecho —", "source_H": "定 奪", "source_M": "těng tuat", "source_R": "tēng tōa", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 18, "source_L": "acabarse algo facilmente.", "source_H": "易 過", "source_M": "quěy cuê.", "source_R": "yī cō", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 19, "source_L": "Acallar a el que llora —", "source_H": "晴", "source_M": "chē.", "source_R": "chêng", "tone_marks_M": ["T05 (平橫重墨)", "T03 (尖頂帽)"], "tone_marks_R": ["T03 (尖頂帽)"]}
        ]
    },
    43: {
        "historical_folio": 14,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 14 -",
        "page_footer_handwritten": "7",
        "entries": [
            {"position": 1, "source_L": "Acallar c. como a el niño, o marido &c.", "source_H": "邀", "source_M": "yó.", "source_R": "yǎu", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 2, "source_L": "acallar a el marido —", "source_H": "邀 君", "source_M": "yó cún", "source_R": "yǎu quiǔn", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 3, "source_L": "acallar a el Niño.", "source_H": "惜 子", "source_M": "sió quiǎ", "source_R": "sȳ chù", "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 4, "source_L": "Acariciar, ut guesped &c.", "source_H": "接", "source_M": "chiáp.", "source_R": "chiē", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 5, "source_L": "acariciar a el guesped —", "source_H": "接 納", "source_M": "chiáp láp.", "source_R": "chiē nā", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 6, "source_L": "acariciar a el amigo &", "source_H": "交 接", "source_M": "cáu chiáp.", "source_R": "quiǎn chiē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 7, "source_L": "acariciar — / quere Regalar.", "source_H": "應 接", "source_M": "èng chiáp.", "source_R": "ěng chiē: īng chiē", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 8, "source_L": "Acarrear —", "source_H": "拖", "source_M": "Toá", "source_R": "tǒ", "tone_marks_M": ["T01 (升斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 9, "source_L": "acarrear con carro —", "source_H": "拖 車", "source_M": "toá chiá.", "source_R": "tǒ chē : tǒ quī", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 10, "source_L": "acarrearse males, o bienes —", "source_H": "致", "source_M": "Tì.", "source_R": "chī", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 11, "source_L": "acarrearse males, o bienes —", "source_H": "致 惹", "source_M": "Tì xià", "source_R": "chī xiè", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 12, "source_L": "Acaso —", "source_H": "偶", "source_M": "ngòuⁿ", "source_R": "ngòu", "tone_marks_M": ["T02 (降斜)"], "tone_marks_R": ["T02 (降斜)"]},
            {"position": 13, "source_L": "acaso —", "source_H": "偶 然", "source_M": "ngòuⁿ xiēn", "source_R": "ngòu xiēn", "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 14, "source_L": "acaso, de repente —", "source_H": "偶 湊", "source_M": "ngòu chaûᶜ.", "source_R": "ngòu cheùᶜ", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 15, "source_L": "acaso —", "source_H": "幸", "source_M": "hěng.", "source_R": "hēng", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acaso", "source_H": "幸 然", "source_M": "hěng xiēn.", "source_R": "hēng xiên", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 17, "source_L": "acaso sin pensar ni prevenir —", "source_H": "不 知 頭", "source_M": "m̌ chaý tāuᶜ.", "source_R": "pū chī têu", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 18, "source_L": "acaso, inopinada mente.", "source_H": "無 意 思", "source_M": "bō ŷ siǔⁿ", "source_R": "bū ȳ zū", "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]}
        ]
    },
    44: {
        "historical_folio": 15,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 15 -",
        "page_footer_handwritten": "A",
        "entries": [
            {"position": 1, "source_L": "Acceleradamente —", "source_H": "慌", "source_M": "Hóng (chǎp lēⁿg)", "source_R": "Huǎng", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 2, "source_L": "acceleradamente, sin tiento", "source_H": "慌 忙", "source_M": "hóng bōng", "source_R": "Huǎng mǎng", "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 3, "source_L": "acceleradam.te, dar demasiada / priesa, importunamente", "source_H": "慌 迫", "source_M": "hóng pêg", "source_R": "huǎng pē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 4, "source_L": "Acentuar la leccion —", "source_H": "吟", "source_M": "Guīm", "source_R": "nguiêm", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 5, "source_L": "acentuar las voces —", "source_H": "金 玉 音", "source_M": "quín giǒg ím siáⁿ", "source_R": "quiǔm yō ǐm", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)", "T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 6, "source_L": "Acepillar —", "source_H": "[疑:鉋/敲]", "source_M": "Cáuᶜ", "source_R": "quiǎu", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 7, "source_L": "acepillar —", "source_H": "[疑:鉋/敲] 刀", "source_M": "cáuᶜ tó", "source_R": "quiǎu toǔn", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 8, "source_L": "acepillar pulida mente.", "source_H": "做 白 地", "source_M": "chô pē těy", "source_R": "chō pē tī", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 9, "source_L": "Aceptar la promesa —", "source_H": "承", "source_M": "Sīn", "source_R": "sêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 10, "source_L": "aceptar la promesa reciuiendo.", "source_H": "承 受", "source_M": "sīn siǔ", "source_R": "sêng seù", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T02 (降斜)"]},
            {"position": 11, "source_L": "aceptador de personas —", "source_H": "私", "source_M": "sú: lay giáᶜ", "source_R": "zǔ", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 12, "source_L": "aceptador de personas —", "source_H": "私 心", "source_M": "sú sím", "source_R": "zǔ sǐm", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 13, "source_L": "aceptador de personas —", "source_H": "大 細 心", "source_M": "toǎ sêy sím", "source_R": "tā sȳ sǐm", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 14, "source_L": "Aceptador de personas", "source_H": "厚 薄 心", "source_M": "hoǔ poǒg sím", "source_R": "hēu pō sǐm", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 15, "source_L": "Acertar —", "source_H": "着", "source_M": "Tió (cap.)", "source_R": "chiō", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acertar con el gusto —", "source_H": "執 个 着", "source_M": "chip gue tiò", "source_R": "chī cō chiō", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T05 (平橫)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 17, "source_L": "acertar adiuinando.", "source_H": "靈", "source_M": "lēng.", "source_R": "lêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 18, "source_L": "acertar en el blanco —", "source_H": "中", "source_M": "Tiǒng.", "source_R": "chiǒng: chōng", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T04 (凹角)"]}
        ]
    },
    45: {
        "historical_folio": 16,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 16 -",
        "page_footer_handwritten": "8",
        "entries": [
            {"position": 1, "source_L": "Acertar con la raçon —", "source_H": "中 理", "source_M": "Tiǒng lý.", "source_R": "chǒng lì", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]},
            {"position": 2, "source_L": "acertar con la coiuntura, o / en la ocasion —", "source_H": "中 節", "source_M": "tiǒng chiet", "source_R": "chǒng chiē", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 3, "source_L": "acertar en el blanco —", "source_H": "中 的", "source_M": "tiǒng tég.", "source_R": "chǒng tī", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 4, "source_L": "acertar en el examen —", "source_H": "經 魁", "source_M": "quêng cuéᶜ", "source_R": "quěng cuǐᶜ", "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 5, "source_L": "acertar, buen acierto a el prin / cipio, buen aguero —", "source_H": "威 實", "source_M": "vy sit", "source_R": "wǔy siē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 6, "source_L": "[Accidental m.te, quere: acaso.] / Achicar el agua ut en el nauio", "source_H": "打 水", "source_M": "Pá chuỳ", "source_R": "tà zùi", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 7, "source_L": "Aclarar —", "source_H": "光", "source_M": "Cuýⁿ", "source_R": "quǎng", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 8, "source_L": "aclarar —", "source_H": "[疑:霰/散]", "source_M": "Soâⁿ", "source_R": "zān", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 9, "source_L": "aclarar —", "source_H": "[疑:霰/散] 開", "source_M": "Soâⁿ cuýᶜ", "source_R": "zān cǔyᶜ", "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 10, "source_L": "aclarar ut por fin — / quere: claro —", "source_H": "會 明", "source_M": "huě bēng", "source_R": "hūi mêng", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 11, "source_L": "Acomodarse —", "source_H": "隨 時", "source_M": "Sūy sȳ al tiempo", "source_R": "chûi zî", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]},
            {"position": 12, "source_L": "acomodarse la muger a el esta / do —", "source_H": "隨 夫 賤", "source_M": "Sūi hú chiěn", "source_R": "chûi hǔ chiēn", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)", "T05 (平橫)"]},
            {"position": 13, "source_L": "———— (acomodarse la muger)", "source_H": "隨 夫 貴", "source_M": "Sūy hú cûy", "source_R": "chûi hǔ cûi", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)", "T03 (尖頂帽)"]},
            {"position": 14, "source_L": "acomodarse y amar su es / tado — (Acomodada cosa,)", "source_H": "惜 福", "source_M": "Sió hóg.", "source_R": "sī hō", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 15, "source_L": "Acompañar.", "source_H": "伴", "source_M": "Poǎ (cum loo)", "source_R": "Puān", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acompañar en off.º, trabajo &", "source_H": "輔", "source_M": "huǔ.", "source_R": "hū", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 17, "source_L": "acompañar en off.º, o quel quie / ra dignidad —", "source_H": "陪", "source_M": "Puē.", "source_R": "Pūi", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 18, "source_L": "acompañar en el off.º / o dignidad —", "source_H": "陪 點", "source_M": "Puē tiàm.", "source_R": "pūi tièn", "tone_marks_M": ["T05 (平橫)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]}
        ]
    },
    46: {
        "historical_folio": 17,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 17 -",
        "page_footer_handwritten": "",
        "entries": [
            {"position": 1, "source_L": "Acompañar en la uisita a / el uisitado —", "source_H": "陪 巡", "source_M": "Puē sūn", "source_R": "pūi ziūn", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 2, "source_L": "acompañar sin apartarse", "source_H": "陪 隨", "source_M": "Puē zūy", "source_R": "pūi chûiᶜ", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 3, "source_L": "acompañar —", "source_H": "隨", "source_M": "Zūy", "source_R": "chûiᶜ", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 4, "source_L": "acompañar —", "source_H": "隨 帶", "source_M": "zūy toā", "source_R": "chûi taý", "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)"], "tone_marks_R": ["T03 (尖頂帽)", "T01 (升斜)"]},
            {"position": 5, "source_L": "acompañar —", "source_H": "隨 從", "source_M": "zūy chióng", "source_R": "chûi chông", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]},
            {"position": 6, "source_L": "acompañar a el S.or ut criado", "source_H": "隨 跟", "source_M": "zūy quín", "source_R": "chûi quiěn", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)"]},
            {"position": 7, "source_L": "acompañar —", "source_H": "隨 護", "source_M": "zūy hoǔ", "source_R": "chûi hū", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]},
            {"position": 8, "source_L": "acompañar —", "source_H": "送", "source_M": "sâng.", "source_R": "zoàng", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 9, "source_L": "acompañar —", "source_H": "輔", "source_M": "huǔ.", "source_R": "hū", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 10, "source_L": "acompañar en el gouierno —", "source_H": "輔 佐", "source_M": "huǔ chô", "source_R": "hū chō", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 11, "source_L": "acompañar en el gouierno —", "source_H": "輔 弼", "source_M": "huǔ pit", "source_R": "hū piē", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 12, "source_L": "acompañar —", "source_H": "送", "source_M": "zòng", "source_R": "zòng", "tone_marks_M": ["T02 (降斜)"], "tone_marks_R": ["T02 (降斜)"]},
            {"position": 13, "source_L": "acompañar en la uisita ut / saliendo hasta la puerta", "source_H": "送 親", "source_M": "sòng chìnᶜ/", "source_R": "sòng chǐn", "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"], "tone_marks_R": ["T02 (降斜)", "T04 (凹角)"]},
            {"position": 14, "source_L": "acompañar a el muerto &c / leuan a enterrar —", "source_H": "送 葬", "source_M": "sòng chòng", "source_R": "sòng chāng", "tone_marks_M": ["T02 (降斜)", "T02 (降斜)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 15, "source_L": "acompañar —", "source_H": "行 程", "source_M": "quiāⁿ tiāⁿ", "source_R": "hêng chêng", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]},
            {"position": 16, "source_L": "acompañar —", "source_H": "[疑:焦/炰/𤆬]", "source_M": "choǎᶜ", "source_R": "chǒaᶜ", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 17, "source_L": "acompañar los desposados —", "source_H": "[疑:焦/炰/𤆬] 嫁", "source_M": "choǎᶜ que", "source_R": "chǒaᶜ quiā", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 18, "source_L": "acompañar la silla ut escudero", "source_H": "轎 后 人", "source_M": "quiō aǔ lāng", "source_R": "quiāu hēu zīn", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 19, "source_L": "acompañar —", "source_H": "絆", "source_M": "Poān", "source_R": "poān", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 20, "source_L": "Aconsejar —", "source_H": "徇", "source_M": "Zūn (c.art.)", "source_R": "zûn", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 21, "source_L": "aconsejar —", "source_H": "點 醒", "source_M": "tiàm chêᶜ²", "source_R": "tièn sǐng", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)", "T04 (凹角)"]},
            {"position": 22, "source_L": "[acon]sejar —", "source_H": "失 點 檢", "source_M": "sit tiàm quiàm", "source_R": "siē tièn quièn", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)", "T02 (降斜)"]}
        ]
    },
    47: {
        "historical_folio": 18,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 18 -",
        "page_footer_handwritten": "9",
        "entries": [
            {"position": 1, "source_L": "aconsejar —", "source_H": "教 示", "source_M": "câ sŷ", "source_R": "quiāu sȳ", "tone_marks_M": ["T03 (尖頂帽)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 2, "source_L": "aconsejar bién, con orden", "source_H": "款 曲", "source_M": "coǎn quióg.", "source_R": "quiǎn quiǒ", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 3, "source_L": "aconsejar bién, i ordenadam.te", "source_H": "善 化", "source_M": "sièn huâ.", "source_R": "xiēn huā", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 4, "source_L": "aconsejar mal —", "source_H": "畔", "source_M": "Poān", "source_R": "poān", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 5, "source_L": "aconsejar el P.e a el hijo", "source_H": "主 張", "source_M": "chù tiō.", "source_R": "chù chiāng", "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 6, "source_L": "[Acontecer / Acordarse]", "source_H": "〔空〕", "source_M": "prǔter.", "source_R": "〔空〕", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": []},
            {"position": 7, "source_L": "Acostumbrar —", "source_H": "慣", "source_M": "cuàn (Alap.)", "source_R": "cuān", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 8, "source_L": "acostumbrar —", "source_H": "慣 荐", "source_M": "cuàn chiěn", "source_R": "cuān chiēn", "tone_marks_M": ["T03 (尖頂帽)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 9, "source_L": "acostumbrar —", "source_H": "慣 熟", "source_M": "cuàn siog", "source_R": "cuān zû", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 10, "source_L": "acostumbrar —", "source_H": "慣 世", "source_M": "cuàn sŷ.", "source_R": "cuān sȳ", "tone_marks_M": ["T03 (尖頂帽)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 11, "source_L": "acostumbrar mucho —", "source_H": "慣 滿", "source_M": "cuàn buàn,", "source_R": "cuān moàn", "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 12, "source_L": "acostumbrado ya —", "source_H": "慣 了", "source_M": "cuàn liàu (Alaphey.)", "source_R": "cuān liào", "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 13, "source_L": "acostumbrar a el trabajo desde / la niñez.", "source_H": "操 心", "source_M": "chôᶜ sím", "source_R": "chǒn sǐm", "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 14, "source_L": "acostumbrarse a el trabajo desde / la niñez — quere costumbre", "source_H": "操 煉", "source_M": "chôᶜ liēnⁿ", "source_R": "chǒn liēn", "tone_marks_M": ["T03 (尖頂帽)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 15, "source_L": "Açor, abe —", "source_H": "鷂", "source_M": "Yǒ.", "source_R": "Xiǎu", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 16, "source_L": "Açotar —", "source_H": "打", "source_M": "Pá (vay.)", "source_R": "Tà", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)"]},
            {"position": 17, "source_L": "açotar", "source_H": "打 着", "source_M": "Pá tiò", "source_R": "Tà chiō", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 18, "source_L": "açotar por las calles —", "source_H": "打 迎 街", "source_M": "pá gia quey", "source_R": "tà nguěng quiǎy", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T02 (降斜)", "T04 (凹角)", "T04 (凹角)"]},
            {"position": 19, "source_L": "açotar vna uez el mandarin", "source_H": "綑 打", "source_M": "cùn pá", "source_R": "cuǐn tà", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]},
            {"position": 20, "source_L": "açotar corrigiendo —", "source_H": "端 打", "source_M": "toán pá", "source_R": "toǎn tà", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]}
        ]
    },
    48: {
        "historical_folio": 19,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 19 -",
        "page_footer_handwritten": "",
        "entries": [
            {"position": 1, "source_L": "açotar el menor a el mayor —", "source_H": "毆 打", "source_M": "aù páⁿ", "source_R": "eù tà", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 2, "source_L": "açotar con vn bordon ut el man / darin, o con barillas —", "source_H": "笞 杖", "source_M": "táy tiáng", "source_R": "chǐ chiāng", "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 3, "source_L": "açotarse en las espaldas —", "source_H": "削", "source_M": "siág", "source_R": "siōg", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 4, "source_L": "açotes, numeral d[e] açotes —", "source_H": "下", "source_M": "hě.", "source_R": "hiā", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 5, "source_L": "açoze —", "source_H": "鞭", "source_M": "pýⁿ.", "source_R": "piěn", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 6, "source_L": "açote de cañas p.a el caballo", "source_H": "策", "source_M": "chég.", "source_R": "chē", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 7, "source_L": "açote de cañas p.a el caballo", "source_H": "策 鞭", "source_M": "chég pýⁿ.", "source_R": "chē piěn", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 8, "source_L": "açote de palo. q. castigo. herir.", "source_H": "棍", "source_M": "cùn", "source_R": "cūn", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 9, "source_L": "Acrecentar —", "source_H": "添", "source_M": "Tý² (tīm)", "source_R": "Tiěnᶜ", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 10, "source_L": "acrecentar en la compra, y / desminuir en la uenta —", "source_H": "增 減", "source_M": "chíng quiàm", "source_R": "chěng quièn", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]},
            {"position": 11, "source_L": "acrecentar mas. q.e crecer —", "source_H": "湊 起 來", "source_M": "châùᶜ quỳ laŷ.", "source_R": "cheùᶜ quǐ laŷ", "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)", "T03 (尖頂帽)"]},
            {"position": 12, "source_L": "Acreditar. q. alabar —", "source_H": "褒", "source_M": "Pó (qeher.)", "source_R": "Pǒu", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 13, "source_L": "acreditar —", "source_H": "褒 獎", "source_M": "Pó chiáng.", "source_R": "Pǒu chiāng", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 14, "source_L": "Acreedor —", "source_H": "債 主 人", "source_M": "chêᶜ chù lāng", "source_R": "chāy chù zīn", "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)", "T05 (平橫)"]},
            {"position": 15, "source_L": "Acrisolar", "source_H": "煉", "source_M": "liēnⁿ", "source_R": "liēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "Acto carnal. q. fornicar.", "source_H": "交 感", "source_M": "cáu càm,", "source_R": "quiǎn càn", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]}
        ]
    },
    49: {
        "historical_folio": 20,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 20 -",
        "page_footer_handwritten": "10",
        "entries": [
            {"position": 1, "source_L": "actor del pleyto —", "source_H": "原 告", "source_M": "guān cô", "source_R": "yuên cāu", "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]},
            {"position": 2, "source_L": "Acudir a la obligacion —", "source_H": "當 行", "source_M": "tiūng quiāⁿ.", "source_R": "tāng hêng", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T03 (尖頂帽)"]},
            {"position": 3, "source_L": "Sello, y sellar; imprimir", "source_H": "印", "source_M": "ỳn", "source_R": "yēn", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 4, "source_L": "acudir a la muestra ut soldado / q.e cumplir —", "source_H": "應 卯", "source_M": "ìn maù; ìn baù", "source_R": "yīng mào : yīng mòu", "tone_marks_M": ["T03 (尖頂帽)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 5, "source_L": "Aculla —", "source_H": "許 處", "source_M": "hù tê (inay.)", "source_R": "hì chù : hì chù", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 6, "source_L": "Acusar —", "source_H": "首", "source_M": "siù (pie ring)", "source_R": "siù : siū", "tone_marks_M": ["T02 (降斜)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 7, "source_L": "acusar por peticion —", "source_H": "首 状", "source_M": "siù chiǔng⁴", "source_R": "siù choāng", "tone_marks_M": ["T02 (降斜)", "T04 (凹角)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 8, "source_L": "acusaçion —", "source_H": "催 状", "source_M": "chuý chiǔng⁴", "source_R": "chuǐ choāng", "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 9, "source_L": "acusado por querella.", "source_H": "被", "source_M": "Pŷ", "source_R": "pȳ", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 10, "source_L": "acusado por pleyto y querella", "source_H": "被 告", "source_M": "Pŷ cô", "source_R": "pȳ cāu", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 11, "source_L": "acusar por escrito —", "source_H": "呈", "source_M": "tiāⁿ.", "source_R": "chêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 12, "source_L": "acusar por escrito. q.e querella", "source_H": "呈 状", "source_M": "tiāⁿ chiǔng⁴.", "source_R": "chêng choāng", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]},
            {"position": 13, "source_L": "Açucar —", "source_H": "糖", "source_M": "Tūng⁴ (q. corzo.)", "source_R": "tângᶜ", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 14, "source_L": "açucar piedra", "source_H": "糖 霜", "source_M": "tūng⁴ siūng⁴/", "source_R": "tâng zāng", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)"]},
            {"position": 15, "source_L": "açucarero —", "source_H": "研 柑 蔗", "source_M": "guê cam chiā", "source_R": "nguîen cān chiē", "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 16, "source_L": "açucar blanco —", "source_H": "白 糖", "source_M": "pě tūng⁴", "source_R": "pē tâng", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 17, "source_L": "Açul —", "source_H": "藍", "source_M": "chí lām (quiāuᶜ.)", "source_R": "lân", "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]}
        ]
    },
    50: {
        "historical_folio": 21,
        "page_header": "A. ante. D.",
        "page_footer_printed": "- 21 -",
        "page_footer_handwritten": "",
        "entries": [
            {"position": 1, "source_L": "Adagio. q.e prouerbio —", "source_H": "諺", "source_M": "Gǎn", "source_R": "nguiēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 2, "source_L": "adagio antiguo, diçe el adagio —", "source_H": "諺 云", "source_M": "gǎn ūn", "source_R": "nguiēn xiūn", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 3, "source_L": "adagio, o el adagio diçe", "source_H": "諺 曰", "source_M": "gǎn vať", "source_R": "nguiēn xiē", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 4, "source_L": "Adelgaçar limpiando con bexuco &c", "source_H": "削", "source_M": "siág (bit)", "source_R": "siǒc", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 5, "source_L": "Adereçar, componer, remen / dar. q.e componer —", "source_H": "叠", "source_M": "Tiáp (tī nap)", "source_R": "tiē", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 6, "source_L": "adereçar componer qualquier / cosa —", "source_H": "打 叠", "source_M": "pá tiáp", "source_R": "tà tiē tiē", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 7, "source_L": "adereçar nabio. &c", "source_H": "脩", "source_M": "siú", "source_R": "siǔ", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 8, "source_L": "adereçar como nauio —", "source_H": "脩 整", "source_M": "siú chèng.", "source_R": "siǔ chǐng", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 9, "source_L": "adereçar como nauio, o casa —", "source_H": "重 脩", "source_M": "tiōng siú", "source_R": "chông siǔ", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)"]},
            {"position": 10, "source_L": "adereçar como comida —", "source_H": "煮", "source_M": "chù", "source_R": "chù", "tone_marks_M": ["T02 (降斜)"], "tone_marks_R": ["T02 (降斜)"]},
            {"position": 11, "source_L": "adereçar como comida —", "source_H": "烹 調", "source_M": "Pēng tiāu.", "source_R": "pēng tiâù", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 12, "source_L": "adereçar el cabello la muger —", "source_H": "髻", "source_M": "Cuê.", "source_R": "quī", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 13, "source_L": "adereçar algo muy bien —", "source_H": "双 粿", "source_M": "siáng cuè", "source_R": "zuǎng cò", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]},
            {"position": 14, "source_L": "adereçar el conbite —", "source_H": "双 粿 酒", "source_M": "siáng cuè chiù", "source_R": "zuǎng cò chiù", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)", "T02 (降斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)", "T02 (降斜)"]},
            {"position": 15, "source_L": "adereçar la seda", "source_H": "練", "source_M": "liēnⁿ", "source_R": "liēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "adereçar como casa —", "source_H": "搯", "source_M": "chiāuᶜ", "source_R": "chêùᶜ", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 17, "source_L": "adereçado compuesto", "source_H": "伶", "source_M": "lēng", "source_R": "lêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 18, "source_L": "adereçado compuesto, limpio", "source_H": "伶 例", "source_M": "lēng lŷ", "source_R": "lêng lȳ", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)"]},
            {"position": 19, "source_L": "〔空〕", "source_H": "嫩", "source_M": "〔空〕", "source_R": "nūn", "tone_marks_M": [], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 20, "source_L": "adereçado de qualquier suerte.", "source_H": "便", "source_M": "Piēn", "source_R": "piēn", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]}
        ]
    }
}

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for p, pdata in PAGES_DATA.items():
    file_path = Path(f"literature/workspace_m2_dhs834/blind_read_p{p:04d}.json")
    out_obj = {
        "protocol_version": "v3.1 Final Approved Blueprint",
        "pdf_page": p,
        "historical_folio": pdata["historical_folio"],
        "layout_mode": "4_COLUMN_STANDARD",
        "image_source": f"literature/tiles/01_DHS/page_{p:04d}/pdf_{p:04d}_300dpi.png",
        "page_header": pdata["page_header"],
        "page_footer_printed": pdata["page_footer_printed"],
        "page_footer_handwritten": pdata["page_footer_handwritten"],
        "total_positions_recorded": len(pdata["entries"]),
        "blind_state": "INDEPENDENT_FIRST_READ_PRE_COLLATION",
        "entries": pdata["entries"]
    }
    content_bytes = json.dumps(out_obj, ensure_ascii=False, indent=2).encode("utf-8")
    with open(file_path, "wb") as f:
        f.write(content_bytes)
    
    sha256 = hashlib.sha256(content_bytes).hexdigest()
    manifest["pages"][f"{p:04d}"] = {
        "pdf_page": p,
        "historical_folio": pdata["historical_folio"],
        "positions_count": len(pdata["entries"]),
        "blind_first_read_file": str(file_path).replace("\\", "/"),
        "blind_first_read_sha256": sha256,
        "status": "LOCKED_PRE_COLLATION"
    }
    print(f"Page {p:04d}: {len(pdata['entries'])} positions, SHA-256 = {sha256}")

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("\n[SUCCESS] Updated BLIND_READ_MANIFEST.json with all 10 pages (0041 to 0050)!")
