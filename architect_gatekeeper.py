"""
CHIEF ARCHITECT IMMUTABLE GATEKEEPER (architect_gatekeeper.py)
==============================================================
STRICTLY FORBIDDEN TO EDIT OR MODIFY THIS FILE — except through the architect-ratified
amendment protocol in docs/GATE_AMENDMENT_PROTOCOL.md (versioned, tested, changelogged).

Version history:
  v1.0 (initial) — M1 batch/master checks; M2 seal/tone/orthography checks.
  v1.1 (2026-11-12, architect directive) — NEW coverage invariant: union(M2 sealed pages,
       M1 layer_0_visual_anchor.page_pdf anchors) must cover PDF 0030-1140 minus registered
       non-lexicographic pages. Motivated by LESSONS L3/L20 (140-page phantom-gap audit) and
       the 0621-0630 silent page-drop risk. Monotonic tightening only: no existing check was
       removed or loosened; regression on the current corpus passes (937 M2 seals ∪ 306 M1
       page anchors = 1103/1103 expected pages).

Enforces 100% genuine entry-by-entry philological curation across all 14 M1 batches
(656 entries) + 5,762 master merge, and M2 visual blind readings.
"""

import json
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

M1_DIR = Path("literature/workspace_m1_dhs306")
M2_DIR = Path("literature/workspace_m2_dhs834")
TILES_DIR = Path("literature/tiles/01_DHS")

BATCH_SPECS = [
    ("batch_01_m1_disambiguated_50.json", 50),
    ("batch_02_m1_disambiguated_50.json", 50),
    ("batch_03_m1_disambiguated_50.json", 50),
    ("batch_04_m1_disambiguated_50.json", 50),
    ("batch_05_m1_disambiguated_50.json", 50),
    ("batch_06_m1_disambiguated_50.json", 50),
    ("batch_07_m1_disambiguated_50.json", 50),
    ("batch_08_m1_disambiguated_50.json", 50),
    ("batch_09_m1_disambiguated_50.json", 50),
    ("batch_10_m1_disambiguated_50.json", 50),
    ("batch_11_m1_disambiguated_50.json", 50),
    ("batch_12_m1_disambiguated_50.json", 50),
    ("batch_13_m1_disambiguated_50.json", 50),
    ("batch_14_m1_disambiguated_06.json", 6),
]

FORBIDDEN_LATIN_ACCENTS = re.compile(r"[áéíóúàèìòùâêîôûǎěǐǒǔāēīōūᶜ]")
FORBIDDEN_GLOSS_SUBSTRINGS = [
    "未展開",
    "unexpanded",
    "依手稿四欄對讀",
    "語境釋義未定",
    "Disambiguated via cross-column",
    "暫不細定",
    "未定字",
    "left unresolved",
    # Anti-regex-replacement bans (caught in build_all_certified_batches_07_to_14.py):
    "對應西文",
    "Corresponds to Spanish",
    "已完整考定",
    "fully expanded",
    "已考定",
    "fully resolved",
    "經手稿四欄對讀",
    "經上下文考定",
    "Authenticated via cross-column",
    "考訂字",
]
FORBIDDEN_NOTES_SUBSTRINGS = [
    "Disambiguated from DHS folio",
    "Collated from DHS original diacritics",
    "collated with Minnan colloquial register",
]
FORBIDDEN_BASIS_SUBSTRINGS = [
    "17th-c. Chiang-chiu / Manila Sangley manuscript phonology",
    "17th-century Zhangzhou dialect phonology preserving historic initial",
]
FORBIDDEN_WRONG_TONE_LABELS = [
    "T01 (尖角)",
    "T02 (銳角)",
    "T03 (鈍角)",
    "T05 (反折)",
    "T06 (平橫)",
]


def fail(msg: str):
    print(f"\n[ARCHITECT GATE FAILED] {msg}")
    sys.exit(1)


