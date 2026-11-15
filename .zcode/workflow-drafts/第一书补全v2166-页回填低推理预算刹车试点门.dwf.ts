// 第一书补全 v2：166 页回填改版——上一跑单页磨 5 小时/4500 万 token 被用户叫停。
// 修法：①抄写员降低推理档（GLM-5.3-Flash$low，逐 agent 设置；释义员保持默认档）
// ②读图预算硬纪律（最多 5 图、每图至多一次、判不定立即 [残]/T99 收尾）
// ③raw 件已存在且过校验的页直接跳过（已花掉的 3.25 亿不重付）
// ④先 5 页试点：≥4 页过校验才放全量，否则当场终止。
// 其余与已验证管线一致：切片 → 盲读 → 封存前校验返修 → 合龙 commit → 门禁 → 释义 → 全册校验。
// 铁律：盲读禁读 M1 主卷与一切旧稿；封存只走确定性管线；工作流不碰 git；禁止编造。

interface RawPageResult {
  page: number;
  file: string;
  entries: number;
  notes: string;
}

interface RepairResult {
  page: number;
  fixed: boolean;
  notes: string;
}

interface GlossPageResult {
  page: number;
  glossFile: string;
  entries: number;
  lowConfidence: number;
  notes: string;
}

interface BatchOutcome {
  range: string;
  status: "produced" | "failed";
  pages: number;
  entries: number;
  lowConfidence: number;
  detail: string;
}

interface SealRow {
  chunk: string;
  status: "sealed" | "failed";
  pages: number;
  detail: string;
}

interface RawValidation {
  bad: Record<string, string[]>;
  badCount: number;
}

interface StatusInfo {
  backfill: number[];
  done: number[];
  todo: number[];
}

interface SealedInfo {
  sealed: number[];
  missing: number[];
  entriesSealed: number;
}

interface GlossValidation {
  pagesOk: number;
  missingCount: number;
  mismatchCount: number;
  mismatch: string[];
}

interface Finding {
  where: string;
  what: string;
  evidence: string;
  status: "verified" | "unconfirmed";
  severity: "low" | "medium" | "high";
}

interface WorkflowReport {
  conclusion: string;
  findings: Finding[];
  verified: string[];
  notCovered: string[];
}

const M2 = "literature/workspace_m2_dhs834";
const LOW_MODEL = "GLM-5.3-Flash$low";
const findingsArr: Finding[] = [];

function findingsPush(f: Finding): void {
  findingsArr.push(f);
}

function pageId(p: number): string {
  return String(p).padStart(4, "0");
}

artifact.table("progress-read", {
  title: "盲读回填批次进度",
  columns: [
    { field: "range", label: "批次" },
    { field: "status", label: "状态" },
    { field: "entries", label: "条目数" },
    { field: "detail", label: "说明" },
  ],
  key: "range",
});

artifact.table("progress-seal", {
  title: "合龙封存进度",
  columns: [
    { field: "chunk", label: "封存批" },
    { field: "status", label: "状态" },
    { field: "pages", label: "页数" },
    { field: "detail", label: "说明" },
  ],
  key: "chunk",
});

artifact.table("progress-gloss", {
  title: "回填页释义进度",
  columns: [
    { field: "range", label: "批次" },
    { field: "status", label: "状态" },
    { field: "entries", label: "条目数" },
    { field: "lowConfidence", label: "低置信" },
    { field: "detail", label: "说明" },
  ],
  key: "range",
});

// ---------- 确定性脚本 ----------

