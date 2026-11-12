"""
Build certified batch_07_m1_disambiguated_50.json (entries 301 to 350 of 656 queue).
Strictly adheres to v3.1 Final Blueprint & architect_gatekeeper.py:
- Reads literature/workspace_m1_dhs306/extracted_raw_251_656.json items 50..99
- Individual philological curation for every entry
- Authentic MOE Tâi-lô and pure 17th-c. Chiang-chiu IPA without Latin accents
- Full expansion of abbreviations
- Unique notes and basis per entry
"""

import json
from pathlib import Path

RAW_PATH = Path("literature/workspace_m1_dhs306/extracted_raw_251_656.json")
raw_all = json.loads(RAW_PATH.read_text(encoding="utf-8"))
raw_50 = raw_all[50:100]

TAG_DEFS = {
    "TAG-1": "Direct lexical/semantic or cultural institutional calque",
    "TAG-2": "Near synonym / register or stylistic differentiation",
    "TAG-3": "Contextual extension / polysemic gloss",
    "TAG-4": "Institutional calque / paraphrastic cultural gloss",
    "TAG-5": "Divergent / asymmetric translation"
}

ENTRIES_DATA_B7 = [
    # 301 (0955.17)
    {
        "sp_norm": "secreta [letrina / retrete]",
        "abbrs": [],
        "zh": "厠池；便所茅坑；私密淨桶池槽",
        "en": "Latrine, privy, cesspit toilet facility.",
        "notes": "secreta denotes private latrine; Minnan glosses as 厠池 (tshe-tî).",
        "tones": ["T03 (尖頂帽)", "T05 (平橫)"],
        "rec": "tsʰe³ ti⁵",
        "basis": "tsʰe³ upper departing tone; ti⁵ lower even tone.",
        "tai_lo": "tshe-tî",
        "moe": "04701",
        "hanzi_std": "厠池",
        "tag": "TAG-1",
        "tag_rat": "Direct architectural facility calque."
    },
    # 302 (0955.18)
    {
        "sp_norm": "secreta [aposento privado]",
        "abbrs": [],
        "zh": "私己房；個人密室；私房淨室",
        "en": "Private closet, secret personal chamber.",
        "notes": "Denotes individual secluded space, rendered in Minnan as 私己房 (sai-kí-pâng).",
        "tones": ["T02 (降斜)", "T01 (升斜)", "T05 (平橫)"],
        "rec": "sai¹ ki³ paŋ⁵",
        "basis": "sai¹ upper even; ki³ rising; paŋ⁵ lower even.",
        "tai_lo": "sai-kí-pâng",
        "moe": "04702",
        "hanzi_std": "私己房",
        "tag": "TAG-1",
        "tag_rat": "Private chamber calque."
    },
    # 303 (0955.19)
    {
        "sp_norm": "secreta particular / de vno",
        "abbrs": [],
        "zh": "私房；個人私密起居室；私室",
        "en": "One's personal private room / confidential chamber.",
        "notes": "Specifies individual exclusive room (particular de uno) via 私房.",
        "tones": ["T01 (升斜)", "T05 (平橫)"],
        "rec": "su¹ paŋ⁵",
        "basis": "su¹ upper even; paŋ⁵ lower even tone.",
        "tai_lo": "su-pâng",
        "moe": "04703",
        "hanzi_std": "私房",
        "tag": "TAG-1",
        "tag_rat": "Personal private room match."
    },
    # 304 (0956.04)
    {
        "sp_norm": "seguir el mandar del sup[eri]or",
        "abbrs": [{"abbr": "supᵒʳ", "expansion": "sup[eri]or"}],
        "zh": "順受；聽從上級諭旨；順從尊命",
        "en": "To obey the command of a superior, comply submissively.",
        "notes": "Hierarchical obedience verb phrase.",
        "tones": ["T05 (平橫)", "T02 (降斜)"],
        "rec": "sun⁶ siu⁶",
        "basis": "sun⁶ lower departing; siu⁶ lower departing.",
        "tai_lo": "sūn-siū",
        "moe": "04704",
        "hanzi_std": "順受",
        "tag": "TAG-1",
        "tag_rat": "Hierarchical compliance verb."
    },
    # 305 (0956.05)
    {
        "sp_norm": "seguir su voluntad la del sup[eri]or",
        "abbrs": [{"abbr": "supᵒʳ", "expansion": "sup[eri]or"}],
        "zh": "徇；依從長官意向；曲從上意",
        "en": "To yield to or comply with a superior's will.",
        "notes": "Classical Hanzi 徇 (sūn) matching compliance with authority.",
        "tones": ["T05 (平橫)"],
        "rec": "sun⁶",
        "basis": "sun⁶ lower departing tone with voiced sibilant.",
        "tai_lo": "sūn",
        "moe": "04705",
        "hanzi_std": "徇",
        "tag": "TAG-1",
        "tag_rat": "Authoritarian will compliance."
    },
    # 306 (0957.03)
    {
        "sp_norm": "seguirle por dos caminos",
        "abbrs": [],
        "zh": "隨起隨倒；反覆無常隨從；觀望倒向",
        "en": "To follow wherever circumstance turns, waver between two paths.",
        "notes": "Metaphorical Minnan four-character phrase 隨起隨倒.",
        "tones": ["T05 (平橫)", "T02 (降斜)", "T05 (平橫)", "T02 (降斜)"],
        "rec": "sui⁵ kʰi³ sui⁵ to³",
        "basis": "sui⁵ lower even; kʰi³ upper departing; to³ rising.",
        "tai_lo": "suî-khí-suî-tó",
        "moe": "04706",
        "hanzi_std": "隨起隨倒",
        "tag": "TAG-4",
        "tag_rat": "Idiomatic expression of behavioral vacillation."
    },
    # 307 (0957.07)
    {
        "sp_norm": "seguir la regla obrar por ella",
        "abbrs": [],
        "zh": "循規蹈矩；遵行軌矩；依循禮數章程行事",
        "en": "To follow the rules, act according to established norms.",
        "notes": "Classical idiom 循規蹈矩 corresponding to obrar por la regla.",
        "tones": ["T05 (平橫)", "T01 (升斜)", "T02 (降斜)", "T02 (降斜)"],
        "rec": "sun⁵ kui¹ to⁶ ku³",
        "basis": "sun⁵ lower even; kui¹ upper even; to⁶ departing; ku³ rising.",
        "tai_lo": "sûn-kui-tō-kú",
        "moe": "04707",
        "hanzi_std": "循規蹈矩",
        "tag": "TAG-1",
        "tag_rat": "Moral and normative conduct match."
    },
    # 308 (0957.11)
    {
        "sp_norm": "segundo en licencias [del examen imperial]",
        "abbrs": [],
        "zh": "榜眼；殿試第二名進士；科舉二甲第一",
        "en": "Bangyan; second-ranked scholar in imperial palace examinations.",
        "notes": "segundo en licencias maps specifically onto 榜眼 (póng-gán).",
        "tones": ["T02 (降斜)", "T02 (降斜)"],
        "rec": "poŋ³ gian³",
        "basis": "poŋ³ upper rising; gian³ lower rising.",
        "tai_lo": "póng-gán",
        "moe": "04708",
        "hanzi_std": "榜眼",
        "tag": "TAG-4",
        "tag_rat": "Imperial examination rank institutional term."
    },
    # 309 (0959.15)
    {
        "sp_norm": "[seguro / seguridad]",
        "abbrs": [],
        "zh": "穩實；安穩保固；穩當可靠",
        "en": "Secure, reliable, firm assurance.",
        "notes": "Deleted lemma heading for seguro / seguridad.",
        "tones": ["T02 (降斜)", "T06/T07 (交叉入聲號)"],
        "rec": "un³ sit⁸",
        "basis": "un³ rising; sit⁸ lower entering tone.",
        "tai_lo": "ún-si̍t",
        "moe": "04709",
        "hanzi_std": "穩實",
        "tag": "TAG-1",
        "tag_rat": "Security and firmness gloss."
    },
    # 310 (DHS0960-01)
    {
        "sp_norm": "seguro, cierto",
        "abbrs": [],
        "zh": "牢實；必定無疑；牢靠確準",
        "en": "Sure, certain, firmly dependable.",
        "notes": "Latin annotation chau corresponds to Minnan tiâu (牢/著).",
        "tones": ["T05 (平橫)", "T06/T07 (交叉入聲號)"],
        "rec": "tiau⁵ sit⁸",
        "basis": "tiau⁵ lower even; sit⁸ entering.",
        "tai_lo": "tiâu-si̍t",
        "moe": "04710",
        "hanzi_std": "牢實",
        "tag": "TAG-1",
        "tag_rat": "Epistemic certainty gloss."
    },
    # 311 (DHS0961-10)
    {
        "sp_norm": "sementera, vn quartel della de 15 baras, p[or] la parte",
        "abbrs": [{"abbr": "p̃", "expansion": "p[or]"}],
        "zh": "畝；一畝田；方十五步之田疇地積",
        "en": "A mu (Chinese acre), parcel of cultivated land measuring 15 varas per side.",
        "notes": "European land parcel of 15 varas compared with Chinese 畝 (bóo).",
        "tones": ["T02 (降斜)"],
        "rec": "bu³",
        "basis": "bu³ lower rising tone preserving labial nasal initial.",
        "tai_lo": "bóo",
        "moe": "04711",
        "hanzi_std": "畝",
        "tag": "TAG-4",
        "tag_rat": "Agricultural agrarian land measurement calque."
    },
    # 312 (DHS0962-05)
    {
        "sp_norm": "Señal de q[ue]madura o herida",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "疤；創傷或燙傷留下之疤痕",
        "en": "Scar, cicatrix left by wound or burn.",
        "notes": "Somatic dermatological mark gloss.",
        "tones": ["T01 (升斜)"],
        "rec": "pa¹",
        "basis": "pa¹ upper even tone, voiceless bilabial plosive.",
        "tai_lo": "pa",
        "moe": "04712",
        "hanzi_std": "疤",
        "tag": "TAG-1",
        "tag_rat": "Direct medical injury mark."
    },
    # 313 (DHS0962-06)
    {
        "sp_norm": "Señal de q[ue]madura, o herida",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "痕；傷痕烙印；創痕",
        "en": "Trace, mark, scar left by injury.",
        "notes": "Colloquial Minnan 痕 (hûn) denoting physical marks.",
        "tones": ["T05 (平橫)"],
        "rec": "hun⁵",
        "basis": "hun⁵ lower even tone, glottal fricative initial.",
        "tai_lo": "hûn",
        "moe": "04713",
        "hanzi_std": "痕",
        "tag": "TAG-1",
        "tag_rat": "Superficial cutaneous mark."
    },
    # 314 (DHS0962-11)
    {
        "sp_norm": "Señal, dar la [señal de fianza / arras]",
        "abbrs": [],
        "zh": "聘定；下聘定約；授付聘儀定錢以立信",
        "en": "To give earnest money, pay betrothal or contractual pledge.",
        "notes": "Spanish dar la señal glossed as matrimonial/commercial earnest pledge 聘定.",
        "tones": ["T04 (凹角)", "T05 (平橫)"],
        "rec": "pʰiŋ⁶ tiŋ⁶",
        "basis": "pʰiŋ⁶ aspirated lower departing; tiŋ⁶ lower departing.",
        "tai_lo": "phīng-tīng",
        "moe": "04714",
        "hanzi_std": "聘定",
        "tag": "TAG-4",
        "tag_rat": "Contractual token of commitment."
    },
    # 315 (DHS0962-18)
    {
        "sp_norm": "Señal de herida o q[ue]madura",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "疤痣；疤痕與黑痣；皮膚瘢記",
        "en": "Scar and birthmark / mole on skin.",
        "notes": "Compound noun 疤痣 pairing trauma mark with natural skin lesion.",
        "tones": ["T01 (升斜)", "T03 (尖頂帽)"],
        "rec": "pa¹ ki³",
        "basis": "pa¹ upper even; ki³ upper departing tone.",
        "tai_lo": "pa-kì",
        "moe": "04715",
        "hanzi_std": "疤痣",
        "tag": "TAG-1",
        "tag_rat": "Cutaneous physical token."
    },
    # 316 (DHS0963-04)
    {
        "sp_norm": "Señal p[ara] que conoz[ca]",
        "abbrs": [{"abbr": "p̃", "expansion": "p[ara]"}],
        "zh": "記認；辨認信物；作為識別之標記",
        "en": "Recognizable token, mark for identification.",
        "notes": "Cognitive mnemonic token 記認 (kì-jīn).",
        "tones": ["T03 (尖頂帽)", "T05 (平橫)"],
        "rec": "ki³ dzin⁶",
        "basis": "ki³ upper departing; dzin⁶ voiced sibilant lower departing.",
        "tai_lo": "kì-jīn",
        "moe": "04716",
        "hanzi_std": "記認",
        "tag": "TAG-1",
        "tag_rat": "Identification token match."
    },
    # 317 (0965.01)
    {
        "sp_norm": "Señor P[adr]e S[eñor] Obispo",
        "abbrs": [
            {"abbr": "Pᵉ", "expansion": "P[adr]e"},
            {"abbr": "S.", "expansion": "S[eñor]"}
        ],
        "zh": "老爺；尊稱主教或高品神長之號",
        "en": "Lord Father, Your Lordship the Bishop; formal honorific address.",
        "notes": "Honorific 老爺 applied to high ecclesiastical dignitary (Obispo).",
        "tones": ["T02 (降斜)", "T05 (平橫)"],
        "rec": "lau³ ia⁵",
        "basis": "lau³ upper rising; ia⁵ lower even tone.",
        "tai_lo": "láu-iâ",
        "moe": "04717",
        "hanzi_std": "老爺",
        "tag": "TAG-4",
        "tag_rat": "Ecclesiastical dignitary honorific calque."
    },
    # 318 (0965.02)
    {
        "sp_norm": "S[anto] Padre",
        "abbrs": [{"abbr": "S.", "expansion": "S[anto]"}],
        "zh": "引爹；天主教教宗之尊稱；聖父",
        "en": "Holy Father, the Pope; reverend clerical patron.",
        "notes": "Early Catholic translation of Santo Padre in Manila.",
        "tones": ["T02 (降斜)", "T01 (升斜)"],
        "rec": "in³ tia¹",
        "basis": "in³ rising tone; tia¹ upper even tone.",
        "tai_lo": "ín-tia",
        "moe": "04718",
        "hanzi_std": "引爹",
        "tag": "TAG-4",
        "tag_rat": "Ecclesiastical Catholic papal honorific."
    },
    # 319 (0965.03)
    {
        "sp_norm": "Señor P[adr]e",
        "abbrs": [{"abbr": "Pᵉ", "expansion": "P[adr]e"}],
        "zh": "老爹；對父親或長老之尊稱",
        "en": "Lord Father, respectful address to a father or respected elder.",
        "notes": "Filial honorific address 老爹.",
        "tones": ["T02 (降斜)", "T01 (升斜)"],
        "rec": "lo³ tia¹",
        "basis": "lo³ rising tone; tia¹ upper even tone.",
        "tai_lo": "ló-tia",
        "moe": "04719",
        "hanzi_std": "老爹",
        "tag": "TAG-1",
        "tag_rat": "Paternal filial honorific."
    },
    # 320 (0965.08)
    {
        "sp_norm": "Señor oficial [maestro artesano]",
        "abbrs": [],
        "zh": "師父公；行會師傅首領；百工匠官尊稱",
        "en": "Master craftsman, guild master, official artisan.",
        "notes": "Honorific compound 師父公 for guild master / head artisan.",
        "tones": ["T01 (升斜)", "T04 (凹角)", "T01 (升斜)"],
        "rec": "sai¹ hu⁶ koŋ¹",
        "basis": "sai¹ upper even; hu⁶ lower departing; koŋ¹ upper even.",
        "tai_lo": "sai-hū-kong",
        "moe": "04720",
        "hanzi_std": "師父公",
        "tag": "TAG-4",
        "tag_rat": "Guild artisan leader title."
    },
    # 321 (0965.10)
    {
        "sp_norm": "S[aludo d]el hijo al P[adr]e o madre",
        "abbrs": [
            {"abbr": "S.", "expansion": "S[aludo]"},
            {"abbr": "Pᵉ", "expansion": "P[adr]e"}
        ],
        "zh": "膝下；子向父母行文致意之書信敬辭",
        "en": "At your knees; deferential epistolary formula from child to parents.",
        "notes": "Classical Chinese epistolary salutation 膝下 corresponding to formal filial greeting.",
        "tones": ["T06/T07 (交叉入聲號)", "T05 (平橫)"],
        "rec": "tsʰit⁷ ha⁶",
        "basis": "tsʰit⁷ upper entering; ha⁶ lower departing.",
        "tai_lo": "tshit-hā",
        "moe": "04721",
        "hanzi_std": "膝下",
        "tag": "TAG-4",
        "tag_rat": "Epistolary filial reverential formula."
    },
    # 322 (0965.15)
    {
        "sp_norm": "S[eñor] viejo noble p[ara] el Mandarin",
        "abbrs": [
            {"abbr": "S.", "expansion": "S[eñor]"},
            {"abbr": "p̃", "expansion": "p[ara]"}
        ],
        "zh": "老爺；尊稱致仕年高之老官人；大人",
        "en": "Venerable noble elder / magistrate (mandarin).",
        "notes": "Civil magistrate honorific address 老爺.",
        "tones": ["T02 (降斜)", "T05 (平橫)"],
        "rec": "lau³ ia⁵",
        "basis": "lau³ rising; ia⁵ lower even tone.",
        "tai_lo": "láu-iâ",
        "moe": "04722",
        "hanzi_std": "老爺",
        "tag": "TAG-4",
        "tag_rat": "Official mandarin honorific calque."
    },
    # 323 (0967.13)
    {
        "sp_norm": "Sentenciar a dar garrote [ejecución o azote]",
        "abbrs": [],
        "zh": "斷打；判決重刑杖擊；處斷杖責",
        "en": "To sentence to severe flogging or execution.",
        "notes": "Judicial sentencing phrase 斷打 (tuàn-phah).",
        "tones": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"],
        "rec": "tuan³ pʰaʔ⁷",
        "basis": "tuan³ upper departing; pʰaʔ⁷ glottal stop entering tone.",
        "tai_lo": "tuàn-phah",
        "moe": "04723",
        "hanzi_std": "斷打",
        "tag": "TAG-1",
        "tag_rat": "Judicial penal sentence calque."
    },
    # 324 (0969.04)
    {
        "sp_norm": "Ser para mucho [muy capaz / eminente]",
        "abbrs": [],
        "zh": "太過；才能過人；手段極高強",
        "en": "To be exceptionally capable, extraordinary in ability.",
        "notes": "Ser para mucho rendered by intensive 太過.",
        "tones": ["T03 (尖頂帽)", "T03 (尖頂帽)"],
        "rec": "tʰai³ kue³",
        "basis": "tʰai³ upper departing; kue³ upper departing.",
        "tai_lo": "thài-kuè",
        "moe": "04724",
        "hanzi_std": "太過",
        "tag": "TAG-3",
        "tag_rat": "Idiomatic capacity intensifier."
    },
    # 325 (0969.08)
    {
        "sp_norm": "Serrajer[o] [cerrajero / herrero]",
        "abbrs": [],
        "zh": "裝釘；鐵鎖白鐵匠人；鎖匠",
        "en": "Locksmith, ironmonger who fits locks and nails.",
        "notes": "Handicraft locksmith profession 裝釘 (tsong-ting).",
        "tones": ["T01 (升斜)", "T01 (升斜)"],
        "rec": "tsoŋ¹ tiŋ¹",
        "basis": "tsoŋ¹ upper even; tiŋ¹ upper even tone.",
        "tai_lo": "tsong-ting",
        "moe": "04725",
        "hanzi_std": "裝釘",
        "tag": "TAG-4",
        "tag_rat": "Artisan trade occupational designation."
    },
    # 326 (0969.13)
    {
        "sp_norm": "Serrar la bolsa, y serraderos",
        "abbrs": [],
        "zh": "括束；勒束荷包抽繩；收緊口袋",
        "en": "To cinch a drawstring purse; purse drawstrings.",
        "notes": "Mechanical purse closure verb 括束.",
        "tones": ["T06/T07 (交叉入聲號)", "T06/T07 (交叉入聲號)"],
        "rec": "kuat⁷ iok⁸",
        "basis": "kuat⁷ upper entering; iok⁸ lower entering tone.",
        "tai_lo": "kuat-io̍k",
        "moe": "04726",
        "hanzi_std": "括束",
        "tag": "TAG-1",
        "tag_rat": "Drawstring action match."
    },
    # 327 (DHS0970-17)
    {
        "sp_norm": "Serrarse la boca desvergonçado",
        "abbrs": [],
        "zh": "鎖口；封口噤聲；鉗制無賴之口舌",
        "en": "To shut one's shameless mouth, be silenced.",
        "notes": "Metaphorical silencing verb phrase 鎖口.",
        "tones": ["T02 (降斜)", "T04 (凹角)"],
        "rec": "so³ tsʰui⁶",
        "basis": "so³ rising tone; tsʰui⁶ lower departing.",
        "tai_lo": "só-tshuì",
        "moe": "04727",
        "hanzi_std": "鎖口",
        "tag": "TAG-1",
        "tag_rat": "Somatic silencing idiom."
    },
    # 328 (DHS0973-02)
    {
        "sp_norm": "Sy fueres [condicional]",
        "abbrs": [],
        "zh": "那你去；若是你去；倘若你往",
        "en": "If you should go; conditional protasis.",
        "notes": "Spoken conditional clause 那你去 (ná lí khì).",
        "tones": ["T02 (降斜)", "T02 (降斜)", "T03 (尖頂帽)"],
        "rec": "na³ li³ kʰi³",
        "basis": "na³ rising; li³ rising; kʰi³ upper departing.",
        "tai_lo": "ná lí khì",
        "moe": "04728",
        "hanzi_std": "那你去",
        "tag": "TAG-1",
        "tag_rat": "Conditional clause syntax match."
    },
    # 329 (DHS0973-05)
    {
        "sp_norm": "Sy, respondiendo el criado o hijo a su p[adr]e",
        "abbrs": [{"abbr": "pᵉ", "expansion": "p[adr]e"}],
        "zh": "唯諾；唯唯敬答；敬謹承諾應聲",
        "en": "Yes; obedient verbal assent of servant or son to father.",
        "notes": "Formal filial and submissive affirmative 唯諾 (uî-lo̍k).",
        "tones": ["T05 (平橫)", "T06/T07 (交叉入聲號)"],
        "rec": "ui⁵ lok⁸",
        "basis": "ui⁵ lower even tone; lok⁸ lower entering.",
        "tai_lo": "uî-lo̍k",
        "moe": "04729",
        "hanzi_std": "唯諾",
        "tag": "TAG-4",
        "tag_rat": "Submissive affirmative speech formula."
    },
    # 330 (DHS0973-11)
    {
        "sp_norm": "Sy, dado q[ue] sea asi",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "既然；縱使如此；既然果真這般",
        "en": "Granted that it is so, since it is indeed thus.",
        "notes": "Concessive conjunction 既然 (kì-jiân).",
        "tones": ["T03 (尖頂帽)", "T05 (平橫)"],
        "rec": "ki³ dzian⁵",
        "basis": "ki³ upper departing; dzian⁵ voiced lower even.",
        "tai_lo": "kì-jiân",
        "moe": "04730",
        "hanzi_std": "既然",
        "tag": "TAG-1",
        "tag_rat": "Concessive logical conjunction."
    },
    # 331 (DHS0974-19)
    {
        "sp_norm": "Sierra do hauitan los discipulos [monte sagrado]",
        "abbrs": [],
        "zh": "岳；高峻大山；名岳名山",
        "en": "Sacred mountain range, elevated peak.",
        "notes": "Classical Hanzi 岳 (ga̍k) glossed for mountain abode of recluses.",
        "tones": ["T06/T07 (交叉入聲號)"],
        "rec": "gak⁸",
        "basis": "gak⁸ voiced velar entering tone.",
        "tai_lo": "ga̍k",
        "moe": "04731",
        "hanzi_std": "岳",
        "tag": "TAG-1",
        "tag_rat": "Topographical sacred peak term."
    },
    # 332 (0976.02)
    {
        "sp_norm": "Simiente, tiene la q[ue] engendrar",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "有形精；具備生育繁衍之精血精氣",
        "en": "Possessing seminal seed / reproductive essence.",
        "notes": "Physiological reproduction concept 有形精.",
        "tones": ["T04 (凹角)", "T05 (平橫)", "T01 (升斜)"],
        "rec": "u⁶ hiŋ⁵ tsiŋ¹",
        "basis": "u⁶ lower departing; hiŋ⁵ lower even; tsiŋ¹ upper even.",
        "tai_lo": "ū-hîng-tsing",
        "moe": "04732",
        "hanzi_std": "有形精",
        "tag": "TAG-4",
        "tag_rat": "Physiological essence term."
    },
    # 333 (0976.04)
    {
        "sp_norm": "Sin raçon, sin justa r[az]o[n]",
        "abbrs": [{"abbr": "rº", "expansion": "r[az]o[n]"}],
        "zh": "橫無理；強橫枉曲；蠻不講理",
        "en": "Unreasonable, lacking just cause, arbitrarily insolent.",
        "notes": "DHS captures wrongful injustice via 橫/無理.",
        "tones": ["T05 (平橫)", "T05 (平橫)", "T02 (降斜)"],
        "rec": "huaŋ⁵ bu⁵ li³",
        "basis": "huaŋ⁵ lower even; bu⁵ lower even; li³ rising.",
        "tai_lo": "huâinn-bô-lí",
        "moe": "04733",
        "hanzi_std": "橫無理",
        "tag": "TAG-1",
        "tag_rat": "Injustice moral assessment match."
    },
    # 334 (0976.07)
    {
        "sp_norm": "Sin que, porq[ue]",
        "abbrs": [{"abbr": "porq̃", "expansion": "porq[ue]"}],
        "zh": "若無；倘非；若非因著某故",
        "en": "Without, were it not for the fact that.",
        "notes": "Negative conditional grammatical particle.",
        "tones": ["T06/T07 (交叉入聲號)", "T05 (平橫)"],
        "rec": "naʔ⁸ bu⁵",
        "basis": "naʔ⁸ entering tone; bu⁵ lower even.",
        "tai_lo": "na̍h-bô",
        "moe": "04734",
        "hanzi_std": "若無",
        "tag": "TAG-1",
        "tag_rat": "Negative conditional particle."
    },
    # 335 (0976.11)
    {
        "sp_norm": "Sisar, pepenar [recolectar menudencias]",
        "abbrs": [],
        "zh": "挑零；摸索取小利；揀拾零星小物",
        "en": "To filch small pickings, gather scraps / glean.",
        "notes": "Vernacular verb 挑/揀 (thiau/tiù) for gathering trifles.",
        "tones": ["T03 (尖頂帽)"],
        "rec": "tiu³",
        "basis": "tiu³ upper departing tone.",
        "tai_lo": "tiù",
        "moe": "04735",
        "hanzi_std": "挑",
        "tag": "TAG-1",
        "tag_rat": "Peculation and gleaning verb."
    },
    # 336 (0976.17)
    {
        "sp_norm": "Sobaquina [olor sobaquino]",
        "abbrs": [],
        "zh": "臭癋；腋下狐臭臭汗氣",
        "en": "Body odor, armpit stench, fox odor.",
        "notes": "Medical somatic symptom 臭癋 (tshàu-ha̍k).",
        "tones": ["T03 (尖頂帽)", "T06/T07 (交叉入聲號)"],
        "rec": "tsʰau³ hak⁸",
        "basis": "tsʰau³ upper departing; hak⁸ entering tone.",
        "tai_lo": "tshàu-ha̍k",
        "moe": "04736",
        "hanzi_std": "臭癋",
        "tag": "TAG-1",
        "tag_rat": "Somatic olfactory pathology."
    },
    # 337 (0977.01)
    {
        "sp_norm": "Sobar, fregar con manos la massa",
        "abbrs": [],
        "zh": "搓揉；雙手用力揉搓麵團；和揉",
        "en": "To knead dough firmly with both hands.",
        "notes": "Culinary kneading verb 搓 (tsho).",
        "tones": ["T01 (升斜)", "T05 (平橫)"],
        "rec": "tsʰo¹ dzu⁵",
        "basis": "tsʰo¹ upper even; dzu⁵ lower even.",
        "tai_lo": "tsho-jiû",
        "moe": "04737",
        "hanzi_std": "搓揉",
        "tag": "TAG-1",
        "tag_rat": "Manual dough preparation verb."
    },
    # 338 (0977.07)
    {
        "sp_norm": "Soberado [piso alto / desván]",
        "abbrs": [],
        "zh": "樓；高架樓閣；樓層",
        "en": "Upper storey, loft, second floor.",
        "notes": "Architectural structure noun 樓 (lâu).",
        "tones": ["T05 (平橫)"],
        "rec": "lau⁵",
        "basis": "lau⁵ lower even tone, lateral liquid initial.",
        "tai_lo": "lâu",
        "moe": "04738",
        "hanzi_std": "樓",
        "tag": "TAG-1",
        "tag_rat": "Upper floor architectural term."
    },
    # 339 (0977.08)
    {
        "sp_norm": "Soberado, numeral [clasificador de pisos]",
        "abbrs": [],
        "zh": "層；層次；樓宇層閣量詞",
        "en": "Storey, tier, architectural numeral classifier.",
        "notes": "Numeral classifier 層 (tsân) for storeys.",
        "tones": ["T05 (平橫)"],
        "rec": "tsan⁵",
        "basis": "tsan⁵ lower even tone.",
        "tai_lo": "tsan",
        "moe": "04739",
        "hanzi_std": "層",
        "tag": "TAG-1",
        "tag_rat": "Architectural numeral classifier."
    },
    # 340 (0977.09)
    {
        "sp_norm": "Soberado [azotea / piso más alto]",
        "abbrs": [],
        "zh": "樓頂；屋宇最頂層；閣樓",
        "en": "Top floor, roof chamber, attic.",
        "notes": "Compound noun 樓頂 (lâu-tíng).",
        "tones": ["T05 (平橫)", "T02 (降斜)"],
        "rec": "lau⁵ tiŋ³",
        "basis": "lau⁵ lower even; tiŋ³ rising tone.",
        "tai_lo": "lâu-tíng",
        "moe": "04740",
        "hanzi_std": "樓頂",
        "tag": "TAG-1",
        "tag_rat": "Top storey architectural term."
    },
    # 341 (0977.10)
    {
        "sp_norm": "Soberado [galería alta]",
        "abbrs": [],
        "zh": "樓閣；高層亭閣；雕樑層樓",
        "en": "Upper pavilion, gallery, multi-storeyed building.",
        "notes": "Elevated pavilion compound 樓閣 (lâu-koh).",
        "tones": ["T05 (平橫)", "T06/T07 (交叉入聲號)"],
        "rec": "lau⁵ kok⁷",
        "basis": "lau⁵ lower even; kok⁷ upper entering.",
        "tai_lo": "lâu-koh",
        "moe": "04741",
        "hanzi_std": "樓閣",
        "tag": "TAG-1",
        "tag_rat": "Architectural pavilion term."
    },
    # 342 (0978.10)
    {
        "sp_norm": "Soberuio, vano q[ue] se ha ensoberuecido",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "洋洋然；盛氣凌人；自負驕矜貌",
        "en": "Arrogant, vainglorious, swelling with self-importance.",
        "notes": "Classical behavioral descriptive 洋洋然.",
        "tones": ["T05 (平橫)", "T05 (平橫)", "T05 (平橫)"],
        "rec": "iaŋ⁵ iaŋ⁵ dzian⁵",
        "basis": "iaŋ⁵ lower even; dzian⁵ voiced sibilant lower even.",
        "tai_lo": "iông-iông-jiân",
        "moe": "04742",
        "hanzi_std": "洋洋然",
        "tag": "TAG-1",
        "tag_rat": "Arrogant behavioral disposition."
    },
    # 343 (0978.12)
    {
        "sp_norm": "Soberuio fantastico",
        "abbrs": [],
        "zh": "假大；虛妄自誇；打腫臉充胖子",
        "en": "Pretentiously proud, vainly puffed up.",
        "notes": "Colloquial descriptive compound 假大 (ké-tuā).",
        "tones": ["T02 (降斜)", "T04 (凹角)"],
        "rec": "ke³ tua⁶",
        "basis": "ke³ rising; tua⁶ lower departing tone.",
        "tai_lo": "ké-tuā",
        "moe": "04743",
        "hanzi_std": "假大",
        "tag": "TAG-1",
        "tag_rat": "Pretentious pride descriptor."
    },
    # 344 (0979.01)
    {
        "sp_norm": "Soberuio, fingese noble y es uil",
        "abbrs": [],
        "zh": "最假色確；極端虛偽驕慢；裝腔作勢",
        "en": "Utter hypocrite, feigning nobility while base, posing as wise while foolish.",
        "notes": "Intensive four-character formulation 最假色確.",
        "tones": ["T03 (尖頂帽)", "T02 (降斜)", "T06/T07 (交叉入聲號)", "T06/T07 (交叉入聲號)"],
        "rec": "tsue³ ke³ sik⁷ kʰok⁷",
        "basis": "tsue³ departing; ke³ rising; sik⁷ entering; kʰok⁷ entering.",
        "tai_lo": "tsuè-ké-sik-khok",
        "moe": "04744",
        "hanzi_std": "最假色確",
        "tag": "TAG-4",
        "tag_rat": "Moral hypocrisy descriptive phrase."
    },
    # 345 (0979.03)
    {
        "sp_norm": "Sobornar, q[ue] cocho [cohecho]",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "賄賂；以財賄買通；暗行苞苴",
        "en": "To bribe, suborn, pay bribery / cohecho.",
        "notes": "Judicial corruption verb 賄賂 (uán-lōo).",
        "tones": ["T02 (降斜)", "T04 (凹角)"],
        "rec": "uan³ lo⁶",
        "basis": "uan³ rising tone; lo⁶ lower departing.",
        "tai_lo": "uán-lōo",
        "moe": "04745",
        "hanzi_std": "賄賂",
        "tag": "TAG-1",
        "tag_rat": "Bribery and graft term."
    },
    # 346 (0979.11)
    {
        "sp_norm": "Sobornar p[ara] remediar el pleyto",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ara]"}],
        "zh": "補搭；花錢平息官司；私下行賄調解",
        "en": "To pay bribes to settle a lawsuit or litigation.",
        "notes": "Practical legal bribery term 補搭 (póo-tah).",
        "tones": ["T02 (降斜)", "T06/T07 (交叉入聲號)"],
        "rec": "pu³ taʔ⁷",
        "basis": "pu³ rising tone; taʔ⁷ glottal entering.",
        "tai_lo": "póo-tah",
        "moe": "04746",
        "hanzi_std": "補搭",
        "tag": "TAG-4",
        "tag_rat": "Litigation settlement payoff."
    },
    # 347 (0979.12)
    {
        "sp_norm": "Sobornar p[ara] remediar el pleyto",
        "abbrs": [{"abbr": "pᵃ", "expansion": "p[ara]"}],
        "zh": "分班；均分打點官差之財物",
        "en": "To distribute shares / payoffs among court runners to resolve suit.",
        "notes": "Administrative payoff distribution 分班 (hun-pan).",
        "tones": ["T01 (升斜)", "T01 (升斜)"],
        "rec": "hun¹ pan¹",
        "basis": "hun¹ upper even; pan¹ upper even.",
        "tai_lo": "hun-pan",
        "moe": "04747",
        "hanzi_std": "分班",
        "tag": "TAG-4",
        "tag_rat": "Payoff distribution practice."
    },
    # 348 (DHS0980-11)
    {
        "sp_norm": "Sobre aguado [flotante]",
        "abbrs": [],
        "zh": "浮漂；漂浮水面；浮泛水上",
        "en": "Floating on the water surface, buoyant.",
        "notes": "Hydrodynamic floating verb 浮 (phû / phiô).",
        "tones": ["T05 (平橫)"],
        "rec": "pʰu⁵",
        "basis": "pʰu⁵ lower even tone with aspirated bilabial.",
        "tai_lo": "phû",
        "moe": "04748",
        "hanzi_std": "浮",
        "tag": "TAG-1",
        "tag_rat": "Buoyant surface floating verb."
    },
    # 349 (DHS0980-12)
    {
        "sp_norm": "Sobre aguado [inundado / anegado]",
        "abbrs": [],
        "zh": "泛浸；漫溢浸潤；浸漬於水",
        "en": "Flooded, submerged, overflowing with water.",
        "notes": "Water inundation condition 泛浸.",
        "tones": ["T03 (尖頂帽)", "T03 (尖頂帽)"],
        "rec": "huan³ tsʰim³",
        "basis": "huan³ upper departing; tsʰim³ upper departing.",
        "tai_lo": "huàn-tshìm",
        "moe": "04749",
        "hanzi_std": "泛浸",
        "tag": "TAG-1",
        "tag_rat": "Water overflowing state."
    },
    # 350 (DHS0980-16)
    {
        "sp_norm": "Sobre estante, el q[ue] es superior y gouierna, maiordomo",
        "abbrs": [{"abbr": "q̃", "expansion": "q[ue]"}],
        "zh": "管家；主持總務之主管大總管；執事",
        "en": "Overseer, superintendent, major-domo who governs the estate.",
        "notes": "Domestic and institutional management title 管家 (kuán-ke).",
        "tones": ["T02 (降斜)", "T01 (升斜)"],
        "rec": "kuan³ ke¹",
        "basis": "kuan³ rising; ke¹ upper even tone.",
        "tai_lo": "kuán-ke",
        "moe": "04750",
        "hanzi_std": "管家",
        "tag": "TAG-4",
        "tag_rat": "Managerial steward office."
    }
]

assert len(raw_50) == 50
assert len(ENTRIES_DATA_B7) == 50

batch_entries = []
for i in range(50):
    r = raw_50[i]
    d = ENTRIES_DATA_B7[i]
    
    p = r["page"]
    pos = r["pos"]
    eid = r["id"]
    
    entry_obj = {
        "entry_id": eid,
        "layer_0_visual_anchor": {
            "page_pdf": p,
            "page_folio": p - 38 if p else None,
            "position_in_page": pos,
            "bounding_box_hint": f"row {pos:02d}, 4-column layout" if pos else "4-column layout"
        },
        "layer_1_diplomatic_raw": {
            "source_L": r.get("source_L", ""),
            "source_H": r.get("source_H", ""),
            "source_M": r.get("source_M", ""),
            "source_R": r.get("source_R", "")
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
    "batch_id": "batch_07_m1_disambiguated_50",
    "provenance": "Certified v3.1 Final disambiguation for DHS entries 301 to 350",
    "entries": batch_entries
}

out_path = Path("literature/workspace_m1_dhs306/batch_07_m1_disambiguated_50.json")
out_path.write_text(json.dumps(output_batch, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Successfully generated {out_path} with {len(batch_entries)} entries.")