def check_m1():
    q_path = M1_DIR / "l_layer_gaps_queue.json"
    if not q_path.exists():
        fail("Missing l_layer_gaps_queue.json")
    queue = json.loads(q_path.read_text(encoding="utf-8"))["queue_entries"]
    if len(queue) != 656:
        fail(f"Expected 656 queue entries, got {len(queue)}")

    all_entries = []
    notes_counter = Counter()
    basis_counter = Counter()
    tl_counter = Counter()
    rec_counter = Counter()

    for fname, exp_len in BATCH_SPECS:
        fpath = M1_DIR / fname
        if not fpath.exists():
            fail(f"Missing {fname}")
        data = json.loads(fpath.read_text(encoding="utf-8"))
        entries = data.get("entries", [])
        if len(entries) != exp_len:
            fail(f"{fname}: expected {exp_len} entries, got {len(entries)}")

        for idx_in_batch, e in enumerate(entries):
            global_idx = len(all_entries) + idx_in_batch + 1
            eid = e.get("entry_id", "")
            q_id = queue[global_idx - 1]["id"]
            if eid != q_id:
                fail(f"{fname} item {idx_in_batch} ID '{eid}' != queue ID '{q_id}'")

            raw = e.get("layer_1_diplomatic_raw", {})
            sm = (raw.get("source_M") or "").strip()
            sh = (raw.get("source_H") or "").strip()

            tl = (e.get("layer_4_modern_tai_lo", {}).get("tai_lo_standard") or "").strip()
            has_content = (sm and sm not in ["〔空〕", "[空]"]) or (sh and sh not in ["〔空〕", "[空]"])
            if has_content and not tl:
                fail(f"{fname} entry #{global_idx} ({eid}) has empty tai_lo_standard!")

            # Ban dummy "tsu" / "tsu-tsu" / "tsu-tsu-tsu" fallback
            if re.fullmatch(r"tsu(-tsu)*", tl.lower()):
                fail(f"{fname} entry #{global_idx} ({eid}) uses fake fallback tai_lo_standard='{tl}' for source_H='{sh}' / source_M='{sm}'!")
            if tl:
                tl_counter[tl] += 1

            rec = (e.get("layer_3_historical_phonology", {}).get("reconstructed_17th_c_hokkien") or "").strip()
            if has_content and not rec:
                fail(f"{fname} entry #{global_idx} ({eid}) has empty reconstructed_17th_c_hokkien!")
            if re.fullmatch(r"tsu¹(\s+tsu¹)*", rec.lower()):
                fail(f"{fname} entry #{global_idx} ({eid}) uses fake fallback IPA='{rec}' for source_H='{sh}' / source_M='{sm}'!")
            if rec:
                rec_counter[rec] += 1
                m = FORBIDDEN_LATIN_ACCENTS.search(rec)
                if m:
                    fail(f"{fname} entry #{global_idx} ({eid}) has Latin accent '{m.group(0)}' in IPA: {rec}")

            basis = (e.get("layer_3_historical_phonology", {}).get("phonological_basis") or "").strip()
            if not basis:
                fail(f"{fname} entry #{global_idx} ({eid}) has empty phonological_basis!")
            for bad_b in FORBIDDEN_BASIS_SUBSTRINGS:
                if bad_b in basis:
                    fail(f"{fname} entry #{global_idx} ({eid}) uses template phonological_basis: '{basis}'")
            basis_counter[basis] += 1

            l2 = e.get("layer_2_disambiguation", {})
            zh = (l2.get("zh_disambiguated") or "").strip()
            en = (l2.get("en_disambiguated") or "").strip()
            notes = (l2.get("syntactic_notes") or "").strip()
            if not zh or not en:
                fail(f"{fname} entry #{global_idx} ({eid}) has empty zh or en disambiguation!")
            for bad in FORBIDDEN_GLOSS_SUBSTRINGS:
                if bad in zh or bad in en:
                    fail(f"{fname} entry #{global_idx} ({eid}) contains forbidden/fake substring '{bad}' in zh/en: zh='{zh}' | en='{en}'")
            for bad in FORBIDDEN_NOTES_SUBSTRINGS:
                if bad in notes:
                    fail(f"{fname} entry #{global_idx} ({eid}) contains template syntactic_notes: '{notes}'")
            notes_counter[notes] += 1

        all_entries.extend(entries)

    # Anti-loop check: no single syntactic_notes, phonological_basis, tai_lo_standard, or IPA may repeat abnormally
    most_common_note, note_cnt = notes_counter.most_common(1)[0]
    if note_cnt > 5:
        fail(f"Template syntactic_notes repeated {note_cnt} times: '{most_common_note}'")
    most_common_basis, basis_cnt = basis_counter.most_common(1)[0]
    if basis_cnt > 5:
        fail(f"Template phonological_basis repeated {basis_cnt} times: '{most_common_basis}'")
    most_common_tl, tl_cnt = tl_counter.most_common(1)[0]
    if tl_cnt > 6:
        fail(f"Fallback tai_lo_standard '{most_common_tl}' repeated {tl_cnt} times across corpus!")
    most_common_rec, rec_cnt = rec_counter.most_common(1)[0]
    if rec_cnt > 6:
        fail(f"Fallback IPA '{most_common_rec}' repeated {rec_cnt} times across corpus!")

    master_m1 = M1_DIR / "DHS_p0835_1140_M1_FULL_5762.json"
    if not master_m1.exists():
        fail("Missing merged master corpus DHS_p0835_1140_M1_FULL_5762.json (must merge 5,106 Core + 656 Disambiguated = 5,762 total positions)")
    m_data = json.loads(master_m1.read_text(encoding="utf-8"))
    m_entries = m_data.get("entries", [])
    if len(m_entries) != 5762:
        fail(f"DHS_p0835_1140_M1_FULL_5762.json expected 5762 entries, got {len(m_entries)}")

    print("[PASS] M1 100% COMPLETE: All 656 disambiguated entries (batch_01..14) + 5,762 master corpus verified!")