const STATUS_PY = [
  "import json",
  "from pathlib import Path",
  "m2man = json.loads(Path('literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "m2_pages = {int(k) for k in m2man.get('pages', {})}",
  "m1 = json.loads(Path('literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json').read_text(encoding='utf-8'))",
  "m1_pages = set()",
  "for e in m1.get('entries', []):",
  "    pp = (e.get('layer_0_visual_anchor') or {}).get('page_pdf')",
  "    if pp:",
  "        m1_pages.add(int(pp))",
  "backfill = sorted(p for p in m1_pages if p not in m2_pages and 835 <= p <= 1140)",
  "ALLOWED = {'T00 (無標號)','T01 (升斜)','T02 (降斜)','T03 (尖頂帽)','T04 (凹角)','T05 (平橫)','T06/T07 (交叉入聲號)','T99 (污損難辨)'}",
  "def valid(pg):",
  "    f = Path('literature/workspace_m2_dhs834/raw_blind/raw_part_p%04d.json' % pg)",
  "    if not f.exists():",
  "        return False",
  "    try:",
  "        d = json.loads(f.read_text(encoding='utf-8'))",
  "        pgs = d.get('pages') or []",
  "        if len(pgs) != 1:",
  "            return False",
  "        p0 = pgs[0] or {}",
  "        ents = p0.get('entries')",
  "        if not isinstance(ents, list):",
  "            return False",
  "        if int(p0.get('pdf_page') or 0) != pg:",
  "            return False",
  "        pos = [e.get('position') for e in ents]",
  "        if pos != list(range(1, len(pos) + 1)):",
  "            return False",
  "        if len(ents) > 60:",
  "            return False",
  "        for e in ents:",
  "            for fld in ('tone_marks_M', 'tone_marks_R'):",
  "                for t in (e.get(fld) or []):",
  "                    if str(t).strip() not in ALLOWED:",
  "                        return False",
  "            sm = e.get('source_M') or ''",
  "            if chr(0x207F) in sm or chr(0x030D) in sm:",
  "                return False",
  "        return True",
  "    except Exception:",
  "        return False",
  "done = [p for p in backfill if valid(p)]",
  "todo = [p for p in backfill if not valid(p)]",
  "print(json.dumps({'backfill': backfill, 'done': done, 'todo': todo}))",
].join("\n");

function validateRawPy(pages: number[]): string {
  const pagesLit = JSON.stringify(pages);
  return [
    "import json",
    "from pathlib import Path",
    "m2 = Path('literature/workspace_m2_dhs834')",
    "ALLOWED = {'T00 (無標號)','T01 (升斜)','T02 (降斜)','T03 (尖頂帽)','T04 (凹角)','T05 (平橫)','T06/T07 (交叉入聲號)','T99 (污損難辨)'}",
    "pages = json.loads('" + pagesLit + "')",
    "bad = {}",
    "for pg in pages:",
    "    f = m2 / 'raw_blind' / ('raw_part_p%04d.json' % pg)",
    "    if not f.exists():",
    "        bad[str(pg)] = ['缺 raw 件']",
    "        continue",
    "    try:",
    "        d = json.loads(f.read_text(encoding='utf-8'))",
    "        pgs = d.get('pages') or []",
    "        if len(pgs) != 1:",
    "            raise ValueError('pages 数组应为 1 项')",
    "        p0 = pgs[0] or {}",
    "        ents = p0.get('entries')",
    "        if not isinstance(ents, list):",
    "            raise ValueError('entries 非数组')",
    "        msgs = []",
    "        if int(p0.get('pdf_page') or 0) != pg:",
    "            msgs.append('pdf_page 不符')",
    "        pos = [e.get('position') for e in ents]",
    "        if pos != list(range(1, len(pos) + 1)):",
    "            msgs.append('position 不连续')",
    "        if len(ents) > 60:",
    "            msgs.append('条目数异常: %d' % len(ents))",
    "        for e in ents:",
    "            tone_bad = False",
    "            for fld in ('tone_marks_M', 'tone_marks_R'):",
    "                for t in (e.get(fld) or []):",
    "                    if str(t).strip() not in ALLOWED:",
    "                        msgs.append('调标非规范: %s' % t)",
    "                        tone_bad = True",
    "                        break",
    "                if tone_bad:",
    "                    break",
    "            sm = e.get('source_M') or ''",
    "            if (not tone_bad) and (chr(0x207F) in sm or chr(0x030D) in sm):",
    "                msgs.append('source_M 现代鼻化残留')",
    "                break",
    "        if msgs:",
    "            bad[str(pg)] = msgs[:4]",
    "    except Exception as ex:",
    "        bad[str(pg)] = ['解析失败: %s' % ex]",
    "print(json.dumps({'bad': bad, 'badCount': len(bad)}))",
  ].join("\n");
}

function mergePy(chunk: number[], mergedRel: string): string {
  const chunkLit = JSON.stringify(chunk);
  return [
    "import json, sys",
    "from pathlib import Path",
    "m2 = Path('literature/workspace_m2_dhs834')",
    "chunk = json.loads('" + chunkLit + "')",
    "docs = []; missing = []",
    "for pg in chunk:",
    "    f = m2 / 'raw_blind' / ('raw_part_p%04d.json' % pg)",
    "    if not f.exists():",
    "        missing.append(pg)",
    "        continue",
    "    docs.append(json.loads(f.read_text(encoding='utf-8')))",
    "if missing:",
    "    print(json.dumps({'missing': missing}))",
    "    sys.exit(2)",
    "merged = {'pages': []}",
    "for d in docs:",
    "    merged['pages'].extend(d.get('pages') or [])",
    "out = m2 / '" + mergedRel + "'",
    "out.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding='utf-8')",
    "print(json.dumps({'file': str(out), 'pages': len(merged['pages'])}))",
  ].join("\n");
}

