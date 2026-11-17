import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "literature/tools/seal_and_verify.py"


class SealDriverTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tools = self.root / "literature/tools"
        self.raw = self.root / "literature/workspace_m2_dhs834/raw_blind"
        self.tools.mkdir(parents=True)
        self.raw.mkdir(parents=True)
        self.events = self.root / "events.txt"
        shutil.copyfile(SCRIPT, self.tools / SCRIPT.name)
        for target, event in [
            (self.tools / "zcode_m2_pipeline.py", "commit"),
            (self.root / "architect_gatekeeper.py", "gate"),
            (self.tools / "post_repair_verify.py", "resweep"),
        ]:
            target.write_text(
                "from pathlib import Path\n"
                f"with Path({str(self.events)!r}).open('a', encoding='utf-8') as f: f.write({event + chr(10)!r})\n"
                "print('ok')\n", encoding="utf-8")

    def source(self, value):
        path = self.root / "batch.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_driver(self, *args):
        return subprocess.run([sys.executable, "-X", "utf8", str(self.tools / SCRIPT.name), *args],
                              cwd=self.root, text=True, capture_output=True)

    def raw_page(self, page):
        path = self.raw / f"raw_part_p{page:04d}.json"
        path.write_text('{"pages": [{"entries": []}]}', encoding="utf-8")
        return path

    def assert_no_calls(self):
        self.assertFalse(self.events.exists())
        self.assertEqual(list(self.raw.glob("merged_seal_p*.json")), [])

    def test_unready_source_is_rejected_even_with_explicit_pages(self):
        raw = self.raw_page(1)
        original = raw.read_bytes()
        for status in ("PENDING_RAW_WRITE", "BLOCKED_PHONOTACTIC_DEFERRED", "BLOCKED"):
            with self.subTest(status=status):
                source = self.source({"status": status, "applied": [{"page": 1}]})
                result = self.run_driver("--source", str(source), "--pages", "1")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout.strip())["reason"], "source_not_ready")
                self.assertEqual(raw.read_bytes(), original)
                self.assert_no_calls()

    def test_ready_and_legacy_sources_seal(self):
        self.raw_page(1)
        for status in ("READY_FOR_SEAL", None):
            with self.subTest(status=status):
                source_data = {"applied": [{"page": 1}]}
                if status is not None:
                    source_data["status"] = status
                result = self.run_driver("--source", str(self.source(source_data)))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout.strip().splitlines()[-1])["verdict"], "PASS")
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(),
                         ["commit", "gate", "resweep", "commit", "gate", "resweep"])

    def test_empty_applied_is_not_a_pass(self):
        for source_data in ({"status": "READY_FOR_SEAL", "applied": []}, {"applied": []}):
            with self.subTest(source_data=source_data):
                result = self.run_driver("--source", str(self.source(source_data)))
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout.strip())["verdict"], "NO_OP")
                self.assert_no_calls()

    def test_pages_without_source_and_with_ready_source(self):
        self.raw_page(3)
        # No default batch file exists: --pages alone must still work for M3.
        result = self.run_driver("--pages", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.strip().splitlines()[-1])["sealedPages"], 1)
        # An explicit ready source is checked even when --pages selects the work.
        result = self.run_driver("--source", str(self.source({"status": "READY_FOR_SEAL", "applied": []})),
                                 "--pages", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.strip().splitlines()[-1])["sealedPages"], 1)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(),
                         ["commit", "gate", "resweep", "commit", "gate", "resweep"])


if __name__ == "__main__":
    unittest.main()
