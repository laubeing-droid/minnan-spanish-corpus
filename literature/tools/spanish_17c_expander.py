#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Early Modern (16th-17th c.) Spanish Paleographic Abbreviation Expander
& Manila Sangley (Hokkien) Colonial Glossary Engine
======================================================================
Designed for zero-token, 100% deterministic preprocessing before or after
Chinese VLM / LLM execution in ZCode.
"""

import re
from typing import Dict, List, Any, Tuple

# 1. Deterministic Paleographic Abbreviations (16th-17th c. Dominican Manuscripts)
SPANISH_ABBREV_RULES: List[Tuple[str, str, str]] = [
    # (Regex pattern, display abbr, expanded form)
    (r"\bq̃\b", "q̃", "q[ue]"),
    (r"\bq\.ᵉ\b", "q.ᵉ", "q[ue]"),
    (r"\bqᵉ\b", "qᵉ", "q[ue]"),
    (r"\bp\.ᵃ\b", "p.ᵃ", "p[ar]a"),
    (r"\bpᵃ\b", "pᵃ", "p[ar]a"),
    (r"\bp̃\b", "p̃", "p[ara]"),
    (r"\bp\.ʳ\b", "p.ʳ", "p[o]r"),
    (r"\bpʳ\b", "pʳ", "p[o]r"),
    (r"\bp\.ᵗᵉ\b", "p.ᵗᵉ", "p[ar]te"),
    (r"\bpᵗᵉ\b", "pᵗᵉ", "p[ar]te"),
    (r"\bP\.ᵉ\b", "P.ᵉ", "P[adr]e"),
    (r"\bPᵉ\b", "Pᵉ", "P[adr]e"),
    (r"\bp\.ᵉ\b", "p.ᵉ", "p[adr]e"),
    (r"\bpᵉ\b", "pᵉ", "p[adr]e"),
    (r"\bm\.ᵉ\b", "m.ᵉ", "m[adr]e"),
    (r"\bmᵉ\b", "mᵉ", "m[adr]e"),
    (r"(\w+)m\.ᵗᵉ\b", "m.ᵗᵉ", r"\1m[en]te"),
    (r"(\w+)mᵗᵉ\b", "mᵗᵉ", r"\1m[en]te"),
    (r"\bm\.ᵗᵉ\b", "m.ᵗᵉ", "m[en]te"),
    (r"\bmᵗᵉ\b", "mᵗᵉ", "m[en]te"),
    (r"\bsup\.ᵒʳ\b", "sup.ᵒʳ", "sup[eri]or"),
    (r"\bsupᵒʳ\b", "supᵒʳ", "sup[eri]or"),
    (r"\binf\.ᵒʳ\b", "inf.ᵒʳ", "inf[eri]or"),
    (r"\binfᵒʳ\b", "infᵒʳ", "inf[eri]or"),
    (r"\boff\.º\b", "off.º", "off[ici]o"),
    (r"\boffº\b", "offº", "off[ici]o"),
    (r"\bof\.º\b", "of.º", "of[ici]o"),
    (r"\bofº\b", "ofº", "of[ici]o"),
    (r"\boff\.ˢ\b", "off.ˢ", "off[iciale]s"),
    (r"\boffˢ\b", "offˢ", "off[iciale]s"),
    (r"\bS\.ᵒʳ\b", "S.ᵒʳ", "S[eñ]or"),
    (r"\bSᵒʳ\b", "Sᵒʳ", "S[eñ]or"),
    (r"\bs\.ᵒʳ\b", "s.ᵒʳ", "s[eñ]or"),
    (r"\bsᵒʳ\b", "sᵒʳ", "s[eñ]or"),
    (r"\bN\.?\s*S\.ᵒʳ\b", "N. S.ᵒʳ", "N[uestro] S[eñ]or"),
    (r"\bV\.?\s*M\.?\b", "V. M.", "V[uestra] M[erced]"),
    (r"\bVm\.?\b", "Vm.", "V[uestra] m[erced]"),
    (r"\bv\.ᵉ\b", "v.ᵉ", "v[éas]e"),
    (r"\bvᵉ\b", "vᵉ", "v[éas]e"),
    (r"\balg\.º\b", "alg.º", "alg[un]o"),
    (r"\balgº\b", "algº", "alg[un]o"),
    (r"\balg\.ᵃ\b", "alg.ᵃ", "alg[un]a"),
    (r"\balgᵃ\b", "algᵃ", "alg[un]a"),
    (r"\balg\.ᵒˢ\b", "alg.ᵒˢ", "alg[un]os"),
    (r"\balgᵒˢ\b", "algᵒˢ", "alg[un]os"),
    (r"\balg\.ᵃˢ\b", "alg.ᵃˢ", "alg[un]as"),
    (r"\balgᵃˢ\b", "algᵃˢ", "alg[un]as"),
    (r"\bdho\b", "dho", "d[ic]ho"),
    (r"\bdha\b", "dha", "d[ic]ha"),
    (r"\bnro\b", "nro", "n[uest]ro"),
    (r"\bnra\b", "nra", "n[uest]ra"),
    (r"\bvro\b", "vro", "v[uest]ro"),
    (r"\bvra\b", "vra", "v[uest]ra"),
    (r"\bher\.ᵐᵃⁿᵒ\b", "her.ᵐᵃⁿᵒ", "her[mano]"),
    (r"\bherᵐᵃⁿᵒ\b", "herᵐᵃⁿᵒ", "her[mano]"),
    (r"\bher\.ᵐᵒ\b", "her.ᵐᵒ", "her[man]o"),
    (r"\bherᵐᵒ\b", "herᵐᵒ", "her[man]o"),
    (r"\bher\.ᵐᵒˢ\b", "her.ᵐᵒˢ", "her[man]os"),
    (r"\bherᵐᵒˢ\b", "herᵐᵒˢ", "her[man]os"),
    (r"\bS\.ᵗᵒ\b", "S.ᵗᵒ", "S[an]to"),
    (r"\bSᵗᵒ\b", "Sᵗᵒ", "S[an]to"),
    (r"\bst\.º\b", "st.º", "s[an]to"),
    (r"\bstº\b", "stº", "s[an]to"),
    (r"\bst\.ᵃ\b", "st.ᵃ", "s[an]ta"),
    (r"\bstᵃ\b", "stᵃ", "s[an]ta"),
    (r"\bxpiano\b", "xpiano", "[crist]iano"),
    (r"\bxptiano\b", "xptiano", "[crist]iano"),
    (r"\bXpo\b", "Xpo", "[Crist]o"),
    (r"\btpo\b", "tpo", "t[iem]po"),
    (r"\btp̃o\b", "tp̃o", "t[iem]po"),
    (r"\bdr\.º\b", "dr.º", "d[e]r[ech]o"),
    (r"\bdrº\b", "drº", "d[e]r[ech]o"),
    (r"\bmrd\b", "mrd", "m[erce]d"),
    (r"\bgral\b", "gral", "g[ene]ral"),
    (r"\bg\.ʳᵃˡ\b", "g.ʳᵃˡ", "g[ene]ral"),
    (r"\bpart\.ᵃʳ\b", "part.ᵃʳ", "part[icul]ar"),
    (r"\bpartᵃʳ\b", "partᵃʳ", "part[icul]ar"),
    (r"\bdilig\.ᵃ\b", "dilig.ᵃ", "dilig[enci]a"),
    (r"\bdiligᵃ\b", "diligᵃ", "dilig[enci]a"),
    (r"\bneces\.º\b", "neces.º", "neces[ari]o"),
    (r"\bnecesº\b", "necesº", "neces[ari]o"),
    (r"\bord\.º\b", "ord.º", "ord[inari]o"),
    (r"\bordº\b", "ordº", "ord[inari]o"),
    (r"\bcontr\.º\b", "contr.º", "contr[ari]o"),
    (r"\bcontrº\b", "contrº", "contr[ari]o"),
    (r"(\w+)m\.ᵗᵒ\b", "m.ᵗᵒ", r"\1m[ien]to"),
    (r"(\w+)mᵗᵒ\b", "mᵗᵒ", r"\1m[ien]to"),
]

# 2. Manila Colonial & Sangley Hokkien Loanword Glossary
MANILA_SANGLEY_GLOSSARY: Dict[str, Dict[str, str]] = {
    "cuxin": {
        "hanzi": "舉人",
        "tai_lo": "kí-jîn / kú-jîn",
        "zh_note": "明清鄉試中式之「舉人」（閩南語音譯 cuxin）",
        "en_note": "Provincial civil examination graduate (Juren / licentiate)"
    },
    "sangley": {
        "hanzi": "生理人 / 唐人",
        "tai_lo": "sing-lí-lâng",
        "zh_note": "馬尼拉西班牙殖民當局對閩南華商與華人之稱呼（源自閩南語「生理人」）",
        "en_note": "Sangley; Manila Hokkien Chinese merchant/resident"
    },
    "sangleies": {
        "hanzi": "生理人 / 唐人（複數）",
        "tai_lo": "sing-lí-lâng",
        "zh_note": "馬尼拉閩南華人社群（Sangleyes）",
        "en_note": "Sangleyes; Manila Hokkien Chinese residents"
    },
    "parian": {
        "hanzi": "澗內 / 八連",
        "tai_lo": "kàn-lāi",
        "zh_note": "馬尼拉城外華人聚居與貿易特區「八連 / 澗內」（Parián de los Sangleyes）",
        "en_note": "Parián; the designated Chinese quarter and market in Manila"
    },
    "parián": {
        "hanzi": "澗內 / 八連",
        "tai_lo": "kàn-lāi",
        "zh_note": "馬尼拉城外華人聚居與貿易特區「八連 / 澗內」",
        "en_note": "Parián; the designated Chinese quarter and market in Manila"
    },
    "champan": {
        "hanzi": "舢舨 / 唐船",
        "tai_lo": "sam-pán",
        "zh_note": "往返閩南與呂宋之華人海船或大型舢舨（Champán）",
        "en_note": "Chinese trading junk or sampan vessel"
    },
    "champán": {
        "hanzi": "舢舨 / 唐船",
        "tai_lo": "sam-pán",
        "zh_note": "往返閩南與呂宋之華人海船或大型舢舨（Champán）",
        "en_note": "Chinese trading junk or sampan vessel"
    },
    "tuthoc": {
        "hanzi": "都督",
        "tai_lo": "too-tok",
        "zh_note": "明代福建總兵或水師都督（閩南語音譯 tuthoc）",
        "en_note": "Ming provincial military commander / Grand Coordinator (Dudu)"
    },
    "consi": {
        "hanzi": "公司",
        "tai_lo": "kong-si",
        "zh_note": "華人商幫公所、合股行號或善堂組織（公司）",
        "en_note": "Chinese guild, partnership, or communal association (Kongsi)"
    },
    "chapa": {
        "hanzi": "劄 / 牌照",
        "tai_lo": "tsap / pâi",
        "zh_note": "官府簽發之公文印信、居留許可或貿易牌照（Chapa）",
        "en_note": "Official edict, seal, or trade/residency license"
    },
    "tael": {
        "hanzi": "兩",
        "tai_lo": "niú",
        "zh_note": "中國銀兩衡制單位（Tael，約十錢）",
        "en_note": "Chinese silver tael weight unit"
    },
    "cate": {
        "hanzi": "斤",
        "tai_lo": "kin / kun",
        "zh_note": "中國與東南亞貿易衡制「斤」（Catty，十六兩為一斤）",
        "en_note": "Catty weight unit (approx. 600g, 16 taels)"
    },
    "picul": {
        "hanzi": "擔",
        "tai_lo": "tànn",
        "zh_note": "大宗海貿衡制「擔」（Picul，百斤為一擔）",
        "en_note": "Picul weight unit (100 catties)"
    },
    "ganta": {
        "hanzi": "升 / 斗",
        "tai_lo": "tsin / táu",
        "zh_note": "菲律賓殖民地穀物容量單位（Ganta，約合三公升）",
        "en_note": "Philippine dry volume measure for grain/rice (approx. 3 liters)"
    },
    "cavan": {
        "hanzi": "石 / 袋",
        "tai_lo": "tsio̍h",
        "zh_note": "菲律賓大宗穀物容量單位（Caván = 25 gantas）",
        "en_note": "Philippine dry measure (25 gantas)"
    },
    "buyo": {
        "hanzi": "荖葉檳榔",
        "tai_lo": "láu-hio̍h pin-nn̂g",
        "zh_note": "呂宋與閩南人常嚼之荖葉包檳榔灰捲（Buyo）",
        "en_note": "Betel leaf quid prepared with areca nut and lime"
    },
    "bonga": {
        "hanzi": "檳榔果",
        "tai_lo": "pin-nn̂g",
        "zh_note": "檳榔果實（源自他加祿語 Bunga）",
        "en_note": "Areca nut / betel palm fruit"
    },
    "petate": {
        "hanzi": "草蓆",
        "tai_lo": "tsháu-tshio̍h",
        "zh_note": "編織睡蓆（源自新西班牙納瓦特爾語 Petlatl，經大帆船貿易傳入馬尼拉）",
        "en_note": "Woven palm or reed sleeping mat"
    },
    "tibor": {
        "hanzi": "陶甕 / 呂宋壺",
        "tai_lo": "hûi-àng",
        "zh_note": "華船運往呂宋與美洲之儲物釉陶大甕（Tibor）",
        "en_note": "Large Chinese glazed stoneware storage jar"
    }
}


def expand_spanish_entry(source_l: str) -> Dict[str, Any]:
    """
    Deterministically expand 16th-17th century Spanish abbreviations and identify
    Manila Sangley colonial loanwords.
    Returns:
      {
        "spanish_disambiguated": str,
        "abbreviations_expanded": [{"abbr": ..., "expansion": ...}],
        "loanwords_detected": [{"term": ..., "hanzi": ..., "zh_note": ..., "en_note": ...}]
      }
    """
    if not source_l:
        return {
            "spanish_disambiguated": "",
            "abbreviations_expanded": [],
            "loanwords_detected": []
        }

    # Strip editorial brackets like [重墨], [刪...], 〔...〕 for clean disambiguated text
    cleaned = re.sub(r"\[[^\]]*\]|〔[^〕]*〕", "", source_l)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    abbrs_found: List[Dict[str, str]] = []
    expanded_text = cleaned

    for pattern, abbr_label, repl in SPANISH_ABBREV_RULES:
        matches = list(re.finditer(pattern, expanded_text))
        if matches:
            for m in matches:
                matched_str = m.group(0)
                exp_str = re.sub(pattern, repl, matched_str)
                entry = {"abbr": matched_str, "expansion": exp_str}
                if entry not in abbrs_found:
                    abbrs_found.append(entry)
            expanded_text = re.sub(pattern, repl, expanded_text)

    # Check loanwords
    loanwords_found: List[Dict[str, str]] = []
    words_lower = re.findall(r"[a-záéíóúñ]+", expanded_text.lower())
    for w in words_lower:
        if w in MANILA_SANGLEY_GLOSSARY:
            info = MANILA_SANGLEY_GLOSSARY[w]
            lw_item = {
                "term": w,
                "hanzi": info["hanzi"],
                "tai_lo": info["tai_lo"],
                "zh_note": info["zh_note"],
                "en_note": info["en_note"]
            }
            if lw_item not in loanwords_found:
                loanwords_found.append(lw_item)

    return {
        "spanish_disambiguated": expanded_text,
        "abbreviations_expanded": abbrs_found,
        "loanwords_detected": loanwords_found
    }


if __name__ == "__main__":
    import sys
    import json
    sys.stdout.reconfigure(encoding="utf-8")
    sample = "seguir el mandar del sup.ᵒʳ injustam.ᵗᵉ p.ᵃ el P.ᵉ de cuxin en el parian"
    print(json.dumps(expand_spanish_entry(sample), ensure_ascii=False, indent=2))
