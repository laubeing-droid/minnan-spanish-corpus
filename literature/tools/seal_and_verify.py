#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复批一键落地驱动器（硬刹车 #12 的管线化）。

用法：python literature/tools/seal_and_verify.py [--source REPAIR_BATCH_A_V4.json] [--pages 0030,0031]

流程：
  1. 从修复批报告读脏页（默认 REPAIR_BATCH_A_V4.json 的 applied[].page）；
  2. 逐页重封（含存量非规范调标字面的页**单页跳过入账**——学 p0041 先例，修复留 raw 不丢）；
  3. 跑 architect_gatekeeper.py 全库门禁；
  4. 跑 post_repair_verify.py 强制复扫（硬违类单调下降断言，熔断退出 2）。
任一环节 FAIL：退出码非 0，报告指明卡在哪一步——**不带病宣布完成**。
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from copy import deepcopy
from pathlib import Path

from hokkien_17c_converter import sanitize_17c_missionary_orthography
from repair_batch_a import FIELDS, by_position, same_entries

TOOLS = Path(__file__).resolve().parent
M2 = TOOLS.parent / "workspace_m2_dhs834"
ALLOWED = {"T00 (無標號)", "T01 (升斜)", "T02 (降斜)", "T03 (尖頂帽)", "T04 (凹角)",
           "T05 (平橫)", "T06/T07 (交叉入聲號)", "T99 (污損難辨)"}

args = sys.argv[1:]
source = M2 / "collision_mr" / "REPAIR_BATCH_A_V4.json"
rep = {"applied": []}
if "--source" in args:
    source = Path(args[args.index("--source") + 1])
if "--source" in args or "--pages" not in args:
    rep = json.loads(source.read_text(encoding="utf-8"))
    if isinstance(rep, dict) and "status" in rep and rep["status"] != "READY_FOR_SEAL":
        print(json.dumps({"verdict": "FAIL", "reason": "source_not_ready", "status": rep["status"]}, ensure_ascii=False))
        sys.exit(1)
    if (not isinstance(rep, dict) or not isinstance(rep.get("applied", []), list) or
            any(not isinstance(a, dict) or type(a.get("page")) is not int or type(a.get("position")) is not int or
                a.get("field") not in ("source_M", "source_R") or not isinstance(a.get("old"), str) or
                not isinstance(a.get("new"), str) for a in rep.get("applied", []))):
        print(json.dumps({"verdict": "FAIL", "reason": "source_applied_invalid"}, ensure_ascii=False))
        sys.exit(1)
if "--pages" in args:
    pages = {int(x) for x in args[args.index("--pages") + 1].split(",")}
    if "--source" in args:
        pages.update(int(a["page"]) for a in rep.get("applied", []))
    pages = sorted(pages)
else:
    pages = sorted({int(a["page"]) for a in rep.get("applied", [])})
    # 页集覆盖：显式脏页（如 M3 两栏重构新增页）可经 --pages 注入，默认取修复批账
if not pages:
    print(json.dumps({"verdict": "NO_OP", "reason": "no_pages"}, ensure_ascii=False))
    sys.exit(1)
print("[seal] 修复批脏页:", len(pages))
manifest_path = M2 / "BLIND_READ_MANIFEST.json"
baseline_path = M2 / "collision_mr" / "PHONOTACTICS_BASELINE.json"
manifest_before = None
baseline_before = baseline_path.read_bytes() if baseline_path.exists() else None
sealed_before = {}
before_entries = {}
expected_after = {}
rollback_inputs = {}
rollback_hashes = {}
recovery_dir = Path(tempfile.mkdtemp(prefix="codex_seal_recovery_"))
print("[seal] 回滚材料:", recovery_dir)
tool_names = ("zcode_m2_pipeline.py", "minnan_engine.py", "spanish_17c_expander.py", "hokkien_17c_converter.py")
tool_hashes = {name: hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() for name in tool_names}


