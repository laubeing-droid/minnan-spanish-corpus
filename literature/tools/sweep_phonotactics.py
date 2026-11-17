#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量音系非法扫查 v2（只读封存件，不改数）。

M 栏（闽南音写·多明我规格）违类：
  - 音系非法声母：f-/v-/w-/x- （闽南与多明我规格均无）
  - 现代污染类：U+030D / U+207F / k-/kh- 声母 / ts-/tsh-/chh- 声母 / -k 韵尾
    （沿用 hokkien_17c_converter.has_modern_tailo_contamination 的五条官方规则）
  - 音系非法韵尾：-s -r -b -d -f -v -j -l -z -x 结尾（闽南韵尾仅 -m/-n/ⁿ/-ng/-p/-t/-c/-g/-h）
  - 稀有韵母：剥声母后的韵母在全库频次 <= 2（真韵母表紧凑，误读造一次性韵母）

R 栏（官话对音·拉丁转写）违类：
  - v- 声母（官话无 /v/；w/y 才是合法半元音起头）
  - 音系非法韵尾：-ng 允许；-p/-t/-k/-m 结尾（17c 官话 -m 已消亡，存疑类）单独计
  - 稀有韵母同上（R 栏单独频次表）

纪律：本扫查产出的是**裁决队列**而非错误清单——判死只能靠墨迹裁判。

可导入：run_sweep() 返回计数与命中清单（post_repair_verify.py 复扫复用）。
CLI 直接运行 = 全量扫查并写 SWEEP_PHONOTACTICS_{M,R}.json。
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

M2 = Path(__file__).resolve().parent.parent / "workspace_m2_dhs834"
VOW = "aeiouàáâãǎāèéêëěēìíîĩǐīòóôõǒōùúûũǔū"
VOW_RE = "[" + VOW + "]"

HARD_CLASSES = ("音系非法声母", "音系非法韵尾", "官话非法声母", "现代污染")
SOFT_CLASSES = ("稀有韵母", "官话存疑韵尾")


