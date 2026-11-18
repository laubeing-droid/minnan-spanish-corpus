"""只用合成答卷测试候选判卷；不读取或改写真实答卷。"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
STANDARD = json.loads((DIR / "REFERENCE_ONLY_ORIGINAL_CROPS_NINE.json").read_text(encoding="utf-8"))
base = {
    ("cropD_hanzi" if name == "cropD" else name): [line["truth"] for line in crop["lines"]]
    for name, crop in STANDARD["crops"].items()
}


def run(answers):
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "synthetic.json"
        path.write_text(json.dumps(answers, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(DIR / "grade_original_crops_candidate.py"), str(path)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )


def sample():
    return {key: value.copy() for key, value in base.items()}


def expect(answers, code, *fragments):
    result = run(answers)
    assert result.returncode == code, (result.returncode, result.stdout, result.stderr)
    assert all(fragment in result.stdout for fragment in fragments), result.stdout


expect(sample(), 0, "已确定一致 9/9", "候选达标（非正式放行）")
no_header = sample()
no_header["cropA"].pop(0)
expect(no_header, 0, "A=候选对齐", "已确定一致 9/9")
extra_a = sample()
extra_a["cropA"].pop(0)
extra_a["cropA"].append("多出一行")
expect(extra_a, 2, "A=待核", "A3: 待核", "可能上限 9/9")
missing_a = sample()
missing_a["cropA"].pop()
expect(missing_a, 2, "A=待核", "A5: 待核")
uncertain_first_a = sample()
uncertain_first_a["cropA"].pop(0)
uncertain_first_a["cropA"][0] = "[残]"
expect(uncertain_first_a, 2, "A=待核", "A3: 待核")
partial_nonheader = sample()
partial_nonheader["cropA"].pop(0)
partial_nonheader["cropA"][0] = "hi[残]ū"
expect(partial_nonheader, 0, "A=候选对齐", "按残段位置不能匹配 ante", "已确定一致 9/9")
partial_possible_header = sample()
partial_possible_header["cropA"].pop(0)
partial_possible_header["cropA"][0] = "a[残]e"
expect(partial_possible_header, 2, "A=待核", "A3: 待核")
partial_wrong_end = sample()
partial_wrong_end["cropA"].pop(0)
partial_wrong_end["cropA"][0] = "a[残]n"
expect(partial_wrong_end, 0, "A=候选对齐", "按残段位置不能匹配 ante", "已确定一致 9/9")
missing_b = sample()
missing_b["cropB"].pop(2)
expect(missing_b, 2, "B=待核", "B2: 待核", "B7: 待核")
extra_b = sample()
extra_b["cropB"].extend(["部分一行", "多出一行"])
expect(extra_b, 2, "B=待核", "B5: 待核")
partial_tail = sample()
partial_tail["cropB"].append("[残]")
expect(partial_tail, 0, "B=候选对齐", "已确定一致 9/9")
partial_eighth_without_mark = sample()
partial_eighth_without_mark["cropB"].append("残行可辨字母")
expect(partial_eighth_without_mark, 0, "B=候选对齐", "已确定一致 9/9")
partial_seventh = sample()
partial_seventh["cropB"][-1] = "[残]"
expect(partial_seventh, 0, "B=候选对齐", "B7: 待核", "已确定一致 8/9")
one_wrong = sample()
one_wrong["cropA"][2] = "wrong"
expect(one_wrong, 0, "A3: 分歧", "已确定一致 8/9")
two_wrong = sample()
two_wrong["cropA"][2:4] = ["wrong", "wrong"]
expect(two_wrong, 1, "可能上限 7/9", "候选未达标")
for mark in ("ᶜ", "ͨ"):
    superscript = sample()
    superscript["cropA"][2] = "wrong"
    superscript["cropB"][4] += mark
    expect(superscript, 2, "B5: 待核", "残缺或上置符存在与候选参考一致的可能", "已确定一致 7/9", "可能上限 8/9")
    different_base = sample()
    different_base["cropB"][4] = "sûa pūe" + mark
    expect(different_base, 0, "B5: 分歧", "已见字符及上置符各种可能均无法匹配候选参考", "已确定一致 8/9")
multiple_marks = sample()
multiple_marks["cropB"][5] = "cûa ᶜiòng guêng pūēͨ"
expect(multiple_marks, 0, "B6: 待核", "残缺或上置符存在与候选参考一致的可能")
partial = sample()
partial["cropA"][2] = "wrong"
partial["cropB"][5] = "cûa [残]"
expect(partial, 2, "B6: 待核", "残缺或上置符存在与候选参考一致的可能")
partial_wrong_a = sample()
partial_wrong_a["cropA"][2] = "fo[残] f[残]"
expect(partial_wrong_a, 0, "A3: 分歧", "已见字符及上置符各种可能均无法匹配候选参考")
partial_wrong_b = sample()
partial_wrong_b["cropB"][5] = "sûa ciòng guêng p[残]"
expect(partial_wrong_b, 0, "B6: 分歧", "已见字符及上置符各种可能均无法匹配候选参考")
ng = sample()
ng["cropA"][2] = "wrong"
ng["cropB"][6] = "Péng."
expect(ng, 2, "B7: 待核", "仅ŋ/ng不同")
ng_other_line = sample()
ng_other_line["cropB"][5] = "cûa ciòŋ guêŋ pūē"
expect(ng_other_line, 0, "B6: 分歧", "已确定一致 8/9")
wrong_hanzi = sample()
wrong_hanzi["cropD_hanzi"][0] = "錯"
expect(wrong_hanzi, 1, "D1: 分歧", "汉字明确不同")
missing_hanzi = sample()
missing_hanzi["cropD_hanzi"][1] = ""
expect(missing_hanzi, 2, "D2: 待核", "汉字缺答或残缺后仍可能与候选参考一致")
partial_hanzi = sample()
partial_hanzi["cropD_hanzi"][1] = "割[残]皮"
expect(partial_hanzi, 2, "D2: 待核", "汉字缺答或残缺后仍可能与候选参考一致")
partial_first_hanzi = sample()
partial_first_hanzi["cropD_hanzi"][0] = "割[残]皮"
expect(partial_first_hanzi, 2, "D1: 待核", "汉字缺答或残缺后仍可能与候选参考一致")
partial_wrong_hanzi = sample()
partial_wrong_hanzi["cropD_hanzi"][0] = "錯[残]皮"
expect(partial_wrong_hanzi, 1, "D1: 分歧", "已见汉字无法与候选参考匹配")
short_hanzi = sample()
short_hanzi["cropD_hanzi"].pop()
expect(short_hanzi, 2, "D=待核", "D1: 待核", "D2: 待核")
hard_line = sample()
hard_line["cropC"] = ["部分[残]"]
expect(hard_line, 0, 'C 难题原答：["部分[残]"]', "原图两端截断，不评分、不强行判错")
alignment = run(sample()).stdout
assert alignment.count("位置依赖=") == 9
print("合成自测 33/33：残段位置、多上置符独立、逐题行序、ŋ/ng、汉字及 C 难题。")