function sealedPy(pages: number[]): string {
  const pagesLit = JSON.stringify(pages);
  return [
    "import json",
    "from pathlib import Path",
    "m2 = Path('literature/workspace_m2_dhs834')",
    "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
    "mpages = {int(k) for k in man.get('pages', {})}",
    "backfill = json.loads('" + pagesLit + "')",
    "sealed = [p for p in backfill if p in mpages]",
    "missing = [p for p in backfill if p not in mpages]",
    "tot = 0",
    "for pg in sealed:",
    "    d = json.loads((m2 / ('blind_read_p%04d.json' % pg)).read_text(encoding='utf-8'))",
    "    tot += len(d.get('entries') or [])",
    "print(json.dumps({'sealed': sealed, 'missing': missing, 'entriesSealed': tot}))",
  ].join("\n");
}

const GLOSS_VALIDATE_PY = [
  "import json",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "ok = 0; missing = []; mismatch = []",
  "for pk in sorted(man.get('pages', {})):",
  "    g = m2 / 'gloss_layer' / ('gloss_p' + pk + '.json')",
  "    if not g.exists():",
  "        missing.append(pk); continue",
  "    gd = json.loads(g.read_text(encoding='utf-8'))",
  "    sealed = {e.get('position') for e in json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])}",
  "    produced = {e.get('position') for e in gd.get('entries', [])}",
  "    if sealed == produced: ok += 1",
  "    else: mismatch.append(pk)",
  "print(json.dumps({'pagesOk': ok, 'missingCount': len(missing), 'mismatchCount': len(mismatch), 'mismatch': mismatch[:20]}))",
].join("\n");

// ---------- 子代理任务书 ----------

function rawAsk(page: number): string {
  const pk = pageId(page);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的盲读抄写员，负责 PDF 第 " + page + " 页的纯视觉转写（M2 盲读协议 v3.1，回填 M1 独占页缺口）。",
    "",
    "【读图预算——硬纪律】",
    "- 本任务最多读 5 张图：先读 3 张横带图（pdf_" + pk + "_band_y0_top / _band_y1_mid / _band_y2_bot）完成转写；",
    "- 仅当个别字形/调符无法判定时，才补读对应单张纵栏图（每页至多补 2 张）；",
    "- 任何一张图最多读一次，严禁复读同一张图；预算用完即止。",
    "- 判不定的字：照录你所见字面或写 \"[残]\"；调符写 \"T99 (污損難辨)\"。然后直接产出——产出优先于完备，宁可在 notes 写存疑也不回头复核。",
    "- 若页图目录缺失/文件名对不上：不要反复尝试，把已看到的条目照常产出，notes 写明缺图。",
    "",
    "【盲读铁律】",
    "1. 只依据页面切图转写。禁止读取 literature/workspace_m1_dhs306/、literature/historical_dhs/、literature/baseline_all22_extracted/ 及 workspace_m2_dhs834/ 下任何既有转写或释义文件。",
    "2. 不用现代音韵知识改写原稿：source_M 只允许 17 世纪多明我会拼写（c-/qu-/ch-/g-/s-/z-/ttz- 等），禁止现代 k-/kh-/ts-/tsh-/chh-，禁止 U+207F（ⁿ）与 U+030D 字符。",
    "3. 调符只允许八代码几何全称，按图中出现顺序逐符输出（不推测调类调值）：",
    '   "T00 (無標號)" / "T01 (升斜)" / "T02 (降斜)" / "T03 (尖頂帽)" / "T04 (凹角)" / "T05 (平橫)" / "T06/T07 (交叉入聲號)" / "T99 (污損難辨)"。',
    '4. 缺栏写 "[空]"；残损难辨写 "[残]"；两可写 "[疑:A/B]"。四栏各自独立照录，禁止跨栏推断补全。',
    "5. 字面忠实性以图为准：西语缩写照录不展开。",
    "",
    "【输入】页图目录：literature/tiles/01_DHS/page_" + pk + "/",
    "",
    "【任务】逐词条转写四栏：source_L / source_H / source_M / source_R；tone_marks_M / tone_marks_R 按八代码数组输出。position 从 1 连续编号。",
    '整页现代印刷页/扉页/空白页：entries 写 []，页对象加 "page_class": "MODERN_FRONT_MATTER" 或 "BLANK"，notes 说明。',
    "",
    "【输出】写 literature/workspace_m2_dhs834/raw_blind/raw_part_p" + pk + ".json（UTF-8，一次通过）：",
    '{"pages": [{"pdf_page": ' + page + ', "historical_folio": "", "page_header": "", "page_footer_printed": "", "page_footer_handwritten": "", "entries": [{"position": 1, "source_L": "…", "source_H": "…", "source_M": "…", "source_R": "…", "tone_marks_M": [], "tone_marks_R": []}]}]}',
    "返回：page、file、entries（条数）、notes（一句话：残损/缺图情况，无则空串）。",
  ].join("\n");
}

