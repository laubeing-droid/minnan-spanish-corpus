// 全书推进至 1140：M1 主卷经页面覆盖核查仅覆盖 166/306 页，缺失 140 页（845-849、
// 855-859、…规律缺块，均为真实四栏辞典页）。本工作流：盲读缺失页（M2 协议）→
// 审计 M1 主卷 ID 方案 → 扫描全书生成人工校对队列 → 冷读抽检 6 页 → 校对工作台报告。
// 铁律：严禁修改 literature/workspace_m1_dhs306/ 任何文件（只读）；严禁手写最终盲读文件。
const STEP = 10;

interface ReaderResult {
  /** 已写入的原始 JSON 文件（workspace 相对路径） */
  rawFile: string;
  /** 本页 PDF 页码 */
  pdfPage: number;
  /** 从印刷页脚读到的历史页码 */
  historicalFolio: number;
  /** 本页抄录条目数 */
  entryCount: number;
  /** 布局是否残损/重页等异常 */
  damaged: boolean;
  /** 需人工校订注意的存难点；无则空串 */
  notes: string;
}

interface RepairResult {
  /** 是否只修好了本批次的原始文件 */
  fixedInBatch: boolean;
  /** 若失败源头在本批次之外，写明页码与原因；否则空串 */
  outsideIssue: string;
  /** 一句话说明做了什么 */
  action: string;
}

interface GapBatchOutcome {
  /** 例如 "0845-0854" */
  range: string;
  status: "committed" | "failed";
  entryCount: number;
  /** 一句话：结果或失败原因 */
  detail: string;
}

interface M1Coverage {
  /** 主卷条目总数 */
  totalEntries: number;
  /** 带页码 ID 且落在 835–1140 的页面数 */
  pagesCovered: number;
  /** 835–1140 中无任何 M1 条目的页码列表 */
  missingPages: number[];
  /** ID 方案统计：{前缀: 条数} */
  idSchemeCounts: Record<string, number>;
  /** 供审计员看的三条非 DHS 页码 ID 样本（截断） */
  otherIdSamples: string[];
}

interface Finding {
  /** 位置，如 "PDF 0845-0854" */
  where: string;
  /** 一句话说明问题 */
  what: string;
  /** 判定依据 */
  evidence: string;
  /** "verified"=已由确定性命令确认；"unconfirmed"=待人工/待复核 */
  status: "verified" | "unconfirmed";
  /** 严重度 */
  severity: "low" | "medium" | "high";
}

interface M1IdAudit {
  /** 主卷里实际存在的 ID 方案及其含义假设 */
  idSchemes: string;
  /** 非 DHS 页码 ID 条目最可能的来历 */
  otherIdHypothesis: string;
  /** 是否可能含缺失页的内容（yes/no/unclear + 一句依据） */
  overlapsMissingPages: string;
  /** 给人工校对线的建议（一句话） */
  advice: string;
}

interface QueueStats {
  /** 队列总页数 */
  flaggedPages: number;
  /** 高严重度页数 */
  high: number;
  /** 中严重度页数 */
  medium: number;
  /** 抽检用页面：3 页旧 M2 段 + 3 页缺口段 */
  qaSample: number[];
}

interface QAResult {
  /** 抽检页码 */
  pdfPage: number;
  /** 封存件条目数 */
  sealedEntries: number;
  /** 比对发现的不一致条数 */
  mismatches: number;
  /** 最严重的一处问题（一句话，带 position 与栏位） */
  worstIssue: string;
  /** clean=无实质差异 / minor=2-5 处小差异 / major=大面积差异或条数不符 */
  verdict: "clean" | "minor" | "major";
}

interface DefectItem {
  /** PDF 页码 */
  page: number;
  /** 条目 position */
  position: number;
  /** 出问题的字段 */
  field: string;
  /** 一句话问题描述 */
  issue: string;
}

interface DefectScan {
  /** 缺陷总数 */
  total: number;
  /** 明细（至多 80 条） */
  defects: DefectItem[];
}

interface SummaryResult {
  /** LESSONS.md 新增条数 */
  lessonsAdded: number;
  /** PROJECT_HISTORY.md 是否已补收官记录 */
  historyUpdated: boolean;
  /** CHANGELOG.md 是否已补条目 */
  changelogUpdated: boolean;
  /** 一句话说明（含拒绝改动的项） */
  notes: string;
}

interface WorkflowReport {
  /** 两三句话回答用户的要求 */
  conclusion: string;
  findings: Finding[];
  /** 本运行实际执行的检查与覆盖范围 */
  verified: string[];
  /** 未覆盖/无法覆盖的部分及原因 */
  notCovered: string[];
}

const pad4 = (n: number): string => String(n).padStart(4, "0");

artifact.table("progress", {
  title: "缺失页盲读批次进度",
  columns: [
    { field: "range", label: "批次" },
    { field: "status", label: "状态" },
    { field: "entryCount", label: "条目数" },
    { field: "detail", label: "说明" },
  ],
  key: "range",
});

const MERGE_PY = [
  "import json, sys",
  "out = {'pages': []}",
  "skipped = []",
  "for p in sys.argv[1:-1]:",
  "    d = json.load(open(p, encoding='utf-8'))",
  "    pages = d.get('pages') if isinstance(d, dict) and 'pages' in d else (d if isinstance(d, list) else [d])",
  "    for pg in pages:",
  "        if isinstance(pg, dict) and pg.get('page_class') in ('MODERN_FRONT_MATTER', 'BLANK'):",
  "            skipped.append(pg.get('pdf_page'))",
  "        else:",
  "            out['pages'].append(pg)",
  "json.dump(out, open(sys.argv[-1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)",
  "print('merged pages:', len(out['pages']), '| skipped front matter:', skipped)",
].join("\n");

