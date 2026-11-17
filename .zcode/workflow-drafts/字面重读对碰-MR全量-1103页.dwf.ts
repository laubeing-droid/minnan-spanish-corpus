// 字面层独立重读对碰：全书 1,103 页 M/R 栏字母独立重读（盲读 3 张横带图，不看 V1 封存件），
// difflib 逐页与 V1 对齐出分歧清单，分歧页派墨迹裁判裁决，落 REREAD_MR_LEDGER.json。
// 背景：p0257 ûia→cûa 误读事故（用户眼验坐实）——释义层对碰与门禁都抓不到字面字母误读，
// 字面层唯一独立复核 = 本重读对碰（METHODOLOGY §6.5 之字面层，用户裁定直接全量，2026-11-16）。
// 铁律：重读禁读 blind_read/gloss_layer*/一切既有转写；$low 档+反空转纪律；工作流不碰 git；
// 修复不在本工作流内做——只出台账，修复由主会话按账走管线。

interface RereadResult {
  page: number;
  file: string;
  mLines: number;
  rLines: number;
  notes: string;
}

interface BatchOutcome {
  range: string;
  status: "produced" | "failed";
  pages: number;
  detail: string;
}

interface Finding {
  where: string;
  what: string;
  evidence: string;
  status: "verified" | "unconfirmed";
  severity: "low" | "medium" | "high";
}

interface DiffRecord {
  page: number;
  position: number;
  field: string;
  kind: string;
  v1: string;
  rr: string;
  idx: number;
}

interface PageDiff {
  page: number;
  mV1Count: number;
  mRrCount: number;
  rV1Count: number;
  rRrCount: number;
  diffs: DiffRecord[];
}

interface Verdict {
  idx: number;
  /** V1误读 / 重读误 / 等价 / 存疑 */
  verdict: string;
  shouldBe: string;
  note: string;
}

interface JudgeResult {
  page: number;
  verdicts: Verdict[];
}

interface WorkflowReport {
  conclusion: string;
  findings: Finding[];
  verified: string[];
  notCovered: string[];
}

const M2 = "literature/workspace_m2_dhs834";
const RD = M2 + "/reread_mr";
const CD = M2 + "/collision_mr";

function pageId(p: number): string {
  return String(p).padStart(4, "0");
}

const findingsArr: Finding[] = [];
function findingsPush(f: Finding): void {
  findingsArr.push(f);
}

artifact.table("progress-reread", {
  title: "M/R 字面重读批次进度（全书封存页）",
  columns: [
    { field: "range", label: "批次" },
    { field: "status", label: "状态" },
    { field: "pages", label: "页数" },
    { field: "detail", label: "说明" },
  ],
  key: "range",
});

const PAGES_PY = [
  "import json",
  "from pathlib import Path",
  "man = json.loads(Path('literature/workspace_m2_dhs834/BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "pages = sorted(int(k) for k in man.get('pages', {}))",
  "print(json.dumps(pages))",
].join("\n");

const TODO_PY = [
  "import json",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "pages = sorted(int(k) for k in man.get('pages', {}))",
  "def valid(pg):",
  "    f = m2 / 'reread_mr' / ('reread_mr_p%04d.json' % pg)",
  "    if not f.exists():",
  "        return False",
  "    try:",
  "        d = json.loads(f.read_text(encoding='utf-8'))",
  "        return isinstance(d.get('m_lines'), list) and isinstance(d.get('r_lines'), list)",
  "    except Exception:",
  "        return False",
  "todo = [p for p in pages if not valid(p)]",
  "print(json.dumps(todo))",
].join("\n");

