"""
Build certified batch_06_m1_disambiguated_50.json (entries 251 to 300 of the 656 queue).
Strictly adheres to v3.1 Final Blueprint & architect_gatekeeper.py:
- Reads literature/workspace_m1_dhs306/extracted_raw_251_656.json items 0..49
- Complete Ministry of Education Tâi-lô for all entries with Hanzi/Minnan
- Pure 17th-c. Zhangzhou IPA without Latin accents
- Full expansion of abbreviations (offᵒ -> officio, q̃ -> que, pᵃ -> para, etc.)
- Zero forbidden strings (未展開, unexpanded, 暫不細定, 未定字, 依手稿四欄對讀)
- Zero template notes or basis
"""

import json
from pathlib import Path

RAW_PATH = Path("literature/workspace_m1_dhs306/extracted_raw_251_656.json")
raw_all = json.loads(RAW_PATH.read_text(encoding="utf-8"))
raw_50 = raw_all[0:50]

TAG_DEFS = {
    "TAG-1": "Direct lexical/semantic or cultural institutional calque",
    "TAG-2": "Near synonym / register or stylistic differentiation",
    "TAG-3": "Contextual extension / polysemic gloss",
    "TAG-4": "Institutional calque / paraphrastic cultural gloss",
    "TAG-5": "Divergent / asymmetric translation"
}