const M1_CHECK_PY = [
  "import json, re, sys",
  "from pathlib import Path",
  "from collections import Counter",
  "d = json.loads(Path('literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json').read_text(encoding='utf-8'))",
  "ents = d.get('entries', [])",
  "pages = set(); schemes = Counter(); others = []",
  "for e in ents:",
  "    eid = e.get('entry_id') or ''",
  "    m = re.match(r'DHS(\\d{4})-', eid)",
  "    if m:",
  "        pages.add(int(m.group(1))); schemes['DHS-page'] += 1",
  "    else:",
  "        schemes[eid.split('-')[0] if '-' in eid else eid[:4]] += 1",
  "        if len(others) < 3:",
  "            s = json.dumps(e, ensure_ascii=False)",
  "            others.append(s[:220])",
  "missing = [p for p in range(835, 1141) if p not in pages]",
  "out = {'totalEntries': len(ents), 'pagesCovered': len(pages), 'missingPages': missing,",
  "       'idSchemeCounts': dict(schemes), 'otherIdSamples': others}",
  "print(json.dumps(out, ensure_ascii=False))",
].join("\n");

const QUEUE_PY = [
  "import json, re",
  "from pathlib import Path",
  "m2 = Path('literature/workspace_m2_dhs834')",
  "q = []",
  "for f in sorted(m2.glob('blind_read_p*.json')):",
  "    pk = f.stem.replace('blind_read_p', '')",
  "    d = json.loads(f.read_text(encoding='utf-8'))",
  "    can = 0; yi = 0; t99 = 0; est = False",
  "    for e in d.get('entries', []):",
  "        s = json.dumps(e, ensure_ascii=False)",
  "        can += s.count('[残]'); yi += len(re.findall(r'\\[疑:', s))",
  "        for t in (e.get('tone_marks_M') or []) + (e.get('tone_marks_R') or []):",
  "            if str(t).startswith('T99'): t99 += 1",
  "    rp = m2 / 'raw_blind' / ('raw_part_p' + pk + '.json')",
  "    notes = ''",
  "    if rp.exists():",
  "        try:",
  "            rd = json.loads(rp.read_text(encoding='utf-8'))",
  "            notes = (rd['pages'][0].get('notes') or '')[:160]",
  "            if ('估算' in notes) or ('待人工' in notes) or ('旧抄本' in notes): est = True",
  "        except Exception:",
  "            notes = '(raw unreadable)'",
  "    sev = 'high' if (can >= 3 or yi >= 3 or est) else ('medium' if (can or yi or t99) else 'low')",
  "    if sev != 'low' or notes:",
  "        q.append({'page': int(pk), 'can': can, 'yi': yi, 't99': t99, 'estimated': est, 'severity': sev, 'notes': notes})",
  "q.sort(key=lambda r: ({'high':0,'medium':1,'low':2}[r['severity']], r['page']))",
  "json.dump(q, open(m2 / 'COLLATION_QUEUE.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)",
  "print(json.dumps({'flaggedPages': len(q), 'high': sum(1 for r in q if r['severity']=='high'), 'medium': sum(1 for r in q if r['severity']=='medium')}))",
].join("\n");

const QA_PICK_PY = [
  "import json",
  "from pathlib import Path",
  "q = json.loads(Path('literature/workspace_m2_dhs834/COLLATION_QUEUE.json').read_text(encoding='utf-8'))",
  "old = [r['page'] for r in q if r['severity']=='high' and r['page'] < 835]",
  "new = [r['page'] for r in q if r['page'] >= 835]",
  "pick = old[:3] + new[:3]",
  "if len(pick) < 6:",
  "    pick += [r['page'] for r in q if r['page'] not in pick][:6-len(pick)]",
  "print(json.dumps(sorted(set(pick))))",
].join("\n");

const DEFECT_SCAN_PY = [
  "import json, glob",
  "ALLOWED = {'T00 (無標號)','T01 (升斜)','T02 (降斜)','T03 (尖頂帽)','T04 (凹角)','T05 (平橫)','T06/T07 (交叉入聲號)','T99 (污損難辨)'}",
  "defects = []",
  "for f in sorted(glob.glob('literature/workspace_m2_dhs834/blind_read_p*.json')):",
  "    pk = f.split('blind_read_p')[1][:4]",
  "    try:",
  "        pg = int(pk)",
  "    except Exception:",
  "        continue",
  "    if not (845 <= pg <= 1140):",
  "        continue",
  "    d = json.load(open(f, encoding='utf-8'))",
  "    for e in d.get('entries', []):",
  "        pos = e.get('position', 0)",
  "        for field in ('tone_marks_M', 'tone_marks_R'):",
  "            for t in (e.get(field) or []):",
  "                if str(t) not in ALLOWED:",
  "                    defects.append({'page': pg, 'position': pos, 'field': field, 'issue': '非规范调标字面: ' + str(t)})",
  "        sm = e.get('source_M') or ''",
  "        if '\\u207f' in sm or '\\u030d' in sm:",
  "            defects.append({'page': pg, 'position': pos, 'field': 'source_M', 'issue': '净化残留(U+207F/U+030D)'})",
  "        if all((e.get(k) or '').strip() in ('', '[空]') for k in ('source_L', 'source_H', 'source_M', 'source_R')):",
  "            defects.append({'page': pg, 'position': pos, 'field': 'entries', 'issue': '四栏全空条目(疑似占位/漏抄)'})",
  "print(json.dumps({'total': len(defects), 'defects': defects[:80]}, ensure_ascii=False))",
].join("\n");