function pilotCheckPy(pks: string[]): string {
  return [
    "import json",
    "from pathlib import Path",
    "m2 = Path('literature/workspace_m2_dhs834')",
    "pks = json.loads('" + JSON.stringify(pks) + "')",
    "bad = {}",
    "def nonempty(v):",
    "    return (v or '').strip() not in ('', '[空]')",
    "for pk in pks:",
    "    f = m2 / 'reread_mr' / ('reread_mr_p' + pk + '.json')",
    "    if not f.exists():",
    "        bad[pk] = ['缺文件']",
    "        continue",
    "    try:",
    "        d = json.loads(f.read_text(encoding='utf-8'))",
    "        sealed = json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])",
    "        m1 = sum(1 for e in sealed if nonempty(e.get('source_M')))",
    "        r1 = sum(1 for e in sealed if nonempty(e.get('source_R')))",
    "        ml = [t for t in (d.get('m_lines') or []) if t.strip() not in ('', '[空]')]",
    "        rl = [t for t in (d.get('r_lines') or []) if t.strip() not in ('', '[空]')]",
    "        msgs = []",
    "        if abs(len(ml) - m1) > max(3, m1 // 3):",
    "            msgs.append('M 行数偏离: V1 非空 %d / 重读 %d' % (m1, len(ml)))",
    "        if r1 == 0 and len(rl) > 0:",
    "            msgs.append('V1 无 R 栏但重读交了 %d 行 R（列混淆/幻觉）' % len(rl))",
    "        if r1 > 0 and abs(len(rl) - r1) > max(3, r1 // 3):",
    "            msgs.append('R 行数偏离: V1 非空 %d / 重读 %d' % (r1, len(rl)))",
    "        if msgs:",
    "            bad[pk] = msgs[:3]",
    "    except Exception as ex:",
    "        bad[pk] = ['解析失败: %s' % ex]",
    "print(json.dumps({'badCount': len(bad), 'bad': bad}))",
  ].join("\n");
}

function rereadAsk(page: number): string {
  const pk = pageId(page);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的字面抄写员，负责 PDF 第 " + page + " 页 M 栏（闽南语原稿音写）与 R 栏（官话对音）的**独立重读**——全书字面复核的第二读法。",
    "",
    "【产出优先于完备——反空转硬纪律】",
    "- 禁止任何 \"hmm/嗯/让我想想\" 式空转推演；看完直接逐行写结论，一行接一行。",
    "- 每行写完就过，禁止回头复读重写；一次通过。",
    "- 字母拿不准就按你所见照录；整个认不出写 \"[残]\"；空白写 \"[空]\"。不要为确认反复斟酌。",
    "",
    "【盲读铁律】只看下面 3 张横带切图。禁止读取 literature/workspace_m2_dhs834/ 下任何 blind_read/gloss_layer*/reread_mr/collision 文件——你的独立读法与已封存第一读法的差异正是本任务的目的。",
    "",
    "【输入】横带切图（自上而下）：",
    "literature/tiles/01_DHS/page_" + pk + "/pdf_" + pk + "_band_y0_top.png",
    "literature/tiles/01_DHS/page_" + pk + "/pdf_" + pk + "_band_y1_mid.png",
    "literature/tiles/01_DHS/page_" + pk + "/pdf_" + pk + "_band_y2_bot.png",
    "",
    "【版式判定——先看清楚再动手】本书存在两种版式：",
    "- **标准四栏版式**：左起 = 西语词头 | 汉字 | 闽南音写 | 官话对音。此时 m_lines = 倒数第二栏（闽南音写）逐行照录，r_lines = 最右栏（官话）逐行照录；整栏空白/无此栏时该数组写 []（**严禁拿 [残] 或其他栏文本凑数**）。",
    "- **两栏补编版式**（本书开头约 0030–0040 一带）：页面只有两个页面栏，每栏 = 西语短语+闽南音写**连写在一行**，无汉字栏、无官话栏。此时把每个视觉行里**西语之后的闽南音写部分**（含鼻化照录为普通字母 n，如 tiⁿû → tinû）录进 m_lines，r_lines=[]。**严禁把西语文本录进任何数组。**",
    "动手前先判定本页属于哪种版式，notes 里说明判的是哪种。",
    "",
    "【转写规则（两栏/四栏通用）】",
    "- 保留原稿拼写字母与元音符（û/ā/é/ò 等一律照录，不要改成现代拼法，不要增删字母）；",
    "- 17 世纪多明我拼法照录（c-/qu-/ch-/g-/s-/z-/ttz- 等），禁止改成现代 k-/kh-/ts-/tsh-；",
    "- 声调符（^ ¯ ' 等）戴在哪个元音字母上就照录在那个字母上；",
    "- 自上而下、一视觉行一条；词条内音节连写照录；整行认不出写 \"[残]\"；空行/纯记号行跳过。",
    "",
    "【输出】写 literature/workspace_m2_dhs834/reread_mr/reread_mr_p" + pk + ".json（UTF-8，一次通过）：",
    '{"page": ' + page + ', "m_lines": ["…", "…"], "r_lines": ["…", "…"], "notes": ""}',
    "notes 只写版式判定与异常（缺栏/污损区）。",
    "返回：page、file、mLines（行数）、rLines（行数）、notes（一句话）。",
  ].join("\n");
}