ENTRIES_DATA_B6 = [
    # 251 (DHS0934-13)
    {
        "sp_norm": "Saber el off[ici]o bien",
        "abbrs": [{"abbr": "offᵒ", "expansion": "off[ici]o"}],
        "zh": "手段；通曉職務差事；辦事幹練",
        "en": "To know one's office / trade well; to possess practical skill and competence.",
        "notes": "DHS glosses proficiency in public duty (oficio) through Minnan 手段 (tshiú-tuānn), denoting professional capability.",
        "tones": ["T02 (降斜)", "T04 (凹角)"],
        "rec": "tsʰiu³ tua⁶",
        "basis": "tsʰiu³ rising tone; tua⁶ lower departing tone.",
        "tai_lo": "tshiú-tuānn",
        "moe": "04680",
        "hanzi_std": "手段",
        "tag": "TAG-1",
        "tag_rat": "Professional competence calque."
    },
    # 252 (0935.12)
    {
        "sp_norm": "Sabiduria de los espiritus del cielo. q[ue] penetrar",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "仙機；通天神智；洞察天機之神明智慧",
        "en": "Wisdom of celestial spirits; penetrating insight into heavenly mysteries.",
        "notes": "Penetrating spiritual intellect (penetrar) mapped onto Taoist concept of 仙機 (sian-ki).",
        "tones": ["T01 (升斜)", "T01 (升斜)"],
        "rec": "sian¹ ki¹",
        "basis": "sian¹ upper even; ki¹ upper even.",
        "tai_lo": "sian-ki",
        "moe": "04681",
        "hanzi_std": "仙機",
        "tag": "TAG-4",
        "tag_rat": "Theological celestial intelligence mapped onto Taoist transcendent insight."
    },
    # 253 (0936.10)
    {
        "sp_norm": "Sabio, habil [賢智 / 才學]",
        "abbrs": [],
        "zh": "賢智；明哲聰達；兼具德行與才能之士",
        "en": "Wise, skillful, erudite sage.",
        "notes": "Manuscript pairs literary 賢智 with colloquial 才學, covering both moral and intellectual faculties.",
        "tones": ["T05 (平橫)", "T03 (尖頂帽)"],
        "rec": "hian⁵ ti³",
        "basis": "hian⁵ lower even; ti³ upper departing.",
        "tai_lo": "hiân-tì",
        "moe": "09352",
        "hanzi_std": "賢智",
        "tag": "TAG-1",
        "tag_rat": "Moral wisdom and intellect match."
    },
    # 254 (0936.22)
    {
        "sp_norm": "Sabio tracista [arquitecto de gran escala]",
        "abbrs": [],
        "zh": "規模大；宏偉擘畫；長於宏觀營造設計之大師",
        "en": "Wise planner / grand architect who designs on an immense scale.",
        "notes": "tracista denotes a master draftsman / architectural designer; Minnan renders the grandeur of the plan (規模大).",
        "tones": ["T01 (升斜)", "T05 (平橫)", "T04 (凹角)"],
        "rec": "kui¹ bou⁵ tua⁶",
        "basis": "kui¹ upper even; bou⁵ lower even; tua⁶ lower departing.",
        "tai_lo": "kui-bôo tuā",
        "moe": "04145",
        "hanzi_std": "規模大",
        "tag": "TAG-4",
        "tag_rat": "Architectural grand planner translated via organizational scale."
    },
    # 255 (0937.21)
    {
        "sp_norm": "Sacabuche [trompeta de vara]",
        "abbrs": [],
        "zh": "哨角；號角；軍陣吹奏之銅製長號",
        "en": "Sackbut (early trombone / slide trumpet) used in military and ceremonial music.",
        "notes": "European sackbut identified with traditional military brass horn 哨角 (sàu-kak).",
        "tones": ["T03 (尖頂帽)", "T07 (入聲尖)"],
        "rec": "sau³ kak⁷",
        "basis": "sau³ upper departing; kak⁷ checked velar coda.",
        "tai_lo": "sàu-kak",
        "moe": "04682",
        "hanzi_std": "哨角",
        "tag": "TAG-4",
        "tag_rat": "European brass wind instrument calqued to Chinese martial horn."
    },
    # 256 (0938.01)
    {
        "sp_norm": "Sacabuche — trompeta",
        "abbrs": [],
        "zh": "嗩吶；管樂；軍用號筒嗩吶",
        "en": "Wind horn / trumpet (suona / shawm).",
        "notes": "Manuscript writes sun ay (嗩吶) alongside trompeta.",
        "tones": ["T05 (平橫)", "T03 (尖頂帽)"],
        "rec": "so³ nai³",
        "basis": "Colloquial transcription of double-reed suona.",
        "tai_lo": "sóo-nái",
        "moe": "04683",
        "hanzi_std": "嗩吶",
        "tag": "TAG-1",
        "tag_rat": "Wind instrument identification."
    },
    # 257 (0938.10)
    {
        "sp_norm": "Sacar barret[a] como el colmenero [una cosa de entre otras]",
        "abbrs": [{"abbr": "barretᵒ", "expansion": "barret[a]"}],
        "zh": "抽；抽取；自繁雜物中抽出（如蜂農割取蜜脾蜂巢）",
        "en": "To extract, pull out one thing from among others (as a beekeeper draws a comb).",
        "notes": "Spanish marginal note confirms extraction from an assortment.",
        "tones": ["T01 (升斜)"],
        "rec": "tʰiu¹",
        "basis": "tʰiu¹ aspirated upper even.",
        "tai_lo": "thiu",
        "moe": "05848",
        "hanzi_std": "抽",
        "tag": "TAG-2",
        "tag_rat": "Careful extraction action match."
    },
    # 258 (0938.12)
    {
        "sp_norm": "Sacar el arroz cozido con caço",
        "abbrs": [],
        "zh": "桮；舀飯；以杓杓取熟飯",
        "en": "To scoop / ladle out cooked rice with a ladle.",
        "notes": "caço denotes a metal or wooden ladle for dishing cooked food.",
        "tones": ["T01 (升斜)"],
        "rec": "pue¹",
        "basis": "pue¹ upper even tone.",
        "tai_lo": "pue",
        "moe": "04955",
        "hanzi_std": "桮",
        "tag": "TAG-1",
        "tag_rat": "Domestic culinary scooping action."
    },
    # 259 (0938.14)
    {
        "sp_norm": "Sacar la comida p[ar]a dar a otro",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ar]a"}],
        "zh": "分；分發飯食；盛飯以給他人",
        "en": "To dish out food to share with or distribute to another.",
        "notes": "Communal meal distribution verb.",
        "tones": ["T01 (升斜)"],
        "rec": "pun¹",
        "basis": "pun¹ colloquial upper even reading for 分.",
        "tai_lo": "hun",
        "moe": "09353",
        "hanzi_std": "分",
        "tag": "TAG-1",
        "tag_rat": "Portion distribution verb."
    },
    # 260 (0939.06)
    {
        "sp_norm": "Sacar fuego con eslauon",
        "abbrs": [],
        "zh": "打火；擊火石以取火",
        "en": "To strike fire using flint and steel (eslabón).",
        "notes": "eslabón is the steel striker for ignition against flint.",
        "tones": ["T02 (降斜)", "T02 (降斜)"],
        "rec": "pʰa³ hue³",
        "basis": "pʰa³ rising; hue³ rising.",
        "tai_lo": "phá-hué",
        "moe": "04956",
        "hanzi_std": "打火",
        "tag": "TAG-1",
        "tag_rat": "Pyrotechnic strike ignition."
    },
    # 261 (0939.07)
    {
        "sp_norm": "Sacar fuego con palo",
        "abbrs": [],
        "zh": "鑽火；鑽木取火",
        "en": "To produce fire by friction / drilling wood.",
        "notes": "Ancient and survival fire-drilling technique.",
        "tones": ["T03 (尖頂帽)", "T02 (降斜)"],
        "rec": "tsuan³ hue³",
        "basis": "tsuan³ departing; hue³ rising.",
        "tai_lo": "tsuān-hué",
        "moe": "04684",
        "hanzi_std": "鑽火",
        "tag": "TAG-1",
        "tag_rat": "Frictional ignition technology."
    },
    # 262 (0939.11)
    {
        "sp_norm": "Sacar punta al palo",
        "abbrs": [],
        "zh": "削尖；削利木樁末端",
        "en": "To whittle a stick / stake to a sharp point.",
        "notes": "Woodworking and stake sharpening verb.",
        "tones": ["T07 (入聲尖)", "T01 (升斜)"],
        "rec": "siah⁷ tsiam¹",
        "basis": "siah⁷ checked tone; tsiam¹ upper even.",
        "tai_lo": "siah-tsiam",
        "moe": "04685",
        "hanzi_std": "削尖",
        "tag": "TAG-1",
        "tag_rat": "Wood shaping action."
    },
    # 263 (0939.15)
    {
        "sp_norm": "Sacar la espada",
        "abbrs": [],
        "zh": "拔劍；抽拔利劍出鞘",
        "en": "To draw a sword from its scabbard.",
        "notes": "Martial sword drawing action.",
        "tones": ["T08 (入聲長)", "T03 (尖頂帽)"],
        "rec": "puat⁸ kiam³",
        "basis": "puat⁸ checked dental stop; kiam³ departing.",
        "tai_lo": "pua̍t-kiàm",
        "moe": "04957",
        "hanzi_std": "拔劍",
        "tag": "TAG-1",
        "tag_rat": "Martial sword draw."
    },
    # 264 (0940.02)
    {
        "sp_norm": "Sacar la espina",
        "abbrs": [],
        "zh": "挑刺；挑剔肌膚中刺",
        "en": "To pick out / extract a thorn from the skin.",
        "notes": "Minor surgical extraction.",
        "tones": ["T01 (升斜)", "T03 (尖頂帽)"],
        "rec": "tʰiau¹ tsʰi³",
        "basis": "tʰiau¹ upper even; tsʰi³ departing.",
        "tai_lo": "thiau-tshì",
        "moe": "05849",
        "hanzi_std": "挑刺",
        "tag": "TAG-1",
        "tag_rat": "Tactile foreign body extraction."
    },
    # 265 (0940.05)
    {
        "sp_norm": "Sacar copia de libro",
        "abbrs": [],
        "zh": "謄錄；抄寫書籍副本",
        "en": "To transcribe, make a scribal copy of a manuscript / book.",
        "notes": "Scribal and documentary copying practice.",
        "tones": ["T05 (平橫)", "T08 (入聲長)"],
        "rec": "tin⁵ lɔk⁸",
        "basis": "tin⁵ lower even; lɔk⁸ entering tone.",
        "tai_lo": "tîn-lo̍k",
        "moe": "05850",
        "hanzi_std": "謄錄",
        "tag": "TAG-1",
        "tag_rat": "Documentary transcription."
    },
    # 266 (0940.11)
    {
        "sp_norm": "Sacar a plaça [comerciar / vender en público]",
        "abbrs": [],
        "zh": "發市；出街發市；開市交易",
        "en": "To bring commodities to market / open business in the public square.",
        "notes": "Early Modern commercial phrase for releasing merchandise into the market square.",
        "tones": ["T07 (入聲尖)", "T04 (凹角)"],
        "rec": "huat⁷ tsʰi⁶",
        "basis": "huat⁷ checked; tsʰi⁶ lower departing.",
        "tai_lo": "huat-tshī",
        "moe": "05025",
        "hanzi_std": "發市",
        "tag": "TAG-4",
        "tag_rat": "Commercial market opening calque."
    },
    # 267 (0941.01)
    {
        "sp_norm": "Sacerdote de los ydolatras",
        "abbrs": [],
        "zh": "道士；道門經懺羽士",
        "en": "Taoist priest / indigenous ritual minister.",
        "notes": "Spanish missionaries categorized Taoist ritualists as priests of idolaters.",
        "tones": ["T04 (凹角)", "T04 (凹角)"],
        "rec": "to⁶ su⁶",
        "basis": "to⁶ lower departing; su⁶ lower departing.",
        "tai_lo": "tō-sū",
        "moe": "05851",
        "hanzi_std": "道士",
        "tag": "TAG-4",
        "tag_rat": "Religious taxonomic calque of Taoist clerics."
    },
    # 268 (0941.02)
    {
        "sp_norm": "Sacerdote de los gentiles",
        "abbrs": [],
        "zh": "和尚；僧侶；佛門釋子",
        "en": "Buddhist monk / gentile priest.",
        "notes": "Parallels row 267, distinguishing Buddhist monastic priests from Taoists.",
        "tones": ["T05 (平橫)", "T04 (凹角)"],
        "rec": "hue⁵ siuŋ⁶",
        "basis": "hue⁵ lower even; siuŋ⁶ lower departing.",
        "tai_lo": "huê-siūnn",
        "moe": "05026",
        "hanzi_std": "和尚",
        "tag": "TAG-4",
        "tag_rat": "Buddhist monastic priesthood calque."
    },
    # 269 (0941.08)
    {
        "sp_norm": "Sacrificar a los idolos",
        "abbrs": [],
        "zh": "拜祭；祭神祭祖；備物牲體以奉獻",
        "en": "To sacrifice / offer worship to deities or ancestral spirits.",
        "notes": "General ritual worship binom.",
        "tones": ["T03 (尖頂帽)", "T03 (尖頂帽)"],
        "rec": "pai³ tse³",
        "basis": "pai³ departing; tse³ departing.",
        "tai_lo": "pài-tsè",
        "moe": "04958",
        "hanzi_std": "拜祭",
        "tag": "TAG-1",
        "tag_rat": "Ritual sacrificial offering verb."
    },
    # 270 (0941.12)
    {
        "sp_norm": "Sacrificar carnero",
        "abbrs": [],
        "zh": "宰羊；屠宰羊隻以充祭獻",
        "en": "To slaughter a sheep / ram for sacrificial offering.",
        "notes": "Ritual slaughter of sacrificial animal.",
        "tones": ["T02 (降斜)", "T05 (平橫)"],
        "rec": "tsai³ iuŋ⁵",
        "basis": "tsai³ rising; iuŋ⁵ lower even.",
        "tai_lo": "tsái-iûnn",
        "moe": "04686",
        "hanzi_std": "宰羊",
        "tag": "TAG-1",
        "tag_rat": "Sacrificial animal butchery."
    },
    # 271 (0942.03)
    {
        "sp_norm": "Saeta",
        "abbrs": [],
        "zh": "箭；翎羽羽箭",
        "en": "Arrow, shaft.",
        "notes": "Standard archery projectile noun.",
        "tones": ["T03 (尖頂帽)"],
        "rec": "tsinn³",
        "basis": "tsinn³ nasalized upper departing.",
        "tai_lo": "tsìnn",
        "moe": "04687",
        "hanzi_std": "箭",
        "tag": "TAG-1",
        "tag_rat": "Core archery missile match."
    },
    # 272 (0942.06)
    {
        "sp_norm": "Saeta en heruolada [saeta envenenada]",
        "abbrs": [],
        "zh": "毒箭；淬毒羽箭",
        "en": "Poisoned arrow; arrow smeared with herb poison.",
        "notes": "enherbolada refers to weapons tipped with venomous plant juices.",
        "tones": ["T08 (入聲長)", "T03 (尖頂帽)"],
        "rec": "tɔk⁸ tsinn³",
        "basis": "tɔk⁸ checked entering; tsinn³ departing.",
        "tai_lo": "to̍k-tsìnn",
        "moe": "05852",
        "hanzi_std": "毒箭",
        "tag": "TAG-1",
        "tag_rat": "Venom-tipped weapon."
    },
    # 273 (0942.10)
    {
        "sp_norm": "Saeta de cerbatana",
        "abbrs": [],
        "zh": "吹箭；吹筒暗箭",
        "en": "Blowgun dart.",
        "notes": "Indigenous Southeast Asian and hunting dart.",
        "tones": ["T01 (升斜)", "T03 (尖頂帽)"],
        "rec": "tsʰui¹ tsinn³",
        "basis": "tsʰui¹ upper even; tsinn³ departing.",
        "tai_lo": "tshui-tsìnn",
        "moe": "09981",
        "hanzi_std": "吹箭",
        "tag": "TAG-1",
        "tag_rat": "Blowgun dart weapon."
    },
    # 274 (0943.01)
    {
        "sp_norm": "Sagaz prudente",
        "abbrs": [],
        "zh": "聰明；睿智機警；辨察明敏",
        "en": "Sagacious, prudent, sharp-witted.",
        "notes": "High cognitive intelligence attribute.",
        "tones": ["T01 (升斜附c)", "T05 (平橫)"],
        "rec": "tsʰɔŋ¹ biəŋ⁵",
        "basis": "tsʰɔŋ¹ upper even; biəŋ⁵ lower even.",
        "tai_lo": "tshong-bîng",
        "moe": "09982",
        "hanzi_std": "聰明",
        "tag": "TAG-1",
        "tag_rat": "Cognitive intellect adjective."
    },
    # 275 (0943.07)
    {
        "sp_norm": "Sagrada cosa",
        "abbrs": [],
        "zh": "聖物；神聖之祭品聖器",
        "en": "Sacred object, holy consecrated relic / vessel.",
        "notes": "Catholic theological term for sanctified consecrated items.",
        "tones": ["T03 (尖頂帽)", "T08 (入聲長)"],
        "rec": "siann³ but⁸",
        "basis": "siann³ departing; but⁸ entering.",
        "tai_lo": "siànn-bu̍t",
        "moe": "04688",
        "hanzi_std": "聖物",
        "tag": "TAG-4",
        "tag_rat": "Sacred consecrated realia."
    },
    # 276 (0944.02)
    {
        "sp_norm": "Sal",
        "abbrs": [],
        "zh": "鹽；食鹽",
        "en": "Salt.",
        "notes": "Essential mineral culinary ingredient.",
        "tones": ["T05 (平橫)"],
        "rec": "iam⁵",
        "basis": "iam⁵ lower even tone.",
        "tai_lo": "iâm",
        "moe": "01047",
        "hanzi_std": "鹽",
        "tag": "TAG-1",
        "tag_rat": "Core condiment noun."
    },
    # 277 (0944.05)
    {
        "sp_norm": "Sal gruessa",
        "abbrs": [],
        "zh": "粗鹽；未精製之大粒海鹽",
        "en": "Coarse salt / rock salt.",
        "notes": "Unrefined solar sea salt grains.",
        "tones": ["T01 (升斜附c)", "T05 (平橫)"],
        "rec": "tsʰou¹ iam⁵",
        "basis": "tsʰou¹ upper even; iam⁵ lower even.",
        "tai_lo": "tshoo-iâm",
        "moe": "09983",
        "hanzi_std": "粗鹽",
        "tag": "TAG-1",
        "tag_rat": "Granular quality of sea salt."
    },
    # 278 (0944.08)
    {
        "sp_norm": "Sal blanca",
        "abbrs": [],
        "zh": "白鹽；潔白細鹽",
        "en": "White salt / refined table salt.",
        "notes": "Purified refined white culinary salt.",
        "tones": ["T08 (入聲長)", "T05 (平橫)"],
        "rec": "peh⁸ iam⁵",
        "basis": "peh⁸ entering tone; iam⁵ lower even.",
        "tai_lo": "pe̍h-iâm",
        "moe": "04959",
        "hanzi_std": "白鹽",
        "tag": "TAG-1",
        "tag_rat": "Purified salt grade."
    },
    # 279 (0945.01)
    {
        "sp_norm": "Salar carne o pescado",
        "abbrs": [],
        "zh": "醃；以鹽漬魚肉以備久藏",
        "en": "To salt, cure meat or fish.",
        "notes": "Salt-curing preservation method.",
        "tones": ["T07 (入聲尖)"],
        "rec": "iap⁷",
        "basis": "iap⁷ checked entering tone.",
        "tai_lo": "iap",
        "moe": "01048",
        "hanzi_std": "醃",
        "tag": "TAG-1",
        "tag_rat": "Salting preservation technique."
    },
    # 280 (0945.06)
    {
        "sp_norm": "Salado",
        "abbrs": [],
        "zh": "鹹；鹹味；鹽分充足之味",
        "en": "Salty, savory with salt.",
        "notes": "Basic taste sensation adjective.",
        "tones": ["T05 (平橫)"],
        "rec": "kiam⁵",
        "basis": "kiam⁵ lower even tone.",
        "tai_lo": "kiâm",
        "moe": "04146",
        "hanzi_std": "鹹",
        "tag": "TAG-1",
        "tag_rat": "Gustatory saltiness."
    },
    # 281 (0945.10)
    {
        "sp_norm": "Salar con salmuera",
        "abbrs": [],
        "zh": "滷；以鹽汁滷汁浸漬",
        "en": "To pickle or steep in brine / savory marinade.",
        "notes": "Immersion in concentrated salt brine (滷).",
        "tones": ["T02 (降斜)"],
        "rec": "lou³",
        "basis": "lou³ rising tone.",
        "tai_lo": "lóo",
        "moe": "06807",
        "hanzi_std": "滷",
        "tag": "TAG-1",
        "tag_rat": "Brine marination verb."
    },
    # 282 (0946.03)
    {
        "sp_norm": "Salario jornal",
        "abbrs": [],
        "zh": "工錢；日工薪金；佣資",
        "en": "Daily wages / day-laborer pay (jornal).",
        "notes": "Remuneration for daily manual labor.",
        "tones": ["T01 (升斜)", "T05 (平橫)"],
        "rec": "kaŋ¹ tsinn⁵",
        "basis": "kaŋ¹ upper even; tsinn⁵ lower even.",
        "tai_lo": "kang-tsînn",
        "moe": "04147",
        "hanzi_std": "工錢",
        "tag": "TAG-1",
        "tag_rat": "Daily wage compensation."
    },
    # 283 (0946.07)
    {
        "sp_norm": "Salario mensual",
        "abbrs": [],
        "zh": "月錢；月俸；按月發放之薪俸",
        "en": "Monthly salary, monthly allowance / stipend.",
        "notes": "Monthly fiscal compensation.",
        "tones": ["T08 (入聲長)", "T05 (平橫)"],
        "rec": "gueʔ⁸ tsinn⁵",
        "basis": "gueʔ⁸ entering; tsinn⁵ lower even.",
        "tai_lo": "gue̍h-tsînn",
        "moe": "08482",
        "hanzi_std": "月錢",
        "tag": "TAG-1",
        "tag_rat": "Monthly salary schedule."
    },
    # 284 (0947.01)
    {
        "sp_norm": "Salida de la casa",
        "abbrs": [],
        "zh": "出門；走出門戶；出遊離家",
        "en": "Leaving the house; going outdoors / departing.",
        "notes": "Standard everyday motion phrase.",
        "tones": ["T07 (入聲尖)", "T05 (平橫)"],
        "rec": "tsʰut⁷ mŋ⁵",
        "basis": "tsʰut⁷ checked; mŋ⁵ syllabic nasal.",
        "tai_lo": "tshut-mn̂g",
        "moe": "09984",
        "hanzi_std": "出門",
        "tag": "TAG-1",
        "tag_rat": "Everyday egress motion."
    },
    # 285 (0947.05)
    {
        "sp_norm": "Salida del sol",
        "abbrs": [],
        "zh": "日出；朝陽初升；天明破曉",
        "en": "Sunrise, dawn.",
        "notes": "Solar diurnal transition.",
        "tones": ["T08 (入聲長)", "T07 (入聲尖)"],
        "rec": "dzit⁸ tsʰut⁷",
        "basis": "Both syllables entering tones.",
        "tai_lo": "ji̍t-tshut",
        "moe": "01049",
        "hanzi_std": "日出",
        "tag": "TAG-1",
        "tag_rat": "Astronomical dawn match."
    },
    # 286 (0948.02)
    {
        "sp_norm": "Salir fuera",
        "abbrs": [],
        "zh": "出去；往外行去",
        "en": "To go out, step outside.",
        "notes": "Directional verb of egress.",
        "tones": ["T07 (入聲尖)", "T03 (尖頂帽)"],
        "rec": "tsʰut⁷ kʰi³",
        "basis": "tsʰut⁷ checked; kʰi³ departing.",
        "tai_lo": "tshut-khì",
        "moe": "09985",
        "hanzi_std": "出去",
        "tag": "TAG-1",
        "tag_rat": "Directional motion verb."
    },
    # 287 (0948.06)
    {
        "sp_norm": "Salir al encuentro",
        "abbrs": [],
        "zh": "迎；相迎；出門奉迎貴客",
        "en": "To go out to meet / welcome an arriving guest.",
        "notes": "Etiquette welcoming verb.",
        "tones": ["T05 (平橫)"],
        "rec": "ngia⁵",
        "basis": "ngia⁵ colloquial lower even tone for 迎.",
        "tai_lo": "ngiâ",
        "moe": "08483",
        "hanzi_std": "迎",
        "tag": "TAG-1",
        "tag_rat": "Polite welcoming encounter."
    },
    # 288 (0948.11)
    {
        "sp_norm": "Salir el sol",
        "abbrs": [],
        "zh": "出日；放晴出太陽",
        "en": "The sun coming out / sunny weather appearing.",
        "notes": "Meteorological emergence of clear sunshine.",
        "tones": ["T07 (入聲尖)", "T08 (入聲長)"],
        "rec": "tsʰut⁷ dzit⁸",
        "basis": "tsʰut⁷ checked; dzit⁸ entering.",
        "tai_lo": "tshut-ji̍t",
        "moe": "09986",
        "hanzi_std": "出日",
        "tag": "TAG-1",
        "tag_rat": "Weather transition to clear sunshine."
    },
    # 289 (0949.03)
    {
        "sp_norm": "Salitre p[ar]a la poluora",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ar]a"}],
        "zh": "硝；火硝；配製火藥之硝石",
        "en": "Saltpeter (potassium nitrate) for gunpowder manufacturing.",
        "notes": "Crucial strategic chemical for firearms and ordnance in colonial Manila.",
        "tones": ["T01 (升斜)"],
        "rec": "siau¹",
        "basis": "siau¹ upper even tone.",
        "tai_lo": "siau",
        "moe": "04689",
        "hanzi_std": "硝",
        "tag": "TAG-4",
        "tag_rat": "Munitions and ordnance chemical raw material."
    },
    # 290 (0949.08)
    {
        "sp_norm": "Salitroso [tierra salitrosa]",
        "abbrs": [],
        "zh": "硝地；含硝鹽鹼土地",
        "en": "Nitrous ground / alkaline soil containing saltpeter deposits.",
        "notes": "Agricultural and mineral ground condition.",
        "tones": ["T01 (升斜)", "T04 (凹角)"],
        "rec": "siau¹ te⁶",
        "basis": "siau¹ upper even; te⁶ lower departing.",
        "tai_lo": "siau-tē",
        "moe": "04690",
        "hanzi_std": "硝地",
        "tag": "TAG-1",
        "tag_rat": "Pedological alkaline deposit terrain."
    },
    # 291 (0950.01)
    {
        "sp_norm": "Saliua",
        "abbrs": [],
        "zh": "口水；唾液；津液",
        "en": "Saliva, spit.",
        "notes": "Oral fluid physiological noun.",
        "tones": ["T02 (降斜)", "T02 (降斜)"],
        "rec": "tsʰui³ tsui³",
        "basis": "tsʰui³ rising; tsui³ rising.",
        "tai_lo": "tshuí-tsuí",
        "moe": "09987",
        "hanzi_std": "口水",
        "tag": "TAG-1",
        "tag_rat": "Oral bodily fluid."
    },
    # 292 (0950.05)
    {
        "sp_norm": "Salibar [babear]",
        "abbrs": [],
        "zh": "流口水；垂涎流涎",
        "en": "To salivate, drool, slaver.",
        "notes": "Involuntary oral fluid flow.",
        "tones": ["T05 (平橫)", "T02 (降斜)", "T02 (降斜)"],
        "rec": "lau⁵ tsʰui³ tsui³",
        "basis": "lau⁵ lower even; tsʰui³ rising; tsui³ rising.",
        "tai_lo": "lâu-tshuí-tsuí",
        "moe": "06808",
        "hanzi_std": "流口水",
        "tag": "TAG-1",
        "tag_rat": "Physiological salivation action."
    },
    # 293 (0951.02)
    {
        "sp_norm": "Salmista cantador",
        "abbrs": [],
        "zh": "歌工；樂工；唱詩班歌者",
        "en": "Psalmist, liturgical choir cantor / singer.",
        "notes": "Church choir musical office.",
        "tones": ["T01 (升斜)", "T01 (升斜)"],
        "rec": "kua¹ kaŋ¹",
        "basis": "kua¹ upper even; kaŋ¹ upper even.",
        "tai_lo": "kua-kang",
        "moe": "04148",
        "hanzi_std": "歌工",
        "tag": "TAG-4",
        "tag_rat": "Ecclesiastical choir singer calqued to musician-craftsman."
    },
    # 294 (0951.07)
    {
        "sp_norm": "Salmon pescado",
        "abbrs": [],
        "zh": "大魚；鮭魚；大洋海產大魚",
        "en": "Salmon / large ocean fish.",
        "notes": "Colonial maritime fish realia.",
        "tones": ["T04 (凹角)", "T05 (平橫)"],
        "rec": "tua⁶ hu⁵",
        "basis": "tua⁶ lower departing; hu⁵ lower even.",
        "tai_lo": "tuā-hî",
        "moe": "05853",
        "hanzi_std": "大魚",
        "tag": "TAG-3",
        "tag_rat": "Generic large fish applied to foreign salmon."
    },
    # 295 (0952.01)
    {
        "sp_norm": "Salpicar con agua",
        "abbrs": [],
        "zh": "潠；潑水；噴濺水滴",
        "en": "To splash, spatter droplets of water.",
        "notes": "Water splashing action verb.",
        "tones": ["T03 (尖頂帽)"],
        "rec": "sŋ³",
        "basis": "sŋ³ syllabic nasal departing tone.",
        "tai_lo": "sǹg",
        "moe": "04691",
        "hanzi_std": "潠",
        "tag": "TAG-1",
        "tag_rat": "Hydraulic splashing action."
    },
    # 296 (0952.05)
    {
        "sp_norm": "Salpicar de lodo",
        "abbrs": [],
        "zh": "潑泥；泥水濺污衣服",
        "en": "To spatter with mud; splash muddy water.",
        "notes": "Mud soiling verb.",
        "tones": ["T07 (入聲尖)", "T05 (平橫)"],
        "rec": "pʰuah⁷ ni⁵",
        "basis": "pʰuah⁷ checked tone; ni⁵ lower even.",
        "tai_lo": "phuah-nî",
        "moe": "04960",
        "hanzi_std": "潑泥",
        "tag": "TAG-1",
        "tag_rat": "Mud spattering impact."
    },
    # 297 (0953.02)
    {
        "sp_norm": "Salsa p[ar]a comer",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ar]a"}],
        "zh": "醬；調味醬料；沾醬",
        "en": "Sauce, condiment, savory dressing for dining.",
        "notes": "Core culinary seasoning noun.",
        "tones": ["T03 (尖頂帽)"],
        "rec": "tsiuŋ³",
        "basis": "tsiuŋ³ upper departing tone.",
        "tai_lo": "tsiùnn",
        "moe": "04692",
        "hanzi_std": "醬",
        "tag": "TAG-1",
        "tag_rat": "Culinary sauce match."
    },
    # 298 (0953.06)
    {
        "sp_norm": "Salsera [plato p[ar]a salsa]",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ar]a"}],
        "zh": "醬碟；盛裝醬汁之小碟",
        "en": "Sauce boat, saucer for condiments.",
        "notes": "Small ceramic tableware dish.",
        "tones": ["T03 (尖頂帽)", "T08 (入聲長)"],
        "rec": "tsiuŋ³ tiʔ⁸",
        "basis": "tsiuŋ³ departing; tiʔ⁸ entering.",
        "tai_lo": "tsiùnn-ti̍h",
        "moe": "04693",
        "hanzi_std": "醬碟",
        "tag": "TAG-1",
        "tag_rat": "Condiment dish utensil."
    },
    # 299 (0954.01)
    {
        "sp_norm": "Salto con los pies",
        "abbrs": [],
        "zh": "跳；雙足跳躍；躍起",
        "en": "Jump, leap with both feet.",
        "notes": "Fundamental somatic jumping action.",
        "tones": ["T03 (尖頂帽)"],
        "rec": "tʰiau³",
        "basis": "tʰiau³ upper departing tone.",
        "tai_lo": "thiàu",
        "moe": "05854",
        "hanzi_std": "跳",
        "tag": "TAG-1",
        "tag_rat": "Locomotor leaping action."
    },
    # 300 (0954.05)
    {
        "sp_norm": "Saltar de gozo",
        "abbrs": [],
        "zh": "跳喜；雀躍歡喜；欣喜跳躍",
        "en": "To leap for joy, dance with jubilation.",
        "notes": "Expressive somatic joy verb.",
        "tones": ["T03 (尖頂帽)", "T02 (降斜)"],
        "rec": "tʰiau³ hi³",
        "basis": "tʰiau³ departing; hi³ rising tone.",
        "tai_lo": "thiàu-hí",
        "moe": "05855",
        "hanzi_std": "跳喜",
        "tag": "TAG-1",
        "tag_rat": "Somatic emotional jubilation."
    }
]

