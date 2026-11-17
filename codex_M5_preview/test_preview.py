"""在临时 Git 仓库验证 M5 预览，不触碰正式数据。"""
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import preview


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


class PreviewTest(unittest.TestCase):
    def test_original_values_candidates_conflicts_and_no_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            work = root / "literature" / "workspace_m2_dhs834"
            rr_dir = work / "reread_mr"
            out = root / "codex_M5_preview"
            def row(pos, h, m, r="[空]"):
                return {"position": pos, "source_H": h, "source_M": m, "source_R": r}
            first = {"entries": [row(1, "魚", "pēŋ"), row(2, "魚", "tī"),
                                 row(3, "魚", "[空]"), row(4, "魚[疑]", "[空]"),
                                 row(5, "魚", "pēŋ")]}
            second = {"entries": [row(1, "甲", "[残]")]}
            for page, doc in (("0041", first), ("0042", second)):
                write(work / f"blind_read_p{page}.json", doc)
            def manifest():
                return {"pages": {page: {"blind_first_read_sha256": hashlib.sha256(
                    (work / f"blind_read_p{page}.json").read_bytes()).hexdigest()}
                    for page in ("0041", "0042")}}
            write(work / "BLIND_READ_MANIFEST.json", manifest())
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "baseline"], cwd=root, check=True)
            first["entries"][0]["source_M"] = "changed"
            write(work / "blind_read_p0041.json", first)
            write(work / "BLIND_READ_MANIFEST.json", manifest())
            write(rr_dir / "reread_mr_p0041.json", {"m_lines": ["Peŋ", "ti", "[空]", "[空]", "pēŋ"],
                  "r_lines": ["[空]"] * 5, "notes": "第2行（魚）"})
            write(rr_dir / "reread_mr_p0042.json", {"m_lines": ["ma", "ma"], "r_lines": [],
                  "notes": "第1行（甲）"})
            before = {p: p.read_bytes() for p in work.rglob("*.json")}
            previous = preview.ROOT, preview.WORK, preview.OUT, preview.BASE
            preview.ROOT, preview.WORK, preview.OUT, preview.BASE = root, work, out, "HEAD"
            try:
                preview.build()
            finally:
                preview.ROOT, preview.WORK, preview.OUT, preview.BASE = previous
            self.assertEqual(before, {p: p.read_bytes() for p in work.rglob("*.json")})
            source = json.loads((out / "candidate_sources.json").read_text(encoding="utf-8"))["sources"]
            targets = json.loads((out / "candidate_targets.json").read_text(encoding="utf-8"))["targets"]
            stats = json.loads((out / "summary.json").read_text(encoding="utf-8"))["counts"]
            anchors = json.loads((out / "note_anchors.json").read_text(encoding="utf-8"))["anchors"]
            old = next(s for s in source if s["position"] == 1)
            self.assertEqual((old["v1"], old["current_value"]), ("pēŋ", "changed"))
            self.assertTrue(all(not s["auto_fill"] for s in source))
            self.assertTrue(all(not a["auto_fill"] for a in anchors))
            target = next(t for t in targets if t["page"] == 41 and t["position"] == 3 and t["field"] == "M")
            self.assertEqual(target["status"], "候选音节组冲突，定位未证")
            self.assertEqual(sorted(len(g["source_ids"]) for g in target["candidate_groups"]), [1, 2])
            r_target = next(t for t in targets if t["page"] == 41 and t["position"] == 3 and t["field"] == "R")
            self.assertEqual(r_target["candidate_groups"], [])
            self.assertEqual(stats["M_line_count_mismatch_pages"], 1)
            self.assertEqual(stats["proven_auto_fill_sources"], 0)
            self.assertEqual(stats["target_M_without_exact_hanzi"], 1)
            uncertain = next(t for t in targets if t["page"] == 41 and t["position"] == 4 and t["field"] == "M")
            self.assertEqual(uncertain["status"], "汉字缺损或歧义")
            self.assertEqual(uncertain["candidate_groups"], [])
            self.assertFalse((work / "raw_blind").exists())

    def test_normalization(self):
        self.assertEqual(preview.soup("pēⁿ"), preview.soup("pen"))
        self.assertNotEqual(preview.soup("Pēŋ"), preview.soup("Pe"))
        self.assertEqual(preview.soup("foo [残]"), preview.soup("foo [疑]"))
        self.assertEqual(preview.han_key("割 玉 脛 皮"), "割玉脛皮")
        self.assertEqual(preview.han_key("魚[疑]"), "")
        self.assertFalse(preview.roman("foo [残]"))


if __name__ == "__main__":
    unittest.main()
