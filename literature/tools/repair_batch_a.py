#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按冻结队列裁决生成修复 raw：--pages 0041,0042，单批最多 20 页。

输出独立批次账；重封使用 seal_and_verify.py --source <批次账>。
封存件是比较基准；不覆盖已有未封存 raw，不修改封存件或队列。
"""
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from hokkien_17c_converter import sanitize_17c_missionary_orthography

M2 = Path("literature/workspace_m2_dhs834")
CD = M2 / "collision_mr"
ADK = CD / "adk"
RAW = M2 / "raw_blind"
FREEZE = Path("codex_M1_adk_queue_freeze.json")
LEDGER = CD / "ADK_ADJUDICATION_LEDGER.json"
ALLOWED = {"T00 (無標號)", "T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)", "T04 (凹角)",
           "T05 (平橫)", "T06/T07 (交叉入聲號)", "T99 (污損難辨)"}
FIELDS = ("source_L", "source_H", "source_M", "source_R", "tone_marks_M", "tone_marks_R")
FIELD_MAP = {"M": "source_M", "R": "source_R", "source_M": "source_M", "source_R": "source_R"}


def soup(s):
    s = unicodedata.normalize("NFD", s or "").replace("ⁿ", "n")
    return "".join(c for c in s.lower() if (c.isascii() and c.isalnum()) or
                   unicodedata.name(c, "").startswith("LATIN "))


def soup_with_modifiers(s):
    s = unicodedata.normalize("NFD", s or "").lower()
    return "".join(c if unicodedata.category(c) == "Lm" or
                   unicodedata.name(c, "").startswith("COMBINING LATIN") else soup(c) for c in s)


def identity(row):
    if not isinstance(row, dict) or type(row.get("position")) is not int:
        return None
    if not all(isinstance(row.get(k), str) for k in ("field", "v1", "rr")):
        return None
    return (row["position"], row["field"], row["v1"], row["rr"])


def verify_frozen(frozen):
    records = {row["path"]: row for row in frozen["files"]}
    queues = {path.as_posix(): path for path in ADK.glob("adk_p*.json")}
    if (len(records) != len(frozen["files"]) or len(queues) != frozen["queue_count"] or
            set(queues) != set(records)):
        raise SystemExit("冻结队列页集或数量不匹配，未修改任何 raw")
    for name, path in queues.items():
        data = path.read_bytes()
        record = records[name]
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise SystemExit(f"冻结队列不匹配：{path.name}，未修改任何 raw")
    return records


def by_position(entries):
    result = {e["position"]: e for e in entries}
    if len(result) != len(entries):
        raise ValueError("条目 position 重复")
    return result


def same_entries(sealed, raw):
    a, b = by_position(sealed), by_position(raw)
    if a.keys() != b.keys():
        return False
    return all((a[p].get(f) or ([] if f.startswith("tone_marks_") else "")) ==
               (b[p].get(f) or ([] if f.startswith("tone_marks_") else ""))
               for p in a for f in FIELDS)


def nonstandard_tones(entries):
    return any(str(t).strip() not in ALLOWED for e in entries
               for f in ("tone_marks_M", "tone_marks_R") for t in (e.get(f) or []))


def tone_disposition(v):
    """判读回执的声调处置声明；返回 (处置码, 新数组, 核查依据, 失败原因)。

    口径（2026-11-19 用户批准，宽松版+置信度门槛）：每条 source_M/source_R
    修复落地前，回执必须提供三者之一——原图核定的新数组（tone_marks_new）、
    明确不变确认（tone_marks_unchanged=true）、或联网核查依据（tone_basis，
    ≥2 个可核查来源一致支持）；三者缺一即延迟待核，不以程序推断放行。
    """
    codes = v.get("tone_marks_new")
    if codes is not None:
        if not isinstance(codes, list) or not codes or any(t not in ALLOWED for t in codes):
            return None, None, None, "声调新数组无效（代码不在 T00–T99 允许清单）；待核"
        return "confirmed_new", codes, None, None
    if v.get("tone_marks_unchanged") is True:
        return "confirmed_unchanged", None, None, None
    basis = v.get("tone_basis")
    if isinstance(basis, str) and basis.strip():
        return "released_with_basis", None, basis.strip(), None
    return None, None, None, "声调处置未记录（原图新数组/不变确认/核查依据三者缺一）；待核"


def illegal_initial(ink, field):
    text = unicodedata.normalize("NFD", ink).lower()
    text = "".join(c for c in text if not unicodedata.combining(c))
    syllables = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)
    forbidden = "fvwx" if field == "source_M" else "v"
    return any(s[0] in forbidden for s in syllables)


def single_latin_word(text):
    text = unicodedata.normalize("NFD", text)
    return bool(text) and all(
        c == "ⁿ" or (c.isascii() and c.isalpha()) or
        unicodedata.name(c, "").startswith("LATIN ") or unicodedata.category(c).startswith("M")
        for c in text
    ) and not unicodedata.category(text[0]).startswith("M")


def token_offset(text, token):
    if not single_latin_word(token):
        return None, "任务 v1 非单个拉丁词段"
    pos = text.find(token)
    if pos < 0:
        return None, "封存件现值与任务 v1 漂移；不覆盖后续修正"
    if text.find(token, pos + 1) >= 0:
        return None, "任务 v1 在封存栏内出现多次"
    def joined(c):
        return c.isalnum() or unicodedata.category(c).startswith("M") or c in "_-'’ʼ‐‑‒–—\u200c\u200d"
    end = pos + len(token)
    if (pos and joined(text[pos - 1])) or (end < len(text) and joined(text[end])):
        return None, "任务 v1 嵌套或词边界不清"
    for left, right in (("[", "]"), ("〔", "〕"), ("⟨", "⟩")):
        if text.rfind(left, 0, pos) > text.rfind(right, 0, pos):
            return None, "任务 v1 位于未决标注内"
    return pos, ""


def main():
    parser = argparse.ArgumentParser(description="按冻结判决分批生成 raw；不直接修改封存件")
    parser.add_argument("--pages", required=True, help="逗号分隔 PDF 页码，最多 20 页")
    args = parser.parse_args()
    try:
        pages = sorted({int(x.strip()) for x in args.pages.split(",")})
    except ValueError:
        parser.error("--pages 必须是逗号分隔的整数")
    if not pages or len(pages) > 20 or any(p < 30 or p > 1140 for p in pages):
        parser.error("--pages 需为 0030–1140 内最多 20 页")

    frozen = json.loads(FREEZE.read_text(encoding="utf-8"))
    manifests = verify_frozen(frozen)
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger.get("protocol") != "ADK_ADJUDICATION_LEDGER_V1" or not isinstance(ledger.get("rows"), list):
        raise SystemExit("先运行收集器生成完整裁决账；未修改任何 raw")
    selected_rows = defaultdict(list)
    for row in ledger["rows"]:
        if row.get("page") in pages:
            selected_rows[row["page"]].append(row)
    queues = {}
    missing = []
    for pg in pages:
        pk = f"{pg:04d}"
        q = ADK / f"adk_p{pk}.json"
        vf = ADK / f"adk_verdict_p{pk}.json"
        if not q.exists():
            missing.append({"page": pg, "reason": "缺任务文件"})
            continue
        record = manifests.get(q.as_posix())
        data = q.read_bytes()
        if not record or len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise SystemExit(f"冻结队列不匹配：p{pk}，未修改任何 raw")
        queue = json.loads(data.decode("utf-8"))
        if queue.get("page") != pg or not isinstance(queue.get("items"), list):
            raise SystemExit(f"冻结队列格式错误：p{pk}，未修改任何 raw")
        if not vf.exists():
            missing.append({"page": pg, "reason": "缺判决文件"})
            continue
        queues[pg] = (queue["items"], vf)

    applied, deferred, batch_b_rows, problems = [], [], [], []
    dirty = {}
    skipped = Counter()
    illegal_by_page = Counter()
    visited = []
    for pg, (items, vf) in queues.items():
        visited.append(pg)
        pk = f"{pg:04d}"
        try:
            receipt = json.loads(vf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append({"page": pg, "reason": f"判决 JSON 错误：{exc.msg}"})
            continue
        if not isinstance(receipt, dict) or receipt.get("page") != pg or not isinstance(receipt.get("verdicts"), list):
            problems.append({"page": pg, "reason": "判决格式或页码错误"})
            continue
        verdicts = receipt["verdicts"]
        item_keys = [identity(it) for it in items]
        verdict_keys = [identity(v) for v in verdicts]
        item_count = Counter(k for k in item_keys if k is not None)
        verdict_count = Counter(k for k in verdict_keys if k is not None)
        item_values = Counter(k[1:] for k in item_keys if k is not None)
        verdict_values = Counter(k[1:] for k in verdict_keys if k is not None)
        item_targets = Counter((it["position"], FIELD_MAP.get(it["field"], it["field"])) for it in items
                               if isinstance(it, dict) and type(it.get("position")) is int and
                               isinstance(it.get("field"), str))
        collected_targets = Counter((r.get("position"), FIELD_MAP.get(r.get("field"), r.get("field")))
                                    for r in selected_rows[pg])
        if not selected_rows[pg]:
            continue

        sealed = json.loads((M2 / f"blind_read_p{pk}.json").read_text(encoding="utf-8"))
        entries = sealed["entries"]
        raw_path = RAW / f"raw_part_p{pk}.json"
        if raw_path.exists():
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw_pages = raw.get("pages", [])
            if len(raw_pages) != 1 or raw_pages[0].get("pdf_page") != pg:
                problems.append({"page": pg, "reason": "现有 raw 页结构不匹配；未覆盖"})
                continue
            raw_page = raw_pages[0]
        else:
            raw_page = {k: sealed.get(k, "") for k in
                        ("historical_folio", "page_header", "page_footer_printed", "page_footer_handwritten")}
            raw_page["pdf_page"] = pg
            if "layout_mode" in sealed:
                raw_page["layout_mode"] = sealed["layout_mode"]
            raw_page["entries"] = json.loads(json.dumps(entries, ensure_ascii=False))
            raw = {"pages": [raw_page]}
        try:
            raw_entries = raw_page["entries"]
            sealed_pos, raw_pos = by_position(entries), by_position(raw_entries)
            raw_matches = same_entries(entries, raw_entries)
        except (KeyError, TypeError, ValueError):
            problems.append({"page": pg, "reason": "条目结构或 position 无效；未覆盖 raw"})
            continue
        tone_problem = nonstandard_tones(entries) or nonstandard_tones(raw_entries)

        def matched_receipt(collected):
            key = identity(collected)
            source = collected.get("receipt") or {}
            index = source.get("index")
            if (key is None or source.get("file") != vf.as_posix() or type(index) is not int or
                    not 1 <= index <= len(verdicts)):
                return None
            v = verdicts[index - 1]
            vkey = identity(v)
            match = source.get("match")
            exact = (match == "position_and_values" and vkey == key and
                     item_count[key] == 1 and verdict_count[key] == 1)
            fallback = (match == "unique_values" and vkey is not None and vkey[1:] == key[1:] and
                        item_values[key[1:]] == 1 and verdict_values[key[1:]] == 1 and
                        item_count[key] == 1)
            if not (exact or fallback) or v.get("verdict") != collected.get("verdict") or v.get("ink") != collected.get("ink"):
                return None
            return key, source, v, match

        groups = defaultdict(list)
        for r in selected_rows[pg]:
            groups[(r.get("position"), FIELD_MAP.get(r.get("field"), r.get("field")))].append(r)
        merged = {}
        if pg not in range(30, 41) and raw_matches and not tone_problem and all(k is not None for k in item_keys):
            for target, group in groups.items():
                pos, fld = target
                if (len(group) < 2 or item_targets[target] != len(group) or
                        pos not in sealed_pos or pos not in raw_pos or fld not in ("source_M", "source_R") or
                        fld not in sealed_pos[pos] or fld not in raw_pos[pos]):
                    continue
                old = str(sealed_pos[pos].get(fld) or "")
                matches = [matched_receipt(r) for r in group]
                if any(m is None for m in matches) or any(r.get("v1") != old for r in group):
                    continue
                if len({m[1]["index"] for m in matches}) != len(group):
                    continue
                choices = []
                for r, m in zip(group, matches):
                    v = m[2]
                    ink = v.get("ink")
                    if ink is not None and not isinstance(ink, str):
                        break
                    ink = (ink or "").strip()
                    if v.get("verdict") == "重读对":
                        rr = r["rr"].strip()
                        if ink and ink != rr:
                            break
                        ink = ink or rr
                    elif v.get("verdict") != "两皆误":
                        break
                    if not ink or "[" in ink or "]" in ink:
                        break
                    choices.append(ink)
                if len(choices) == len(group) and len(set(choices)) == 1 and soup(old) != soup(choices[0]):
                    merged[target] = group

        for collected in selected_rows[pg]:
            row = {k: collected.get(k) for k in ("page", "position", "field", "v1", "rr", "verdict", "ink")}
            matched = matched_receipt(collected)
            if matched is None:
                deferred.append({**row, "reason": "收集器回执与冻结任务不匹配或匹配不唯一"})
                continue
            key, source, v, match = matched
            pos, task_field, vd = key[0], key[1], v.get("verdict")
            fld = FIELD_MAP.get(task_field)
            if fld is None:
                deferred.append({**row, "reason": "字段非 source_M/source_R"})
                continue
            group = merged.get((pos, fld))
            if group and collected is not group[0]:
                continue
            if (item_targets[(pos, fld)] != 1 or collected_targets[(pos, fld)] != 1) and not group:
                deferred.append({**row, "reason": "任务或收集账目标重复"})
                continue
            if vd in ("V1对", "等价", "墨迹不明"):
                skipped[vd] += 1
                continue
            if v.get("ink") is not None and not isinstance(v.get("ink"), str):
                deferred.append({**row, "reason": "回执 ink 类型无效"})
                continue
            ink = str(v.get("ink") or "").strip()
            if vd == "重读对":
                if ink and (soup(ink) != soup(row["rr"]) or
                            soup_with_modifiers(ink) != soup_with_modifiers(row["rr"])):
                    deferred.append({**row, "receipt": source, "reason": "重读对的 ink 与 rr 字母不一致"})
                    continue
                ink_source = "ink" if ink else "rr"
                ink = ink or row["rr"].strip()
                if not ink:
                    deferred.append({**row, "reason": "重读对缺少可用 rr"})
                    continue
            elif vd == "两皆误" and ink:
                ink_source = "ink"
            else:
                deferred.append({**row, "reason": "无效判决或两皆误缺少 ink"})
                continue
            row["ink"] = ink
            if pg in range(30, 41):
                batch_b_rows.append(row)
                continue
            if tone_problem:
                deferred.append({**row, "reason": "本页含存量非规范调标；未覆盖 raw"})
                continue
            if not raw_matches:
                deferred.append({**row, "reason": "现有 raw 与封存件不一致；未覆盖未封存工作"})
                continue
            if (pos not in sealed_pos or pos not in raw_pos or fld not in sealed_pos[pos] or
                    fld not in raw_pos[pos]):
                deferred.append({**row, "reason": "封存件或 raw 缺少目标 position"})
                continue
            old = str(sealed_pos[pos].get(fld) or "")
            if old == row["v1"] and soup(old) == soup(ink):
                if soup_with_modifiers(old) != soup_with_modifiers(ink):
                    deferred.append({**row, "receipt": source, "reason": "上置或修饰字母差异；字母汤忽略，待核"})
                else:
                    skipped["字母汤等价"] += 1
                continue
            token_change = None
            if old != row["v1"]:
                context = json.dumps({"note": v.get("note"), "evidence": v.get("evidence"),
                                      "collected_note": collected.get("note"), "receipt": source.get("metadata")},
                                     ensure_ascii=False)
                if re.search(r"跨\s*[栏列线]|分栏|栏界|西语|西班牙|注释|旁注|cross[\s_-]*(column|line)",
                             context, re.IGNORECASE):
                    deferred.append({**row, "reason": "跨栏或注释归属存疑；不替换词段"})
                    continue
                if group or item_targets[(pos, fld)] != 1 or collected_targets[(pos, fld)] != 1:
                    deferred.append({**row, "reason": "词段目标存在其他任务"})
                    continue
                if not single_latin_word(ink):
                    deferred.append({**row, "reason": "候选 ink 非单个拉丁词段"})
                    continue
                offset, reason = token_offset(old, row["v1"])
                if offset is None:
                    deferred.append({**row, "reason": reason})
                    continue
                if soup(row["v1"]) == soup(ink):
                    if soup_with_modifiers(row["v1"]) != soup_with_modifiers(ink):
                        deferred.append({**row, "receipt": source, "reason": "上置或修饰字母差异；字母汤忽略，待核"})
                    else:
                        skipped["字母汤等价"] += 1
                    continue
                token_change = {"old_token": row["v1"], "new_token": ink, "offset": offset,
                                "offset_unit": "unicode_codepoint",
                                "byte_offset": len(old[:offset].encode("utf-8"))}
            if illegal_initial(ink, fld):
                for r in (group or [collected]):
                    illegal_by_page[pg] += 1
                    deferred.append({**{k: r.get(k) for k in ("page", "position", "field", "v1", "rr", "verdict", "ink")},
                                     "receipt": r.get("receipt"), "reason": "音系门禁：至少一个音节声母需人工复核"})
                if illegal_by_page[pg] > 100:
                    break
                continue
            new = (old[:token_change["offset"]] + ink + old[token_change["offset"] + len(row["v1"]):]
                   if token_change else ink)
            if fld == "source_M":
                prepared = sanitize_17c_missionary_orthography(new.strip(), str(sealed_pos[pos].get("source_H") or "").strip())
                if unicodedata.normalize("NFC", prepared) != unicodedata.normalize("NFC", new.strip()):
                    for original in (group or [collected]):
                        deferred.append({**{k: original.get(k) for k in ("page", "position", "field", "v1", "rr", "verdict", "ink")},
                                         "receipt": original.get("receipt"), "reason": "重封净化会改写字面音写；待核"})
                    continue
            check, new_tones, tone_basis, tone_reason = tone_disposition(v)
            if check is None:
                deferred.append({**row, "receipt": source, "reason": tone_reason})
                continue
            tone_field = "tone_marks_" + fld[-1]
            old_tones = sealed_pos[pos].get(tone_field) or []
            raw_pos[pos][fld] = new
            if new_tones is not None:
                raw_pos[pos][tone_field] = new_tones
            dirty[pg] = (raw_path, raw)
            applied.append({"page": pg, "position": pos, "field": fld, "old": old, "new": new,
                            "task_field": task_field, "verdict": vd, "ink_source": ink_source, "queue_v1": row["v1"],
                            "queue_rr": row["rr"], "receipt": source, "match": match,
                            "tone_check": check, "tone_marks_old": old_tones,
                            **({"tone_marks_new": new_tones} if new_tones is not None else {}),
                            **({"tone_basis": tone_basis} if tone_basis else {}),
                            **(token_change or {}),
                            **({"merged_receipts": [{k: r.get(k) for k in
                                 ("position", "field", "v1", "rr", "verdict", "ink", "receipt")} for r in group]}
                               if group else {})})
        if illegal_by_page[pg] > 100:
            break

    upgrades = [{"page": p, "phonotacticDeferred": n} for p, n in sorted(illegal_by_page.items()) if n > 100]
    planned = applied
    verify_frozen(frozen)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out_path = CD / f"REPAIR_BATCH_A_{pages[0]:04d}_{pages[-1]:04d}_{stamp}.json"
    out = {"protocol": "REPAIR_BATCH_A_V4", "selectedPages": pages,
           "status": "BLOCKED_PHONOTACTIC_DEFERRED" if upgrades else "PENDING_RAW_WRITE",
           "appliedCount": 0, "pagesTouched": 0, "dirtyPages": [],
           "deferredCount": len(deferred), "deferred": deferred,
           "phonotacticDeferredByPage": dict(illegal_by_page), "upgrade": upgrades,
           "missingPages": missing, "receiptProblems": problems, "skipped": dict(skipped),
           "unprocessedPages": [p for p in pages if p not in visited],
           "collectorPending": [r for r in ledger.get("pending", []) if r.get("page") in pages],
           "collectorUnmatched": [r for r in ledger.get("unmatchedVerdicts", []) if r.get("page") in pages],
           "batchB": {"pages": sorted({r["page"] for r in batch_b_rows}), "rows": batch_b_rows},
           "applied": [], "plannedNotWritten": planned}
    with out_path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    if upgrades:
        print(f"升级：单页音系门禁延迟超过 100 条；本批未写 raw；批次账: {out_path}")
        return 2
    temp_raw = []
    for raw_path, raw in dirty.values():
        temp_path = raw_path.with_name(raw_path.name + f".{stamp}.tmp")
        temp_path.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        temp_raw.append((temp_path, raw_path))
    for temp_path, raw_path in temp_raw:
        temp_path.replace(raw_path)
    out.update({"status": "READY_FOR_SEAL", "appliedCount": len(applied),
                "pagesTouched": len(dirty), "dirtyPages": sorted(dirty),
                "applied": applied, "plannedNotWritten": []})
    temp_out = out_path.with_suffix(".tmp")
    temp_out.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    temp_out.replace(out_path)
    print(f"修复批账: {out_path} | 应用 {len(applied)} 条 / {len(dirty)} 页 | 延迟 {len(deferred)} 条")
    print(f"重封命令：python literature/tools/seal_and_verify.py --source {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