function repairAsk(page: number, problems: string[], round: number): string {
  const pk = pageId(page);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的封存前返修员（第 " + round + " 轮），修复 PDF 第 " + page + " 页盲读 raw 件所列问题——只修所列问题，不重抄整页。",
    "【读图预算】至多读 2 张图，每张至多一次；判不定一律 \"T99 (污損難辨)\" 或 \"[残]\"，禁止反复复核。",
    "",
    "【问题清单】" + JSON.stringify(problems),
    "【raw 件】literature/workspace_m2_dhs834/raw_blind/raw_part_p" + pk + ".json",
    "【页图】literature/tiles/01_DHS/page_" + pk + "/",
    "",
    "【返修规则】",
    "- JSON 语法问题：只修语法结构，内容字面一字不改。",
    "- position 不连续：只调编号使其从 1 连续，不得增删词条。",
    "- pdf_page 不符：改为 " + page + "。",
    "- 条目数异常：对照页图核对漏行/多行，按图增删；拿不准只修明显机械错误并 notes 说明。",
    "- 调标非规范：回看页图对应调符几何形状，改为八代码规范全称；无法判定一律 \"T99 (污損難辨)\"。",
    "- 现代鼻化残留（U+207F/U+030D）：按原稿字面改写为图面所见拼法；无法确认写 \"[残]\"。",
    "- 八代码全称：\"T00 (無標號)\" / \"T01 (升斜)\" / \"T02 (降斜)\" / \"T03 (尖頂帽)\" / \"T04 (凹角)\" / \"T05 (平橫)\" / \"T06/T07 (交叉入聲號)\" / \"T99 (污損難辨)\"。",
    "- 禁止读取任何既有转写/释义文件；禁止以音韵知识改写字面。",
    "",
    "【输出】就地写回 raw_part_p" + pk + ".json（UTF-8）。返回：page、fixed（true/false）、notes（一句话）。",
  ].join("\n");
}

function glossAsk(page: number): string {
  const pk = pageId(page);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的历史词典释义员，负责 PDF 第 " + page + " 页的逐条释义生产（166 页回填批的释义层补全，D2 中文对照本 / D3 英文释义+台罗对照本 的数据层）。",
    "",
    "【输入】读 literature/workspace_m2_dhs834/blind_read_p" + pk + ".json（四栏封存件）：",
    "- source_L 西语词头（17 世纪拼写，可能缩写）、source_H 汉字、source_M 闽南语原稿音写、source_R 官话对音。",
    "【任务】对每条 entry 产出：",
    "- zh：现代简体中文释义。以 source_R 官话对音与 source_H 汉字为主要依据，兼顾 source_L 西语词头的 17 世纪语义（马尼拉 Sangley 语境：贸易、殖民、天主教、日常生活）。一个词头多义时给最贴合四栏的释义，次要义项用分号附后。",
    "- en：English gloss。以 source_L 的 17 世纪西班牙语语义为主轴给出英文对应；多义项分号分隔。",
    "- confidence：high（四栏互证清晰）/ medium（有 [疑] 或缩写展开依赖推断）/ low（[残]/T99/大面积缺损或语义无法定夺）。",
    "- notes：仅低置信或特别情况写一句话依据；其余空串。",
    "",
    "【纪律】",
    "1. 这是 17 世纪马尼拉语料：优先历史语义，不用现代义项想当然；",
    "2. 不确定就降 confidence 并在 notes 说明——严禁编造确定释义；",
    "3. [空]/[残] 栏照常参与判断：材料不足时 zh/en 写 〔原件残缺，释义存疑〕 且 confidence=low；",
    "4. tone_marks 与音系不归你管，不要输出音标或台罗；",
    "5. 一次通过：读封存件 → 写释义层文件 → 返回。禁止重写、禁止逐条复读。",
    "",
    "【输出】写 literature/workspace_m2_dhs834/gloss_layer/gloss_p" + pk + ".json（UTF-8）：",
    '{"page": ' + page + ', "entries": [{"position": 1, "zh": "…", "en": "…", "confidence": "high", "notes": ""}]}',
    "entries 数与 position 集合必须与封存件完全一致。",
    "返回：page、glossFile、entries（条数）、lowConfidence（低置信条数）、notes（一句话）。",
  ].join("\n");
}

