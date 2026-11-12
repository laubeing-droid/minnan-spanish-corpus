import json
import hashlib
from pathlib import Path

MANIFEST_PATH = Path("literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json")

PAGES_DATA = {
    42: {
        "historical_folio": 13,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 13 -",
        "page_footer_handwritten": "A",
        "entries": [
            {"position": 1, "source_L": "Acabado, deshecho —", "source_H": "卒", "source_M": "chut chût xiēn", "source_R": "chuēt", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T03 (尖頂帽)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 2, "source_L": "acabado deshecho —", "source_H": "喪", "source_M": "sóng", "source_R": "sǒng", "tone_marks_M": ["T01 (升斜重墨)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 3, "source_L": "acabarse, aberse acabado o pasado como el tiempo &c —", "source_H": "殘", "source_M": "choā / chān", "source_R": "chān", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 4, "source_L": "acabarse la pascua de linternᵗᵉ / acabarse el goze de la camisa —", "source_H": "殘灯", "source_M": "choā tēng", "source_R": "chông téng", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T01 (升斜)"]},
            {"position": 5, "source_L": "acabado perfecto —", "source_H": "做成", "source_M": "chô chiā", "source_R": "chō chêng", "tone_marks_M": ["T03 (尖頂帽)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 6, "source_L": "acabar el offᶦᵒ el juez o prelado —", "source_H": "任滿", "source_M": "xǐm moáⁿ", "source_R": "xīm moàn", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 7, "source_L": "acabado, bien hecho —", "source_H": "定當了", "source_M": "těng tiàng liàu", "source_R": "tēng kē liào", "tone_marks_M": ["T04 (凹角)", "T02 (降斜)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]},
            {"position": 8, "source_L": "acabado, o acabar con ello —", "source_H": "事定了", "source_M": "sǔ tiǎⁿ liàu", "source_R": "çū tēn liào", "tone_marks_M": ["T04 (凹角)", "T04 (凹角)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"]},
            {"position": 9, "source_L": "acabarse el pleyto, cortalle la Raiz —", "source_H": "斷根", "source_M": "tuỳ quín", "source_R": "toān quǐn", "tone_marks_M": ["T02 (降斜)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 10, "source_L": "acabar bien hasta el fin —", "source_H": "結果", "source_M": "quiét cò", "source_R": "quiē cò", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 11, "source_L": "acabar hasta el fin —", "source_H": "竭尽", "source_M": "quiét chiǔ", "source_R": "quiēn chiēn", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 12, "source_L": "acabado que no sobra", "source_H": "衰微", "source_M": "sué bī", "source_R": "çuǎy mǐ", "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 13, "source_L": "acabado perfecta mᵗᵉ hecho.", "source_H": "隨手成", "source_M": "sūy chiú chiā", "source_R": "chûy chiên chěng", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 14, "source_L": "acabado concluido —", "source_H": "總結", "source_M": "quià quiét", "source_R": "quiàn quiē", "tone_marks_M": ["T02 (降斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 15, "source_L": "acabado concluido —", "source_H": "成事", "source_M": "sēng sǔ", "source_R": "chěng çū", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 16, "source_L": "acabado concluido —", "source_H": "事明白", "source_M": "sǔ bēng pec", "source_R": "çū mèng pē", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)", "T05 (平橫)"]},
            {"position": 17, "source_L": "acabado, hecho —", "source_H": "定奪", "source_M": "těng tuot", "source_R": "těng tō", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 18, "source_L": "acabarse algo facilmente.", "source_H": "易過", "source_M": "quěy uê", "source_R": "yī cō", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 19, "source_L": "Acallar al que llora —", "source_H": "晴", "source_M": "chē", "source_R": "chêng", "tone_marks_M": ["T05 (平橫重墨)"], "tone_marks_R": ["T03 (尖頂帽)"]}
        ]
    },
    43: {
        "historical_folio": 14,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 14 -",
        "page_footer_handwritten": "7",
        "entries": [
            {"position": 1, "source_L": "Acallar como a el niño, o marido &.", "source_H": "[疑:邀/慇/殀]", "source_M": "yó", "source_R": "yǔ", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 2, "source_L": "acallar a el marido —", "source_H": "[疑:邀/慇/殀]君", "source_M": "yó cún", "source_R": "yǔ quiǒn", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 3, "source_L": "acallar a el Niño.", "source_H": "惜子", "source_M": "sió quiǎ", "source_R": "sī chù", "tone_marks_M": ["T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 4, "source_L": "Acariciar, uẽ guesped &.", "source_H": "接", "source_M": "chiáp", "source_R": "chiē", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 5, "source_L": "acariciar a el guesped —", "source_H": "接納", "source_M": "chiáp láp", "source_R": "chiē nā", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 6, "source_L": "acariciar a el amigo &", "source_H": "交接", "source_M": "cáu chiáp", "source_R": "quiǎn chiē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 7, "source_L": "acariciar — / quere Regalar.", "source_H": "應接", "source_M": "èng chiáp", "source_R": "ěng chiē: īng chiē", "tone_marks_M": ["T02 (降斜重墨)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 8, "source_L": "Acarrear —", "source_H": "拖", "source_M": "Toá", "source_R": "tǒ", "tone_marks_M": ["T01 (升斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 9, "source_L": "acarrear con carro.", "source_H": "拖車", "source_M": "toá chiá", "source_R": "tǒ chē: tǒ quī", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 10, "source_L": "acarrearse males o bienes.", "source_H": "致", "source_M": "Tì", "source_R": "chī", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 11, "source_L": "acarrearse males o bienes.", "source_H": "致惹", "source_M": "Tì xià", "source_R": "chī xiè", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]},
            {"position": 12, "source_L": "Acaso —", "source_H": "偶", "source_M": "ngòu", "source_R": "ngòu", "tone_marks_M": ["T02 (降斜)"], "tone_marks_R": ["T02 (降斜)"]},
            {"position": 13, "source_L": "acaso —", "source_H": "偶然", "source_M": "ngòu xiān", "source_R": "ngòu xiēn", "tone_marks_M": ["T02 (降斜)", "T05 (平橫)"], "tone_marks_R": ["T02 (降斜)", "T05 (平橫)"]},
            {"position": 14, "source_L": "acaso, de repente —", "source_H": "偶湊", "source_M": "ngòu châù", "source_R": "ngòu chèu", "tone_marks_M": ["T02 (降斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 15, "source_L": "acaso —", "source_H": "幸", "source_M": "hěng", "source_R": "hēng", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acaso", "source_H": "幸然", "source_M": "hěng xiēn", "source_R": "hēng xiên", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 17, "source_L": "acaso sin pensar ni prevenir.", "source_H": "不知頭", "source_M": "mě chaý tāu", "source_R": "pū chī têu", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 18, "source_L": "acaso, inopinada mente.", "source_H": "無意思", "source_M": "bō ŷ sǔ", "source_R": "bū ȳ çū", "tone_marks_M": ["T05 (平橫)", "T03 (尖頂帽)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]}
        ]
    },
    44: {
        "historical_folio": 15,
        "page_header": "A. ante. C",
        "page_footer_printed": "- 15 -",
        "page_footer_handwritten": "A",
        "entries": [
            {"position": 1, "source_L": "Aceleradamente —", "source_H": "慌", "source_M": "Hóng", "source_R": "Huǎng", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 2, "source_L": "aceleradamente, sin tiento", "source_H": "慌忙", "source_M": "hóng bōng", "source_R": "Huǎng mǎng", "tone_marks_M": ["T01 (升斜)", "T05 (平橫)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 3, "source_L": "aceleradamᵗᵉ, dar demasiada priesa, importunamente", "source_H": "慌迫", "source_M": "hóng péc", "source_R": "huǎng pē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 4, "source_L": "Acentuar la leccion.", "source_H": "吟", "source_M": "Guīm", "source_R": "nguîen", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 5, "source_L": "acentuar las Voces —", "source_H": "金玉音", "source_M": "quīm giŏc ím", "source_R": "quiǔn yō ǐm", "tone_marks_M": ["T05 (平橫)", "T06/T07 (交叉入聲號)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 6, "source_L": "Acepillar —", "source_H": "[疑:鉋/敲]", "source_M": "Cáu", "source_R": "quiǎu", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 7, "source_L": "acepillar —", "source_H": "[疑:鉋/敲]刀", "source_M": "cáu tó", "source_R": "quiǎu toǔn", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 8, "source_L": "acepillar pulida mente.", "source_H": "做白地", "source_M": "chô pec těy", "source_R": "chō pē tī", "tone_marks_M": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)", "T04 (凹角)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 9, "source_L": "Aceptar la promesa —", "source_H": "承", "source_M": "Sīn", "source_R": "sêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 10, "source_L": "aceptar la promesa reciuiendo.", "source_H": "承受", "source_M": "sīn siǔ", "source_R": "sêng seǔ", "tone_marks_M": ["T05 (平橫)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)"]},
            {"position": 11, "source_L": "aceptador de personas —", "source_H": "私", "source_M": "sú: loy giá", "source_R": "çǔ", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 12, "source_L": "aceptador de personas —", "source_H": "私心", "source_M": "sú sím", "source_R": "çǔ sǐm", "tone_marks_M": ["T01 (升斜)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 13, "source_L": "aceptador de personas —", "source_H": "大細心", "source_M": "toǎ sêy sím", "source_R": "tā sȳ sǐm", "tone_marks_M": ["T04 (凹角)", "T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 14, "source_L": "Aceptador de personas", "source_H": "厚薄心", "source_M": "hoǔ poǒc sím", "source_R": "hēu pō sǐm", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T04 (凹角)"]},
            {"position": 15, "source_L": "Acertar.", "source_H": "着", "source_M": "Tió", "source_R": "chiō", "tone_marks_M": ["T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acertar con gusto —", "source_H": "執个着", "source_M": "chip gue tiò", "source_R": "chī cō chiō", "tone_marks_M": ["T06/T07 (交叉入聲號)", "T05 (平橫)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"]},
            {"position": 17, "source_L": "acertar adiuinando.", "source_H": "靈", "source_M": "lēng", "source_R": "lêng", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)"]},
            {"position": 18, "source_L": "acertar en el blanco —", "source_H": "中", "source_M": "Tiǒng", "source_R": "chiǒng: chōng", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T04 (凹角)"]}
        ]
    },
    45: {
        "historical_folio": 16,
        "page_header": "A. ante. C.",
        "page_footer_printed": "- 16 -",
        "page_footer_handwritten": "8",
        "entries": [
            {"position": 1, "source_L": "Acertar con la raçon —", "source_H": "中理", "source_M": "Tiǒng lí", "source_R": "chǒng lì", "tone_marks_M": ["T04 (凹角)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T02 (降斜)"]},
            {"position": 2, "source_L": "acertar con la coyuntura, o en la ocasion —", "source_H": "中節", "source_M": "tiǒng chiet", "source_R": "chǒng chiē", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 3, "source_L": "acertar en el blanco.", "source_H": "中的", "source_M": "tiǒng téc", "source_R": "chǒng tī", "tone_marks_M": ["T04 (凹角)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 4, "source_L": "acertar en el examen —", "source_H": "經魁", "source_M": "quêng cué", "source_R": "quěng cuǐ", "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T04 (凹角)", "T04 (凹角)"]},
            {"position": 5, "source_L": "acertar, buen acierto a el principio, buen aguero —", "source_H": "威實", "source_M": "uy sit", "source_R": "wǔy siē", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T04 (凹角)", "T05 (平橫)"]},
            {"position": 6, "source_L": "Achicar el agua, ut en el nabio", "source_H": "打水", "source_M": "Tá chui", "source_R": "tà çuì", "tone_marks_M": ["T01 (升斜)", "T02 (降斜)"], "tone_marks_R": ["T02 (降斜)", "T02 (降斜)"]},
            {"position": 7, "source_L": "Aclarar —", "source_H": "光", "source_M": "Cuy", "source_R": "quǎng", "tone_marks_M": ["T01 (升斜)"], "tone_marks_R": ["T04 (凹角)"]},
            {"position": 8, "source_L": "aclarar —", "source_H": "[疑:散/霰]", "source_M": "Soâⁿ", "source_R": "çān", "tone_marks_M": ["T03 (尖頂帽)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 9, "source_L": "aclarar —", "source_H": "[疑:散/霰]開", "source_M": "Soâⁿ cuy", "source_R": "çān cuǐ", "tone_marks_M": ["T03 (尖頂帽)", "T01 (升斜)"], "tone_marks_R": ["T05 (平橫)", "T04 (凹角)"]},
            {"position": 10, "source_L": "aclarar ut por fin — / quere: claro —", "source_H": "會明", "source_M": "huě bēng", "source_R": "hūi mêng", "tone_marks_M": ["T04 (凹角)", "T05 (平橫)"], "tone_marks_R": ["T05 (平橫)", "T03 (尖頂帽)"]},
            {"position": 11, "source_L": "Acomodarse —", "source_H": "隨時", "source_M": "Sūy sȳ", "source_R": "chûi çî", "tone_marks_M": ["T05 (平橫)", "T05 (平橫)"], "tone_marks_R": ["T03 (尖頂帽)", "T03 (尖頂帽)"]},
            {"position": 12, "source_L": "acomodarse la muger a el estado —", "source_H": "隨夫賤", "source_M": "Sūy hú chiěn", "source_R": "chûi hǔ chiēn", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T04 (凹角)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)", "T05 (平橫)"]},
            {"position": 13, "source_L": "acomodarse la muger a el estado —", "source_H": "隨夫貴", "source_M": "Sūy hú cûy", "source_R": "chûi hǔ cûi", "tone_marks_M": ["T05 (平橫)", "T01 (升斜)", "T03 (尖頂帽)"], "tone_marks_R": ["T03 (尖頂帽)", "T04 (凹角)", "T03 (尖頂帽)"]},
            {"position": 14, "source_L": "acomodarse y amar su estado —", "source_H": "惜福", "source_M": "Sió hóc", "source_R": "sī hō", "tone_marks_M": ["T01 (升斜)", "T06/T07 (交叉入聲號)"], "tone_marks_R": ["T05 (平橫)", "T05 (平橫)"]},
            {"position": 15, "source_L": "Acompañar.", "source_H": "伴", "source_M": "Poǎ", "source_R": "Puān", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 16, "source_L": "acompañar en offᶦᵒ trabajo &", "source_H": "輔", "source_M": "huǔ", "source_R": "hū", "tone_marks_M": ["T04 (凹角)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 17, "source_L": "acompañar en offᶦᵒ que le quiera dignidad —", "source_H": "陪", "source_M": "Puē", "source_R": "Pūi", "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": ["T05 (平橫)"]},
            {"position": 18, "source_L": "acompañar en el offᶦᵒ o dignidad —", "source_H": "陪[疑:點]", "source_M": "Puē tiàm", "source_R": "pūi tièn", "tone_marks_M": ["T05 (平橫)", "T02 (降斜)"], "tone_marks_R": ["T05 (平橫)", "T02 (降斜)"]}
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

print("[SUCCESS] Updated BLIND_READ_MANIFEST.json with pages 0041 to 0045!")