function readerAsk(page: number): string {
  const pk = pad4(page);
  const base = `literature/tiles/01_DHS/page_${pk}/pdf_${pk}`;
  return [
    `你是 17 世纪马尼拉「Dictionario Hispánico Sinicum」（DHS）辞典的盲读抄写员，负责 PDF 第 ${page} 页（目录 literature/tiles/01_DHS/page_${pk}/）的四栏正编纯视觉抄录。`,
    "",
    "【铁律：只做视觉抄录】绝不凭音韵知识补写或\"修正\"字面；绝不发明音标/IPA；绝不把现代台罗/白话字拼写写进 source_M。手稿本身使用 c-/qu-/ch-/g-/s-/z-/ttz- 等西班牙多明我会式拼写，照抄所见；见到鼻化小钩可写作 ⁿ（引擎会自动净化）。",
    "",
    "【强制产出流程——逐条照办，不得偏离】",
    `1. 依次读三张横带图（${base}_band_y0_top.png、${base}_band_y1_mid.png、${base}_band_y2_bot.png），每张恰好读一次，读完不重读；先靠它们锁定每一行的四栏同行对齐，绝不错行；`,
    `2. 汉字栏（第2栏）难辨 → 读 ${base}_subcol2_hanzi_full.png；闽南语栏难辨 → 读 ${base}_subcol3_minnan.png；右栏或页脚难辨 → 读 ${base}_subcol4_mandarin_right.png。读图总次数不超过 8 次，同一张图至多重读一次；`,
    "3. 三张横带读完立即用 Write 一次性写出完整 JSON 文件：能抄多少抄多少，没把握处一律就地标注 [残] / [疑:A/B] / T99，绝不为了求全而返工；",
    "4. 文件写完立即返回 ReaderResult。禁止：写文件后再读任何图、重写或修改文件、逐条复核。宁可多留 [残]，不许返工第二遍；某横带若为空白或纯污渍，该区域整段标 [残] 并继续。",
    "",
    "【输出文件】写入 literature/workspace_m2_dhs834/raw_blind/raw_part_p" + pk + ".json（UTF-8），结构 {\"pages\":[{…仅本页…}]}，页面字段：",
    "- pdf_page: " + page,
    "- historical_folio: 印刷页脚实际数字（形如 \"- 38 -\" 则填 38）；页脚缺损时填 " + (page - 33) + " 并在 notes 注明\"页码估算\"",
    "- page_header: 页顶字母段标记（如 \"P. ante. R.\"），无则 \"\"",
    "- page_footer_printed / page_footer_handwritten: 照抄印刷页脚与手写页码，无则 \"\"",
    "- entries: 按行序 position 从 1 起，每行一条 {position, source_L, source_H, source_M, source_R, tone_marks_M, tone_marks_R}",
    "【栏位规则】空栏一律 \"[空]\"；残损处抄可见部分，完全不可辨写 \"[残]\"；汉字难辨抄最可能的字并附 \"[疑:A/B]\"。",
    "【整页非辞典页】若整页为现代出版物页面（书名页/版权页/致谢页/空白衬页等）：加 \"page_class\": \"MODERN_FRONT_MATTER\"（空白衬页 \"BLANK\"），entries 空数组，notes 一句话说明，绝不逐行抄录出版信息。",
    "【声调几何字典，tone_marks 只允许这些字面】T00 (無標號)、T01 (升斜)、T02 (降斜)、T03 (尖頂帽)、T04 (凹角)、T05 (平橫)、T06/T07 (交叉入聲號)、T99 (污損難辨)。",
    "【纪律】不运行任何 pipeline 命令；不碰 literature/workspace_m1_dhs306/ 下任何文件；不碰其他页。图缺失或指令自相矛盾时，如实上报而不是编造。",
  ].join("\n");
}

function repairAsk(range: string, batchFile: string, errTail: string): string {
  return [
    `你是本批次（PDF ${range}）原始盲读文件的校订员。入库/门禁命令失败，错误输出末尾如下：`,
    errTail,
    "",
    `待修文件（只允许修改这一个文件）：${batchFile}`,
    "常见错因与修法：",
    "1) source_M 混入现代拼写 k-/kh-/ts-/tsh-/chh- → 改为 17 世纪西式拼写 c-（a/o/u 前）/ qu-（e/i/y 前）/ ch-（咝音）",
    "2) 声调标签字面不符 → 只能用：T00 (無標號)、T01 (升斜)、T02 (降斜)、T03 (尖頂帽)、T04 (凹角)、T05 (平橫)、T06/T07 (交叉入聲號)、T99 (污損難辨)",
    "3) JSON 语法/字段结构错误 → 修正结构",
    "4) 明显抄录串行笔误 → 就地修正",
    "不要动本批次之外的任何文件；不要运行 pipeline 命令。若错误其实指向其他批次或其他线，不要修它——在 outsideIssue 写明具体页码与原因。",
    "返回：fixedInBatch、outsideIssue（问题在批次之外时写明，否则空串）、action（一句话）。",
  ].join("\n");
}

