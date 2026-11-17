import hashlib
import json
import os
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
        self.previews = self.root / "preview_events.txt"
        self.inputs = self.root / "commit_inputs.txt"
        self.partial_commit = self.root / "simulate_partial_commit"
        (self.raw.parent / "BLIND_READ_MANIFEST.json").write_text('{"pages": {}}', encoding="utf-8")
        shutil.copyfile(SCRIPT, self.tools / SCRIPT.name)
        shutil.copyfile(SCRIPT.parent / "hokkien_17c_converter.py", self.tools / "hokkien_17c_converter.py")
        shutil.copyfile(SCRIPT.parent / "repair_batch_a.py", self.tools / "repair_batch_a.py")
        for name in ("minnan_engine.py", "spanish_17c_expander.py"):
            shutil.copyfile(SCRIPT.parent / name, self.tools / name)
        (self.tools / "zcode_m2_pipeline.py").write_text(
            "import hashlib, json, sys\n"
            "from pathlib import Path\n"
            "M2_DIR = Path(__file__).resolve().parent.parent / 'workspace_m2_dhs834'\n"
            f"FORMAL = Path({str(self.raw.parent)!r})\n"
            f"EVENTS = Path({str(self.events)!r})\n"
            f"PREVIEWS = Path({str(self.previews)!r})\n"
            f"INPUTS = Path({str(self.inputs)!r})\n"
            f"PARTIAL = Path({str(self.partial_commit)!r})\n"
            "def cmd_commit(input_file):\n"
            "    payload = json.loads(Path(input_file).read_text(encoding='utf-8'))\n"
            "    pages = payload.get('pages') or [payload]\n"
            "    for page in pages:\n"
            "        pg = page['pdf_page']; pk = f'{pg:04d}'\n"
            "        entries = page.get('entries') or []\n"
            "        content = (json.dumps({'pdf_page': pg, 'entries': entries}, ensure_ascii=False, indent=2) + '\\n').encode('utf-8')\n"
            "        M2_DIR.mkdir(parents=True, exist_ok=True)\n"
            "        (M2_DIR / f'blind_read_p{pk}.json').write_bytes(content)\n"
            "        if M2_DIR.resolve() == FORMAL.resolve() and Path(input_file).name.startswith('merged_seal_') and PARTIAL.exists():\n"
            "            with EVENTS.open('a', encoding='utf-8') as f: f.write('commit_partial\\n')\n"
            "            with INPUTS.open('a', encoding='utf-8') as f: f.write(str(input_file) + '\\n')\n"
            "            raise SystemExit(7)\n"
            "        manifest_path = M2_DIR / 'BLIND_READ_MANIFEST.json'\n"
            "        manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'pages': {}}\n"
            "        manifest['pages'][pk] = {'pdf_page': pg, 'entries_count': len(entries), 'blind_first_read_sha256': hashlib.sha256(content).hexdigest()}\n"
            "        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')\n"
            "        if M2_DIR.resolve() == FORMAL.resolve():\n"
            "            with EVENTS.open('a', encoding='utf-8') as f: f.write('commit\\n')\n"
            "            with INPUTS.open('a', encoding='utf-8') as f: f.write(str(input_file) + '\\n')\n"
            "        else:\n"
            "            with PREVIEWS.open('a', encoding='utf-8') as f: f.write(str(input_file) + '\\n')\n"
            "if __name__ == '__main__':\n"
            "    if len(sys.argv) != 4 or sys.argv[1:3] != ['commit', '--input']: raise SystemExit(2)\n"
            "    cmd_commit(sys.argv[3])\n",
            encoding="utf-8")
        for target, event in [
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

    def run_driver(self, *args, env=None):
        return subprocess.run([sys.executable, "-X", "utf8", str(self.tools / SCRIPT.name), *args],
                              cwd=self.root, text=True, capture_output=True, env=env)

    def seed_seal(self, page, entries):
        content = (json.dumps({"pdf_page": page, "entries": entries}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        (self.raw.parent / f"blind_read_p{page:04d}.json").write_bytes(content)
        path = self.raw.parent / "BLIND_READ_MANIFEST.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["pages"][f"{page:04d}"] = {"pdf_page": page, "entries_count": len(entries),
                                            "blind_first_read_sha256": hashlib.sha256(content).hexdigest()}
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    def raw_page(self, page):
        path = self.raw / f"raw_part_p{page:04d}.json"
        path.write_text(json.dumps({"pages": [{"pdf_page": page, "entries": []}]}), encoding="utf-8")
        self.seed_seal(page, [])
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
        raw = self.raw_page(1)
        raw.write_text(json.dumps({"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}), encoding="utf-8")
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        for status in ("READY_FOR_SEAL", None):
            with self.subTest(status=status):
                source_data = {"applied": [{"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]}
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

    def test_phonological_rewrite_defers_page_and_preserves_raw(self):
        raw = self.raw_page(1)
        raw.write_text(json.dumps({"pages": [{"pdf_page": 1, "entries": [{"position": 5, "source_M": "kiap", "source_H": "挾"}]}]},
                                  ensure_ascii=False), encoding="utf-8")
        original = raw.read_bytes()
        result = self.run_driver("--pages", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "PASS_WITH_DEFERRED")
        self.assertEqual(report["deferredLiteralPages"], [1])
        self.assertEqual(report["literalChanges"][0]["raw"], "kiap")
        self.assertEqual(report["literalChanges"][0]["sanitized"], "quiap")
        self.assertEqual(raw.read_bytes(), original)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])
        self.assertEqual(list(self.raw.glob("merged_seal_p*.json")), [])

    def test_unrecorded_changes_and_unapplied_batch_are_deferred(self):
        raw = self.raw_page(1)
        seal = self.raw.parent / "blind_read_p0001.json"
        self.seed_seal(1, [{"position": 1, "source_L": "new", "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_L": "old", "source_M": "ba"}]}]}', encoding="utf-8")
        result = self.run_driver("--pages", "1")
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["deferredUnexpectedPages"], [1])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_L": "new", "source_M": "ba"}]}]}', encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["deferredUnexpectedPages"], [1])
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep", "gate", "resweep"])
        self.assertEqual(list(self.raw.glob("merged_seal_p*.json")), [])

    def test_m3_pages_can_replace_the_whole_layout(self):
        raw = self.raw_page(30)
        raw.write_text('{"pages": [{"pdf_page": 30, "entries": [{"position": 1, "source_M": "ba"}]}]}', encoding="utf-8")
        result = self.run_driver("--pages", "30")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.strip().splitlines()[-1])["sealedPages"], 1)

    def test_raw_page_mismatch_never_commits_other_page(self):
        raw = self.raw_page(30)
        raw.write_text('{"pages": [{"pdf_page": 31, "entries": []}]}', encoding="utf-8")
        result = self.run_driver("--pages", "30")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["commitErrors"][0]["page"], 30)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])

    def test_source_pages_and_explicit_m3_pages_are_unioned(self):
        raw = self.raw_page(1)
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        self.raw_page(30)
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source), "--pages", "30")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["sealedPages"], 2)
        self.assertTrue(report["coverageOK"])
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["commit", "commit", "gate", "resweep"])

    def test_missing_raw_still_runs_gate_and_resweep(self):
        self.raw_page(1)
        result = self.run_driver("--pages", "1,2")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["commitErrors"][0]["page"], 2)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(),
                         ["commit", "gate", "resweep", "gate", "resweep"])

    def test_m3_position_must_be_unique_integer(self):
        raw = self.raw_page(30)
        raw.write_text('{"pages": [{"pdf_page": 30, "entries": [{"position": {"column": "L", "row": 1}}]}]}', encoding="utf-8")
        result = self.run_driver("--pages", "30")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["commitErrors"][0]["page"], 30)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])

    def test_resweep_failure_restores_seal_manifest_and_baseline(self):
        raw = self.raw_page(1)
        seal = self.raw.parent / "blind_read_p0001.json"
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        baseline = self.raw.parent / "collision_mr" / "PHONOTACTICS_BASELINE.json"
        baseline.parent.mkdir(parents=True)
        baseline.write_text('{"hardTotal": 1}', encoding="utf-8")
        before = {p: p.read_bytes() for p in (raw, seal, manifest, baseline)}
        (self.tools / "post_repair_verify.py").write_text(
            "from pathlib import Path\n"
            f"p=Path({str(self.events)!r}); old=p.read_text(encoding='utf-8') if p.exists() else ''\n"
            "with p.open('a', encoding='utf-8') as f: f.write('resweep\\n')\n"
            "if 'resweep' not in old:\n"
            f"    Path({str(baseline)!r}).write_text('changed', encoding='utf-8')\n"
            "    raise SystemExit(2)\n"
            "print('ok')\n",
            encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertNotEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual((report["verdict"], report["sealedPages"], report["attemptedSealedPages"]), ("FAIL", 0, 1))
        self.assertTrue(report["rolledBack"])
        self.assertIsNone(report["rollbackError"])
        self.assertTrue(report["rollbackGatePass"])
        self.assertEqual(report["rollbackResweepExit"], 0)
        self.assertTrue(all(path.read_bytes() == data for path, data in before.items()))
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(),
                         ["commit", "gate", "resweep", "commit", "gate", "resweep"])
        inputs = [Path(x).name for x in self.inputs.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(inputs, ["merged_seal_p0001.json", "rollback_raw_p0001.json"])
        previews = [Path(x).name for x in self.previews.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(previews, ["rollback_raw_p0001.json", "candidate_raw_p0001.json"])

    def test_same_page_external_change_is_not_overwritten_during_rollback(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        external = (json.dumps({"pdf_page": 1, "entries": [{"position": 1, "source_M": "external"}]},
                               ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        entry = {"pdf_page": 1, "entries_count": 1, "blind_first_read_sha256": hashlib.sha256(external).hexdigest()}
        (self.root / "architect_gatekeeper.py").write_text(
            "import json\nfrom pathlib import Path\n"
            f"Path({str(seal)!r}).write_bytes({external!r})\n"
            f"p=Path({str(manifest)!r}); d=json.loads(p.read_text(encoding='utf-8'))\n"
            f"d['pages']['0001']={entry!r}; p.write_text(json.dumps(d), encoding='utf-8')\n"
            f"with Path({str(self.events)!r}).open('a', encoding='utf-8') as f: f.write('gate\\n')\n"
            "print('ok')\n",
            encoding="utf-8")
        (self.tools / "post_repair_verify.py").write_text(
            "from pathlib import Path\n"
            f"with Path({str(self.events)!r}).open('a', encoding='utf-8') as f: f.write('resweep\\n')\n"
            "raise SystemExit(2)\n", encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertNotEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertFalse(report["rolledBack"])
        self.assertIn("非本批变化", report["rollbackError"])
        self.assertEqual(seal.read_bytes(), external)
        self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["pages"]["0001"], entry)
        self.assertEqual([Path(x).name for x in self.inputs.read_text(encoding="utf-8").splitlines()],
                         ["merged_seal_p0001.json"])

    def test_same_page_change_after_batch_check_is_not_overwritten(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        external = (json.dumps({"pdf_page": 1, "entries": [{"position": 1, "source_M": "external"}]},
                               ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        entry = {"pdf_page": 1, "entries_count": 1, "blind_first_read_sha256": hashlib.sha256(external).hexdigest()}
        marker = self.root / "external_update_done"
        with (self.tools / "repair_batch_a.py").open("a", encoding="utf-8") as f:
            f.write("\n_original_same_entries = same_entries\n"
                    "def same_entries(sealed, raw):\n"
                    "    result = _original_same_entries(sealed, raw)\n"
                    f"    marker = Path({str(marker)!r})\n"
                    "    if result and not marker.exists():\n"
                    f"        Path({str(seal)!r}).write_bytes({external!r})\n"
                    f"        p = Path({str(manifest)!r}); d = json.loads(p.read_text(encoding='utf-8'))\n"
                    f"        d['pages']['0001'] = {entry!r}; p.write_text(json.dumps(d), encoding='utf-8')\n"
                    "        marker.write_text('done', encoding='utf-8')\n"
                    "    return result\n")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertTrue(marker.exists())
        self.assertNotEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertIn("写前封存或清册页项变化", report["commitErrors"][0]["err"])
        self.assertEqual(seal.read_bytes(), external)
        self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["pages"]["0001"], entry)
        self.assertFalse(self.inputs.exists())
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])

    def test_partial_commit_failure_recovers_via_pipeline(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        before = {p: p.read_bytes() for p in (raw, seal, manifest)}
        self.partial_commit.write_text("yes", encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertNotEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertTrue(report["rolledBack"])
        self.assertIsNone(report["rollbackError"])
        self.assertTrue(report["rollbackGatePass"])
        self.assertEqual(report["rollbackResweepExit"], 0)
        self.assertTrue(all(p.read_bytes() == value for p, value in before.items()))
        self.assertEqual([Path(x).name for x in self.inputs.read_text(encoding="utf-8").splitlines()],
                         ["merged_seal_p0001.json", "rollback_raw_p0001.json"])
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(),
                         ["commit_partial", "gate", "resweep", "commit", "gate", "resweep"])

    def test_old_seal_that_cannot_be_replayed_is_deferred(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        original = seal.read_bytes() + b" "
        seal.write_bytes(original)
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["pages"]["0001"]["blind_first_read_sha256"] = hashlib.sha256(original).hexdigest()
        manifest.write_text(json.dumps(data), encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "PASS_WITH_DEFERRED")
        self.assertEqual(report["deferredRecoveryPages"], [1])
        self.assertEqual(seal.read_bytes(), original)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])
        self.assertFalse(self.inputs.exists())

    def test_old_seal_preview_nontone_error_fails(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        before = {p: p.read_bytes() for p in (raw, seal, manifest)}
        pipeline = self.tools / "zcode_m2_pipeline.py"
        script = pipeline.read_text(encoding="utf-8")
        needle = "def cmd_commit(input_file):\n"
        self.assertIn(needle, script)
        script = script.replace(needle, needle +
                                "    if Path(input_file).name.startswith('rollback_raw_') and M2_DIR.resolve() != FORMAL.resolve():\n"
                                "        raise RuntimeError('injected nontone preview failure')\n", 1)
        pipeline.write_text(script, encoding="utf-8")
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        result = self.run_driver("--source", str(source))
        self.assertNotEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["deferredRecoveryPages"], [])
        self.assertEqual(report["commitErrors"][0]["page"], 1)
        self.assertIn("injected nontone preview failure", report["commitErrors"][0]["err"])
        self.assertTrue(all(p.read_bytes() == value for p, value in before.items()))
        self.assertFalse(self.inputs.exists())
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["gate", "resweep"])

    def test_invalid_applied_row_is_rejected_before_any_commit(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        original = seal.read_bytes()
        valid = {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}
        for invalid in (
            {"page": 2, "position": {}, "field": "source_M", "old": "ba", "new": "ca"},
            {"page": 2, "position": 1, "field": "source_H", "old": "甲", "new": "乙"},
            {"page": 2, "position": 1, "field": "source_M", "old": "ba", "new": 7},
        ):
            with self.subTest(invalid=invalid):
                result = self.run_driver("--source", str(self.source({"status": "READY_FOR_SEAL",
                                                                     "applied": [valid, invalid]})))
                self.assertNotEqual(result.returncode, 0)
                report = json.loads(result.stdout.strip().splitlines()[-1])
                self.assertEqual((report["verdict"], report["reason"]), ("FAIL", "source_applied_invalid"))
                self.assertEqual(seal.read_bytes(), original)
                self.assert_no_calls()
                self.assertFalse(self.inputs.exists())

    def test_nonlist_tone_is_deferred_without_skipping_gate_and_resweep(self):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        raw2 = self.raw_page(2)
        self.seed_seal(2, [{"position": 1, "source_M": "ba"}])
        raw2.write_text('{"pages": [{"pdf_page": 2, "entries": [{"position": 1, "source_M": "ba", "tone_marks_M": 1}]}]}', encoding="utf-8")
        seal2 = self.raw.parent / "blind_read_p0002.json"
        before2 = (raw2.read_bytes(), seal2.read_bytes())
        raw3 = self.raw_page(3)
        self.seed_seal(3, [{"position": 1, "source_M": "ba"}])
        raw3.write_text('{"pages": [{"pdf_page": 3, "entries": [{"position": 1, "source_M": "ba", "tone_marks_M": 0}]}]}', encoding="utf-8")
        seal3 = self.raw.parent / "blind_read_p0003.json"
        before3 = (raw3.read_bytes(), seal3.read_bytes())
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"},
            {"page": 2, "position": 1, "field": "source_M", "old": "ba", "new": "ba"},
            {"page": 3, "position": 1, "field": "source_M", "old": "ba", "new": "ba"}]})
        result = self.run_driver("--source", str(source))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual((report["verdict"], report["sealedPages"], report["deferredTonePages"]),
                         ("PASS_WITH_DEFERRED", 1, [2, 3]))
        self.assertTrue(report["gatePass"])
        self.assertEqual(report["resweepExit"], 0)
        self.assertEqual((raw2.read_bytes(), seal2.read_bytes()), before2)
        self.assertEqual((raw3.read_bytes(), seal3.read_bytes()), before3)
        self.assertEqual(self.events.read_text(encoding="utf-8").splitlines(), ["commit", "gate", "resweep"])

    def check_subprocess_oserror_rolls_back(self, failed_program):
        raw = self.raw_page(1)
        self.seed_seal(1, [{"position": 1, "source_M": "ba"}])
        raw.write_text('{"pages": [{"pdf_page": 1, "entries": [{"position": 1, "source_M": "ca"}]}]}', encoding="utf-8")
        seal = self.raw.parent / "blind_read_p0001.json"
        manifest = self.raw.parent / "BLIND_READ_MANIFEST.json"
        before = {p: p.read_bytes() for p in (raw, seal, manifest)}
        source = self.source({"status": "READY_FOR_SEAL", "applied": [
            {"page": 1, "position": 1, "field": "source_M", "old": "ba", "new": "ca"}]})
        hook = self.root / "subprocess_hook"
        hook.mkdir()
        marker = hook / "failure_injected"
        (hook / "sitecustomize.py").write_text(
            "import subprocess\nfrom pathlib import Path\n"
            "original = subprocess.run\n"
            "def injected(command, *args, **kwargs):\n"
            f"    marker = Path({str(marker)!r})\n"
            f"    if len(command) > 1 and Path(str(command[1])).name == {failed_program!r} and not marker.exists():\n"
            "        marker.write_text('done', encoding='utf-8')\n"
            "        raise OSError('injected subprocess failure')\n"
            "    return original(command, *args, **kwargs)\n"
            "subprocess.run = injected\n", encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(hook) + os.pathsep + env.get("PYTHONPATH", "")
        result = self.run_driver("--source", str(source), env=env)
        self.assertTrue(marker.exists())
        self.assertNotEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.strip().splitlines()
        self.assertTrue(lines and lines[-1].startswith("{"), (result.stdout, result.stderr))
        report = json.loads(lines[-1])
        self.assertEqual(report["verdict"], "FAIL")
        self.assertTrue(report["rolledBack"])
        self.assertIsNone(report["rollbackError"])
        self.assertTrue(report["rollbackGatePass"])
        self.assertEqual(report["rollbackResweepExit"], 0)
        self.assertTrue(all(p.read_bytes() == value for p, value in before.items()))
        self.assertEqual([Path(x).name for x in self.inputs.read_text(encoding="utf-8").splitlines()],
                         ["merged_seal_p0001.json", "rollback_raw_p0001.json"])

    def test_gate_subprocess_oserror_runs_pipeline_rollback(self):
        self.check_subprocess_oserror_rolls_back("architect_gatekeeper.py")

    def test_resweep_subprocess_oserror_runs_pipeline_rollback(self):
        self.check_subprocess_oserror_rolls_back("post_repair_verify.py")


if __name__ == "__main__":
    unittest.main()
