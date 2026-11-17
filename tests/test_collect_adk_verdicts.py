import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "literature/tools/collect_adk_verdicts.py"


def item(position, v1, rr):
    return {"position": position, "field": "source_M", "kind": "synthetic", "v1": v1, "rr": rr}


def verdict(row, position=None, **extra):
    return {**row, "position": row["position"] if position is None else position,
            "verdict": "V1对", "ink": "", "note": "", "letters": "V1", "tone_mark": "一致", **extra}


def freeze(root, paths):
    files = []
    for path in paths:
        content = path.read_bytes()
        files.append({"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(content).hexdigest()})
    (root / "codex_M1_legacy_verdict_freeze.json").write_text(
        json.dumps({"files": files}), encoding="utf-8")


def collect(root, adk):
    subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT)], cwd=root,
                   text=True, capture_output=True, check=True)
    return json.loads((adk.parent / "ADK_ADJUDICATION_LEDGER.json").read_text(encoding="utf-8"))


class CollectorTest(unittest.TestCase):
    def test_full_ledger_and_unambiguous_matching(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adk = root / "literature/workspace_m2_dhs834/collision_mr/adk"
            adk.mkdir(parents=True)

            def write(name, value):
                (adk / name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

            large = [item(i, f"v1-{i}", f"rr-{i}") for i in range(3005)]
            write("adk_p1000.json", {"page": 1000, "items": large})
            write("adk_verdict_p1000.json", {
                "page": 1000, "arbiter": "synthetic-author", "verdicts": [verdict(row) for row in large],
            })

            a, b, c = item(1, "a", "aa"), item(2, "b", "bb"), item(3, "c", "cc")
            dup, e, f = item(4, "dup", "dd"), item(5, "e", "ee"), item(6, "f", "ff")
            g, h, h2 = item(7, "g", "gg"), item(8, "h", "hh"), item(9, "h", "hh")
            dup_receipt, dup_queue = item(11, "j", "jj"), item(12, "k", "kk")
            prefix1 = item(13, "same-prefix-value-one", "rr-one")
            prefix2 = item(13, "same-prefix-value-two", "rr-two")
            cases = [a, b, c, dup, dup, e, f, g, h, h2, dup_receipt, dup_queue, dup_queue, prefix1, prefix2]
            missing_echo = {k: v for k, v in verdict(f).items() if k != "rr"}
            receipts = [
                verdict(a, letters="等价", tone_mark="一致", reviewer="synthetic-reviewer"),
                verdict(b, 20),
                verdict(c, rr="different"),
                verdict(dup), verdict(dup, verdict="重读对"),
                verdict(e, verdict="两皆误"), missing_echo, verdict(g, v1="different"),
                verdict(h), verdict(h2, 40),
                verdict(dup_receipt), verdict(dup_receipt, verdict="重读对"),
                verdict(dup_queue), verdict(prefix1), verdict(prefix2, verdict="重读对"),
            ]
            write("adk_p1001.json", {"page": 1001, "items": cases})
            write("adk_verdict_p1001.json", {"page": 1001, "model": "synthetic-model", "verdicts": receipts})

            for page in range(1002, 1253):
                write(f"adk_p{page}.json", {"page": page, "items": [item(1, "x", "y")]})
            (adk / "adk_verdict_p1252.json").write_text("{", encoding="utf-8")

            freeze(root, [])
            ledger = collect(root, adk)
            stats = ledger["stats"]
            sample = [row for row in ledger["rows"] if row["page"] == 1001]

            self.assertEqual((ledger["queueItems"], stats["judged"], stats["unjudged"]), (3271, 3010, 261))
            self.assertEqual((len(ledger["rows"]), len(stats["missingPages"])), (3010, 251))
            self.assertEqual((len(ledger["pending"]), len(ledger["unmatchedVerdicts"])), (10, 10))
            self.assertEqual([row["position"] for row in sample], [1, 2, 8, 13, 13])
            self.assertEqual(next(row for row in sample if row["position"] == 2)["receipt"]["match"], "unique_values")
            first = next(row for row in sample if row["position"] == 1)
            self.assertEqual((first["letters"], first["tone_mark"]), ("等价", "一致"))
            self.assertEqual(first["receipt"]["metadata"]["reviewer"], "synthetic-reviewer")
            self.assertTrue(any(row["metadata"].get("model") == "synthetic-model" for row in ledger["receiptSources"]))
            self.assertIsNone(ledger["arbiter"])
            self.assertEqual([row["verdict"] for row in sample if row["position"] == 13], ["V1对", "重读对"])

    def test_legacy_exemption_dual_grades_and_candidate_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adk = root / "literature/workspace_m2_dhs834/collision_mr/adk"
            adk.mkdir(parents=True)
            row = item(1, "synthetic-v1", "synthetic-rr")
            old = {k: v for k, v in verdict(row).items() if k not in ("letters", "tone_mark")}
            cases = {
                1000: ({}, old),
                1001: ({}, old),
                1002: ({}, verdict(row, letters=None)),
                1003: ({}, verdict(row, letters="invalid")),
                1004: ({}, verdict(row, tone_mark="invalid")),
                1005: ({}, verdict(row)),
                1006: ({}, old),
                1007: ({"protocol": "historical"}, old),
                1008: ({"status": "候选"}, verdict(row)),
                1009: ({"status": "PROVISIONAL"}, verdict(row)),
                1010: ({}, verdict(row, status="CANDIDATE")),
                1011: ({}, verdict(row, provisional=True)),
                1012: ({}, verdict(row, letters=None)),
            }
            for page, (metadata, decision) in cases.items():
                (adk / f"adk_p{page}.json").write_text(json.dumps({"items": [row]}), encoding="utf-8")
                (adk / f"adk_verdict_p{page}.json").write_text(
                    json.dumps({"page": page, **metadata, "verdicts": [decision]}, ensure_ascii=False), encoding="utf-8")
            historic = [adk / f"adk_verdict_p{page}.json" for page in (1000, 1006, 1012)]
            freeze(root, historic)
            # Same path with changed bytes must no longer receive the historical exemption.
            changed = json.loads(historic[1].read_text(encoding="utf-8"))
            changed["protocol"] = "historical"
            historic[1].write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")

            ledger = collect(root, adk)
            self.assertEqual((ledger["stats"]["judged"], ledger["stats"]["unjudged"]), (2, 11))
            self.assertEqual({r["page"] for r in ledger["rows"]}, {1000, 1005})
            legacy_row = next(r for r in ledger["rows"] if r["page"] == 1000)
            self.assertTrue(legacy_row["receipt"]["legacyExempt"])
            self.assertNotIn("letters", legacy_row)
            self.assertNotIn("tone_mark", legacy_row)
            reasons = {r["page"]: r["reason"] for r in ledger["pending"]}
            for page in (1001, 1002, 1003, 1004, 1006, 1007, 1012):
                self.assertEqual(reasons[page], "双判级缺失或无效")
            for page in (1008, 1009, 1010, 1011):
                self.assertEqual(reasons[page], "候选回执未确认")


if __name__ == "__main__":
    unittest.main()
