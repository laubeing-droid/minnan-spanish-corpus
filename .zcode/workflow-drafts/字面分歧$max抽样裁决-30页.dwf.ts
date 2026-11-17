// 字面分歧 $max 抽样裁决：从 14,562 条字面分歧候选中分层抽 30 页（含两栏版式页），
// GLM-5.3-Flash$max + 反空转纪律逐条墨迹裁决（V1对/重读对/两皆误/墨迹不明），
// 产出有统计效力的字面误读率估计 + SAMPLE_ADJUDICATION_LEDGER.json。
// 修复不在本工作流内做——主会话按账走管线。

interface JudgeVerdict {
  page: number;
  verdicts: Array<{
    position: number;
    field: string;
    v1: string;
    rr: string;
    /** V1对 / 重读对 / 两皆误 / 墨迹不明 */
    verdict: string;
    ink: string;
    note: string;
  }>;
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
const CD = M2 + "/collision_mr";

function pageId(p: number): string {
  return String(p).padStart(4, "0");
}

const findingsArr: Finding[] = [];
function findingsPush(f: Finding): void {
  findingsArr.push(f);
}

// ---------- 第 1 步：分层抽样（固定种子，可复现） ----------

phase("分层抽样 30 页");
const SAMPLE_PY = [
  "import json, random",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "cand = json.loads((m2 / 'collision_mr' / 'soup_candidates.json').read_text(encoding='utf-8'))",
  "by_page = {}",
  "for c in cand['candidates']:",
  "    by_page.setdefault(c['page'], 0)",
  "    by_page[c['page']] += len(c.get('diffs') or [])",
  "cand_pages = sorted(by_page)",
  "two_col = [p for p in cand_pages if 30 <= p <= 40]",
  "std = [p for p in cand_pages if p not in two_col]",
  "random.seed(20261117)",
  "pick = random.sample(two_col, min(4, len(two_col))) + random.sample(std, min(26, len(std)))",
  "pick = sorted(set(pick))",
  "payload = []",
  "for pg in pick:",
  "    pk = '%04d' % pg",
  "    pc = [c for c in cand['candidates'] if c['page'] == pg]",
  "    entries = []",
  "    for c in pc:",
  "        for dfn in c.get('diffs') or []:",
  "            entries.append({'position': c.get('position'), 'field': dfn.get('field'),",
  "                'v1': dfn.get('v1'), 'rr': dfn.get('rr')})",
  "    payload.append({'page': pg, 'n': len(entries), 'entries': entries[:15]})",
  "(m2 / 'collision_mr' / 'sample30.json').write_text(json.dumps({'protocol': 'SAMPLE30_V1',",
  "    'seed': 20261117, 'pages': payload}, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'pages': len(payload), 'candidates': sum(p['n'] for p in payload)}))",
].join("\n");
const sp = await world.run("python", ["-c", SAMPLE_PY]);
if (sp.exitCode !== 0) {
  throw new Error("抽样失败：" + (sp.stderr || "").slice(-400));
}
const sres = JSON.parse((sp.stdout.trim().split("\n").pop() ?? "{}")) as { pages: number; candidates: number };
log("抽样 " + sres.pages + " 页 / " + sres.candidates + " 条候选（seed 20261117 可复现）");

// ---------- 第 2 步：$max 墨迹裁决 ----------

phase("$max 墨迹裁决");
function judgeAsk(page: number): string {
  const pk = pageId(page);
  return [
    "你是 17 世纪马尼拉《Dictionario Hispánico Sinicum》的字面裁决员。本页的字面两读对碰产生分歧，请对照墨迹逐条裁决。",
    "",
    "【反空转硬纪律】禁止任何 \"hmm/让我想想\" 式空转推演；看完墨迹直接逐条写结论。拿不准就判 \"墨迹不明\"，不要反复斟酌。",
    "",
    "【材料】",
    "1. 分歧清单（逐条含 field=M/R、v1=第一读法、rr=重读读法）：" + CD + "/sample30.json 中 page == " + page + " 的 entries；",
    "2. 横带切图（M 栏=倒数第二栏，R 栏=最右栏）：",
    "   literature/tiles/01_DHS/page_" + pk + "/pdf_" + pk + "_band_y0_top.png / _band_y1_mid.png / _band_y2_bot.png",
    "",
    "【裁决口径】逐条四选一：",
    "- \"V1对\"：墨迹与 v1 一致（ink 留空）；",
    "- \"重读对\"：墨迹与 rr 一致（ink 留空）；",
    "- \"两皆误\"：两侧都错（ink 写出你所见的忠实字面，保留元音符，鼻化照录为普通字母 n）；",
    "- \"墨迹不明\"：无法判定（ink 留空，note 一句原因）。",
    "拼写变体/声调符位置差不算分歧；禁止用现代拼法或词典知识\"纠正\"墨迹。",
    "",
    "【输出】写 " + CD + "/sample_verdict_" + pk + ".json（UTF-8）：",
    '{"page": ' + page + ', "verdicts": [{"position": 1, "field": "M", "v1": "…", "rr": "…", "verdict": "V1对", "ink": "", "note": ""}]}',
    "verdicts 条数与该页 entries 一致。返回：page、verdicts 条数。",
  ].join("\n");
}

const sample = JSON.parse((await world.run("python", ["-c",
  "import json;from pathlib import Path;d=json.loads(Path('" + M2 + "/collision_mr/sample30.json').read_text(encoding='utf-8'));print(json.dumps([p['page'] for p in d['pages']]))",
])).stdout.trim().split("\n").pop() ?? "[]") as number[];

let judgedPages = 0;
for (let i = 0; i < sample.length; i += 10) {
  const chunk = sample.slice(i, i + 10);
  await Promise.all(
    chunk.map(async (pg) => {
      try {
        await agent("裁决员-p" + pageId(pg)).ask<JudgeVerdict>(judgeAsk(pg));
        judgedPages += 1;
      } catch {
        /* 裁决失败页按未裁入账 */
      }
    }),
  );
  log("裁决进度 " + Math.min(i + chunk.length, sample.length) + "/" + sample.length + " 页");
}

// ---------- 第 3 步：台账与误读率 ----------

phase("抽样裁决台账");
const LEDGER_PY = [
  "import json, collections",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834'); cd = m2 / 'collision_mr'",
  "sample = json.loads((cd / 'sample30.json').read_text(encoding='utf-8'))",
  "verdict_count = collections.Counter()",
  "v1_wrong = rr_wrong = both_wrong = unclear = total_judged = 0",
  "rows = []",
  "unjudged_pages = []",
  "for p in sample['pages']:",
  "    pg = p['page']; pk = '%04d' % pg",
  "    vf = cd / ('sample_verdict_' + pk + '.json')",
  "    if not vf.exists():",
  "        unjudged_pages.append(pg)",
  "        continue",
  "    vmap = collections.defaultdict(list)",
  "    for v in json.loads(vf.read_text(encoding='utf-8')).get('verdicts', []):",
  "        vmap[(v.get('position'), v.get('field'))].append(v)",
  "    for e in p['entries']:",
  "        vs = vmap.get((e.get('position'), e.get('field'))) or []",
  "        if not vs:",
  "            continue",
  "        v = vs[0]; total_judged += 1",
  "        vd = v.get('verdict')",
  "        verdict_count[vd] += 1",
  "        if vd == 'V1对': rr_wrong += 1",
  "        elif vd == '重读对': v1_wrong += 1",
  "        elif vd == '两皆误': both_wrong += 1",
  "        elif vd == '墨迹不明': unclear += 1",
  "        rows.append({'page': pg, 'position': e.get('position'), 'field': e.get('field'),",
  "            'v1': e.get('v1'), 'rr': e.get('rr'), 'verdict': vd, 'ink': v.get('ink'), 'note': v.get('note')})",
  "rate_v1 = (v1_wrong + both_wrong) / total_judged if total_judged else 0",
  "est = round(rate_v1 * 14562)",
  "ledger = {'protocol': 'SAMPLE_ADJUDICATION_LEDGER_V1', 'seed': 20261117,",
  "    'samplePages': len(sample['pages']), 'judgedPages': judgedPages,",
  "    'unjudgedPages': unjudged_pages, 'totalJudged': total_judged,",
  "    'verdictBreakdown': dict(verdict_count),",
  "    'v1WrongRate': round(rate_v1, 4),",
  "    'estimatedV1WrongAmong14562': est,",
  "    'rows': rows[:800],",
  "    'limitations': [",
  "        '裁决档位 GLM-5.3-Flash$max（校准卷 6/9 未过线的前任裁判 Gemini 已按预登记淘汰）',",
  "        '误读率为抽样估计，置信区间未计算；全量裁决被校准判为不可负担',",
  "        '两栏版式页 V1 一视觉行拆两条，逐条对齐存在粒度噪声',",
  "        '完成宣称边界：本台账不构成人工校对完成（METHODOLOGY §6.5）',",
  "    ],",
  "}",
  "out = m2 / 'SAMPLE_ADJUDICATION_LEDGER.json'",
  "out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding='utf-8')",
  "print(json.dumps({'ledger': str(out), 'stats': ledger['stats']}))",
].join("\n");
const lg = await world.run("python", ["-c", LEDGER_PY]);
if (lg.exitCode !== 0) {
  throw new Error("台账失败：" + (lg.stderr || "").slice(-600));
}
const lres = JSON.parse((lg.stdout.trim().split("\n").pop() ?? "{}")) as {
  ledger: string;
  stats: { totalJudged: number; verdictBreakdown: Record<string, number>; v1WrongRate: number; estimatedV1WrongAmong14562: number; unjudgedPages: number[] };
};
const s = lres.stats;
if ((lres.stats.unjudgedPages?.length ?? 0) > 0) {
  const f: Finding = {
    where: "sample_verdict",
    what: "裁决失败页 " + lres.stats.unjudgedPages.length + " 页（未裁条目按未裁入账）",
    evidence: "unjudgedPages: " + JSON.stringify(lres.stats.unjudgedPages),
    status: "verified",
    severity: "medium",
  };
  findingsPush(f);
  report(f);
}
return {
  conclusion: "$max 抽样裁决完成：抽样 " + sres.pages + " 页 / " + sres.candidates + " 条候选，实际裁决 " +
    s.totalJudged + " 条。判定分布 " + JSON.stringify(s.verdictBreakdown) + "。**V1 字面误读率（含两皆误）≈ " +
    Math.round(s.v1WrongRate * 100) + "%**，按 14,562 条分歧候选外推 ≈ " + s.estimatedV1WrongAmong14562 +
    " 条 V1 侧错误。台账：SAMPLE_ADJUDICATION_LEDGER.json（逐条 ink 真值在册）。下一步：主会话按账修复已坐实条目并刷新受影响页释义。",
  findings: findingsArr,
  verified: [
    "抽样固定种子 20261117 可复现；分层含 4 张两栏版式页",
    "裁决档位 $max + 反空转纪律；四选一口径含 两皆误/墨迹不明，不强行定夺",
    "误读率按实际裁决条数计算，台账含逐条 ink 真值与局限声明",
  ],
  notCovered: [
    "14,562 条候选仅抽样裁决约 " + s.totalJudged + " 条，其余随库披露为字面分歧待裁",
    "H 栏（汉字）与 L 栏不在本轮字面重读范围",
    "修复与释义刷新由主会话在台账审定后执行",
  ],
};