def strip_marks(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def tokenize(s: str):
    s = re.sub(r"\[[^\]]*\]|〔[^〕]*〕|⟨[^⟩]*⟩", " ", s or "")
    return re.findall(r"[A-Za-z" + VOW + "]+", s)


def rime_of(tok_lower_stripped: str) -> str:
    t = tok_lower_stripped
    for pre in ("qu", "gu", "ch", "ttz", "kh", "th", "ph", "chh", "ng", "gh"):
        if t.startswith(pre) and len(t) > len(pre) and t[len(pre)] in VOW:
            return t[len(pre):]
    m = re.match(r"^[bcdfghjklmnpqrstvxzw]+", t)
    return t[m.end():] if m else t


def check_modern(s_stripped: str):
    nfd = unicodedata.normalize("NFD", s_stripped)
    out = []
    if "\u030d" in nfd:
        out.append("现代污染:U+030D")
    if "\u207f" in nfd:
        out.append("现代污染:U+207F")
    if re.search(r"\b[kK]h?[aeiouyAEIOUY]", nfd):
        out.append("现代污染:k-/kh-声母")
    if re.search(r"\b([tT]sh?|[cC]hh)[aeiouyAEIOUY]", nfd):
        out.append("现代污染:ts-/tsh-/chh-声母")
    if re.search(r"[aeiouyAEIOUY][\u0300-\u036f]*k\b", nfd):
        out.append("现代污染:-k韵尾")
    return out


def run_sweep(pages=None, rare_max=2):
    """全库扫查。返回 dict：m_hits / r_hits / m_cls / r_cls / rare_rimes / hardTotal。"""
    if pages is None:
        man = json.loads((M2 / "BLIND_READ_MANIFEST.json").read_text(encoding="utf-8"))
        pages = sorted(int(k) for k in man.get("pages", {}))
    m_tokens_all = []
    r_tokens_all = []
    for pg in pages:
        d = json.loads((M2 / ("blind_read_p%04d.json" % pg)).read_text(encoding="utf-8")).get("entries", [])
        for e in d:
            for fld in ("source_M", "source_R"):
                for tok in tokenize(str(e.get(fld) or "")):
                    (m_tokens_all if fld == "source_M" else r_tokens_all).append(
                        (pg, e.get("position"), fld, tok))

    m_rime_freq = Counter(rime_of(strip_marks(t).lower()) for _, _, _, t in m_tokens_all)
    r_rime_freq = Counter(rime_of(strip_marks(t).lower()) for _, _, _, t in r_tokens_all)

    m_hits = []
    r_hits = []
    for pg, pos, fld, tok in m_tokens_all:
        stripped = strip_marks(tok).lower()
        rime = rime_of(stripped)
        msgs = list(check_modern(tok))
        if stripped and stripped[0] in "fvwx":
            msgs.append("音系非法声母:" + stripped[0])
        if stripped and stripped[-1] in "srbdfvjlzx":
            msgs.append("音系非法韵尾:-" + stripped[-1])
        if rime and m_rime_freq[rime] <= rare_max and len(rime) >= 2:
            msgs.append("稀有韵母:-%s(全库%d次)" % (rime, m_rime_freq[rime]))
        for msg in msgs:
            m_hits.append({"page": pg, "position": pos, "field": "M", "token": tok,
                           "class": msg, "context_v1": tok})
    for pg, pos, fld, tok in r_tokens_all:
        stripped = strip_marks(tok).lower()
        rime = rime_of(stripped)
        msgs = []
        if stripped and stripped[0] == "v":
            msgs.append("官话非法声母:v")
        if stripped and stripped[-1] in "ptkm":
            msgs.append("官话存疑韵尾:-" + stripped[-1])
        if rime and r_rime_freq[rime] <= rare_max and len(rime) >= 2:
            msgs.append("稀有韵母:-%s(全库%d次)" % (rime, r_rime_freq[rime]))
        for msg in msgs:
            r_hits.append({"page": pg, "position": pos, "field": "R", "token": tok,
                           "class": msg, "context_v1": tok})

    def dedup(hits):
        seen = {}
        for h in hits:
            seen[(h["page"], h["position"], h["field"], h["token"], h["class"])] = h
        return list(seen.values())

    m_hits = dedup(m_hits)
    r_hits = dedup(r_hits)
    m_cls = Counter(h["class"].split(":")[0].split("(")[0] for h in m_hits)
    r_cls = Counter(h["class"].split(":")[0].split("(")[0] for h in r_hits)
    rare_m = sorted([r for r, n in m_rime_freq.items() if n <= rare_max and len(r) >= 2])
    hard = sum(n for k, n in list(m_cls.items()) + list(r_cls.items())
               if k.startswith(HARD_CLASSES))
    return {"pages": pages, "m_hits": m_hits, "r_hits": r_hits, "m_cls": dict(m_cls),
            "r_cls": dict(r_cls), "rare_rimes_m": rare_m, "hardTotal": hard,
            "classCounts": {**m_cls, **r_cls}}


def main():
    res = run_sweep()
    cd = M2 / "collision_mr"
    cd.mkdir(exist_ok=True)
    (cd / "SWEEP_PHONOTACTICS_M.json").write_text(json.dumps(
        {"protocol": "SWEEP_PHONOTACTICS_M_V2", "classCounts": res["m_cls"],
         "rareRimes": res["rare_rimes_m"][:300], "hits": res["m_hits"]},
        ensure_ascii=False, indent=1), encoding="utf-8")
    (cd / "SWEEP_PHONOTACTICS_R.json").write_text(json.dumps(
        {"protocol": "SWEEP_PHONOTACTICS_R_V2", "classCounts": res["r_cls"],
         "hits": res["r_hits"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("M 栏命中:", len(res["m_hits"]), "处 | 分类:", res["m_cls"])
    print("R 栏命中:", len(res["r_hits"]), "处 | 分类:", res["r_cls"])
    print("硬违类合计（音系非法+现代污染）:", res["hardTotal"])
    print("M 稀有韵母:", len(res["rare_rimes_m"]), "个")


if __name__ == "__main__":
    main()