def restore_baseline(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        temp.write(data)
        temp_name = temp.name
    os.replace(temp_name, path)
    if path.read_bytes() != data:
        raise OSError(f"回滚字节不一致: {path}")


def preview_commit(input_path, probe_dir, pk):
    probe_tools = probe_dir / "literature" / "tools"
    probe_tools.mkdir(parents=True, exist_ok=True)
    for name in tool_names:
        shutil.copyfile(TOOLS / name, probe_tools / name)
    result = subprocess.run([sys.executable, "-X", "utf8", str(probe_tools / "zcode_m2_pipeline.py"),
                             "commit", "--input", str(input_path)], capture_output=True, text=True)
    if result.returncode:
        raise ValueError("隔离 commit 失败: " + (result.stderr or result.stdout)[-200:])
    probe_m2 = probe_dir / "literature" / "workspace_m2_dhs834"
    page_bytes = (probe_m2 / ("blind_read_p" + pk + ".json")).read_bytes()
    entry = json.loads((probe_m2 / "BLIND_READ_MANIFEST.json").read_bytes())["pages"][pk]
    return page_bytes, entry


def run_check(script):
    try:
        return subprocess.run([sys.executable, str(script)], capture_output=True, text=True), None
    except (OSError, UnicodeError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
# 1. 逐页重封（存量非规范调标页单页跳过；其余 commit 错误判 FAIL 不与调标延迟混类）
ok = []
defer_tone = []
defer_literal = []
literal_changes = []
defer_unexpected = []
defer_recovery = []
commit_errors = []
for pg in pages:
    pk = "%04d" % pg
    try:
        raw = json.loads((M2 / ("raw_blind/raw_part_p" + pk + ".json")).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        commit_errors.append({"page": pg, "err": f"读取 raw 失败: {exc}"})
        print("[seal] p%s COMMIT_ERROR: 读取 raw 失败: %s" % (pk, exc))
        continue
    if not isinstance(raw, dict):
        commit_errors.append({"page": pg, "err": "raw 顶层不是对象"})
        continue
    bad_tone = False
    raw_pages = raw.get("pages") or [raw]
    if (not isinstance(raw_pages, list) or len(raw_pages) != 1 or
            not isinstance(raw_pages[0], dict) or raw_pages[0].get("pdf_page") != pg):
        commit_errors.append({"page": pg, "err": "raw 文件页号与请求页不一致"})
        print("[seal] p%s COMMIT_ERROR: raw 文件页号与请求页不一致" % pk)
        continue
    entries = raw_pages[0].get("entries")
    if (not isinstance(entries, list) or any(not isinstance(e, dict) or type(e.get("position")) is not int for e in entries)
            or len({e["position"] for e in entries}) != len(entries)):
        commit_errors.append({"page": pg, "err": "条目 position 须为互不重复的整数"})
        print("[seal] p%s COMMIT_ERROR: 条目 position 须为互不重复的整数" % pk)
        continue
    for p0 in raw_pages:
        for e in (p0.get("entries") or []):
            for fld in ("tone_marks_M", "tone_marks_R"):
                tones = e.get(fld)
                if tones is None:
                    tones = []
                if not isinstance(tones, list):
                    bad_tone = True
                    break
                for t in tones:
                    if str(t).strip() not in ALLOWED:
                        bad_tone = True
                        break
                if bad_tone:
                    break
            if bad_tone:
                break
        if bad_tone:
            break
    if bad_tone:
        defer_tone.append(pg)
        print("[seal] p%s 延迟：含存量非规范调标字面（修复留 raw，待调标线）" % pk)
        continue
    changed = []
    for p0 in raw_pages:
        for e in p0.get("entries") or []:
            value = str(e.get("source_M") or "").strip()
            output = sanitize_17c_missionary_orthography(value, str(e.get("source_H") or "").strip())
            if unicodedata.normalize("NFC", value) != unicodedata.normalize("NFC", output):
                changed.append({"page": pg, "position": e.get("position"), "raw": value, "sanitized": output})
    if changed:
        defer_literal.append(pg)
        literal_changes.extend(changed)
        print("[seal] p%s 延迟：净化将改写 %d 条字面音写" % (pk, len(changed)))
        continue
    try:
        if manifest_before is None:
            manifest_before = manifest_path.read_bytes()
        manifest_snapshot = json.loads(manifest_before)
        seal_path = M2 / ("blind_read_p" + pk + ".json")
        original = seal_path.read_bytes()
        original_entry = manifest_snapshot["pages"][pk]
        current_entry = json.loads(manifest_path.read_bytes())["pages"].get(pk)
        if current_entry != original_entry:
            raise ValueError("清册页项在批次开始后变化")
        sealed = json.loads(original)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        commit_errors.append({"page": pg, "err": f"读取封存基准失败: {exc}"})
        print("[seal] p%s COMMIT_ERROR: 读取封存基准失败: %s" % (pk, exc))
        continue
    if pg not in range(30, 41):
        try:
            expected = deepcopy(sealed["entries"])
            expected_by_pos = by_position(expected)
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            commit_errors.append({"page": pg, "err": f"读取封存基准失败: {exc}"})
            print("[seal] p%s COMMIT_ERROR: 读取封存基准失败: %s" % (pk, exc))
            continue
        intended = [a for a in rep.get("applied", []) if a.get("page") == pg]
        valid = True
        for a in intended:
            pos, field = a.get("position"), a.get("field")
            if (pos not in expected_by_pos or field not in FIELDS or "old" not in a or "new" not in a or
                    expected_by_pos[pos].get(field) not in (a["old"], a["new"])):
                valid = False
                break
            expected_by_pos[pos][field] = a["new"]
        if not valid or not same_entries(expected, raw_pages[0].get("entries") or []):
            defer_unexpected.append(pg)
            print("[seal] p%s 延迟：raw 与现封存及批次 old/new 不一致" % pk)
            continue
    out = M2 / ("raw_blind/merged_seal_p" + pk + ".json")
    try:
        backup = recovery_dir / ("rollback_raw_p" + pk + ".json")
        backup.write_bytes(json.dumps({"pages": [json.loads(original)]}, ensure_ascii=False, indent=2).encode("utf-8"))
        try:
            old_proof = preview_commit(backup, recovery_dir / ("old_" + pk), pk)
        except ValueError as exc:
            if "非规范调标" not in str(exc):
                raise
            defer_recovery.append(pg)
            print("[seal] p%s 延迟：原封存回滚预演失败: %s" % (pk, exc))
            continue
        if old_proof != (original, original_entry):
            defer_recovery.append(pg)
            print("[seal] p%s 延迟：原封存无法经 commit 精确重建" % pk)
            continue
        candidate = recovery_dir / ("candidate_raw_p" + pk + ".json")
        candidate.write_bytes(json.dumps(raw, ensure_ascii=False, indent=2).encode("utf-8"))
        expected_after[pk] = preview_commit(candidate, recovery_dir / ("new_" + pk), pk)
        receipt = {"page": pg, "originalSealSha256": hashlib.sha256(original).hexdigest(),
                   "rollbackRawSha256": hashlib.sha256(backup.read_bytes()).hexdigest(),
                   "candidateRawSha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                   "expectedSealSha256": hashlib.sha256(expected_after[pk][0]).hexdigest(),
                   "originalManifestEntry": original_entry, "expectedManifestEntry": expected_after[pk][1],
                   "toolSha256": tool_hashes}
        (recovery_dir / ("receipt_p" + pk + ".json")).write_bytes(
            json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
        current = (seal_path.read_bytes(), json.loads(manifest_path.read_bytes())["pages"].get(pk))
        if current != (original, original_entry):
            commit_errors.append({"page": pg, "err": "写前封存或清册页项变化；未覆盖"})
            continue
        if any(hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() != sha for name, sha in tool_hashes.items()):
            commit_errors.append({"page": pg, "err": "commit 工具在预演后变化；未覆盖"})
            continue
        sealed_before[pk], before_entries[pk], rollback_inputs[pk] = original, original_entry, backup
        rollback_hashes[pk] = receipt["rollbackRawSha256"]
        out.write_bytes(json.dumps(raw, ensure_ascii=False, indent=1).encode("utf-8"))
        r = subprocess.run([sys.executable, str(TOOLS / "zcode_m2_pipeline.py"),
                            "commit", "--input", str(out)], capture_output=True, text=True)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        commit_errors.append({"page": pg, "err": f"准备或执行 commit 失败: {exc}"})
        print("[seal] p%s COMMIT_ERROR: 准备或执行 commit 失败: %s" % (pk, exc))
        continue
    if r.returncode == 0:
        try:
            actual = (seal_path.read_bytes(), json.loads(manifest_path.read_bytes())["pages"][pk])
        except (OSError, ValueError, KeyError, TypeError) as exc:
            commit_errors.append({"page": pg, "err": f"读取 commit 结果失败: {exc}"})
            continue
        if actual != expected_after[pk]:
            commit_errors.append({"page": pg, "err": "commit 结果与隔离预演不同"})
            continue
        ok.append(pg)
    else:
        err = (r.stderr or r.stdout or "")
        try:
            unchanged = (seal_path.read_bytes() == original and
                         json.loads(manifest_path.read_bytes())["pages"].get(pk) == original_entry)
        except (OSError, ValueError, KeyError, TypeError):
            unchanged = False
        if unchanged and ("非规范调标" in err or "normalize_tone_list" in err):
            defer_tone.append(pg)
            print("[seal] p%s 延迟：非规范调标（修复留 raw）" % pk)
        else:
            commit_errors.append({"page": pg, "err": err[-200:]})
            print("[seal] p%s COMMIT_ERROR:" % pk, err[-200:])
print("[seal] 重封完成: %d 页 OK / %d 页调标延迟 / %d 页字面延迟 / %d 页差异延迟 / %d 页回滚预演延迟 / %d 页 commit 错误"
      % (len(ok), len(defer_tone), len(defer_literal), len(defer_unexpected), len(defer_recovery), len(commit_errors)))

# 1b. 覆盖断言：处理页 + 延迟页 + 错误页 必须等于输入页集（Codex RSI 提案）
covered = set(ok) | set(defer_tone) | set(defer_literal) | set(defer_unexpected) | set(defer_recovery) | {c["page"] for c in commit_errors}
coverage_ok = covered == set(pages)
print("[seal] 页集覆盖断言:", "OK" if coverage_ok else "FAIL %s"
      % sorted(set(pages) - covered))

# 2. 全库门禁
ROOT = TOOLS.parent.parent
gate, gate_error = run_check(ROOT / "architect_gatekeeper.py")
gate_pass = gate is not None and gate.returncode == 0 and "[FAIL]" not in gate.stdout
print("[gate]", "PASS" if gate_pass else "FAIL")

# 3. 强制复扫（硬刹车 #12）
pv, resweep_error = run_check(TOOLS / "post_repair_verify.py")
resweep_exit = pv.returncode if pv is not None else -1
print("[resweep]", (pv.stdout or "").strip()[-400:] if pv is not None else resweep_error)
print("[resweep] exit:", resweep_exit)
baseline_error = None
try:
    baseline_after = baseline_path.read_bytes() if baseline_path.exists() else None
except OSError as exc:
    baseline_after = None
    baseline_error = str(exc)

failed = not gate_pass or resweep_exit != 0 or bool(commit_errors) or not coverage_ok or baseline_error is not None
rolled_back = False
rollback_error = None
if failed and sealed_before:
    try:
        if any(hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() != sha for name, sha in tool_hashes.items()):
            raise ValueError("commit 工具在预演后变化，未执行回滚")
        current_pages = json.loads(manifest_path.read_bytes())["pages"]
        for pk, original in sealed_before.items():
            actual = (M2 / ("blind_read_p" + pk + ".json")).read_bytes()
            current_entry = current_pages.get(pk)
            expected_page, expected_entry = expected_after[pk]
            if ((actual, current_entry) != (original, before_entries[pk]) and
                    not (actual == expected_page and current_entry in (expected_entry, before_entries[pk]))):
                raise ValueError(f"p{pk} 或清册已发生非本批变化，未覆盖其他工作")
        for pk, original in sealed_before.items():
            current_pages = json.loads(manifest_path.read_bytes())["pages"]
            actual = (M2 / ("blind_read_p" + pk + ".json")).read_bytes()
            if (actual, current_pages.get(pk)) == (original, before_entries[pk]):
                continue
            expected_page, expected_entry = expected_after[pk]
            if actual != expected_page or current_pages.get(pk) not in (expected_entry, before_entries[pk]):
                raise ValueError(f"p{pk} 在回滚前发生非本批变化，未覆盖其他工作")
            if hashlib.sha256(rollback_inputs[pk].read_bytes()).hexdigest() != rollback_hashes[pk]:
                raise ValueError(f"p{pk} 回滚 raw 摘要不一致")
            r = subprocess.run([sys.executable, str(TOOLS / "zcode_m2_pipeline.py"),
                                "commit", "--input", str(rollback_inputs[pk])], capture_output=True, text=True)
            if r.returncode:
                raise ValueError(f"p{pk} 回滚 commit 失败: " + (r.stderr or r.stdout)[-200:])
            restored = ((M2 / ("blind_read_p" + pk + ".json")).read_bytes(),
                        json.loads(manifest_path.read_bytes())["pages"].get(pk))
            if restored != (original, before_entries[pk]):
                raise ValueError(f"p{pk} 回滚后与原封存或原清册页项不一致")
        rolled_back = True
    except (OSError, ValueError, KeyError, TypeError) as exc:
        rollback_error = str(exc)
if failed:
    try:
        if baseline_error:
            raise OSError("无法读取复扫基线: " + baseline_error)
        current_baseline = baseline_path.read_bytes() if baseline_path.exists() else None
        if current_baseline != baseline_after:
            raise OSError("复扫基线在检查后变化，未覆盖其他工作")
        if baseline_before is None:
            if baseline_path.exists():
                baseline_path.unlink()
        else:
            restore_baseline(baseline_path, baseline_before)
    except OSError as exc:
        rollback_error = "; ".join(filter(None, (rollback_error, str(exc))))

rollback_gate_pass = None
rollback_resweep_exit = None
if rolled_back and not rollback_error:
    check, _ = run_check(ROOT / "architect_gatekeeper.py")
    rollback_gate_pass = check is not None and check.returncode == 0 and "[FAIL]" not in check.stdout
    resweep, _ = run_check(TOOLS / "post_repair_verify.py")
    rollback_resweep_exit = resweep.returncode if resweep is not None else -1
    if not rollback_gate_pass or rollback_resweep_exit:
        rollback_error = "回滚后门禁或复扫失败"
    try:
        if baseline_before is None:
            if baseline_path.exists():
                baseline_path.unlink()
        elif baseline_path.read_bytes() != baseline_before:
            restore_baseline(baseline_path, baseline_before)
    except OSError as exc:
        rollback_error = "; ".join(filter(None, (rollback_error, str(exc))))

verdict = "FAIL" if failed or rollback_error else \
          "PASS_WITH_DEFERRED" if defer_tone or defer_literal or defer_unexpected or defer_recovery else "PASS"
sealed_count = None if rollback_error else 0 if rolled_back else len(ok)
print(json.dumps({"verdict": verdict, "sealedPages": sealed_count, "attemptedSealedPages": len(ok),
                  "deferredTonePages": defer_tone, "deferredLiteralPages": defer_literal,
                  "deferredUnexpectedPages": defer_unexpected, "deferredRecoveryPages": defer_recovery,
                  "literalChanges": literal_changes, "commitErrors": commit_errors,
                  "coverageOK": coverage_ok, "gatePass": gate_pass, "gateError": gate_error,
                  "resweepExit": resweep_exit, "resweepError": resweep_error,
                  "rolledBack": rolled_back, "rollbackError": rollback_error,
                  "rollbackGatePass": rollback_gate_pass, "rollbackResweepExit": rollback_resweep_exit,
                  "recoveryDir": str(recovery_dir)}, ensure_ascii=False))
# Codex RSI 提案采纳：commit 错误（非调标延迟）→ 最终 FAIL 非零退出，不得当成功
sys.exit(0 if not failed and not rollback_error else 1)
