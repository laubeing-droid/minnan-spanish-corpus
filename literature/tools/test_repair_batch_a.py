#!/usr/bin/env python3
"""隔离回归：全部输入、raw 和账目均位于临时目录，不读取正式转写。"""
import copy
import hashlib
import json
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")


def entry(pos=1, m="ba", r="ra", tones=None):
    return {"position": pos, "source_L": "L", "source_H": "H", "source_M": m,
            "source_R": r, "tone_marks_M": tones or [], "tone_marks_R": []}


def item(pos=1, field="M", v1="ba", rr="ca"):
    return {"position": pos, "field": field, "kind": "letter", "v1": v1, "rr": rr}


def verdict(it, ink="la", vd="两皆误", pos=None, rr=None, **extra):
    return {"position": it["position"] if pos is None else pos, "field": it["field"],
            "v1": it["v1"], "rr": it["rr"] if rr is None else rr, "verdict": vd, "ink": ink, **extra}


def setup(root, pg, items, verdicts, entries, raw=None):
    m = root / "literature/workspace_m2_dhs834"
    q = m / "collision_mr/adk" / f"adk_p{pg:04}.json"
    write(q, {"page": pg, "items": items})
    graded = [dict(v, letters="两皆误", tone_mark="存疑") for v in verdicts]
    write(q.with_name(f"adk_verdict_p{pg:04}.json"), {"page": pg, "verdicts": graded})
    write(m / f"blind_read_p{pg:04}.json", {"pdf_page": pg, "entries": entries})
    (m / "raw_blind").mkdir(exist_ok=True)
    if raw is not None:
        write(m / "raw_blind" / f"raw_part_p{pg:04}.json",
              {"pages": [{"pdf_page": pg, "entries": raw, "preserve": "yes"}]})
    return q


