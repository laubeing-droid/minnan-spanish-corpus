#!/usr/bin/env python3
"""隔离回归：apply_verdicts / calibration_diff / extract_candidates。
全部输入输出位于临时目录，不触正式数据（extract 用合成台账）。"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")


def item(idx, field="M", v1="ba", rr="ca"):
    return {"position": idx, "field": field, "kind": "letter", "v1": v1, "rr": rr}


def run(root, script, *args):
    return subprocess.run([sys.executable, "-X", "utf8", str(TOOLS / script), *args],
                          cwd=root, capture_output=True, text=True)


def base_setup(root):
    write(root / "literature/workspace_m2_dhs834/collision_mr/adk/adk_p0700.json",
          {"page": 700, "items": [item(1), item(2, "R", "ra", "sa")]})


def j(idx, **kw):
    d = {"verdict": "两皆误", "letters": "两皆误", "tone_mark": "存疑", "ink": "la"}
    d.update(kw)
    return d


def apply_ok_test(root):
    base_setup(root)
    jp = root / "_scratch/j_ok.json"
    write(jp, {"page": 700, "arbiter": "t", "method": "t",
               "judgments": {"1": j(1), "2": {"verdict": "重读对", "letters": "rr",
                                              "tone_mark": "一致", "tone_marks_unchanged": True}}})
    out = root / "_scratch/receipt_p0700.json"
    r = run(root, "apply_verdicts.py", "--page", "700", "--judgments", str(jp), "--out", str(out))
    assert r.returncode == 0, (r.stdout, r.stderr)
    rec = json.loads(out.read_text(encoding="utf-8"))
    assert rec["page"] == 700 and len(rec["verdicts"]) == 2
    v1 = rec["verdicts"][0]
    assert v1["position"] == 1 and v1["field"] == "M" and v1["v1"] == "ba" and v1["rr"] == "ca"
    assert v1["verdict"] == "两皆误" and v1["ink"] == "la"
    assert rec["verdicts"][1]["tone_marks_unchanged"] is True


def apply_reject_test(root):
    base_setup(root)
    cases = [
        {"1": j(1, verdict="乱判"), "2": j(2, verdict="乱判")},                    # verdict 非法
        {"1": j(1)},                                                              # 覆盖缺失
        {"1": j(1), "2": j(2), "3": j(3)},                                        # 覆盖超出
        {"1": {"verdict": "两皆误", "letters": "两皆误", "tone_mark": "存疑"},     # 两皆误缺 ink
         "2": {"verdict": "重读对", "letters": "rr", "tone_mark": "一致"}},
        {"1": j(1, letters="待核"), "2": j(2)},                                   # 待核仅限墨迹不明
        {"1": j(1, ink="la [残]"), "2": j(2)},                                    # ink 含未决括注
        {"1": j(1, tone_marks_new=["T99 (乱写)"]), "2": j(2)},                    # 调码非法
        {"1": j(1, tone_marks_unchanged="yes"), "2": j(2)},                       # unchanged 非 true
        {"1": j(1, tone_basis="  "), "2": j(2)},                                  # basis 空串
    ]
    for i, judgments in enumerate(cases):
        jp = root / f"_scratch/j_bad{i}.json"
        write(jp, {"page": 700, "judgments": judgments})
        out = root / f"_scratch/receipt_bad{i}.json"
        r = run(root, "apply_verdicts.py", "--page", "700", "--judgments", str(jp), "--out", str(out))
        assert r.returncode != 0, f"case{i} 应拒绝"
        assert not out.exists(), f"case{i} 不应写文件"


def pending_letter_test(root):
    """letters=待核 + verdict=墨迹不明 → 合法（诚实落 pending 路径）。"""
    base_setup(root)
    jp = root / "_scratch/j_pending.json"
    write(jp, {"page": 700, "judgments": {
        "1": {"verdict": "墨迹不明", "letters": "待核", "tone_mark": "存疑"},
        "2": {"verdict": "墨迹不明", "letters": "rr", "tone_mark": "存疑"}}})
    out = root / "_scratch/receipt_pending.json"
    r = run(root, "apply_verdicts.py", "--page", "700", "--judgments", str(jp), "--out", str(out))
    assert r.returncode == 0, (r.stdout, r.stderr)
    rec = json.loads(out.read_text(encoding="utf-8"))
    assert rec["verdicts"][0]["letters"] == "待核"


def diff_test(root):
    a = {"verdicts": [
        {"position": 1, "field": "M", "v1": "ba", "rr": "ca", "verdict": "两皆误",
         "letters": "两皆误", "tone_mark": "存疑", "ink": "lá"},
        {"position": 2, "field": "R", "v1": "ra", "rr": "sa", "verdict": "V1对",
         "letters": "V1", "tone_mark": "一致"}]}
    b = {"verdicts": [
        {"position": 1, "field": "M", "v1": "ba", "rr": "ca", "verdict": "两皆误",
         "letters": "两皆误", "tone_mark": "存疑", "ink": "la"},   # ink 仅调符差异→汤一致
        {"position": 2, "field": "R", "v1": "ra", "rr": "sa", "verdict": "重读对",
         "letters": "rr", "tone_mark": "一致"}]}                   # verdict/letters 分歧
    fa, fb = root / "_scratch/da.json", root / "_scratch/db.json"
    write(fa, a)
    write(fb, b)
    r = run(root, "calibration_diff.py", "--files", str(fa), str(fb), "--labels", "甲", "乙")
    assert r.returncode == 1, (r.stdout, r.stderr)
    payload = json.loads(r.stdout.splitlines()[0])
    assert payload["total"] == 2 and payload["disagree"] == 1
    assert payload["disagreements"][0]["position"] == 2
    # 全一致路径
    r = run(root, "calibration_diff.py", "--files", str(fa), str(fa))
    assert r.returncode == 0


def extract_test(root):
    m2 = root / "literature/workspace_m2_dhs834"
    led = {"rows": [
        {"page": 700, "position": 1, "field": "M", "kind": "k", "v1": "ba", "rr": "ca",
         "verdict": "两皆误", "ink": "la", "receipt": {"file": "f", "index": 1}},
        {"page": 700, "position": 2, "field": "R", "kind": "k", "v1": "ra", "rr": "sa",
         "verdict": "墨迹不明", "ink": None, "receipt": {}},
    ]}
    write(m2 / "collision_mr/ADK_ADJUDICATION_LEDGER.json", led)
    write(m2 / "blind_read_p0700.json", {"entries": [
        {"position": 1, "source_H": "漢", "source_M": "ba", "source_R": "ra",
         "tone_marks_M": ["T05 (平橫)"], "tone_marks_R": []}]})
    (root / "literature/tiles/01_DHS/page_0700").mkdir(parents=True, exist_ok=True)
    out = root / "_scratch/cands.json"
    r = run(root, "extract_candidates.py", "--pages", "700", "--out", str(out))
    assert r.returncode == 0, (r.stdout, r.stderr)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["candidateCount"] == 1  # 墨迹不明不入选
    c = data["candidates"][0]
    assert c["task_field"] == "source_M" and c["sealed_H"] == "漢"
    assert c["tone_marks"]["M"] == ["T05 (平橫)"] and "tiles" in c


if __name__ == "__main__":
    for test in (apply_ok_test, apply_reject_test, pending_letter_test, diff_test, extract_test):
        with tempfile.TemporaryDirectory() as td:
            test(Path(td))
        print(test.__name__, "PASS")
