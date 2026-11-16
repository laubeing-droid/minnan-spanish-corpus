// 对碰 V2 盲产：第一书释义层第二版独立盲产（矩阵对碰 K=3 的第 2 版，METHODOLOGY §6.5）。
// 铁律：盲产——子代理禁止读取 gloss_layer/（v1）及任何既有释义文件，只允许读封存件；
// 只写 gloss_layer_v2/；不碰 M1 冻结区；不碰 git；禁止编造——不确定一律降 confidence。

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

interface ValidationResult {
  pagesOk: number;
  missingPages: number[];
  missingCount: number;
  positionMismatch: number[];
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

const STEP = 10;
const M2 = "literature/workspace_m2_dhs834";
const OUT_DIR = M2 + "/gloss_layer_v2";
const findingsArr: Finding[] = [];

function findingsPush(f: Finding): void {
  findingsArr.push(f);
}

artifact.table("progress-v2", {
  title: "对碰 V2 盲产批次进度（全书封存页，按 BLIND_READ_MANIFEST 实时取数）",
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

const VALIDATE_PY = [
  "import json",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "man = json.loads((m2 / 'BLIND_READ_MANIFEST.json').read_text(encoding='utf-8'))",
  "ok = 0; missing = []; mismatch = []",
  "for pk in sorted(man.get('pages', {})):",
  "    g = m2 / 'gloss_layer_v2' / ('gloss_p' + pk + '.json')",
  "    if not g.exists():",
  "        missing.append(pk); continue",
  "    gd = json.loads(g.read_text(encoding='utf-8'))",
  "    sealed = {e.get('position') for e in json.loads((m2 / ('blind_read_p' + pk + '.json')).read_text(encoding='utf-8')).get('entries', [])}",
  "    produced = {e.get('position') for e in gd.get('entries', [])}",
  "    if sealed == produced: ok += 1",
  "    else: mismatch.append(pk)",
  "print(json.dumps({'pagesOk': ok, 'missingPages': missing[:20], 'missingCount': len(missing), 'positionMismatch': mismatch[:20]}))",
].join("\n");

function glossAsk(page: number): string {
  const pk = String(page).padStart(4, "0");
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的历史词典释义员，负责 PDF 第 " + page + " 页的逐条释义生产（矩阵对碰终检的第 2 版独立盲产）。",
    "",
    "【盲产铁律】本任务为独立盲产：禁止读取 literature/workspace_m2_dhs834/gloss_layer/、gloss_layer_v2、gloss_layer_v3",
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
    "【输出】写 literature/workspace_m2_dhs834/gloss_layer_v2/gloss_p" + pk + ".json（UTF-8）：",
    '{"page": ' + page + ', "entries": [{"position": 1, "zh": "…", "en": "…", "confidence": "high", "notes": ""}]}',
    "entries 数与 position 集合必须与封存件完全一致。",
    "返回：page、glossFile、entries（条数）、lowConfidence（低置信条数）、notes（一句话）。",
  ].join("\n");
}

phase("读清单与分组");
const pagesRun = await world.run("python", ["-c", PAGES_PY]);
if (pagesRun.exitCode !== 0) {
  throw new Error("清册读取失败：" + (pagesRun.stderr || "").slice(-300));
}
const allPages: number[] = JSON.parse((pagesRun.stdout.trim().split("\n").pop() ?? "[]"));
log("封存页 " + allPages.length + " 页，按 " + STEP + " 页一批盲产 V2");

const outcomes: BatchOutcome[] = [];
let lowTotal = 0;
let entryTotal = 0;

for (let i = 0; i < allPages.length; i += STEP) {
  const chunk = allPages.slice(i, i + STEP);
  const firstPg = chunk[0] ?? 0;
  const lastPg = chunk[chunk.length - 1] ?? 0;
  const range = String(firstPg).padStart(4, "0") + "-" + String(lastPg).padStart(4, "0");

  phase("盲产批");
  log("批次 " + range + "：" + chunk.length + " 页派盲产释义员");
  type Res = GlossPageResult | { error: string };
  const first = await Promise.all(
    chunk.map(async (p): Promise<Res> => {
      try {
        return await agent("盲产v2-p" + String(p).padStart(4, "0")).ask<GlossPageResult>(glossAsk(p));
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
    log(failedPages.length + " 页失败，重试一次");
    const second = await Promise.all(
      failedPages.map(async (p): Promise<Res> => {
        try {
          return await agent("盲产v2-p" + String(p).padStart(4, "0") + "-重试").ask<GlossPageResult>(glossAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    for (const r of second) {
      if (!("error" in r)) produced.push(r);
    }
  }
  produced.sort((a, b) => a.page - b.page);
  const entries = produced.reduce((a, r) => a + r.entries, 0);
  const low = produced.reduce((a, r) => a + r.lowConfidence, 0);
  lowTotal += low;
  entryTotal += entries;
  const stillMissing = chunk.filter((p) => !produced.some((r) => r.page === p));
  let outcome: BatchOutcome;
  if (stillMissing.length > 0) {
    const missList = stillMissing.map((p) => String(p).padStart(4, "0")).join("、");
    outcome = { range, status: "failed", pages: chunk.length, entries, lowConfidence: low,
      detail: "缺页：" + missList };
    const f: Finding = { where: "PDF " + range, what: "V2 盲产缺页 " + stillMissing.length + " 页：" + missList,
      evidence: "两轮派发均未返回", status: "unconfirmed", severity: "high" };
    findingsPush(f);
    report(f);
  } else {
    outcome = { range, status: "produced", pages: chunk.length, entries, lowConfidence: low, detail: "V2 盲产落盘" };
  }
  outcomes.push(outcome);
  report(outcome, "progress-v2");
}

phase("V2 校验");
const val = await world.run("python", ["-c", VALIDATE_PY]);
if (val.exitCode !== 0) {
  throw new Error("V2 校验失败：" + (val.stderr || "").slice(-300));
}
const vres: ValidationResult = JSON.parse((val.stdout.trim().split("\n").pop() ?? "{}"));
log("V2 校验：" + vres.pagesOk + " 页 OK | 缺页 " + vres.missingCount + " | position 不齐 " + vres.positionMismatch.length);

phase("收官报告");
const failedBatches = outcomes.filter((b) => b.status === "failed");
return {
  conclusion: "对碰 V2 独立盲产完成：" + allPages.length + " 页 / 约 " + entryTotal + " 条（zh+en），低置信自报 " + lowTotal +
    " 条；校验 " + vres.pagesOk + " 页 OK、缺页 " + vres.missingCount + "。失败批次 " + failedBatches.length + " 个" +
    (failedBatches.length > 0 ? "（见 findings）" : "") + "。下一跑：V3 盲产 + 三版对碰。",
  findings: findingsArr,
  verified: [
    "每页由独立子代理盲产并写 gloss_layer_v2/gloss_pXXXX.json",
    "校验脚本逐页核对 position 集合与封存件一致（VALIDATE_PY）",
    "盲产铁律写入每页任务书：禁读 gloss_layer/（v1）与任何既有释义",
  ],
  notCovered: [
    "V2 与 V1 的对碰在 V3 落盘后统一执行（对碰脚本见 对碰V3-第一书盲产加对碰）",
    "M1 独占 166 页不在本轮",
  ],
};
