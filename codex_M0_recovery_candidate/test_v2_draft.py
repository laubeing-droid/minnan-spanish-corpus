"""在临时目录用合成答卷测试 V2 草案；不改正式标准、判卷器或真实答卷。"""
import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "codex_M0_recovery_candidate/REFERENCE_ONLY_CALIBRATION_STANDARD_V2_DRAFT.json"
spec = importlib.util.spec_from_file_location("grade_calibration", ROOT / "literature/tools/grade_calibration.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class V2DraftTest(unittest.TestCase):
    def setUp(self):
        self.std = json.loads(STANDARD.read_text(encoding="utf-8"))
        self.answers = {
            ("cropD_hanzi" if crop == "cropD" else crop): [line["truth"] for line in item["lines"]]
            for crop, item in self.std["crops"].items()
        }

    def grade(self, std=None):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            std_path, answer_path = folder / "standard.json", folder / "answer.json"
            std_path.write_text(json.dumps(std or self.std, ensure_ascii=False), encoding="utf-8")
            answer_path.write_text(json.dumps(self.answers, ensure_ascii=False), encoding="utf-8")
            saved_std = grader.STD
            try:
                grader.STD = std_path
                with contextlib.redirect_stdout(io.StringIO()):
                    return grader.main(answer_path)
            finally:
                grader.STD = saved_std

    def test_all_nine_correct(self):
        self.assertEqual(grader.core_count(self.std), 9)
        self.assertEqual(self.grade(), 0)

    def test_one_latin_wrong_passes_eight_of_nine(self):
        self.answers["cropA"][2] = "wrong"
        self.assertEqual(self.grade(), 0)

    def test_two_latin_wrong_fail(self):
        self.answers["cropA"][2:4] = ["wrong", "wrong"]
        self.assertEqual(self.grade(), 1)

    def test_one_latin_missing_counts_as_one_error(self):
        self.answers["cropA"][2] = ""
        self.assertEqual(self.grade(), 0)

    def test_two_latin_missing_fail(self):
        self.answers["cropA"][2:4] = ["", ""]
        self.assertEqual(self.grade(), 1)

    def test_one_hanzi_wrong_fails(self):
        self.answers["cropD_hanzi"][1] = "錯"
        self.assertEqual(self.grade(), 1)

    def test_one_hanzi_missing_fails(self):
        self.answers["cropD_hanzi"].pop()
        self.assertEqual(self.grade(), 1)

    def test_inconsistent_count_refuses_grading(self):
        broken = copy.deepcopy(self.std)
        broken["crops"]["cropA"]["lines"][2]["core"] = False
        self.assertEqual(self.grade(broken), 2)

    def test_existing_unicode_comparison_is_not_silently_changed(self):
        self.assertNotEqual(grader.soup("Pēŋ"), grader.soup("Péng"))
        self.assertEqual(grader.soup("pueͨ"), grader.soup("pue"))
        self.assertNotEqual(grader.soup("pueᶜ"), grader.soup("pue"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