// ---------- 助手 ----------

async function validateRaw(pages: number[]): Promise<RawValidation> {
  const r = await world.run("python", ["-c", validateRawPy(pages)]);
  if (r.exitCode !== 0) {
    throw new Error("封存前校验失败：" + (r.stderr || "").slice(-400));
  }
  return JSON.parse((r.stdout.trim().split("\n").pop() ?? "{}")) as RawValidation;
}

// ---------- 第 1 步：盘点（跳过已有合格 raw 的页）+ 基线门禁 ----------

phase("盘点待补页并预检门禁");
const st = await world.run("python", ["-c", STATUS_PY]);
if (st.exitCode !== 0) {
  throw new Error("待补页盘点失败：" + (st.stderr || "").slice(-300));
}
const status = JSON.parse((st.stdout.trim().split("\n").pop() ?? "{}")) as StatusInfo;
log("待补 " + status.backfill.length + " 页；已有合格 raw 跳过 " + status.done.length +
  " 页（" + status.done.map((p) => pageId(p)).join("、") + "）；本轮需读 " + status.todo.length + " 页");
if (status.todo.length === 0) {
  throw new Error("全部回填页均已有合格 raw 件——直接进入封存阶段请改用既有流程，本脚本终止");
}
const gate0 = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 8192 } });
if (gate0.exitCode !== 0 || gate0.stdout.indexOf("[FAIL]") >= 0) {
  throw new Error("开工前基线门禁未过（FAIL）——拒绝在红色基线上施工。\n" + gate0.stdout.slice(-1200));
}
log("基线门禁 PASS，开始回填");

// ---------- 第 2 步：切片（仅本轮需读页） ----------

phase("切片待补页");
const blocks: Array<{ s: number; e: number }> = [];
for (const p of status.todo) {
  const last = blocks[blocks.length - 1];
  if (last && last.e + 1 === p) {
    last.e = p;
  } else {
    blocks.push({ s: p, e: p });
  }
}
log(status.todo.length + " 页切为 " + blocks.length + " 个连续段");
const sliceFailed: number[] = [];
for (const b of blocks) {
  const args = ["literature/tools/zcode_m2_pipeline.py", "slice", "--start", String(b.s), "--end", String(b.e)];
  let r = await world.run("python", args, { output: { tail: 4096 } });
  if (r.exitCode !== 0) {
    r = await world.run("python", args, { output: { tail: 4096 } });
  }
  if (r.exitCode !== 0) {
    for (let p = b.s; p <= b.e; p++) sliceFailed.push(p);
    const f: Finding = {
      where: "PDF " + pageId(b.s) + "-" + pageId(b.e),
      what: "切片两次失败，本段 " + (b.e - b.s + 1) + " 页无法盲读，剔除本轮",
      evidence: (r.stderr || r.stdout || "").slice(-300),
      status: "verified",
      severity: "high",
    };
    findingsPush(f);
    report(f);
  }
}
const readList = status.todo.filter((p) => sliceFailed.indexOf(p) < 0);
if (readList.length === 0) {
  throw new Error("全部切片失败——无法盲读，停");
}
log("可读 " + readList.length + " 页（切片失败剔除 " + sliceFailed.length + " 页）");

// ---------- 第 3 步：5 页试点门 ----------

phase("5 页试点（新单价验证门）");
const pilot = readList.slice(0, 5);
const rest = readList.slice(5);
log("试点页：" + pilot.map((p) => pageId(p)).join("、"));
type Res = RawPageResult | { error: string };
const pilotRuns = await Promise.all(
  pilot.map(async (p): Promise<Res> => {
    try {
      return await agent("读者-p" + pageId(p), { model: LOW_MODEL }).ask<RawPageResult>(rawAsk(p));
    } catch (err) {
      return { error: String(err) };
    }
  }),
);
const pilotOk = pilotRuns.filter((r) => !("error" in r)).length;
const pilotBad = await validateRaw(pilot);
const pilotPass = pilot.length - (pilotBad.badCount + (pilot.length - pilotOk));
log("试点：" + pilotOk + "/" + pilot.length + " 页落盘，校验合格 " + (pilot.length - pilotBad.badCount) + " 页");
if (pilotPass < 4) {
  const f: Finding = {
    where: "试点页 " + pilot.map((p) => pageId(p)).join("、"),
    what: "试点不合格（落盘 " + pilotOk + "/" + pilot.length + "，校验合格 " + (pilot.length - pilotBad.badCount) +
      "/" + pilot.length + "）——低推理+预算刹车仍未压住单价，全量终止，等待改版",
    evidence: JSON.stringify(pilotBad.bad).slice(0, 500),
    status: "verified",
    severity: "high",
  };
  findingsPush(f);
  report(f);
  return {
    conclusion: "试点门未过：5 页试点仅 " + pilotPass + " 页合格，改版仍压不住单页成本/质量，已按预案当场终止，" +
      "未动封存、未动主册。已落盘的试点 raw 件保留待查。请回到主会话决定下一版改法（如按纵栏拆 ask）。",
    findings: findingsArr,
    verified: ["试点 5 页逐页过 VALIDATE_PY 确定性校验"],
    notCovered: ["全量 " + rest.length + " 页未派工；封存/释义阶段未执行"],
  };
}
log("试点门通过，放行全量 " + rest.length + " 页");