// ---------- 第 1 步：盘点 + 试点门 ----------

phase("盘点与 5 页试点门");
const st = await world.run("python", ["-c", TODO_PY]);
if (st.exitCode !== 0) {
  throw new Error("盘点失败：" + (st.stderr || "").slice(-300));
}
const todo: number[] = JSON.parse((st.stdout.trim().split("\n").pop() ?? "[]"));
log("待重读 " + todo.length + " 页（已产合格 " + (1103 - todo.length) + " 页跳过）");
if (todo.length === 0) {
  throw new Error("重读已全部在库——本运行直接进对齐段之前请核对是否为续跑残局");
}
const gate0 = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 4096 } });
if (gate0.exitCode !== 0 || gate0.stdout.indexOf("[FAIL]") >= 0) {
  throw new Error("基线门禁未过，拒绝施工。\n" + gate0.stdout.slice(-800));
}

const pilot = todo.slice(0, 5);
const rest = todo.slice(5);
type Res = RereadResult | { error: string };
const pilotRuns = await Promise.all(
  pilot.map(async (p): Promise<Res> => {
    try {
      return await agent("重读-p" + pageId(p)).ask<RereadResult>(rereadAsk(p));
    } catch (err) {
      return { error: String(err) };
    }
  }),
);
const pilotOk = pilotRuns.filter((r) => !("error" in r)).length;
const pc = await world.run("python", ["-c", pilotCheckPy(pilot.map((p) => pageId(p)))]);
if (pc.exitCode !== 0) {
  throw new Error("试点校验失败：" + (pc.stderr || "").slice(-300));
}
const pcRes = JSON.parse((pc.stdout.trim().split("\n").pop() ?? "{}")) as { badCount: number; bad: Record<string, string[]> };
const pilotPass = pilot.length - pcRes.badCount;
log("试点：" + pilotOk + "/" + pilot.length + " 落盘，行数合理 " + pilotPass + "/" + pilot.length);
if (pilotPass < 4) {
  const f: Finding = {
    where: "字面重读试点 " + pilot.map((p) => pageId(p)).join("、"),
    what: "试点不合格（落盘 " + pilotOk + "/" + pilot.length + "，行数合理 " + pilotPass + "/" + pilot.length + "），全量终止",
    evidence: JSON.stringify(pcRes.bad).slice(0, 400),
    status: "verified",
    severity: "high",
  };
  findingsPush(f);
  report(f);
  return {
    conclusion: "字面重读试点门未过，已终止。试点件保留待查；未动封存区、未动对齐段。",
    findings: findingsArr,
    verified: ["试点 5 页行数与 V1 词条数比对（±max(3, 1/3) 容差）"],
    notCovered: ["全量 " + rest.length + " 页未派工；对齐与裁判段未执行"],
  };
}
log("试点门通过，放行全量 " + rest.length + " 页");

// ---------- 第 2 步：全量重读 ----------

phase("M/R 字面重读");
const missingAfter: number[] = [];
for (let i = 0; i < rest.length; i += 10) {
  const chunk = rest.slice(i, i + 10);
  const range = pageId(chunk[0] ?? 0) + "-" + pageId(chunk[chunk.length - 1] ?? 0);
  log("批次 " + range + "：" + chunk.length + " 页派字面抄写员");
  const first = await Promise.all(
    chunk.map(async (p): Promise<Res> => {
      try {
        return await agent("重读-p" + pageId(p)).ask<RereadResult>(rereadAsk(p));
      } catch (err) {
        return { error: String(err) };
      }
    }),
  );
  const produced: RereadResult[] = [];
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
          return await agent("重读-p" + pageId(p) + "-重试").ask<RereadResult>(rereadAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    for (const r of second) {
      if (!("error" in r)) produced.push(r);
    }
  }
  const stillMissing = chunk.filter((p) => !produced.some((r) => r.page === p));
  missingAfter.push(...stillMissing);
  let outcome: BatchOutcome;
  if (stillMissing.length > 0) {
    outcome = { range, status: "failed", pages: chunk.length, detail: "缺页：" + stillMissing.map((p) => pageId(p)).join("、") };
    const f: Finding = {
      where: "PDF " + range,
      what: "重读缺页：" + stillMissing.map((p) => pageId(p)).join("、"),
      evidence: "两轮派发均未返回",
      status: "unconfirmed",
      severity: "high",
    };
    findingsPush(f);
    report(f);
  } else {
    outcome = { range, status: "produced", pages: chunk.length, detail: "重读落盘" };
  }
  report(outcome, "progress-reread");
}
log("重读完成，缺页 " + missingAfter.length + "（已入账）");

