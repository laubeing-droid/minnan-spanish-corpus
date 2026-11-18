"""对原四图答卷作用户九值候选比较；不修改原标准或答卷。"""
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "codex_M0_recovery_candidate/REFERENCE_ONLY_ORIGINAL_CROPS_NINE.json"
spec = importlib.util.spec_from_file_location("grade_calibration", ROOT / "literature/tools/grade_calibration.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


def incomplete(value):
    return not value.strip() or "[残]" in value or "[未答]" in value


def fits_visible(value, truth, latin=True, allow_ng=False):
    """按原位置展开未知片段；每个上置符各自可算 c 或标记。"""
    value = value.replace("[未答]", "[残]")
    if latin:
        value = unicodedata.normalize("NFD", value)
    tokens = re.split(r"(\[残\]|ᶜ|ͨ)" if latin else r"(\[残\])", value)

    def clean(text):
        result = grader.soup(text) if latin else grader.cjk(text)
        return result.replace("ŋ", "ng") if allow_ng else result

    pattern = "".join(".*" if token == "[残]" else "(?:c|)" if latin and token in ("ᶜ", "ͨ")
                      else re.escape(clean(token)) for token in tokens)
    return re.fullmatch(pattern, clean(truth)) is not None


def could_be_header(value):
    return not value.strip() or fits_visible(value, "ante")


def latin_status(value, truth, allow_ng=False):
    if not value.strip():
        return "待核", "缺答"
    normalized = unicodedata.normalize("NFD", value)
    if incomplete(value) or "ᶜ" in normalized or "ͨ" in normalized:
        if fits_visible(value, truth, allow_ng=allow_ng):
            return "待核", "残缺或上置符存在与候选参考一致的可能"
        return "分歧", "已见字符及上置符各种可能均无法匹配候选参考"
    got, expected = grader.soup(value), grader.soup(truth)
    if got == expected:
        return "一致", ""
    if allow_ng and got.replace("ŋ", "ng") == expected.replace("ŋ", "ng"):
        return "待核", "仅ŋ/ng不同"
    return "分歧", ""


def grade(answer_path):
    std = json.loads(STANDARD.read_text(encoding="utf-8"))
    answers = json.loads(Path(answer_path).read_text(encoding="utf-8"))
    a = answers.get("cropA", [])
    b = answers.get("cropB", [])
    c = answers.get("cropC", [])
    d = answers.get("cropD_hanzi", answers.get("cropD", []))
    if not all(isinstance(rows, list) and all(isinstance(x, str) for x in rows) for rows in (a, b, c, d)):
        raise ValueError("cropA、cropB、cropC、cropD_hanzi 必须是字符串数组")

    has_header = bool(a) and grader.soup(a[0]) == grader.soup("ante")
    a_aligned = (has_header and len(a) == 6) or (
        not has_header and len(a) == 5 and (not incomplete(a[0]) or not could_be_header(a[0]))
    )
    a_rows = a if has_header else [""] + a
    b_aligned = len(b) in (7, 8)
    d_aligned = len(d) == 2
    print("用户九值候选比较；仅在逐行无漏行、无多行的前提下按位置对齐，长度本身不证明行序。")
    print(f"行序：A={'候选对齐' if a_aligned else '待核'}；B={'候选对齐' if b_aligned else '待核'}；D={'候选对齐' if d_aligned else '待核'}。")
    if len(a) == 5 and incomplete(a[0]) and a_aligned:
        print("A 首项残缺，但按残段位置不能匹配 ante，候选按不含页眉对齐；原答保留。")
    print("严格 soup 原始诊断（只按答卷数组序号展示，不据内容凑行）：")
    for name, values in (("A", a), ("B", b)):
        print(f"  {name}: " + json.dumps([grader.soup(x) for x in values], ensure_ascii=False))
    print("C 难题原答：" + json.dumps(c, ensure_ascii=False) + "；原图两端截断，不评分、不强行判错。")

    statuses = []
    hanzi = []
    for crop, values, aligned in (("cropA", a_rows, a_aligned), ("cropB", b, b_aligned), ("cropD", d, d_aligned)):
        for row in std["crops"][crop]["lines"]:
            if not row.get("core") or row.get("hard"):
                continue
            idx, truth = row["idx"], row["truth"]
            value = values[idx] if aligned else None
            if not aligned:
                status, reason = "待核", "该组行序或数量待核"
            elif crop == "cropD":
                if incomplete(value):
                    if not value.strip() or fits_visible(value, truth, latin=False):
                        status, reason = "待核", "汉字缺答或残缺后仍可能与候选参考一致"
                    else:
                        status, reason = "分歧", "已见汉字无法与候选参考匹配"
                else:
                    status, reason = ("一致", "") if grader.cjk(value) == grader.cjk(truth) else ("分歧", "汉字明确不同")
                hanzi.append(status)
            else:
                status, reason = latin_status(value, truth, allow_ng=(crop == "cropB" and idx == 6))
            if crop == "cropD" and not aligned:
                hanzi.append(status)
            statuses.append(status)
            strict = "未定位" if value is None else (
                f"{grader.cjk(value)!r}/{grader.cjk(truth)!r}" if crop == "cropD" else
                f"{grader.soup(value)!r}/{grader.soup(truth)!r}"
            )
            dependency = "页眉识别及 A 行序" if crop == "cropA" else f"{crop[-1]} 行序"
            display = status + "（相对候选参考）" if status == "分歧" else status
            print(f"{crop[-1]}{idx + 1}: {display}；答={value!r}；严格比={strict}；位置依赖={dependency}逐行不漏不多" + (f"；{reason}" if reason else ""))

    matched, pending = statuses.count("一致"), statuses.count("待核")
    possible = matched + pending
    print(f"已确定一致 {matched}/9；可能上限 {possible}/9；汉字：{','.join(hanzi)}。")
    if matched >= 8 and hanzi == ["一致", "一致"]:
        print("候选达标（非正式放行）")
        return 0
    if possible < 8 or "分歧" in hanzi:
        print("候选未达标")
        return 1
    print("待核")
    return 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("用法：python -B -X utf8 grade_original_crops_candidate.py 答卷.json")
    sys.exit(grade(sys.argv[1]))
