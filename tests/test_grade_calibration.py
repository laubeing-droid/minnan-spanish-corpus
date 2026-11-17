import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("grade_calibration", ROOT / "literature/tools/grade_calibration.py")
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


class CalibrationTest(unittest.TestCase):
    def test_full_grading_and_invalid_standard(self):
        latin = ["ba", "ca", "da", "ea", "fa", "ga", "ha"]
        standard = {
            "grading": {"coreCount": 9},
            "crops": {
                "cropA": {"lines": [{"idx": i, "truth": s, "core": True} for i, s in enumerate(latin)]},
                "cropD": {"compare": "CJK_EXACT", "lines": [
                    {"idx": 0, "truth": "甲", "core": True},
                    {"idx": 1, "truth": "乙", "core": True},
                ]},
            },
        }
        answer = {"cropA": latin, "cropD_hanzi": ["甲", "乙"]}
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            path = Path(d)
            std = path / "standard.json"
            ans = path / "answer.json"
            old_std = grader.STD
            try:
                grader.STD = std
                std.write_text(json.dumps(standard, ensure_ascii=False), encoding="utf-8")
                ans.write_text(json.dumps(answer, ensure_ascii=False), encoding="utf-8")
                self.assertEqual(grader.main(ans), 0)
                answer["cropD_hanzi"][1] = "[未答]"
                ans.write_text(json.dumps(answer, ensure_ascii=False), encoding="utf-8")
                self.assertEqual(grader.main(ans), 1)
                standard["crops"]["cropA"]["lines"][0]["core"] = False
                std.write_text(json.dumps(standard, ensure_ascii=False), encoding="utf-8")
                self.assertEqual(grader.main(ans), 2)
            finally:
                grader.STD = old_std
        self.assertNotEqual(grader.soup("Pēŋ"), grader.soup("Pe"))


if __name__ == "__main__":
    unittest.main()