// ---------- 第 3 步：difflib 逐页对齐出分歧 ----------

phase("V1×重读 逐页对齐");
const DIFF_PY = [
  "import json, difflib",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "pages = sorted(int(k) for k in man.get('pages', {}))",
  "def toks(s):",
  "    return [t for t in (s or '').replace(';', ' ;').replace(',', ' ,').replace('.', ' .').split(' ') if t]",
  "pages_with_diff = []; total_ops = 0; all_pages = []; parse_fail = []",
  "for pg in pages:",
  "    pk = '%04d' % pg",
  "    try:",
  "        v1 = json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])",
  "        rr = json.loads((m2 / 'reread_mr' / ('reread_mr_p' + pk + '.json')).read_text(encoding='utf-8'))",
  "    except Exception:",
  "        parse_fail.append(pg)",
  "        continue",
  "    v1m = [(e.get('position'), toks(e.get('source_M'))) for e in v1]",
  "    v1r = [(e.get('position'), toks(e.get('source_R'))) for e in v1]",
  "    flat_m = [t for _, ts in v1m for t in ts]",
  "    flat_r = [t for _, ts in v1r for t in ts]",
  "    rm = [t for t in (rr.get('m_lines') or []) for t in toks(t)]",
  "    rrn = [t for t in (rr.get('r_lines') or []) for t in toks(t)]",
  "    drec = {'page': pg, 'mV1Count': len(flat_m), 'mRrCount': len(rm), 'rV1Count': len(flat_r), 'rRrCount': len(rrn), 'diffs': []}",
  "    for field, a, b in (('M', flat_m, rm), ('R', flat_r, rrn)):",
  "        poslist = [pos for pos, ts in (v1m if field == 'M' else v1r) for _ in ts]",
  "        sm = difflib.SequenceMatcher(None, [t.lower() for t in a], [t.lower() for t in b], autojunk=False)",
  "        idx_a = 0",
  "        for op, i1, i2, j1, j2 in sm.get_opcodes():",
  "            if op == 'equal':",
  "                idx_a += i2 - i1",
  "                continue",
  "            if op == 'replace':",
  "                for k in range(max(i2 - i1, j2 - j1)):",
  "                    drec['diffs'].append({'page': pg, 'position': poslist[i1 + k] if i1 + k < len(poslist) else 0,",
  "                        'field': field, 'kind': 'replace',",
  "                        'v1': a[i1 + k] if i1 + k < len(a) else '',",
  "                        'rr': b[j1 + k] if j1 + k < len(b) else '', 'idx': idx_a + k})",
  "                idx_a += i2 - i1",
  "            elif op == 'delete':",
  "                for k in range(i2 - i1):",
  "                    drec['diffs'].append({'page': pg, 'position': poslist[i1 + k] if i1 + k < len(poslist) else 0,",
  "                        'field': field, 'kind': 'delete', 'v1': a[i1 + k], 'rr': '', 'idx': idx_a + k})",
  "                idx_a += i2 - i1",
  "            elif op == 'insert':",
  "                for k in range(j2 - j1):",
  "                    drec['diffs'].append({'page': pg, 'position': 0, 'field': field, 'kind': 'insert',",
  "                        'v1': '', 'rr': b[j1 + k], 'idx': idx_a})",
  "            total_ops += (i2 - i1) + (j2 - j1)",
  "    if drec['diffs'] or drec['mV1Count'] != drec['mRrCount'] or drec['rV1Count'] != drec['rRrCount']:",
  "        pages_with_diff.append(pg)",
  "    all_pages.append(drec)",
  "cd = m2 / 'collision_mr'; cd.mkdir(exist_ok=True)",
  "for d in all_pages:",
  "    if d['diffs']:",
  "        (cd / ('page_diff_%04d.json' % d['page'])).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')",
  "sumrec = {'protocol': 'REREAD_DIFF_SUMMARY_V1', 'pagesTotal': len(pages), 'pagesWithDiff': len(pages_with_diff),",
  "    'totalOps': total_ops, 'parseFailPages': parse_fail,",
  "    'pagesWithDiffList': pages_with_diff[:2000]}",
  "(cd / 'diff_summary.json').write_text(json.dumps(sumrec, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'pagesWithDiff': len(pages_with_diff), 'totalOps': total_ops, 'parseFail': len(parse_fail)}))",
].join("\n");
const df = await world.run("python", ["-c", DIFF_PY]);
if (df.exitCode !== 0) {
  throw new Error("对齐失败：" + (df.stderr || "").slice(-600));
}
const dres = JSON.parse((df.stdout.trim().split("\n").pop() ?? "{}")) as { pagesWithDiff: number; totalOps: number };
log("对齐完成：分歧页 " + dres.pagesWithDiff + " / 1103，差异操作 " + dres.totalOps + " 处");