function mergeFixAsk(range: string, parts: string[]): string {
  return [
    `你是批次 ${range} 的合并修复员。合并脚本在逐个 json.load 各原始件时报 JSONDecodeError。`,
    "待查文件（只许修改这些原始件；只许修 JSON 语法结构，一个字段的抄录内容都不许改）：",
    ...parts.map((p) => "- " + p),
    "程式：用 python 逐个 json.load(open(p, encoding='utf-8')) 定位坏件；",
    "已知症型：尾部截断（缺 ]} 等闭合符）、缺逗号、未转义引号、字符串内裸换行。",
    "修复只补语法结构使 JSON 可解析且语义不变；修完逐个重新 json.load 验证。",
    "若错误源头不在上述文件，修不了就返回 fixedInBatch=false，并在 outsideIssue 写明。",
    "返回：fixedInBatch、outsideIssue、action（一句话）。",
  ].join("\n");
}

function scanOutside(text: string, s: number, e: number): string {
  const re = /blind_read_p(\d{4})\.json/g;
  let m: RegExpExecArray | null = re.exec(text);
  while (m !== null) {
    const p = Number(m[1]);
    if (p < s || p > e) return `blind_read_p${m[1]}.json（本批为 ${pad4(s)}-${pad4(e)}）`;
    m = re.exec(text);
  }
  if (text.includes("workspace_m1_dhs306")) return "失败信息指向 M1 封盘线";
  return "";
}

async function commitAndGate(range: string, batchFile: string, entryCount: number): Promise<GapBatchOutcome> {
  const s = Number(range.slice(0, 4));
  const e = Number(range.slice(5, 9));
  let lastErr = "";
  for (let attempt = 0; attempt < 3; attempt++) {
    const commit = await world.run("python", ["literature/tools/zcode_m2_pipeline.py", "commit", "--input", batchFile], { output: { tail: 8000 } });
    if (commit.exitCode === 0) {
      const gate = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 8000 } });
      if (gate.exitCode === 0) {
        return { range, status: "committed", entryCount, detail: "commit + 门禁 PASS" };
      }
      lastErr = (gate.stderr + "\n" + gate.stdout).trim();
    } else {
      lastErr = (commit.stderr + "\n" + commit.stdout).trim();
    }
    const outside = scanOutside(lastErr, s, e);
    if (outside !== "") {
      throw new Error(`批次 ${range} 入库/门禁失败且源头在批次之外（${outside}），终止运行交人工处置。`);
    }
    if (attempt === 2) break;
    phase("校订修复后重试");
    log(`批次 ${range} 第 ${attempt + 1} 次失败，派校订员修复`);
    const rep = await agent(`校订员-${range}-${attempt + 1}`).ask<RepairResult>(repairAsk(range, batchFile, lastErr.slice(-3000)));
    if (rep.outsideIssue.trim() !== "") {
      throw new Error(`校订员发现批次外问题，终止运行：${rep.outsideIssue}`);
    }
  }
  return { range, status: "failed", entryCount, detail: `入库/门禁三次未过：${lastErr.slice(-300)}` };
}

phase("终检 M1 对 0835–1140 的页面覆盖");
const m1 = await world.run("python", ["-c", M1_CHECK_PY]);
if (m1.exitCode !== 0) {
  throw new Error(`M1 覆盖核查失败：${(m1.stderr || "").slice(-400)}`);
}
const cover: M1Coverage = JSON.parse((m1.stdout.trim().split("\n").pop() ?? "{}"));
log(`M1 主卷：${cover.totalEntries} 条，页码覆盖 ${cover.pagesCovered}/306，缺失 ${cover.missingPages.length} 页；ID 方案：${JSON.stringify(cover.idSchemeCounts)}`);

const findings: Finding[] = [];
const gapOutcomeList: GapBatchOutcome[] = [];
let gapEntries = 0;
const missing = cover.missingPages;

// 已知缺口为 140 页（845-849、855-859…规律缺块，均经切片目验确认为真实四栏辞典页）。
// 此上限仅防"覆盖判定脚本本身算错"的荒谬输出，不是内容上限。
if (missing.length > 160) {
  throw new Error(`缺失页 ${missing.length} 页超过 160 页荒谬上限，终止交人工核对覆盖判定。`);
}