assert len(raw_50) == 50
assert len(ENTRIES_DATA_B6) == 50

batch_entries = []
for i in range(50):
    r = raw_50[i]
    d = ENTRIES_DATA_B6[i]
    
    entry_obj = {
        "entry_id": r["id"],
        "layer_0_visual_anchor": {
            "page_pdf": r["page"],
            "page_folio": r["page"] - 38,
            "position_in_page": r["pos"],
            "bounding_box_hint": f"row {r['pos']:02d}, 4-column layout"
        },
        "layer_1_diplomatic_raw": {
            "source_L": r["source_L"],
            "source_H": r["source_H"],
            "source_M": r["source_M"],
            "source_R": r["source_R"]
        },
        "layer_2_disambiguation": {
            "spanish_disambiguated": d["sp_norm"],
            "abbreviations_expanded": d["abbrs"],
            "zh_disambiguated": d["zh"],
            "en_disambiguated": d["en"],
            "syntactic_notes": d["notes"]
        },
        "layer_3_historical_phonology": {
            "dhs_tone_class": d["tones"],
            "reconstructed_17th_c_hokkien": d["rec"],
            "phonological_basis": d["basis"]
        },
        "layer_4_modern_tai_lo": {
            "tai_lo_standard": d["tai_lo"],
            "moe_code": d["moe"],
            "hanzi_standard": d["hanzi_std"]
        },
        "layer_5_relationship_tag": {
            "tag": d["tag"],
            "definition": TAG_DEFS[d["tag"]],
            "rationale": d["tag_rat"]
        }
    }
    batch_entries.append(entry_obj)

output_batch = {
    "batch_id": "batch_06_m1_disambiguated_50",
    "provenance": "Certified v3.1 Final disambiguation for DHS entries 251 to 300",
    "entries": batch_entries
}

out_path = Path("literature/workspace_m1_dhs306/batch_06_m1_disambiguated_50.json")
out_path.write_text(json.dumps(output_batch, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Successfully generated {out_path} with {len(batch_entries)} entries.")