def freeze(root, queues):
    files = []
    for q in queues:
        data = q.read_bytes()
        files.append({"path": q.relative_to(root).as_posix(), "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()})
    write(root / "codex_M1_adk_queue_freeze.json", {"queue_count": len(files), "files": files})
    write(root / "codex_M1_legacy_verdict_freeze.json", {"files": []})


def run(root, script, *args):
    return subprocess.run([sys.executable, "-X", "utf8", str(TOOLS / script), *args],
                          cwd=root, capture_output=True, text=True)


def batch_test(root):
    queues = []
    i, i2 = item(), item(2, "R", "ra", "sa")
    entries = [entry(), entry(2, m="bi")]
    queues.append(setup(root, 50, [i, i2], [verdict(i, tone_marks_unchanged=True),
                                            verdict(i2, None, "重读对", tone_marks_unchanged=True)],
                        entries, copy.deepcopy(entries)))
    i = item()
    queues.append(setup(root, 51, [i], [verdict(i)], [entry()], [entry(m="unsaved")]))
    entries = [entry(tones=["bad-tone"])]
    queues.append(setup(root, 52, [i], [verdict(i)], entries, copy.deepcopy(entries)))
    i = item(field="source_M")
    queues.append(setup(root, 53, [i], [verdict(i, pos=9, tone_marks_unchanged=True)], [entry()], [entry()]))
    a, b = item(rr="ca"), item(field="source_M", rr="da")
    queues.append(setup(root, 54, [a, b], [verdict(a), verdict(b, ink="ma")], [entry()], [entry()]))
    i = item(field="L", v1="L")
    queues.append(setup(root, 55, [i], [verdict(i)], [entry()], [entry()]))
    i = item()
    queues.append(setup(root, 56, [i], [verdict(i, ink="la fa")], [entry()], [entry()]))
    queues.append(setup(root, 57, [i], [verdict(i)], [entry(m="bá")], [entry(m="bá")]))
    queues.append(setup(root, 58, [i], [verdict(i, rr="wrong")], [entry()], [entry()]))
    i = item(field="source_R", v1="ra", rr="sa")
    queues.append(setup(root, 59, [i], [verdict(i, None, "重读对", tone_marks_unchanged=True)], [entry()], [entry()]))

    m = root / "literature/workspace_m2_dhs834"
    outside = m / "raw_blind/raw_part_p0060.json"
    old = m / "collision_mr/REPAIR_BATCH_A_V4.json"
    write(outside, {"untouched": True})
    write(old, {"old_ledger": "untouched"})
    protected = {p: p.read_bytes() for p in (outside, old)}
    protected.update({m / "raw_blind" / f"raw_part_p{pg:04}.json":
                      (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes()
                      for pg in (51, 52, 54, 55, 56, 57, 58)})
    freeze(root, queues)
    result = run(root, "collect_adk_verdicts.py")
    assert result.returncode == 0, result.stderr
    result = run(root, "repair_batch_a.py", "--pages", ",".join(map(str, range(50, 60))))
    assert result.returncode == 0, (result.stdout, result.stderr)
    logs = list((m / "collision_mr").glob("REPAIR_BATCH_A_0050_0059_*.json"))
    assert len(logs) == 1
    log = json.loads(logs[0].read_text(encoding="utf-8"))
    assert log["status"] == "READY_FOR_SEAL" and len(log["applied"]) == 4
    for row in log["applied"]:
        raw = json.loads((m / "raw_blind" / f"raw_part_p{row['page']:04}.json").read_text(encoding="utf-8"))
        target = next(e for e in raw["pages"][0]["entries"] if e["position"] == row["position"])
        assert target[row["field"]] == row["new"]
    assert next(r for r in log["applied"] if r["page"] == 50 and r["position"] == 1)["task_field"] == "M"
    assert next(r for r in log["applied"] if r["page"] == 53)["match"] == "unique_values"
    assert next(r for r in log["applied"] if r["page"] == 59)["ink_source"] == "rr"
    for pg, reason in ((51, "未封存"), (52, "调标"), (55, "字段非"), (56, "音系门禁"), (57, "漂移")):
        assert any(r["page"] == pg and reason in r["reason"] for r in log["deferred"])
    assert len([r for r in log["deferred"] if r["page"] == 54]) == 2
    assert any(r["page"] == 58 for r in log["collectorPending"])
    assert all(path.read_bytes() == data for path, data in protected.items())
    assert json.loads((m / "raw_blind/raw_part_p0050.json").read_text(encoding="utf-8"))["pages"][0]["preserve"] == "yes"


def threshold_test(root):
    items = [item(i) for i in range(1, 102)]
    entries = [entry(i) for i in range(1, 102)]
    q = setup(root, 61, items, [verdict(i, ink="fa") for i in items], entries, copy.deepcopy(entries))
    freeze(root, [q])
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    raw = m / "raw_blind/raw_part_p0061.json"
    before = raw.read_bytes()
    result = run(root, "repair_batch_a.py", "--pages", "61")
    assert result.returncode == 2, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0061_0061_*.json")).read_text(encoding="utf-8"))
    assert raw.read_bytes() == before and log["deferredCount"] == 101 and log["appliedCount"] == 0
    assert log["upgrade"][0]["page"] == 61


def frozen_test(root):
    i = item()
    q = setup(root, 62, [i], [verdict(i)], [entry()], [entry()])
    freeze(root, [q])
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    raw = m / "raw_blind/raw_part_p0062.json"
    before = raw.read_bytes()
    changed = json.loads(q.read_text(encoding="utf-8"))
    changed["items"][0]["rr"] = "modified"
    write(q, changed)
    result = run(root, "repair_batch_a.py", "--pages", "62")
    assert result.returncode != 0 and "冻结队列不匹配" in (result.stdout + result.stderr)
    assert raw.read_bytes() == before
    assert not list((m / "collision_mr").glob("REPAIR_BATCH_A_0062_0062_*.json"))


def outside_frozen_test(root):
    i = item()
    selected = setup(root, 62, [i], [verdict(i)], [entry()], [entry()])
    outside = setup(root, 63, [i], [verdict(i)], [entry()], [entry()])
    freeze(root, [selected, outside])
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    raw = m / "raw_blind/raw_part_p0062.json"
    before = raw.read_bytes()
    original = outside.read_bytes()

    changed = json.loads(original)
    changed["items"][0]["rr"] = "modified"
    write(outside, changed)
    result = run(root, "repair_batch_a.py", "--pages", "62")
    assert result.returncode != 0 and "冻结队列不匹配" in (result.stdout + result.stderr)
    assert raw.read_bytes() == before

    outside.unlink()
    result = run(root, "repair_batch_a.py", "--pages", "62")
    assert result.returncode != 0 and "冻结队列页集或数量不匹配" in (result.stdout + result.stderr)
    assert raw.read_bytes() == before

    outside.write_bytes(original)
    extra = outside.with_name("adk_p0064.json")
    extra.write_bytes(original)
    result = run(root, "repair_batch_a.py", "--pages", "62")
    assert result.returncode != 0 and "冻结队列页集或数量不匹配" in (result.stdout + result.stderr)
    assert raw.read_bytes() == before
    assert not list((m / "collision_mr").glob("REPAIR_BATCH_A_0062_0062_*.json"))


def soup_test(root):
    soup = runpy.run_path(str(TOOLS / "repair_batch_a.py"))["soup"]
    assert soup("foo [残]") == soup("foo [疑]")
    assert soup("Pēŋ") != soup("Pe")
    assert soup("tiⁿû") == soup("tinu")
    i = item(v1="foo [残]")
    q = setup(root, 64, [i], [verdict(i, ink="foo [疑]")], [entry(m="foo [残]")],
              [entry(m="foo [残]")])
    freeze(root, [q])
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    raw = m / "raw_blind/raw_part_p0064.json"
    before = raw.read_bytes()
    result = run(root, "repair_batch_a.py", "--pages", "64")
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0064_0064_*.json")).read_text(encoding="utf-8"))
    assert raw.read_bytes() == before and log["appliedCount"] == 0
    assert log["skipped"]["字母汤等价"] == 1


def modifier_deferred_test(root):
    queues = []
    cases = [
        (108, "chûi tay", "chûi tay", "chûiᶜ tay̌", "两皆误", "other"),
        (109, "hi pien bye", "pien", "pieⁿ", "两皆误", "other"),
        (110, "bao", "bao", "chûiᶜ", "重读对", "chui"),
        (111, "ba", "ba", "bā", "两皆误", "other"),
    ]
    for pg, old, v1, ink, vd, rr in cases:
        it = item(field="R", v1=v1, rr=rr)
        entries = [entry(r=old)]
        queues.append(setup(root, pg, [it], [verdict(it, ink=ink, vd=vd)], entries, copy.deepcopy(entries)))
    freeze(root, queues)
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    before = {pg: (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() for pg, *_ in cases}
    result = run(root, "repair_batch_a.py", "--pages", ",".join(str(x[0]) for x in cases))
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0108_0111_*.json")).read_text(encoding="utf-8"))
    assert log["appliedCount"] == 0 and log["skipped"]["字母汤等价"] == 1
    assert {r["page"] for r in log["deferred"]} == {108, 109, 110}
    assert all(r["v1"] and r["rr"] and r["receipt"]["file"] for r in log["deferred"])
    assert all((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() == data for pg, data in before.items())


def sanitizer_guard_test(root):
    queues = []
    for pg, ink, h in ((112, "kiap", "H"), (113, "khoàⁿ", "看山"), (114, "pu\u0301", "H")):
        it = item()
        entries = [entry()]
        entries[0]["source_H"] = h
        queues.append(setup(root, pg, [it], [verdict(it, ink=ink, tone_marks_unchanged=True)],
                            entries, copy.deepcopy(entries)))
    a, b = item(rr="ca"), item(field="source_M", rr="da")
    entries = [entry()]
    queues.append(setup(root, 115, [a, b], [verdict(a, ink="kiap"), verdict(b, ink="kiap")],
                        entries, copy.deepcopy(entries)))
    freeze(root, queues)
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    protected = {pg: (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() for pg in (112, 113, 115)}
    result = run(root, "repair_batch_a.py", "--pages", "112,113,114,115")
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0112_0115_*.json")).read_text(encoding="utf-8"))
    assert {r["page"] for r in log["deferred"] if "净化会改写" in r["reason"]} == {112, 113, 115}
    assert {r["rr"] for r in log["deferred"] if r["page"] == 115} == {"ca", "da"}
    assert [r["page"] for r in log["applied"]] == [114]
    assert all((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() == data for pg, data in protected.items())


def duplicate_merge_test(root):
    queues = []
    for pg in range(70, 82):
        a, b = item(rr="ca"), item(field="source_M", rr="da")
        va, vb = verdict(a, tone_marks_unchanged=True), verdict(b, tone_marks_unchanged=True)
        entries = [entry()]
        if pg == 71:
            vb["ink"] = "ma"
        elif pg == 72:
            vb.update({"verdict": "墨迹不明", "ink": None})
        elif pg == 73:
            b["v1"], vb["v1"] = "bá", "bá"
        elif pg == 74:
            vb = None
        elif pg == 75:
            va["ink"] = vb["ink"] = "la [残]"
        elif pg == 76:
            a["rr"], va["rr"], va["verdict"], va["ink"] = "la", "la", "重读对", None
        elif pg == 77:
            del b["v1"]
            vb = None
        elif pg == 80:
            va["ink"] = vb["ink"] = "fa"
        elif pg == 81:
            vb["ink"] = "lā"
        queues.append(setup(root, pg, [a, b], [v for v in (va, vb) if v], entries, copy.deepcopy(entries)))
    freeze(root, queues)
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    protected_pages = (71, 72, 73, 74, 75, 77, 80, 81)
    before = {pg: (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() for pg in protected_pages}
    result = run(root, "repair_batch_a.py", "--pages", ",".join(map(str, range(70, 82))))
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0070_0081_*.json")).read_text(encoding="utf-8"))
    for pg in (70, 76, 78, 79):
        applied = [r for r in log["applied"] if r["page"] == pg]
        assert len(applied) == 1 and applied[0]["new"] == "la"
        refs = applied[0]["merged_receipts"]
        assert len(refs) == 2 and {r["field"] for r in refs} == {"M", "source_M"}
        assert all(r["v1"] == "ba" and isinstance(r["rr"], str) and "verdict" in r and "ink" in r
                   and r["receipt"]["index"] > 0 for r in refs)
        raw = json.loads((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_text(encoding="utf-8"))
        assert raw["pages"][0]["entries"][0]["source_M"] == "la"
    assert next(r for r in log["applied"] if r["page"] == 76)["ink_source"] == "rr"
    for pg, old in before.items():
        assert (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() == old
    assert len([r for r in log["deferred"] if r["page"] == 80 and "音系门禁" in r["reason"]]) == 2
    assert log["phonotacticDeferredByPage"]["80"] == 2


def token_repair_test(root):
    cases = {
        90: ("si ba, li!", "ba", "la"),
        91: ("ā ba! ü", "ba", "la"),
        92: ("ba, ba", "ba", "la"),
        93: ("aba", "ba", "la"),
        94: ("si ba, li", "ba", "la li"),
        95: ("si ba, li", "ba", "la"),
        96: ("[疑:ba] hi", "ba", "la"),
        97: ("si ba, li", "ba", "la"),
        98: ("si-ba", "ba", "la"),
        99: ("aaa", "aa", "la"),
        100: ("（ba），hi", "ba", "la"),
        101: ("si ba, li", "ba", "li好"),
        102: ("si ba, li", "ba", "la"),
        103: ("si ba, li", "ba", "bā"),
        104: ("ba", "ba", "la li"),
        105: ("b\u0301a", "b", "la"),
        106: ("〔疑:ba〕 hi", "ba", "la"),
        107: ("si ba, li", "ba", "la"),
    }
    queues = []
    for pg, (old, v1, ink) in cases.items():
        i = item(v1=v1)
        v = verdict(i, ink=ink)
        if pg in (90, 91, 100, 104):
            v["tone_marks_unchanged"] = True
        items, verdicts = [i], [v]
        if pg == 95:
            v["note"] = "跨栏存疑"
        elif pg == 97:
            second = item(field="source_M", v1="si", rr="zu")
            items.append(second)
            verdicts.append(verdict(second, ink="le"))
        elif pg == 102:
            v["evidence"] = "西语注释跨越栏界"
        elif pg == 107:
            second = item(field="source_M", v1="ba", rr="da")
            items.append(second)
            verdicts.append(verdict(second, ink="la"))
        entries = [entry(m=old)]
        queues.append(setup(root, pg, items, verdicts, entries, copy.deepcopy(entries)))
    freeze(root, queues)
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    changed_pages = {90, 91, 100, 104}
    protected = {pg: (m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes()
                 for pg in cases if pg not in changed_pages}
    result = run(root, "repair_batch_a.py", "--pages", ",".join(map(str, cases)))
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0090_0107_*.json")).read_text(encoding="utf-8"))
    applied = {r["page"]: r for r in log["applied"]}
    assert set(applied) == changed_pages
    for pg, expected in ((90, "si la, li!"), (91, "ā la! ü"), (100, "（la），hi"), (104, "la li")):
        raw = json.loads((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_text(encoding="utf-8"))
        assert raw["pages"][0]["entries"][0]["source_M"] == expected
        assert applied[pg]["old"] == cases[pg][0] and applied[pg]["new"] == expected
        if pg != 104:
            row = applied[pg]
            assert row["old_token"] == "ba" and row["new_token"] == "la"
            assert row["offset_unit"] == "unicode_codepoint" and row["receipt"]["index"] > 0
            assert row["old"][:row["offset"]] + row["new_token"] + row["old"][row["offset"] + 2:] == row["new"]
            assert (row["old"].encode("utf-8")[:row["byte_offset"]] + row["new_token"].encode("utf-8") +
                    row["old"].encode("utf-8")[row["byte_offset"] + len(row["old_token"].encode("utf-8")):]) == row["new"].encode("utf-8")
    assert applied[91]["offset"] == 2 and applied[91]["byte_offset"] == 3
    assert "old_token" not in applied[104]
    assert all((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_bytes() == data
               for pg, data in protected.items())
    for pg, reason in ((92, "多次"), (93, "词边界"), (94, "非单个"), (95, "跨栏"),
                       (96, "未决标注"), (97, "目标重复"), (98, "词边界"),
                       (99, "多次"), (101, "非单个"), (102, "跨栏"),
                       (105, "词边界"), (106, "未决标注"), (107, "目标重复")):
        assert any(r["page"] == pg and reason in r["reason"] for r in log["deferred"]), pg


def tone_sync_test(root):
    """声调数组同步口径（2026-11-19 批准）：新数组/不变确认/核查依据三选一，缺一延迟。"""
    queues = []
    base = ["T05 (平橫)"]
    new_arr = ["T03 (尖頂帽)", "T05 (平橫)"]
    cases = [
        (117, {"tone_marks_new": new_arr}, True, "confirmed_new"),
        (118, {"tone_basis": "甘为霖《厦门音新字典》(1913) 与 Douglas (1873) 均支持该音节拼读（隔离测试用例）"},
         True, "released_with_basis"),
        (119, {}, False, None),
        (120, {"tone_marks_new": ["T07"]}, False, None),
        (121, {"tone_marks_unchanged": True}, True, "confirmed_unchanged"),
    ]
    for pg, extra, *_ in cases:
        i = item()
        entries = [entry(tones=base)]
        queues.append(setup(root, pg, [i], [verdict(i, **extra)], entries, copy.deepcopy(entries)))
    freeze(root, queues)
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    result = run(root, "repair_batch_a.py", "--pages", "117,118,119,120,121")
    assert result.returncode == 0, (result.stdout, result.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0117_0121_*.json")).read_text(encoding="utf-8"))
    applied = {r["page"]: r for r in log["applied"]}
    assert set(applied) == {117, 118, 121}
    assert applied[117]["tone_check"] == "confirmed_new"
    assert applied[117]["tone_marks_old"] == base and applied[117]["tone_marks_new"] == new_arr
    raw117 = json.loads((m / "raw_blind/raw_part_p0117.json").read_text(encoding="utf-8"))
    assert raw117["pages"][0]["entries"][0]["tone_marks_M"] == new_arr
    assert applied[118]["tone_check"] == "released_with_basis" and "甘为霖" in applied[118]["tone_basis"]
    assert "tone_marks_new" not in applied[118]
    assert applied[121]["tone_check"] == "confirmed_unchanged" and "tone_basis" not in applied[121]
    raw121 = json.loads((m / "raw_blind/raw_part_p0121.json").read_text(encoding="utf-8"))
    assert raw121["pages"][0]["entries"][0]["tone_marks_M"] == base
    for pg, kw in ((119, "处置未记录"), (120, "新数组无效")):
        assert any(r["page"] == pg and kw in r["reason"] for r in log["deferred"]), pg
        raw = json.loads((m / "raw_blind" / f"raw_part_p{pg:04}.json").read_text(encoding="utf-8"))
        assert raw["pages"][0]["entries"][0]["source_M"] == "ba"


def defer_ids_test(root):
    """--defer-ids：指定候选延迟不落地；缺省时行为不变。"""
    i = item()
    q = setup(root, 122, [i], [verdict(i, tone_marks_unchanged=True)], [entry()], [entry()])
    freeze(root, [q])
    assert run(root, "collect_adk_verdicts.py").returncode == 0
    m = root / "literature/workspace_m2_dhs834"
    raw = m / "raw_blind/raw_part_p0122.json"
    before = raw.read_bytes()
    # 缺省：照常落地
    r = run(root, "repair_batch_a.py", "--pages", "122")
    assert r.returncode == 0 and r.stdout.count("应用 1"), (r.stdout, r.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0122_0122_*.json")).read_text(encoding="utf-8"))
    assert len(log["applied"]) == 1
    # 还原 raw 后再跑：带 --defer-ids 则该候选延迟
    raw.write_bytes(before)
    for old in (m / "collision_mr").glob("REPAIR_BATCH_A_0122_0122_*.json"):
        old.unlink()
    r = run(root, "repair_batch_a.py", "--pages", "122", "--defer-ids", "122:1:R,122:1:source_M")
    assert r.returncode == 0, (r.stdout, r.stderr)
    log = json.loads(next((m / "collision_mr").glob("REPAIR_BATCH_A_0122_0122_*.json")).read_text(encoding="utf-8"))
    assert log["appliedCount"] == 0 and raw.read_bytes() == before
    assert any("终审延迟" in d["reason"] for d in log["deferred"])


if __name__ == "__main__":
    for test in (batch_test, threshold_test, frozen_test, outside_frozen_test, soup_test, modifier_deferred_test, sanitizer_guard_test,
                 duplicate_merge_test, token_repair_test, tone_sync_test, defer_ids_test):
        with tempfile.TemporaryDirectory() as td:
            test(Path(td))
        print(test.__name__, "PASS")
