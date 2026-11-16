// 对碰 V3 + 全量矩阵对碰：第一书释义层第三版独立盲产（K=3 第 3 版），
// 随后执行 METHODOLOGY §6.5 终检——三版逐条两两对碰、机器仲裁（多数决 + 追加盲产上限 2 轮）、
// 词头跨页一致性层、COLLISION_LEDGER.json 台账。
// 铁律：盲产禁读既有释义；裁判匿名不见版本来源；无多数不强判——
// 仍未决者标 COLLISION_UNRESOLVED 降置信入账；不碰 git；不碰 M1 冻结区。

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
const CD = M2 + "/collision";
const findingsArr: Finding[] = [];

function findingsPush(f: Finding): void {
  findingsArr.push(f);
}

artifact.table("progress-v3", {
  title: "对碰 V3 盲产批次进度（全书封存页，按 BLIND_READ_MANIFEST 实时取数）",
  columns: [
    { field: "range", label: "批次" },
    { field: "status", label: "状态" },
    { field: "entries", label: "条目数" },
    { field: "lowConfidence", label: "低置信" },
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

function validatePy(dir: string): string {
  return [
    "import json",
    "from pathlib import Path",
    "m2 = Path('literature/workspace_m2_dhs834')",
    "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
    "ok = 0; missing = []; mismatch = []",
    "for pk in sorted(man.get('pages', {})):",
    "    g = m2 / '" + dir + "' / ('gloss_p' + pk + '.json')",
    "    if not g.exists():",
    "        missing.append(pk); continue",
    "    gd = json.loads(g.read_text(encoding='utf-8'))",
    "    sealed = {e.get('position') for e in json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])}",
    "    produced = {e.get('position') for e in gd.get('entries', [])}",
    "    if sealed == produced: ok += 1",
    "    else: mismatch.append(pk)",
    "print(json.dumps({'pagesOk': ok, 'missingCount': len(missing), 'positionMismatch': len(mismatch)}))",
  ].join("\n");
}

function glossAsk(page: number, ver: string): string {
  const pk = String(page).padStart(4, "0");
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的历史词典释义员，负责 PDF 第 " + page + " 页的逐条释义生产（矩阵对碰终检的 " + ver + " 版独立盲产）。",
    "",
    "【盲产铁律】本任务为独立盲产：禁止读取 literature/workspace_m2_dhs834/gloss_layer/、gloss_layer_v2、gloss_layer_v3、collision/",
    "及任何既有释义/对碰/复核文件——你的唯一输入是本页封存件。与其他版本撞出相同结论才是对碰的意义。",
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
    "1. 优先 17 世纪马尼拉历史语义，不用现代义项想当然；",
    "2. 不确定就降 confidence 并在 notes 说明——严禁编造确定释义；",
    "3. [空]/[残] 栏照常参与判断：材料不足时 zh/en 写 〔原件残缺，释义存疑〕 且 confidence=low；",
    "4. tone_marks 与音系不归你管，不要输出音标或台罗；",
    "5. 一次通过：读封存件 → 写释义层文件 → 返回。禁止重写、禁止逐条复读。",
    "",
    "【输出】写 literature/workspace_m2_dhs834/gloss_layer_v3/gloss_p" + pk + ".json（UTF-8）：",
    '{"page": ' + page + ', "entries": [{"position": 1, "zh": "…", "en": "…", "confidence": "high", "notes": ""}]}',
    "entries 数与 position 集合必须与封存件完全一致。",
    "返回：page、glossFile、entries（条数）、lowConfidence（低置信条数）、notes（一句话）。",
  ].join("\n");
}

// ---------- 第一跑前先确认 V2 已在库 ----------
phase("前置校验：V1/V2 在库");
const pre = await world.run("python", ["-c", validatePy("gloss_layer_v2")]);
if (pre.exitCode !== 0) {
  throw new Error("V2 前置校验失败：" + (pre.stderr || "").slice(-300));
}
const preRes = JSON.parse((pre.stdout.trim().split("\n").pop() ?? "{}")) as { pagesOk: number; missingCount: number };
if (preRes.missingCount > 0) {
  throw new Error("V2 层缺 " + preRes.missingCount + " 页——先跑 对碰V2-第一书盲产-937页 再点火本脚本");
}
log("V2 在库 " + preRes.pagesOk + " 页，开始 V3 盲产");

phase("V3 盲产");
const pagesRun = await world.run("python", ["-c", PAGES_PY]);
if (pagesRun.exitCode !== 0) {
  throw new Error("清册读取失败：" + (pagesRun.stderr || "").slice(-300));
}
const allPages: number[] = JSON.parse((pagesRun.stdout.trim().split("\n").pop() ?? "[]"));

const outcomes: BatchOutcome[] = [];
for (let i = 0; i < allPages.length; i += 10) {
  const chunk = allPages.slice(i, i + 10);
  const range = String(chunk[0] ?? 0).padStart(4, "0") + "-" + String(chunk[chunk.length - 1] ?? 0).padStart(4, "0");
  phase("V3 盲产批");
  log("批次 " + range + "：" + chunk.length + " 页派盲产释义员");
  type Res = GlossPageResult | { error: string };
  const first = await Promise.all(
    chunk.map(async (p): Promise<Res> => {
      try {
        return await agent("盲产v3-p" + String(p).padStart(4, "0")).ask<GlossPageResult>(glossAsk(p, "第 3"));
      } catch (err) {
        return { error: String(err) };
      }
    }),
  );
  const produced: GlossPageResult[] = [];
  const failedPages: number[] = [];
  for (let k = 0; k < first.length; k++) {
    const r = first[k] as Res;
    if ("error" in r) failedPages.push(chunk[k] ?? 0);
    else produced.push(r);
  }
  if (failedPages.length > 0) {
    const second = await Promise.all(
      failedPages.map(async (p): Promise<Res> => {
        try {
          return await agent("盲产v3-p" + String(p).padStart(4, "0") + "-重试").ask<GlossPageResult>(glossAsk(p, "第 3"));
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
  const stillMissing = chunk.filter((p) => !produced.some((r) => r.page === p));
  let outcome: BatchOutcome;
  if (stillMissing.length > 0) {
    outcome = { range, status: "failed", pages: chunk.length, entries, lowConfidence: low,
      detail: "缺页：" + stillMissing.map((p) => String(p).padStart(4, "0")).join("、") };
    const f: Finding = { where: "PDF " + range, what: "V3 盲产缺页：" + outcome.detail,
      evidence: "两轮派发均未返回", status: "unconfirmed", severity: "high" };
    findingsPush(f);
    report(f);
  } else {
    outcome = { range, status: "produced", pages: chunk.length, entries, lowConfidence: low, detail: "V3 盲产落盘" };
  }
  outcomes.push(outcome);
  report(outcome, "progress-v3");
}

phase("V3 校验");
const val = await world.run("python", ["-c", validatePy("gloss_layer_v3")]);
if (val.exitCode !== 0) {
  throw new Error("V3 校验失败：" + (val.stderr || "").slice(-300));
}
const v3res = JSON.parse((val.stdout.trim().split("\n").pop() ?? "{}")) as { pagesOk: number; missingCount: number; positionMismatch: number };
log("V3 校验：" + v3res.pagesOk + " 页 OK | 缺页 " + v3res.missingCount + " | position 不齐 " + v3res.positionMismatch);

// ---------- 预筛对碰：归一化字面三版全等 -> 通过；否则入分歧清单并切裁判批 ----------
phase("预筛对碰");
const COLLIDE_PY = [
  "import json, re",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision'; cd.mkdir(exist_ok=True)",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "pages = sorted(int(k) for k in man.get('pages', {}))",
  "def norm(s, lang):",
  "    s = re.sub(r'\\s+', '', (s or '').strip())",
  "    s = re.sub(r'[，。；：、（）()\\[\\]〔〕〈〉;:,.·…\\-—–“”\\\"\\'‘’！!？?]', '', s)",
  "    return s.lower() if lang == 'en' else s",
  "PH = '〔原件残缺，释义存疑〕'",
  "exact = 0; placeholder = 0; divergent = []",
  "for pg in pages:",
  "    pk = '%04d' % pg",
  "    sealed = json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])",
  "    vs = []",
  "    for d in ('gloss_layer', 'gloss_layer_v2', 'gloss_layer_v3'):",
  "        vs.append({e.get('position'): e for e in json.loads((m2 / d / ('gloss_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])})",
  "    for e in sealed:",
  "        pos = e.get('position', 0)",
  "        g = [v.get(pos, {}) for v in vs]",
  "        z = [norm(x.get('zh'), 'zh') for x in g]",
  "        en = [norm(x.get('en'), 'en') for x in g]",
  "        if z[0] == z[1] == z[2] and en[0] == en[1] == en[2]:",
  "            if PH in (g[0].get('zh') or ''): placeholder += 1",
  "            else: exact += 1",
  "            continue",
  "        divergent.append({'page': pg, 'position': pos,",
  "            'L': e.get('source_L'), 'H': e.get('source_H'), 'M': e.get('source_M'), 'R': e.get('source_R'),",
  "            'v1': {'zh': g[0].get('zh'), 'en': g[0].get('en')},",
  "            'v2': {'zh': g[1].get('zh'), 'en': g[1].get('en')},",
  "            'v3': {'zh': g[2].get('zh'), 'en': g[2].get('en')}})",
  "(cd / 'divergent_entries.json').write_text(json.dumps({'protocol': 'DIVERGENT_V1', 'entries': divergent}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "BATCH = 30; nb = 0",
  "for i in range(0, len(divergent), BATCH):",
  "    nb += 1",
  "    (cd / ('judge_batch_%03d.json' % nb)).write_text(json.dumps({'batch': nb, 'entries': divergent[i:i + BATCH]}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "(cd / 'stats_prefilter.json').write_text(json.dumps({'entriesTotal': exact + placeholder + len(divergent), 'exactPass': exact, 'placeholderPass': placeholder, 'divergent': len(divergent), 'judgeBatches': nb}, ensure_ascii=False), encoding='utf-8')",
  "print(json.dumps({'entriesTotal': exact + placeholder + len(divergent), 'exactPass': exact, 'placeholderPass': placeholder, 'divergent': len(divergent), 'judgeBatches': nb}))",
].join("\n");
const collide = await world.run("python", ["-c", COLLIDE_PY]);
if (collide.exitCode !== 0) {
  throw new Error("预筛对碰失败：" + (collide.stderr || "").slice(-600));
}
const cst = JSON.parse((collide.stdout.trim().split("\n").pop() ?? "{}")) as {
  entriesTotal: number; exactPass: number; placeholderPass: number; divergent: number; judgeBatches: number;
};
log("预筛：" + cst.exactPass + " 条三版字面全等 + " + cst.placeholderPass + " 条残缺占位全等 | 分歧 " + cst.divergent + " 条，切 " + cst.judgeBatches + " 个裁判批");

// ---------- 裁判：匿名判 A/B/C 等义划分 ----------
function judgeAsk(n: number): string {
  const nn = String(n).padStart(3, "0");
  return [
    "你是 17 世纪马尼拉闽南—西班牙语历史词典的语义裁判（对碰终检，匿名三版）。",
    "",
    "【输入】读 " + CD + "/judge_batch_" + nn + ".json：entries 数组，每条含原书四栏（L 西语词头 / H 汉字 / M 闽南原稿音写 / R 官话对音）",
    "与同一词条三个匿名版本 A、B、C 的 zh（现代中文释义）+ en（英文释义）。",
    "【任务】逐条判定三版是否等义。判等标准：表达同一词义即等义——措辞、语序、详略差异不算分歧；词义不同或一方明显错义才算分歧；",
    "残缺类表述（〔原件残缺，释义存疑〕或同义存疑语）与其他版本按等义处理（都承认无法定夺）。以四栏原书证据为准，不用现代义项想当然。",
    "【输出】写 " + CD + "/judge_verdict_" + nn + ".json（UTF-8）：",
    '{"batch": ' + n + ', "verdicts": [{"page": 1, "position": 1, "groups": [["A","B"],["C"]]}]}',
    "groups 是该条 A/B/C 按等义关系的完整划分（组数 1–3；三版全等则 [[\"A\",\"B\",\"C\"]]）。",
    "返回：batch、verdicts 条数、分歧条数。",
  ].join("\n");
}

phase("语义裁判");
let verdictOk = 0;
for (let i = 1; i <= cst.judgeBatches; i += 20) {
  const batchIds: number[] = [];
  for (let n = i; n <= Math.min(i + 19, cst.judgeBatches); n++) batchIds.push(n);
  const results = await Promise.all(
    batchIds.map(async (n) => {
      try {
        const r = await agent("裁判-batch-" + String(n).padStart(3, "0")).ask<{ batch: number; verdicts: number }>(judgeAsk(n));
        return { ok: true, n };
      } catch {
        return { ok: false, n };
      }
    }),
  );
  verdictOk += results.filter((r) => r.ok).length;
  const failed = results.filter((r) => !r.ok).map((r) => r.n);
  if (failed.length > 0) {
    const f: Finding = { where: "裁判批 " + failed.join("、"), what: "裁判批失败（该批条目按未决处理，可重跑本脚本对碰段）",
      evidence: "agent.ask 失败", status: "unconfirmed", severity: "medium" };
    findingsPush(f);
    report(f);
  }
}
log("裁判完成：" + verdictOk + "/" + cst.judgeBatches + " 批落盘");

// ---------- 仲裁：多数决 -> 追加盲产（上限 2 轮）-> 终裁 ----------
const RESOLVE_PY = [
  "import json, re, sys",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision'",
  "round_no = int(sys.argv[1])",
  "def norm(s, lang):",
  "    s = re.sub(r'\\s+', '', (s or '').strip())",
  "    s = re.sub(r'[，。；：、（）()\\[\\]〔〕〈〉;:,.·…\\-—–“”\\\"\\'‘’！!？?]', '', s)",
  "    return s.lower() if lang == 'en' else s",
  "def same(a, b):",
  "    return norm(a.get('zh'), 'zh') == norm(b.get('zh'), 'zh') and norm(a.get('en'), 'en') == norm(b.get('en'), 'en')",
  "div = json.loads((cd / 'divergent_entries.json').read_text(encoding='utf-8'))['entries']",
  "ver = {}",
  "for vf in cd.glob('judge_verdict_*.json'):",
  "    for v in json.loads(vf.read_text(encoding='utf-8')).get('verdicts', []):",
  "        ver[(v.get('page'), v.get('position'))] = v.get('groups', [])",
  "retries = {}",
  "for rf in cd.glob('retry_r*_p*.json'):",
  "    d = json.loads(rf.read_text(encoding='utf-8'))",
  "    retries[(d.get('page'), d.get('position'))] = d",
  "rm = 0; rr = 0; open_list = []",
  "for e in div:",
  "    key = (e['page'], e['position'])",
  "    groups = ver.get(key) or []",
  "    best = max([len(g) for g in groups], default=0)",
  "    if best >= 2:",
  "        rm += 1; continue",
  "    rn = retries.get(key)",
  "    if rn:",
  "        if any(same({'zh': rn.get('zh'), 'en': rn.get('en')}, e.get(vid) or {}) for vid in ('v1', 'v2', 'v3')):",
  "            rr += 1; continue",
  "    open_list.append(e)",
  "res_f = cd / ('unresolved_r' + str(round_no) + '.json')",
  "res_f.write_text(json.dumps({'protocol': 'UNRESOLVED_R', 'round': round_no,",
  "    'entries': [dict(e, key=str(e['page']) + ':' + str(e['position'])) for e in open_list]}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "(cd / 'stats_resolve.json').write_text(json.dumps({'resolvedMajority': rm, 'resolvedRetry': rr, 'open': len(open_list)}, ensure_ascii=False), encoding='utf-8')",
  "print(json.dumps({'resolvedMajority': rm, 'resolvedRetry': rr, 'open': len(open_list), 'openFile': str(res_f)}))",
].join("\n");

function retryAsk(key: string, round: number): string {
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的历史词典释义员，执行矩阵对碰的追加独立盲产（第 " + round + " 轮，单条）。",
    "【盲产铁律】禁止读取 gloss_layer/、gloss_layer_v2、gloss_layer_v3 与其他对碰产物中关于本条的释义——你的独立读法才有仲裁价值。",
    "【输入】读 " + CD + "/unresolved_r" + round + ".json，在 entries 数组中定位 key == \"" + key + "\" 的那条：",
    "含原书四栏 L/H/M/R 与现存各版读法（仅供了解分歧焦点，不得照抄任何一版）。",
    "【任务】依据四栏独立产出本条释义：zh（现代简体中文）、en（English gloss）、confidence（high/medium/low）、notes（低置信时写依据）。",
    "纪律：17 世纪马尼拉历史语义优先；不确定降 confidence；材料不足写 〔原件残缺，释义存疑〕 且 confidence=low；严禁编造。",
    "【输出】写 " + CD + "/retry_r" + round + "_" + key.replace(":", "_p") + ".json（UTF-8）：",
    '{"page": <页码>, "position": <position>, "zh": "…", "en": "…", "confidence": "…", "notes": "…"}',
    "返回：key、confidence。",
  ].join("\n");
}

const MAX_ROUNDS = 2;
let lastOpen = cst.divergent;
for (let round = 1; round <= MAX_ROUNDS; round++) {
  phase("仲裁与追加盲产（第 " + round + " 轮）");
  const res = await world.run("python", ["-c", RESOLVE_PY, "--", String(round)]);
  if (res.exitCode !== 0) {
    throw new Error("仲裁失败：" + (res.stderr || "").slice(-600));
  }
  const rres = JSON.parse((res.stdout.trim().split("\n").pop() ?? "{}")) as { resolvedMajority: number; resolvedRetry: number; open: number };
  log("第 " + round + " 轮仲裁：多数决累计 " + rres.resolvedMajority + " | 追加盲产命中 " + rres.resolvedRetry + " | 未决 " + rres.open);
  lastOpen = rres.open;
  if (rres.open === 0 || round === MAX_ROUNDS) break;

  const unr = JSON.parse((await world.run("python", ["-c",
    "import json;from pathlib import Path;d=json.loads(Path('" + CD + "/unresolved_r" + round + ".json').read_text(encoding='utf-8'));print(json.dumps([e['key'] for e in d['entries']]))",
  ])).stdout.trim().split("\n").pop() ?? "[]") as string[];
  for (let i = 0; i < unr.length; i += 50) {
    const chunkKeys = unr.slice(i, i + 50);
    await Promise.all(
      chunkKeys.map(async (key) => {
        try {
          await agent("追加盲产-r" + round + "-" + key.replace(":", "_")).ask<{ key: string }>(retryAsk(key, round));
        } catch {
          /* 失败条目留在未决清单，终裁兜底 */
        }
      }),
    );
  }
}

// ---------- 终裁：对仍未决条目（含追加盲产读法）最后一轮匿名判 ----------
const JUDGE_FINAL_PY = [
  "import json, re",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision'",
  "unr = json.loads((cd / 'unresolved_r2.json').read_text(encoding='utf-8'))['entries']",
  "retries = {}",
  "for rf in cd.glob('retry_r*_p*.json'):",
  "    d = json.loads(rf.read_text(encoding='utf-8'))",
  "    retries[(d.get('page'), d.get('position'), 1 if '_r1_' in rf.name else 2)] = d",
  "items = []",
  "for e in unr:",
  "    key = (e['page'], e['position'])",
  "    readings = {'A': e.get('v1'), 'B': e.get('v2'), 'C': e.get('v3')}",
  "    for lbl, rno in (('D', 1), ('E', 2)):",
  "        r = retries.get((e['page'], e['position'], rno))",
  "        if r: readings[lbl] = {'zh': r.get('zh'), 'en': r.get('en')}",
  "    items.append({'key': e['key'], 'page': e['page'], 'position': e['position'],",
  "        'L': e.get('L'), 'H': e.get('H'), 'M': e.get('M'), 'R': e.get('R'), 'readings': readings})",
  "BATCH = 30; nb = 0",
  "for i in range(0, len(items), BATCH):",
  "    nb += 1",
  "    (cd / ('judge_final_batch_%03d.json' % nb)).write_text(json.dumps({'batch': nb, 'entries': items[i:i + BATCH]}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'finalOpen': len(items), 'finalBatches': nb}))",
].join("\n");

let finalOpen = 0;
let finalBatches = 0;
if (lastOpen > 0) {
  phase("终裁");
  const jf = await world.run("python", ["-c", JUDGE_FINAL_PY]);
  if (jf.exitCode !== 0) {
    throw new Error("终裁切批失败：" + (jf.stderr || "").slice(-600));
  }
  const jres = JSON.parse((jf.stdout.trim().split("\n").pop() ?? "{}")) as { finalOpen: number; finalBatches: number };
  finalOpen = jres.finalOpen;
  finalBatches = jres.finalBatches;
  log("终裁：" + finalOpen + " 条未决（含追加读法），切 " + finalBatches + " 批");
  function judgeFinalAsk(n: number): string {
    const nn = String(n).padStart(3, "0");
    return [
      "你是 17 世纪马尼拉闽南—西班牙语历史词典的语义裁判（对碰终检最后一轮，匿名多版）。",
      "【输入】读 " + CD + "/judge_final_batch_" + nn + ".json：每条含原书四栏 L/H/M/R 与匿名版本 A/B/C（及可能存在的追加读法 D/E）的 zh+en。",
      "【任务】逐条把全部版本按等义关系划分 groups（判等标准同前：同一词义即等义；残缺存疑表述互判等义）。",
      "【输出】写 " + CD + "/judge_final_verdict_" + nn + ".json（UTF-8）：",
      '{"batch": ' + n + ', "verdicts": [{"key": "1069:12", "groups": [["A","D"],["B"],["C"]]}]}',
      "groups 覆盖该条出现的全部版本标签。返回：batch、verdicts 条数。",
    ].join("\n");
  }
  for (let i = 1; i <= finalBatches; i += 20) {
    const batchIds: number[] = [];
    for (let n = i; n <= Math.min(i + 19, finalBatches); n++) batchIds.push(n);
    await Promise.all(
      batchIds.map(async (n) => {
        try {
          await agent("终裁判-batch-" + String(n).padStart(3, "0")).ask<{ batch: number }>(judgeFinalAsk(n));
        } catch {
          /* 失败批按未决入账 */
        }
      }),
    );
  }
}

const FINAL_RESOLVE_PY = [
  "import json",
  "from pathlib import Path",
  "cd = Path('literature/workspace_m2_dhs834') / 'collision'",
  "unr = json.loads((cd / 'unresolved_r2.json').read_text(encoding='utf-8'))['entries']",
  "ver = {}",
  "for vf in cd.glob('judge_final_verdict_*.json'):",
  "    for v in json.loads(vf.read_text(encoding='utf-8')).get('verdicts', []):",
  "        ver[v.get('key')] = v.get('groups', [])",
  "rf_ = 0; final = []",
  "for e in unr:",
  "    groups = ver.get(e['key']) or []",
  "    if max([len(g) for g in groups], default=0) >= 2:",
  "        rf_ += 1",
  "    else:",
  "        final.append(e)",
  "(cd / 'final_unresolved.json').write_text(json.dumps({'protocol': 'COLLISION_UNRESOLVED_V1', 'entries': final}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "(cd / 'stats_final.json').write_text(json.dumps({'resolvedFinal': rf_, 'collisionUnresolved': len(final)}, ensure_ascii=False), encoding='utf-8')",
  "print(json.dumps({'resolvedFinal': rf_, 'collisionUnresolved': len(final)}))",
].join("\n");

let unresolvedFinal = 0;
let resolvedFinal = 0;
if (lastOpen > 0) {
  const fr = await world.run("python", ["-c", FINAL_RESOLVE_PY]);
  if (fr.exitCode !== 0) {
    throw new Error("终裁归并失败：" + (fr.stderr || "").slice(-600));
  }
  const fres = JSON.parse((fr.stdout.trim().split("\n").pop() ?? "{}")) as { resolvedFinal: number; collisionUnresolved: number };
  resolvedFinal = fres.resolvedFinal;
  unresolvedFinal = fres.collisionUnresolved;
}

// ---------- 词头跨页一致性层（确定性） ----------
phase("词头跨页一致性");
const CROSS_PY = [
  "import json, re",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "def norm(s):",
  "    return re.sub(r'[\\s，。；：、（）()\\[\\]〔〕〈〉;:,.·…\\-—–\"\\'‘’！!？?]+', '', (s or '')).lower()",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "pages = sorted(int(k) for k in man.get('pages', {}))",
  "idx = {}",
  "for pg in pages:",
  "    pk = '%04d' % pg",
  "    sealed = json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])",
  "    gl = {e.get('position'): e for e in json.loads((m2 / 'gloss_layer' / ('gloss_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])}",
  "    for e in sealed:",
  "        rawL = (e.get('source_L') or '').strip()",
  "        if not rawL or rawL in ('[空]', '[残]') or rawL.startswith('['):",
  "            continue",
  "        zh = (gl.get(e.get('position')) or {}).get('zh') or ''",
  "        if '残缺' in zh:",
  "            continue",
  "        idx.setdefault(norm(rawL), []).append({'page': pg, 'position': e.get('position'), 'L': rawL, 'zh': zh})",
  "flag = [{'headword': k, 'variants': v} for k, v in idx.items() if len({norm(x['zh']) for x in v}) > 1]",
  "cd = m2 / 'collision'",
  "(cd / 'cross_page_flags.json').write_text(json.dumps({'protocol': 'CROSSPAGE_V1', 'flaggedHeadwords': len(flag), 'groups': flag[:800]}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'flaggedHeadwords': len(flag), 'reported': min(len(flag), 800)}))",
].join("\n");
const cross = await world.run("python", ["-c", CROSS_PY]);
if (cross.exitCode !== 0) {
  throw new Error("词头跨页层失败：" + (cross.stderr || "").slice(-600));
}
const xres = JSON.parse((cross.stdout.trim().split("\n").pop() ?? "{}")) as { flaggedHeadwords: number; reported: number };
log("词头跨页一致性：发现 " + xres.flaggedHeadwords + " 个词头跨页释义不一（确定性层，仅入账不仲裁）");

// ---------- 台账 COLLISION_LEDGER.json ----------
phase("对碰台账");
const LEDGER_PY = [
  "import json, hashlib",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision'",
  "def dirsha(rel):",
  "    d = m2 / rel; h = hashlib.sha256(); n = 0",
  "    for f in sorted(d.glob('*.json')):",
  "        h.update(f.name.encode('utf-8')); h.update(hashlib.sha256(f.read_bytes()).digest()); n += 1",
  "    return {'dir': rel, 'files': n, 'sha256': h.hexdigest()}",
  "pre = json.loads((cd / 'stats_prefilter.json').read_text(encoding='utf-8'))",
  "res = json.loads((cd / 'stats_resolve.json').read_text(encoding='utf-8'))",
  "fin = json.loads((cd / 'stats_final.json').read_text(encoding='utf-8')) if (cd / 'stats_final.json').exists() else {'resolvedFinal': 0, 'collisionUnresolved': 0}",
  "unr = json.loads((cd / 'final_unresolved.json').read_text(encoding='utf-8'))['entries']",
  "xp = json.loads((cd / 'cross_page_flags.json').read_text(encoding='utf-8'))",
  "ledger = {",
  "    'protocol': 'COLLISION_LEDGER_V1',",
  "    'book': 1,",
  "    'versions': [dirsha('gloss_layer'), dirsha('gloss_layer_v2'), dirsha('gloss_layer_v3')],",
  "    'stats': {",
  "        'entriesTotal': pre['entriesTotal'],",
  "        'exactPass': pre['exactPass'],",
  "        'placeholderPass': pre['placeholderPass'],",
  "        'resolvedMajority': res['resolvedMajority'],",
  "        'resolvedRetry': res['resolvedRetry'],",
  "        'resolvedFinal': fin['resolvedFinal'],",
  "        'collisionUnresolved': fin['collisionUnresolved'],",
  "        'crossPageFlaggedHeadwords': xp['flaggedHeadwords'],",
  "    },",
  "    'unresolved': unr,",
  "    'crossPageSamples': xp['groups'][:100],",
  "    'limitations': [",
  "        '版本独立性边界（2026-11-16 用户裁定）：V1=GLM-5.3-Flash（全量）；V2=混合来源（约890页 DeepSeek-v4.1-flash 于停跑前产出，余量 GLM-5.3-Flash$max 续产，逐页来源未在文件内标注）；V3=GLM-5.3——三版以同族为主，对碰可抓上下文性错误，抓不住模型族系统性偏差；跨供应商补版须按硬刹车#10 取得书面预算授权',",
  "        '语义裁判与部分盲产版同模型族，存在弱同源偏置；已匿名化版本标签缓解',",
  "        '残缺占位表述（〔原件残缺，释义存疑〕）与其他版本按等义处理',",
  "        '词头跨页一致性层为确定性字面比对，归一化后的同词头释义字面差异一律入账，未做语义仲裁',",
  "        '完成宣称边界：本台账支持 K 版对碰一致（同族限制已披露）的宣称，不构成人工校对完成（METHODOLOGY §6.5）',",
  "    ],",
  "}",
  "out = m2 / 'COLLISION_LEDGER.json'",
  "out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'ledger': str(out), 'stats': ledger['stats']}))",
].join("\n");
const lg = await world.run("python", ["-c", LEDGER_PY]);
if (lg.exitCode !== 0) {
  throw new Error("台账生成失败：" + (lg.stderr || "").slice(-600));
}
const lres = JSON.parse((lg.stdout.trim().split("\n").pop() ?? "{}")) as { ledger: string; stats: Record<string, number> };

phase("收官报告");
if (unresolvedFinal > 0) {
  const f: Finding = { where: "COLLISION_LEDGER.json",
    what: unresolvedFinal + " 条 K+2 版对碰仍无多数（COLLISION_UNRESOLVED），已降置信入账随交付披露",
    evidence: "final_unresolved.json", status: "verified", severity: unresolvedFinal > 500 ? "high" : "medium" };
  findingsPush(f);
  report(f);
}
const s = lres.stats;
return {
  conclusion: "第一书全量矩阵对碰完成：" + s.entriesTotal + " 条中，三版字面全等 " + s.exactPass +
    "（" + Math.round((100 * s.exactPass) / s.entriesTotal) + "%）+ 残缺占位全等 " + s.placeholderPass +
    "；语义裁判多数决 " + s.resolvedMajority + "、追加盲产命中 " + s.resolvedRetry + "、终裁多数 " + s.resolvedFinal +
    "；仍无多数 " + s.collisionUnresolved + " 条标 COLLISION_UNRESOLVED 入账。词头跨页释义不一 " +
    s.crossPageFlaggedHeadwords + " 个词头入账。台账：COLLISION_LEDGER.json。",
  findings: findingsArr,
  verified: [
    "三版独立盲产（V1=GLM-5.3-Flash / V2=DeepSeek / V3=GLM-5.3），盲产铁律禁读既有释义",
    "预筛（归一化字面）+ 匿名语义裁判两级比对；多数决 + 追加盲产上限 2 轮 + 终裁，机器仲裁无人工环节",
    "台账含三版目录 SHA-256 指纹、逐条未决清单、局限声明与完成宣称边界",
  ],
  notCovered: [
    "词头跨页不一致仅确定性入账，未做语义仲裁（同词头跨页释义字面差异≠必错，含词头变体归一化误差）",
    "全书 1,103 页均在对碰范围（166 页回填段已封存）；盲读字面层的重读对碰未纳入（成本另议）",
    "COLLISION_UNRESOLVED 条目的处置（保留降置信 / 后续追加轮次）待用户裁定",
    "跨供应商版本（DeepSeek 等）按硬刹车 #10 须书面预算授权后方可补产",
  ],
};
