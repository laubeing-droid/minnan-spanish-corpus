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

纪律：本扫查产出的是**裁决队列**而非错误清单——判死只能靠墨迹裁判（Gemini 已过校准）。
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

M2 = Path("literature/workspace_m2_dhs834")
MAN = json.loads((M2 / "BLIND_READ_MANIFEST.json").read_text(encoding="utf-8"))
PAGES = sorted(int(k) for k in MAN.get("pages", {}))

VOW = "aeiouàáâãǎāèéêëěēìíîĩǐīòóôõǒōùúûũǔū"
VOW_RE = "[" + VOW + "]"

def strip_marks(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def tokenize(s: str):
    # 剥编辑注记 [..] 〔..〕 ⟨..⟩ 后取字母 token（保留元音符以便韵母判定）
    s = re.sub(r"\[[^\]]*\]|〔[^〕]*〕|⟨[^⟩]*⟩", " ", s or "")
    return re.findall(r"[A-Za-z" + VOW + "ṽ?" + "]+", s)

def rime_of(tok_lower_stripped: str) -> str:
    # 剥声母簇：qu/gu（e,i,y 前）视为单一声母；ch/c/s/z/h/p/b/t/d/k/g/f/v/l/m/n/r/ng/x/w/j
    t = tok_lower_stripped
    for pre in ("qu", "gu", "ch", "ttz", "kh", "th", "ph", "chh", "ng", "gh"):
        if t.startswith(pre) and len(t) > len(pre) and t[len(pre)] in "aeiou" + "àáâãǎāèéêëěēìíîĩǐīòóôõǒōùúûũǔū":
            return t[len(pre):]
    m = re.match(r"^[bcdfghjklmnpqrstvxzw]+", t)
    return t[m.end():] if m else t

def check_modern(s_stripped: str):
    """沿用官方五条现代污染规则（has_modern_tailo_contamination 同口径）。"""
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

M_ILLEGAL_CODA = tuple("srbdfvjlzx")
M_ILLEGAL_ONSET = {"f", "v", "w", "x"}

m_rime_freq = Counter()
m_tokens_all = []  # (page, pos, token)
r_tokens_all = []

for pg in PAGES:
    d = json.loads((M2 / ("blind_read_p%04d.json" % pg)).read_text(encoding="utf-8")).get("entries", [])
    for e in d:
        for fld in ("source_M", "source_R"):
            for tok in tokenize(str(e.get(fld) or "")):
                (m_tokens_all if fld == "source_M" else r_tokens_all).append((pg, e.get("position"), fld, tok))

# 频次表（剥符+小写后）
m_freq = Counter(strip_marks(t).lower() for _, _, _, t in m_tokens_all)
r_freq = Counter(strip_marks(t).lower() for _, _, _, t in r_tokens_all)
m_rime_freq = Counter(rime_of(strip_marks(t).lower()) for _, _, _, t in m_tokens_all)
r_rime_freq = Counter(rime_of(strip_marks(t).lower()) for _, _, _, t in r_tokens_all)

RARE = 2
m_hits = []
r_hits = []
for pg, pos, fld, tok in m_tokens_all:
    stripped = strip_marks(tok).lower()
    rime = rime_of(stripped)
    onset = stripped[: max(0, len(stripped) - len(rime))] or "(零)"
    msgs = []
    if onset and onset[0] in M_ILLEGAL_ONSET:
        msgs.append("音系非法声母:" + onset[0])
    msgs += check_modern(tok)
    if stripped.endswith(M_ILLEGAL_CODA):
        msgs.append("音系非法韵尾:-" + stripped[-1])
    if rime and m_rime_freq[rime] <= RARE and len(rime) >= 2 and stripped not in ("[空]", "[残]"):
        msgs.append("稀有韵母:-%s(全库%d次)" % (rime, m_rime_freq[rime]))
    for msg in msgs:
        m_hits.append({"page": pg, "position": pos, "field": "M", "token": tok,
                       "class": msg, "context_v1": tok})

for pg, pos, fld, tok in r_tokens_all:
    stripped = strip_marks(tok).lower()
    rime = rime_of(stripped)
    onset = stripped[: max(0, len(stripped) - len(rime))] or "(零)"
    msgs = []
    if onset and onset[0] == "v":
        msgs.append("官话非法声母:v")
    if stripped.endswith(("p", "t", "k", "m")):
        msgs.append("官话存疑韵尾:-" + stripped[-1])
    if rime and r_rime_freq[rime] <= RARE and len(rime) >= 2:
        msgs.append("稀有韵母:-%s(全库%d次)" % (rime, r_rime_freq[rime]))
    for msg in msgs:
        r_hits.append({"page": pg, "position": pos, "field": "R", "token": tok,
                       "class": msg, "context_v1": tok})

# 去重（同页同条同 token 同类）
def dedup(hits):
    seen = {}
    for h in hits:
        key = (h["page"], h["position"], h["field"], h["token"], h["class"])
        seen[key] = h
    return list(seen.values())

m_hits = dedup(m_hits)
r_hits = dedup(r_hits)

m_cls = Counter(h["class"].split(":")[0].split("(")[0] for h in m_hits)
r_cls = Counter(h["class"].split(":")[0].split("(")[0] for h in r_hits)
rare_rimes_m = sorted([r for r, n in m_rime_freq.items() if n <= RARE and len(r) >= 2])

(CD := M2 / "collision_mr").mkdir(exist_ok=True)
(CD / "SWEEP_PHONOTACTICS_M.json").write_text(json.dumps(
    {"protocol": "SWEEP_PHONOTACTICS_M_V2", "classCounts": dict(m_cls),
     "rareRimes": rare_rimes_m[:300], "hits": m_hits}, ensure_ascii=False, indent=1), encoding="utf-8")
(CD / "SWEEP_PHONOTACTICS_R.json").write_text(json.dumps(
    {"protocol": "SWEEP_PHONOTACTICS_R_V2", "classCounts": dict(r_cls),
     "hits": r_hits}, ensure_ascii=False, indent=1), encoding="utf-8")

print("M 栏命中:", len(m_hits), "处 | 分类:", dict(m_cls))
print("M 稀有韵母（全库<=2次）:", len(rare_rimes_m), "个 ->", rare_rimes_m[:40])
print("R 栏命中:", len(r_hits), "处 | 分类:", dict(r_cls))
print("--- M 样本 15:")
for h in m_hits[:15]:
    print("  p%04d pos%s %r [%s]" % (h["page"], h["position"], h["token"], h["class"]))
print("--- R 样本 10:")
for h in r_hits[:10]:
    print("  p%04d pos%s %r [%s]" % (h["page"], h["position"], h["token"], h["class"]))