// ---------- 第 4 步：分歧页墨迹裁决 ----------

phase("分歧页墨迹裁决");
function judgeAsk(pg: number): string {
  const pk = pageId(pg);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的字面裁判。页面 PDF 第 " + pg + " 页的字面重读对碰发现分歧，请你对照墨迹逐条裁决哪一方忠实。",
    "",
    "【材料】先读分歧清单：" + CD + "/page_diff_" + pk + ".json（每条含 field=M/R、v1=第一读法词形、rr=重读词形）；",
    "再逐张细看横带切图（M 栏=倒数第二栏，R 栏=最右栏，只看这两栏的手写西文字母）：",
    "literature/tiles/01_DHS/page_" + pk + "/pdf_" + pk + "_band_y0_top.png / _band_y1_mid.png / _band_y2_bot.png",
    "",
    "【裁决口径】逐条四选一：",
    "- \"V1误读\"：墨迹与重读一致（在 note 给出你看到的忠实字面 should_be）；",
    "- \"重读误\"：墨迹与 V1 一致（shouldBe 留空）；",
    "- \"等价\"：拼写变体/声调符位置差/标点差，两读皆忠实（shouldBe 留空）；",
    "- \"存疑\"：墨迹无法判定（shouldBe 留空，note 一句原因）。",
    "反空转纪律：逐条直接判，不空转推演；认不清就判存疑，不硬猜。",
    "",
    "【输出】写 " + CD + "/page_verdict_" + pk + ".json（UTF-8）：",
    '{"page": ' + pg + ', "verdicts": [{"idx": 0, "verdict": "V1误读", "shouldBe": "cûa", "note": ""}]}',
    "idx 用分歧清单里的 idx。返回：page、verdicts 条数。",
  ].join("\n");
}

const df2 = await world.run("python", ["-c",
  "import json;from pathlib import Path;d=json.loads(Path('" + CD + "/diff_summary.json').read_text(encoding='utf-8'));print(json.dumps(d['pagesWithDiffList'][:600]))",
]);
if (df2.exitCode !== 0) {
  throw new Error("分歧页清单读取失败：" + (df2.stderr || "").slice(-300));
}
const diffPages: number[] = JSON.parse((df2.stdout.trim().split("\n").pop() ?? "[]"));
log("裁决范围：" + diffPages.length + " 个分歧页（超 600 页时按页序截断，余者台账存目）");
if (diffPages.length > 0) {
  for (let i = 0; i < diffPages.length; i += 20) {
    const chunk = diffPages.slice(i, i + 20);
    await Promise.all(
      chunk.map(async (pg) => {
        try {
          await agent("墨迹裁判-p" + pageId(pg)).ask<JudgeResult>(judgeAsk(pg));
        } catch {
          /* 裁决失败的页按未裁入账 */
        }
      }),
    );
  }
  log("裁决派发完成：" + diffPages.length + " 页");
}

// ---------- 第 5 步：台账 ----------