def check_m2():
    manifest_path = M2_DIR / "BLIND_READ_MANIFEST.json"
    if not manifest_path.exists():
        fail("Missing BLIND_READ_MANIFEST.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pages_man = manifest.get("pages", {})

    verified_count = 0
    for pkey, info in sorted(pages_man.items()):
        bf_path = M2_DIR / f"blind_read_p{pkey}.json"
        if not bf_path.exists():
            fail(f"Missing {bf_path}")
        raw_bytes = bf_path.read_bytes()
        real_sha = hashlib.sha256(raw_bytes).hexdigest()
        man_sha = info.get("blind_first_read_sha256") or info.get("sha256")
        if real_sha != man_sha:
            fail(f"SHA-256 mismatch for page {pkey}: file={real_sha} vs manifest={man_sha}")
        raw_text = raw_bytes.decode("utf-8")
        for wrong_lbl in FORBIDDEN_WRONG_TONE_LABELS:
            if wrong_lbl in raw_text:
                fail(f"Page {pkey} contains non-standard tone code '{wrong_lbl}' (must use T01=升斜, T02=降斜, T03=尖頂帽, T04=凹角, T05=平橫, T06/T07=入聲)!")

        # Check 17th-century Spanish-Dominican orthography purity in source_M
        page_doc = json.loads(raw_text)
        entries = page_doc.get("entries", [])
        if len(entries) < 3 and int(pkey) not in (31, 32):
            fail(f"Page {pkey} has abnormally few entries ({len(entries)})!")
        for e in entries:
            sm = (e.get("source_M") or "").strip()
            raw_latin = re.sub(r"\[[^\]]*\]|〔[^〕]*〕|⟨[^⟩]*⟩", " ", sm)
            if "\u030d" in raw_latin or "\u207f" in raw_latin:
                fail(f"Page {pkey} pos {e.get('position')} contains modern POJ/Tâi-lô diacritic (U+030D or U+207F) in source_M: '{sm}'")
            if re.search(r"\b[kK]h?[aeiouyAEIOUYáéíóúàèìòùâêîôûǎěǐǒǔāēīōū]", raw_latin):
                fail(f"Page {pkey} pos {e.get('position')} contains modern k-/kh- initial in 17c source_M (must use c-/qu-): '{sm}'")
            if re.search(r"\b([tT]sh?|[cC]hh)[aeiouyAEIOUYáéíóúàèìòùâêîôûǎěǐǒǔāēīōū]", raw_latin):
                fail(f"Page {pkey} pos {e.get('position')} contains modern ts-/tsh-/chh- initial in 17c source_M (must use ch-): '{sm}'")

        verified_count += 1

    # ---- v1.1 coverage invariant (GATE_AMENDMENT_PROTOCOL.md v1.1) ----
    # union(M2 sealed pages, M1 layer_0.page_pdf anchors) must cover 0030-1140
    # minus registered non-lexicographic pages.
    try:
        m1_doc = json.loads((M1_DIR / "DHS_p0835_1140_M1_FULL_5762.json").read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Coverage invariant v1.1 cannot read M1 master: {exc}")
    m1_pages = set()
    for entry in m1_doc.get("entries", []):
        anchor = entry.get("layer_0_visual_anchor") or {}
        page_pdf = anchor.get("page_pdf")
        if page_pdf:
            m1_pages.add(int(page_pdf))
    excluded_pages = set()
    nlex_path = M2_DIR / "non_lexicographic_pages.json"
    if nlex_path.exists():
        nlex = json.loads(nlex_path.read_text(encoding="utf-8"))
        excluded_pages = {int(k) for k in nlex.get("pages", {})}
    expected = set(range(30, 1141)) - excluded_pages
    covered = {int(k) for k in pages_man} | m1_pages
    missing_pages = sorted(expected - covered)
    if missing_pages:
        fail(
            f"Coverage invariant v1.1: {len(missing_pages)} pages in 0030-1140 are neither "
            f"M2-sealed nor anchored in the M1 master: {missing_pages[:20]}"
        )

    print(f"[PASS] M2 Gate: {verified_count} blind-read pages verified with unified tone codes and SHA-256!")
    print(f"[PASS] Coverage invariant v1.1: 0030-1140 fully accounted "
          f"({len(covered & expected)}/{len(expected)} pages via M2 seals union M1 anchors)")


if __name__ == "__main__":
    check_m1()
    check_m2()