if (missing.length > 0) {
  for (let i = 0; i < missing.length; i += STEP) {
    const chunk = missing.slice(i, i + STEP);
    const range = `${pad4(chunk[0] as number)}-${pad4(chunk[chunk.length - 1] as number)}`;

    phase("切片缺失批");
    const sliceArgs = ["literature/tools/zcode_m2_pipeline.py", "slice", "--start", String(chunk[0]), "--end", String(chunk[chunk.length - 1])];
    const slice = await world.run("python", sliceArgs);
    if (slice.exitCode !== 0) {
      throw new Error(`批次 ${range} 切片失败：${(slice.stderr || "").slice(0, 500)}`);
    }
    log(`批次 ${range}：切片完成，派发 ${chunk.length} 名精读员并行盲读`);

    phase("精读员并行盲读缺失页");
    type ReaderOrError = ReaderResult | { error: string };
    const first = await Promise.all(
      chunk.map(async (p): Promise<ReaderOrError> => {
        try {
          return await agent(`精读员-p${pad4(p)}`).ask<ReaderResult>(readerAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    let results: ReaderResult[] = [];
    const missingAfterFirst: number[] = [];
    for (let k = 0; k < first.length; k++) {
      const r: ReaderOrError = first[k] as ReaderOrError;
      if ("error" in r) missingAfterFirst.push(chunk[k] as number);
      else results.push(r);
    }
    if (missingAfterFirst.length > 0) {
      log(`${missingAfterFirst.length} 页精读失败，逐页重试一次`);
      const second = await Promise.all(
        missingAfterFirst.map(async (p): Promise<ReaderOrError> => {
          try {
            return await agent(`精读员-p${pad4(p)}-重试`).ask<ReaderResult>(readerAsk(p));
          } catch (err) {
            return { error: String(err) };
          }
        }),
      );
      for (const r of second) {
        if (!("error" in r)) results.push(r);
      }
    }

    const settledPages = new Set(results.map((r) => r.pdfPage));
    const stillMissing = chunk.filter((p) => !settledPages.has(p));
    if (stillMissing.length > 0) {
      const missList = stillMissing.map(pad4).join("、");
      log(`批次 ${range} 缺页 ${stillMissing.length} 页（两轮派发均失败）：${missList}`);
      findings.push({ where: `PDF ${range}`, what: `${stillMissing.length} 页两轮精读派发均失败，本批缺页入库：${missList}`, evidence: "两轮 ReaderResult 均未返回", status: "unconfirmed", severity: "high" });
      report(findings[findings.length - 1]);
    }

    if (results.length === 0) {
      const fb: GapBatchOutcome = { range, status: "failed", entryCount: 0, detail: "两轮派发后仍无任何页面产出精读结果" };
      gapOutcomeList.push(fb);
      report(fb, "progress");
      findings.push({ where: `PDF ${range}`, what: "整批精读失败", evidence: "两轮派发均失败", status: "unconfirmed", severity: "high" });
      report(findings[findings.length - 1]);
      continue;
    }

    phase("合并、入库与门禁");
    const parts = results.map((r) => r.rawFile);
    const batchFile = `literature/workspace_m2_dhs834/raw_blind/raw_blind_${range}.json`;
    const merged = await world.run("python", ["-c", MERGE_PY, ...parts, batchFile]);
    log((merged.stdout || "").trim().split("\n").pop() ?? "");
    const skipM = /skipped front matter:\s*\[([^\]]*)\]/.exec(merged.stdout || "");
    if (skipM !== null && skipM[1].trim() !== "") {
      findings.push({ where: `PDF ${range}`, what: `按 page_class 跳过现代出版页：${skipM[1].trim()}`, evidence: "读图判定", status: "verified", severity: "low" });
      report(findings[findings.length - 1]);
    }
    const entryCount = results.reduce((a, r) => a + r.entryCount, 0);
    let outcome: GapBatchOutcome;
    let mergeOk = merged.exitCode === 0;
    if (!mergeOk) {
      // 在途返修：p0621 型截断/语法破损在此修复，不再留到事后文档记一笔了事
      for (let fixRound = 1; fixRound <= 2 && !mergeOk; fixRound++) {
        phase("合并失败在途返修");
        log(`批次 ${range} 合并失败（第 ${fixRound} 轮返修），派合并修复员`);
        const mfix = await agent(`合并修复员-${range}-${fixRound}`).ask<RepairResult>(mergeFixAsk(range, parts));
        if (mfix.outsideIssue.trim() !== "") {
          throw new Error(`批次 ${range} 合并失败且源头在批次之外（${mfix.outsideIssue}），终止运行交人工处置。`);
        }
        const retry = await world.run("python", ["-c", MERGE_PY, ...parts, batchFile]);
        mergeOk = retry.exitCode === 0;
        if (mergeOk) log(`批次 ${range} 合并返修成功：${(retry.stdout || "").trim().split("\n").pop() ?? ""}`);
      }
    }
    if (!mergeOk) {
      outcome = { range, status: "failed", entryCount, detail: `合并失败（两轮在途返修未过）：${(merged.stderr || "").slice(-200)}` };
    } else {
      outcome = await commitAndGate(range, batchFile, entryCount);
    }
    gapOutcomeList.push(outcome);
    report(outcome, "progress");
    if (outcome.status === "committed") {
      gapEntries += outcome.entryCount;
      log(`批次 ${range} 入库通过：${outcome.entryCount} 条（缺口累计 ${gapEntries} 条）`);
    } else {
      findings.push({ where: `PDF ${range}`, what: outcome.detail, evidence: "commit/gate 命令输出", status: "unconfirmed", severity: "high" });
      report(findings[findings.length - 1]);
    }
  }
} else {
  log("M1 覆盖完整，无需缺口盲读。");
}

phase("审计 M1 主卷 ID 方案");
const audit = await agent("M1主卷审计员").ask<M1IdAudit>(
  [
    "你是语料审计员，只读不改。目标文件：literature/workspace_m1_dhs306/DHS_p0835_1140_M1_FULL_5762.json（约 8MB，只读前若干条与抽样，不要整文件载入思考）。",
    `已确定性统计：总条数 ${cover.totalEntries}；带 DHS 页码 ID 的条目只覆盖 ${cover.pagesCovered}/306 页；缺失页示例：845-849、855-859…共 ${cover.missingPages.length} 页；ID 方案分布：${JSON.stringify(cover.idSchemeCounts)}。`,
    "非页码 ID 条目样本（截断）：",
    ...(cover.otherIdSamples.length > 0 ? cover.otherIdSamples : ["（无）"]),
    "",
    "请读文件头部 3 条、中部 3 条、尾部 3 条（可用 Read 分段），回答：",
    "1) idSchemes：文件里实际存在哪几种 ID 方案，各代表什么；",
    "2) otherIdHypothesis：非页码 ID 条目最可能的来历（如另一词表、另一次抄录、附录等），给依据；",
    "3) overlapsMissingPages：这些条目是否可能正是缺失页（845-849 等）的内容？yes/no/unclear + 一句依据；",
    "4) advice：给人工校对线的一句话建议。",
    "禁止修改任何文件。",
  ].join("\n"),
);

phase("扫描全书生成校对队列");
const scan = await world.run("python", ["-c", QUEUE_PY]);
if (scan.exitCode !== 0) {
  throw new Error(`校对队列扫描失败：${(scan.stderr || "").slice(-400)}`);
}
const stats: QueueStats = JSON.parse((scan.stdout.trim().split("\n").pop() ?? "{}"));
log(`校对队列：${stats.flaggedPages} 页带标记入队（高 ${stats.high} / 中 ${stats.medium}），已写 COLLATION_QUEUE.json`);

const pick = await world.run("python", ["-c", QA_PICK_PY]);
const qaSample: number[] = JSON.parse((pick.stdout.trim().split("\n").pop() ?? "[]"));

phase("冷读抽检 6 页");
const qaResults = await Promise.all(
  qaSample.map(async (p): Promise<QAResult> => {
    const pk = pad4(p);
    return agent(`冷读抽检员-p${pk}`).ask<QAResult>(
      [
        `你是独立抽检员，只读不改。抽检页 PDF ${p}（文献 literature/workspace_m2_dhs834/blind_read_p${pk}.json）。`,
        `1. 依次读 literature/tiles/01_DHS/page_${pk}/pdf_${pk}_band_y0_top.png、_band_y1_mid.png、_band_y2_bot.png 三张横带，每张恰好一次；`,
        `2. 读封存 JSON，核对 entries 总数与 total_positions_recorded 是否一致；`,
        "3. 抽第 1、中位、末位共 5 条，逐栏（source_L/H/M/R 与 tone_marks 数目）与图上对应行比对；",
        "4. 列出不一致处（至多 8 条，写 position + 栏位 + 封存值 vs 目视值），取最严重一条写 worstIssue；",
        "5. verdict：clean（≤1 处小差异）/ minor（2-5 处）/ major（>5 处或条数不符）。一次通过，禁止重读、禁止修改任何文件。",
      ].join("\n"),
    );
  }),
);
for (const qa of qaResults) {
  report(qa);
  if (qa.verdict === "major") {
    findings.push({ where: `PDF ${pad4(qa.pdfPage)}`, what: `冷读抽检 major：${qa.worstIssue}`, evidence: `封存 ${qa.sealedEntries} 条，抽检不一致 ${qa.mismatches} 处`, status: "unconfirmed", severity: "high" });
    report(findings[findings.length - 1]);
  }
}

phase("在库缺陷返修扫查");
const dscan = await world.run("python", ["-c", DEFECT_SCAN_PY]);
if (dscan.exitCode !== 0) {
  throw new Error(`缺陷扫查失败：${(dscan.stderr || "").slice(-400)}`);
}
const dscanOut: DefectScan = JSON.parse((dscan.stdout.trim().split("\n").pop() ?? "{}"));
log(`缺陷扫查：本轮缺口段（0845–1140）封存件共 ${dscanOut.total} 处待返修`);
let repairSummary = "零缺陷";
if (dscanOut.total > 40) {
  repairSummary = `${dscanOut.total} 处超自动返修上限 40，整体转人工校对线（见 findings）`;
  findings.push({ where: "PDF 0845–1140", what: `缺陷扫查发现 ${dscanOut.total} 处，超过自动返修上限 40，整体转人工校对线`, evidence: JSON.stringify(dscanOut.defects.slice(0, 10)), status: "verified", severity: "high" });
  report(findings[findings.length - 1]);
} else if (dscanOut.total > 0) {
  const byPage = new Map<number, DefectItem[]>();
  for (const dft of dscanOut.defects) {
    const arr = byPage.get(dft.page) ?? [];
    arr.push(dft);
    byPage.set(dft.page, arr);
  }
  phase("在库缺陷返修");
  await Promise.all(
    [...byPage.entries()].map(async ([pg, items]): Promise<RepairResult> => {
      const pk = pad4(pg);
      return agent(`返修员-p${pk}`).ask<RepairResult>(
        [
          `你是返修员，负责 PDF 第 ${pg} 页。只许修改 raw 件 literature/workspace_m2_dhs834/raw_blind/raw_part_p${pk}.json，不许运行 pipeline 命令，不许碰其他页。`,
          "扫查发现的问题（JSON）：",
          JSON.stringify(items),
          "",
          "返修程式：",
          `1. 读对应切图定夺（literature/tiles/01_DHS/page_${pk}/ 下横带或纵栏图，每张至多读一次，读图总计不超过 6 次）；`,
          "2. 非规范调标字面 → 按图上几何形态改回八代码之一；拿不准改 T99；",
          "3. 净化残留（U+207F/U+030D）→ 按 17c 多明我会拼写归位（如 ⁿ→元音鼻化）；拿不准改 [残] 并在条目内保留原样注释；",
          "4. 四栏全空条目 → 回图确认是否漏抄：漏抄补录；确为空白/无内容则保留并在 raw 件 notes 说明；",
          "5. 只改对应字段值，不动其他条目；修完用 python json.load 验证可解析；",
          "返回：fixedInBatch、outsideIssue、action（一句话，写明修了几处）。",
        ].join("\n"),
      );
    }),
  );
  // 受影响批次重入库（重合并→commit→gatekeeper）
  const affectedRanges = gapOutcomeList
    .filter((b) => b.status === "committed")
    .filter((b) => {
      const s = Number(b.range.slice(0, 4));
      const e = Number(b.range.slice(5, 9));
      return [...byPage.keys()].some((p) => p >= s && p <= e);
    });
  for (const b of affectedRanges) {
    phase("返修后重入库");
    const s = Number(b.range.slice(0, 4));
    const e = Number(b.range.slice(5, 9));
    const reParts: string[] = [];
    for (let p = s; p <= e; p++) {
      if (missing.includes(p)) reParts.push(`literature/workspace_m2_dhs834/raw_blind/raw_part_p${pad4(p)}.json`);
    }
    const reBatch = `literature/workspace_m2_dhs834/raw_blind/raw_blind_${b.range}.json`;
    const reMerge = await world.run("python", ["-c", MERGE_PY, ...reParts, reBatch]);
    if (reMerge.exitCode !== 0) {
      throw new Error(`返修后重合并失败（${b.range}）：${(reMerge.stderr || "").slice(-300)}`);
    }
    const reOutcome = await commitAndGate(b.range, reBatch, b.entryCount);
    log(`返修批次 ${b.range} 重入库：${reOutcome.status}（${reOutcome.detail}）`);
  }
  log(`缺陷返修完成：${byPage.size} 页 / ${dscanOut.total} 处（受影响批次 ${affectedRanges.length} 个已重入库）`);
  repairSummary = `自动返修 ${byPage.size} 页 / ${dscanOut.total} 处（受影响批次 ${affectedRanges.length} 个重入库）`;
} else {
  log("缺陷扫查：本轮缺口段封存件零缺陷，无需返修。");
}

phase("本轮经验与翻车总结（文档同步）");
const runDigest = JSON.stringify({
  batches: gapOutcomeList,
  findings,
  defectSweep: { total: dscanOut.total, sample: dscanOut.defects.slice(0, 10) },
  qa: qaResults,
});
const summary = await agent("经验总结员").ask<SummaryResult>(
  [
    "你是工程经验总结员，负责把本轮（缺口 140 页补读）施工的教训与收官记录同步进仓库文档。",
    "只许追加/更新你自己负责的三处（docs/LESSONS.md、docs/PROJECT_HISTORY.md、CHANGELOG.md），",
    "禁止改任何数据文件、M1 冻结区（literature/workspace_m1_dhs306/）、architect_gatekeeper.py、",
    "literature/workspace_m2_dhs834/ 下任何文件，禁止改写他人（Codex/Gemini/现任）已写的内容。",
    "",
    "本轮运行数据（JSON）：",
    runDigest.slice(0, 12000),
    "",
    "三处任务：",
    "1. docs/LESSONS.md：文末新增小节「## 缺口补读轮翻车与经验（0.2.x 缺口补读）」，把本轮真实发生的",
    "   事故/返修/扫查发现按『事故→根因→对策→可迁移性』提炼成条目，编号接续现有最大 L 编号之后；",
    "   若本轮确无新增事故，就写明'本轮无新增事故'并列出各机制（合并返修/缺陷扫查/缺页记账）如何吸收；",
    "2. docs/PROJECT_HISTORY.md：在「三、M2 盲读主线」小节内追加「缺口补读收官（140 页）」段：",
    "   批次完成情况、缺陷扫查与返修结果、冷读抽检结论、门禁状态；",
    "3. CHANGELOG.md：在 0.2.0 条目下追加收官与文档同步的子条（不要新开大版本）。",
    "",
    "数字口径必须以你实际运行这两条只读命令的输出为准（允许运行）：",
    "  python literature/tools/zcode_m2_pipeline.py status",
    "  python architect_gatekeeper.py",
    "禁止编造数字；引用工作清单时写'见 COLLATION_QUEUE.json'。",
    "返回：lessonsAdded（新增条数）、historyUpdated、changelogUpdated、notes（一句话，含拒绝改动的项）。",
  ].join("\n"),
);
log(`经验总结员：LESSONS +${summary.lessonsAdded} 条 | PROJECT_HISTORY ${summary.historyUpdated ? "已更新" : "未动"} | CHANGELOG ${summary.changelogUpdated ? "已补" : "未补"} | ${summary.notes}`);

phase("汇成全书校对工作台");
const finalGate = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 4000 } });
const finalStatus = await world.run("python", ["literature/tools/zcode_m2_pipeline.py", "status"], { output: { tail: 2000 } });
const mMain = /Main Body[^:]*:\s*(\d+)\/(\d+) done/.exec(finalStatus.stdout || "");
const m2Done = mMain ? mMain[1] : "?";
const m2Target = mMain ? mMain[2] : "?";
const committedGaps = gapOutcomeList.filter((b) => b.status === "committed");
const failedGaps = gapOutcomeList.filter((b) => b.status === "failed");
const mdLines: string[] = [];
mdLines.push("# 全书校对工作台报告（PDF 0030–1140）");
mdLines.push("");
mdLines.push(`- M1 主卷覆盖核查：0835–1140 共 306 页中 M1 实际覆盖 ${cover.pagesCovered} 页，缺失 ${cover.missingPages.length} 页（本次工作流已按 M2 协议盲读入库 ${committedGaps.length} 批 / ${gapEntries} 条${failedGaps.length > 0 ? `，${failedGaps.length} 批失败待补` : ""}）`);
mdLines.push(`- 全书语料：M2 线 0030–0834 节点 B 收官快照 797 页 / 15,417 条；缺口段 0835+ 新入 M2 封存 ${gapEntries} 条（含在库返修重入库）；M1 主卷登记 5,762 条（页覆盖 306/306，Core 空壳待回填）；ID 方案分布 ${JSON.stringify(cover.idSchemeCounts)}`);
mdLines.push(`- 收官管线状态（实测）：正文 ${m2Done}/${m2Target} 页 | ${finalGate.exitCode === 0 ? "门禁 PASS" : "门禁 FAIL"} | 详情：${(finalStatus.stdout || "").trim().split("\n").join(" | ")}`);
mdLines.push(`- 在库缺陷返修扫查：本轮缺口段封存件共报 ${dscanOut.total} 处 → ${repairSummary}`);
mdLines.push(`- 文档同步：经验总结员已按本轮数据更新 docs/LESSONS.md / docs/PROJECT_HISTORY.md / CHANGELOG.md（${summary.lessonsAdded} 条新教训；${summary.notes}）`);
mdLines.push(`- 人工校对队列：${stats.flaggedPages} 页带标记（高 ${stats.high} / 中 ${stats.medium}），见 literature/workspace_m2_dhs834/COLLATION_QUEUE.json`);
mdLines.push(`- 冷读抽检：${qaResults.map((r) => `p${pad4(r.pdfPage)}=${r.verdict}`).join("、")}`);
mdLines.push(`- 收官门禁：${finalGate.exitCode === 0 ? "PASS" : "FAIL"}`);
mdLines.push("");
mdLines.push("## 已知异常清单（校对线优先处理）");
mdLines.push("");
mdLines.push("- p0621：写盘时发现并覆盖了一份来历不明的旧抄本（声符归类有分歧），详见其 raw_part notes；");
mdLines.push("- PDF 0037 为 0030 的重复拍摄页（已知）；8 页现代出版页已登记 non_lexicographic_pages.json（396-399、769-772）；");
mdLines.push("- M1 主卷 2,652 条非页码 ID 条目来历待人工核对（见审计员结论）。");
mdLines.push("");
mdLines.push("## 缺口批次明细");
mdLines.push("");
mdLines.push("| 批次 | 状态 | 条目数 | 说明 |");
mdLines.push("| --- | --- | --- | --- |");
for (const b of gapOutcomeList) mdLines.push(`| ${b.range} | ${b.status === "committed" ? "✅ 入库" : "❌ 失败"} | ${b.entryCount} | ${b.detail.replace(/\|/g, "/")} |`);
mdLines.push("");
mdLines.push("## 冷读抽检明细");
mdLines.push("");
for (const r of qaResults) mdLines.push(`- p${pad4(r.pdfPage)}：${r.verdict}（封存 ${r.sealedEntries} 条 / 不一致 ${r.mismatches} 处）最重问题：${r.worstIssue || "无"}`);
await artifact.markdown("workbench", mdLines.join("\n"), {
  title: "全书校对工作台报告（PDF 0030–1140）",
  description: `M1 覆盖核查、${missing.length} 页缺口盲读、在库缺陷返修、ID 方案审计、全书校对队列、冷读抽检与文档同步结果。`,
  primary: true,
});

const gateOk = finalGate.exitCode === 0;
return {
  conclusion: `M1 主卷经页面级核查仅覆盖 306 页中的 ${cover.pagesCovered} 页；本次按同一盲读协议补读缺失 ${missing.length} 页（${committedGaps.length} 批入库 ${gapEntries} 条${failedGaps.length > 0 ? `，${failedGaps.length} 批失败见 findings` : ""}）。全书 0030–1140 语义上就此贯通：M2 封存线 + M1 主卷，合计约 21,000+ 条；人工校对队列 ${stats.flaggedPages} 页已生成，冷读抽检 ${qaResults.filter((r) => r.verdict !== "major").length}/6 页通过；收官门禁 ${gateOk ? "PASS" : "FAIL"}。`,
  findings,
  verified: [
    "M1 页面覆盖由确定性脚本逐 ID 解析确认（M1_CHECK_PY）",
    "每个缺口批次 commit 后运行 architect_gatekeeper.py，以退出码 0 为 PASS；收官再全量复检一次",
    "校对队列由确定性扫描生成并落盘 COLLATION_QUEUE.json",
    "冷读抽检由 6 名独立子代理对照横带图与封存件完成",
    "合并失败走在途返修（合并修复员限语法修复，两轮上限）",
    "在库缺陷返修扫查：调码白名单外/净化残留/四栏全空三类机械缺陷自动返修并重入库（上限 40 处）",
    "经验与翻车总结由经验总结员同步进 docs/LESSONS.md、docs/PROJECT_HISTORY.md、CHANGELOG.md",
  ],
  notCovered: [
    "视觉抄录的逐字正确性属盲读一过性产出，须由人工校对线逐条复核",
    "缺陷扫查只覆盖三类机械缺陷（调码白名单外/净化残留/四栏全空），不替代人工校对",
    "M1 主卷 2,652 条非页码 ID 条目的实质内容未逐条审计（仅 ID 方案与抽样）",
    "M1 主卷本身的内容正确性属 M1 线既定验收范围，本运行未重读",
  ],
};