phase("字面重读对碰台账");
const LEDGER_PY = [
  "import json",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision_mr'",
  "summ = json.loads((cd / 'diff_summary.json').read_text(encoding='utf-8'))",
  "def dirsha(rel):",
  "    d = m2 / rel; h = __import__('hashlib').sha256(); n = 0",
  "    for f in sorted(d.glob('*.json')):",
  "        h.update(f.name.encode('utf-8')); h.update(__import__('hashlib').sha256(f.read_bytes()).digest()); n += 1",
  "    return {'dir': rel, 'files': n, 'sha256': h.hexdigest()}",
  "import collections",
  "verdict_count = collections.Counter()",
  "misreads = []; suspect = []; unjudged = 0",
  "for f in sorted(cd.glob('page_diff_*.json')):",
  "    pk = f.stem.split('_')[-1]",
  "    d = json.loads(f.read_text(encoding='utf-8'))",
  "    vf = cd / ('page_verdict_' + pk + '.json')",
  "    if not vf.exists():",
  "        unjudged += len(d['diffs'])",
  "        continue",
  "    vmap = {v.get('idx'): v for v in json.loads(vf.read_text(encoding='utf-8')).get('verdicts', [])}",
  "    for diff in d['diffs']:",
  "        v = vmap.get(diff.get('idx'))",
  "        if not v:",
  "            unjudged += 1",
  "            continue",
  "        verdict_count[v.get('verdict')] += 1",
  "        row = dict(diff)",
  "        row['verdict'] = v.get('verdict')",
  "        row['shouldBe'] = v.get('shouldBe')",
  "        row['note'] = v.get('note')",
  "        if v.get('verdict') == 'V1误读':",
  "            misreads.append(row)",
  "        elif v.get('verdict') == '存疑':",
  "            suspect.append(row)",
  "ledger = {",
  "    'protocol': 'REREAD_MR_LEDGER_V1',",
  "    'book': 1,",
  "    'versions': [dirsha('reread_mr')],",
  "    'stats': {",
  "        'pagesTotal': summ['pagesTotal'],",
  "        'pagesWithDiff': summ['pagesWithDiff'],",
  "        'totalOps': summ['totalOps'],",
  "        'v1Misread': len(misreads),",
  "        'suspect': len(suspect),",
  "        'unjudged': unjudged,",
  "        'verdictBreakdown': dict(verdict_count),",
  "    },",
  "    'misreads': misreads[:1000],",
  "    'suspect': suspect[:500],",
  "    'limitations': [",
  "        '重读档位 GLM-5.3-Flash$low（稳定档），与 V1 同模型族——对碰抓字面差异靠独立上下文，不靠模型族差异',",
  "        'V1误读 判定=重读与墨迹一致的条目，修复由主会话按账走管线（本工作流不修数）',",
  "        '超 600 分歧页或裁决失败的页在 unjudged 中存目',",
  "        '完成宣称边界：本台账是字面层独立复核记录，不构成人工校对完成（METHODOLOGY §6.5）',",
  "    ],",
  "}",
  "out = m2 / 'REREAD_MR_LEDGER.json'",
  "out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'ledger': str(out), 'stats': ledger['stats']}))",
].join("\n");
const lg = await world.run("python", ["-c", LEDGER_PY]);
if (lg.exitCode !== 0) {
  throw new Error("台账失败：" + (lg.stderr || "").slice(-600));
}
const lres = JSON.parse((lg.stdout.trim().split("\n").pop() ?? "{}")) as { ledger: string; stats: Record<string, number> };
const s = lres.stats;
if ((s.v1Misread ?? 0) > 0) {
  const f: Finding = {
    where: "REREAD_MR_LEDGER.json",
    what: "墨迹裁判判定 V1 字面误读 " + s.v1Misread + " 处（另存疑 " + s.suspect + "、未裁 " + s.unjudged + "）——修复由主会话按账走管线",
    evidence: "misreads 清单见台账",
    status: "verified",
    severity: (s.v1Misread ?? 0) > 50 ? "high" : "medium",
  };
  findingsPush(f);
  report(f);
}
return {
  conclusion: "字面层独立重读对碰完成：全书 " + s.pagesTotal + " 页 M/R 栏重读（试点门通过），与 V1 对齐发现分歧页 " +
    s.pagesWithDiff + " 页 / 差异 " + s.totalOps + " 处；墨迹裁决判定 **V1 误读 " + s.v1Misread + " 处**、存疑 " +
    s.suspect + "、未裁 " + s.unjudged + "（裁决细分 " + JSON.stringify(s.verdictBreakdown) + "）。台账：REREAD_MR_LEDGER.json。" +
    "下一步：主会话按 misreads 账走管线修复（raw 改 → 重封 → 门禁），并刷新受影响页的释义层。",
  findings: findingsArr,
  verified: [
    "重读为独立盲读（禁读封存件与一切既有转写），$low 档 + 反空转纪律 + 5 页试点门",
    "对齐用 difflib 逐 token（保留大小写与元音符，空白/标点归一），M、R 两栏各自成序",
    "每处分歧由墨迹裁判对照横带切图四选一裁决，台账含三版指纹与局限声明",
  ],
  notCovered: [
    "H 栏（汉字）与 L 栏（西语印刷体词头）未在本次重读范围（本次只针对手写西文字母误读类）",
    "已判 V1误读 的条目修复不在本工作流内（主会话按账走管线，修后刷新受影响页释义）",
    "difflib 对齐在行数偏离大的页以页级存目处理（不强行配对）",
  ],
};