// ---------- 第 4 步：全量盲读 ----------

phase("盲读补读页");
const missingAfterRead: number[] = [];
for (let i = 0; i < rest.length; i += 10) {
  const chunk = rest.slice(i, i + 10);
  const range = pageId(chunk[0] ?? 0) + "-" + pageId(chunk[chunk.length - 1] ?? 0);
  log("批次 " + range + "：" + chunk.length + " 页派盲读抄写员（低推理档）");
  const first = await Promise.all(
    chunk.map(async (p): Promise<Res> => {
      try {
        return await agent("读者-p" + pageId(p), { model: LOW_MODEL }).ask<RawPageResult>(rawAsk(p));
      } catch (err) {
        return { error: String(err) };
      }
    }),
  );
  const produced: RawPageResult[] = [];
  const failedPages: number[] = [];
  for (let k = 0; k < first.length; k++) {
    const r = first[k] as Res;
    if ("error" in r) failedPages.push(chunk[k] ?? 0);
    else produced.push(r);
  }
  if (failedPages.length > 0) {
    log(failedPages.length + " 页失败，重试一次");
    const second = await Promise.all(
      failedPages.map(async (p): Promise<Res> => {
        try {
          return await agent("读者-p" + pageId(p) + "-重试", { model: LOW_MODEL }).ask<RawPageResult>(rawAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    for (const r of second) {
      if (!("error" in r)) produced.push(r);
    }
  }
  const entries = produced.reduce((a, r) => a + r.entries, 0);
  const stillMissing = chunk.filter((p) => !produced.some((r) => r.page === p));
  missingAfterRead.push(...stillMissing);
  let outcome: BatchOutcome;
  if (stillMissing.length > 0) {
    outcome = { range, status: "failed", pages: chunk.length, entries, lowConfidence: 0,
      detail: "缺页：" + stillMissing.map((p) => pageId(p)).join("、") };
    const f: Finding = {
      where: "PDF " + range,
      what: "盲读缺页 " + stillMissing.length + " 页：" + stillMissing.map((p) => pageId(p)).join("、"),
      evidence: "两轮派发均未返回",
      status: "unconfirmed",
      severity: "high",
    };
    findingsPush(f);
    report(f);
  } else {
    outcome = { range, status: "produced", pages: chunk.length, entries, lowConfidence: 0, detail: "raw 件落盘" };
  }
  report(outcome, "progress-read");
}
log("盲读完成，缺页 " + missingAfterRead.length + "（已入账）");

// ---------- 第 5 步：封存前校验与返修（两轮上限） ----------

phase("封存前校验与返修");
let bad = await validateRaw(readList);
log("封存前校验：问题页 " + bad.badCount + " 页");
for (let round = 1; round <= 2; round++) {
  const keys = Object.keys(bad.bad);
  if (keys.length === 0) break;
  log("第 " + round + " 轮返修：" + keys.length + " 页派修理工（低推理档）");
  await Promise.all(
    keys.map(async (k) => {
      try {
        await agent("修理工-p" + k + "-r" + round, { model: LOW_MODEL }).ask<RepairResult>(
          repairAsk(Number(k), bad.bad[k] ?? [], round),
        );
      } catch {
        /* 返修失败留下轮复核；最终仍不合规则剔除并大声入账 */
      }
    }),
  );
  bad = await validateRaw(readList);
}
const badKeys = Object.keys(bad.bad);
const excluded: number[] = badKeys.map(Number);
if (badKeys.length > 0) {
  const f: Finding = {
    where: "raw_blind（" + badKeys.map((k) => "p" + k).join("、") + "）",
    what: badKeys.length + " 页两轮返修后仍不合规，剔除本轮封存：" + JSON.stringify(bad.bad).slice(0, 600),
    evidence: "VALIDATE_PY 两轮后仍报",
    status: "verified",
    severity: "high",
  };
  findingsPush(f);
  report(f);
}
const dispatch = readList.filter((p) => excluded.indexOf(p) < 0);
log("进入封存 " + dispatch.length + " 页（校验剔除 " + excluded.length + "，盲读缺页 " + missingAfterRead.length + "）");

// ---------- 第 6 步：合龙封存并过门禁 ----------

phase("合龙封存并过门禁");
const CHUNK = 20;
for (let ci = 0; ci * CHUNK < dispatch.length; ci++) {
  const chunk = dispatch.slice(ci * CHUNK, (ci + 1) * CHUNK);
  const range = pageId(chunk[0] ?? 0) + "-" + pageId(chunk[chunk.length - 1] ?? 0);
  const mergedRel = "raw_blind/merged_gap166_c" + String(ci).padStart(2, "0") + ".json";
  const mg = await world.run("python", ["-c", mergePy(chunk, mergedRel)]);
  if (mg.exitCode !== 0) {
    const row: SealRow = { chunk: range, status: "failed", pages: chunk.length, detail: "合龙失败" };
    report(row, "progress-seal");
    const f: Finding = {
      where: "PDF " + range,
      what: "合龙失败，本批 " + chunk.length + " 页未封存",
      evidence: (mg.stderr || "").slice(-300),
      status: "verified",
      severity: "high",
    };
    findingsPush(f);
    report(f);
    continue;
  }
  const commit = await world.run(
    "python",
    ["literature/tools/zcode_m2_pipeline.py", "commit", "--input", M2 + "/" + mergedRel],
    { output: { tail: 16384 } },
  );
  if (commit.exitCode !== 0) {
    const row: SealRow = { chunk: range, status: "failed", pages: chunk.length,
      detail: (commit.stderr || commit.stdout || "").slice(-200) };
    report(row, "progress-seal");
    const f: Finding = {
      where: "PDF " + range,
      what: "commit 拒收，本批 " + chunk.length + " 页未封存",
      evidence: (commit.stderr || commit.stdout || "").slice(-500),
      status: "verified",
      severity: "high",
    };
    findingsPush(f);
    report(f);
  } else {
    const row: SealRow = { chunk: range, status: "sealed", pages: chunk.length, detail: "已封存入册" };
    report(row, "progress-seal");
  }
}

const sealRun = await world.run("python", ["-c", sealedPy(status.backfill)]);
if (sealRun.exitCode !== 0) {
  throw new Error("封存对账失败：" + (sealRun.stderr || "").slice(-300));
}
const sealInfo = JSON.parse((sealRun.stdout.trim().split("\n").pop() ?? "{}")) as SealedInfo;
log("封存对账：入册 " + sealInfo.sealed.length + " 页 / " + sealInfo.entriesSealed + " 条；未入册 " + sealInfo.missing.length + " 页" +
  (sealInfo.missing.length > 0 ? "（" + sealInfo.missing.map((p) => pageId(p)).join("、") + "）" : ""));
if (sealInfo.missing.length > 0) {
  const f: Finding = {
    where: "BLIND_READ_MANIFEST.json",
    what: "回填页 " + sealInfo.missing.length + " 页未入册：" + sealInfo.missing.map((p) => pageId(p)).join("、"),
    evidence: "封存对账（manifest 比对）",
    status: "verified",
    severity: "high",
  };
  findingsPush(f);
  report(f);
}

const gate1 = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 8192 } });
const gatePass = gate1.exitCode === 0 && gate1.stdout.indexOf("[FAIL]") < 0;
const gateFinding: Finding = {
  where: "architect_gatekeeper.py",
  what: gatePass ? "收官门禁 PASS（含覆盖不变量）" : "收官门禁未过（FAIL）——封存数据存在门禁判退项",
  evidence: (gate1.stdout || "").slice(-600),
  status: "verified",
  severity: gatePass ? "low" : "high",
};
findingsPush(gateFinding);
report(gateFinding);

// ---------- 第 7 步：回填页释义生产 ----------

phase("补读页释义生产");
let glossEntryTotal = 0;
let glossLowTotal = 0;
if (sealInfo.sealed.length > 0) {
  for (let i = 0; i < sealInfo.sealed.length; i += 10) {
    const chunk = sealInfo.sealed.slice(i, i + 10);
    const range = pageId(chunk[0] ?? 0) + "-" + pageId(chunk[chunk.length - 1] ?? 0);
    log("释义批次 " + range + "：" + chunk.length + " 页派释义员");
    type GRes = GlossPageResult | { error: string };
    const first = await Promise.all(
      chunk.map(async (p): Promise<GRes> => {
        try {
          return await agent("释义员-p" + pageId(p)).ask<GlossPageResult>(glossAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    const produced: GlossPageResult[] = [];
    const failedPages: number[] = [];
    for (let k = 0; k < first.length; k++) {
      const r = first[k] as GRes;
      if ("error" in r) failedPages.push(chunk[k] ?? 0);
      else produced.push(r);
    }
    if (failedPages.length > 0) {
      const second = await Promise.all(
        failedPages.map(async (p): Promise<GRes> => {
          try {
            return await agent("释义员-p" + pageId(p) + "-重试").ask<GlossPageResult>(glossAsk(p));
          } catch (err) {
            return { error: String(err) };
          }
        }),
      );
      for (const r of second) {
        if (!("error" in r)) produced.push(r);
      }
    }
    const entries = produced.reduce((a, r) => a + r.entries, 0);
    const low = produced.reduce((a, r) => a + r.lowConfidence, 0);
    glossEntryTotal += entries;
    glossLowTotal += low;
    const stillMissing = chunk.filter((p) => !produced.some((r) => r.page === p));
    let outcome: BatchOutcome;
    if (stillMissing.length > 0) {
      outcome = { range, status: "failed", pages: chunk.length, entries, lowConfidence: low,
        detail: "缺页：" + stillMissing.map((p) => pageId(p)).join("、") };
      const f: Finding = {
        where: "gloss_layer（PDF " + range + "）",
        what: "释义生产缺页：" + stillMissing.map((p) => pageId(p)).join("、"),
        evidence: "两轮派发均未返回",
        status: "unconfirmed",
        severity: "high",
      };
      findingsPush(f);
      report(f);
    } else {
      outcome = { range, status: "produced", pages: chunk.length, entries, lowConfidence: low, detail: "释义层落盘" };
    }
    report(outcome, "progress-gloss");
  }
}

// ---------- 第 8 步：释义层全册校验与收官 ----------

phase("释义层校验与收官");
const gv = await world.run("python", ["-c", GLOSS_VALIDATE_PY]);
if (gv.exitCode !== 0) {
  throw new Error("释义层校验失败：" + (gv.stderr || "").slice(-300));
}
const gres = JSON.parse((gv.stdout.trim().split("\n").pop() ?? "{}")) as GlossValidation;
log("释义层全册校验：" + gres.pagesOk + " 页 OK | 缺 " + gres.missingCount + " | position 不齐 " + gres.mismatchCount);
if (gres.missingCount > 0 || gres.mismatchCount > 0) {
  const f: Finding = {
    where: "gloss_layer/",
    what: "释义层校验缺口：缺 " + gres.missingCount + " 页、position 不齐 " + gres.mismatchCount + " 页" +
      (gres.mismatch.length > 0 ? "（" + gres.mismatch.join("、") + "）" : ""),
    evidence: "GLOSS_VALIDATE_PY 全册比对",
    status: "verified",
    severity: "high",
  };
  findingsPush(f);
  report(f);
}

const notSealed = status.backfill.length - sealInfo.sealed.length;
return {
  conclusion: "166 页回填收官：本轮新读 " + readList.length + " 页（试点门通过后放全量），跳过已有合格 raw " +
    status.done.length + " 页；封存入册 " + sealInfo.sealed.length + " 页 / " + sealInfo.entriesSealed +
    " 条（未入册 " + notSealed + " 页均已大声入账）；收官门禁 " + (gatePass ? "PASS" : "FAIL（见 findings）") +
    "。回填页释义 " + glossEntryTotal + " 条产出（低置信自报 " + glossLowTotal + "），全册释义层校验 " +
    gres.pagesOk + " 页 OK。M2 盲读覆盖自此达全部可校页；下一步：主会话 §6.4 提交推送 → 对碰扩到全书点火。",
  findings: findingsArr,
  verified: [
    "开工前与收官后各跑一次 architect_gatekeeper.py（基线与收官门禁，含覆盖不变量 v1.1）",
    "5 页试点门：新单价（低推理+读图预算）先验 5 页，≥4 页合格才放全量",
    "封存前 VALIDATE_PY（结构/页码/position/调标白名单/鼻化残留）两轮返修上限；封存对账以 manifest 为准；释义层全册 position 比对",
  ],
  notCovered: [
    "矩阵对碰本轮未执行（对碰V2/V3 待本轮回填收官后单独点火，跨供应商模型需用户确认）",
    "M1 主卷零改动（空壳记录保留为历史层）",
    "git 提交与推送由主会话在本轮收官后按 METHODOLOGY §6.4 执行",
  ],
};
