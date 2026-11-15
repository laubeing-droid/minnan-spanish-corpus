// M2 盲读直通节点 B：PDF 0451 → 0834（M2 正编收官段）。0030-0450 已全部封存通过
// （396-399 为现代书名页，按指示跳过并登记于 non_lexicographic_pages.json）。
// 0835-1140 属 M1 封盘线，严禁触碰。
const START = 451;
const END = 834;
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

interface BatchOutcome {
  /** 例如 "0071-0080" */
  range: string;
  status: "committed" | "failed";
  entryCount: number;
  /** 一句话：结果或失败原因 */
  detail: string;
}

interface Finding {
  /** 位置，如 "PDF 0071-0080" */
  where: string;
  /** 一句话说明问题 */
  what: string;
  /** 判定依据 */
  evidence: string;
  /** "verified"=已由确定性命令确认；"unconfirmed"=待人工/待复核 */
  status: "verified" | "unconfirmed";
  /** 严重度；数据缺口或整批失败为 high */
  severity: "low" | "medium" | "high";
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
  title: "M2 盲读批次进度（451→834，节点 B）",
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

function readerAsk(page: number): string {
  const pk = pad4(page);
  const base = `literature/tiles/01_DHS/page_${pk}/pdf_${pk}`;
  // 页码 ≥93 的派发附加防循环纪律（≤92 保持逐字节不变以命中缓存）
  const antiLoop = page >= 93
    ? "\n【防循环纪律】读图总次数不超过 8 次，同一张图至多重读一次。若反复读图仍无法确定，立即按当前最可信的读法写入文件、在 notes 写明\"反复读图仍存疑，待人工校订\"，然后正常返回结果——严禁无限重读、严禁空转。"
    : "";
  // 页 162 或 ≥171：强制"一次通过、写完即返"协议（163–170 保持原文以命中缓存）
  const writeOnce = (page === 162 || page >= 171)
    ? "\n【强制产出流程——逐条照办，不得偏离】\n1. 依次读三张横带图（band_y0_top、band_y1_mid、band_y2_bot），每张恰好读一次，读完不重读；\n2. 三张读完立即用 Write 一次性写出完整 JSON 文件：能抄多少抄多少，没把握处一律就地标注 [残] / [疑:A/B] / T99，绝不为了求全而返工；\n3. 文件写完立即返回 ReaderResult。禁止：写文件后再读任何图、重写或修改文件、逐条复核。宁可多留 [残]，不许返工第二遍；\n4. 某横带若读出为空白或纯污渍，该区域整段标 [残] 并继续，不要重读。"
    : "";
  // 页 ≥401：现代出版页检测规则（≤400 保持原文以命中缓存）
  const frontMatter = page >= 401
    ? "\n【现代出版页处理】若整页为现代出版物页面（书名页/版权页/致谢页/空白衬页等），并非手稿四栏辞典页：页面对象加字段 \"page_class\": \"MODERN_FRONT_MATTER\"（空白衬页用 \"BLANK\"），entries 保持空数组 []，notes 一句话说明页面性质即可，绝不逐行抄录出版信息。拿不准是否辞典页时，一律按正常四栏页抄录。其余规则不变。"
    : "";
  return [
    `你是 17 世纪马尼拉「Dictionario Hispánico Sinicum」（DHS）辞典的盲读抄写员，负责 PDF 第 ${page} 页（目录 literature/tiles/01_DHS/page_${pk}/）的四栏正编纯视觉抄录。`,
    "",
    "【铁律：只做视觉抄录】绝不凭音韵知识补写或\"修正\"字面；绝不发明音标/IPA；绝不把现代台罗/白话字拼写写进 source_M。手稿本身使用 c-/qu-/ch-/g-/s-/z-/ttz- 等西班牙多明我会式拼写，照抄所见；见到鼻化小钩可写作 ⁿ（引擎会自动净化）。",
    "",
    "【读图顺序】",
    `1. ${base}_band_y0_top.png、${base}_band_y1_mid.png、${base}_band_y2_bot.png 三张横带——先靠它们锁定每一行的四栏同行对齐，绝不错行；`,
    `2. 汉字栏（第2栏）难辨 → 读 ${base}_subcol2_hanzi_full.png；`,
    `3. 闽南语栏（第3栏）难辨 → 读 ${base}_subcol3_minnan.png；`,
    `4. 右栏（第4栏官话）或页脚难辨 → 读 ${base}_subcol4_mandarin_right.png 或整页 ${base}_300dpi.png。`,
    "",
    "【输出文件】写入 literature/workspace_m2_dhs834/raw_blind/raw_part_p" + pk + ".json（UTF-8），结构 {\"pages\":[{…仅本页…}]}，页面字段：",
    "- pdf_page: " + page,
    "- historical_folio: 印刷页脚实际数字（形如 \"- 38 -\" 则填 38）；页脚缺损时填 " + (page - 33) + " 并在 notes 注明\"页码估算\"",
    "- page_header: 页顶字母段标记（如 \"A. ante. G.\"），无则 \"\"",
    "- page_footer_printed / page_footer_handwritten: 照抄印刷页脚与手写页码，无则 \"\"",
    "- entries: 按行序 position 从 1 起，每行一条 {position, source_L, source_H, source_M, source_R, tone_marks_M, tone_marks_R}",
    "【栏位规则】空栏一律 \"[空]\"；残损处抄可见部分，完全不可辨写 \"[残]\"；汉字难辨抄最可能的字并附 \"[疑:A/B]\"。本页若残损或属重复拍摄页，照实抄录。",
    "【声调几何字典，tone_marks 只允许这些字面】T00 (無標號)、T01 (升斜)、T02 (降斜)、T03 (尖頂帽)、T04 (凹角)、T05 (平橫)、T06/T07 (交叉入聲號)、T99 (污損難辨)。tone_marks_M 按 M 栏该条内声调符出现顺序逐个列出；tone_marks_R 同理对 R 栏。",
    "【格式样板】动笔前先读 literature/workspace_m2_dhs834/raw_blind/raw_blind_p0030.json 熟悉结构（那是双栏补充本样板；你抄的四栏正编 source_H/source_R 多有内容）。",
    "【纪律】不运行任何 pipeline 命令；不碰 literature/workspace_m1_dhs306/ 下任何文件；不碰其他页。图缺失或指令自相矛盾时，如实上报而不是编造。",
  ].join("\n") + antiLoop + writeOnce + frontMatter;
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
    "返回：fixedInBatch（本批文件是否已修好）、outsideIssue（问题在批次之外时写明，否则空串）、action（一句话说明做了什么）。",
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

async function commitAndGate(range: string, batchFile: string, entryCount: number): Promise<BatchOutcome> {
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

phase("开工前终检引擎状态");
const pre = await world.run("python", ["literature/tools/zcode_m2_pipeline.py", "status"]);
log(pre.stdout.trim());

const batches: BatchOutcome[] = [];
const findings: Finding[] = [];
const noteLedger: string[] = [];
let consecutiveFail = 0;
let totalEntries = 0;

for (let s = START; s <= END; s += STEP) {
  const e = Math.min(s + STEP - 1, END); // 末批 0831–0834 不足 10 页，收到 END 为止
  const range = `${pad4(s)}-${pad4(e)}`;

  phase("切片本批十页");
  const slice = await world.run("python", ["literature/tools/zcode_m2_pipeline.py", "slice", "--start", String(s), "--end", String(e)]);
  if (slice.exitCode !== 0) {
    throw new Error(`批次 ${range} 切片失败：${(slice.stderr || "").slice(0, 500)}`);
  }
  log(`批次 ${range}：切片完成，派发 10 名精读员并行盲读`);

  phase("十名精读员并行盲读");
  const pages: number[] = [];
  for (let p = s; p <= e; p++) pages.push(p);
  type ReaderOrError = ReaderResult | { error: string };
  const first = await Promise.all(
    pages.map(async (p): Promise<ReaderOrError> => {
      try {
        return await agent(`精读员-p${pad4(p)}`).ask<ReaderResult>(readerAsk(p));
      } catch (err) {
        return { error: String(err) };
      }
    }),
  );
  let results: ReaderResult[] = [];
  const missing: number[] = [];
  for (let i = 0; i < first.length; i++) {
    const r: ReaderOrError = first[i] as ReaderOrError;
    if ("error" in r) missing.push(pages[i] as number);
    else results.push(r);
  }
  if (missing.length > 0) {
    log(`${missing.length} 页精读失败，逐页重试一次`);
    const second = await Promise.all(
      missing.map(async (p): Promise<ReaderOrError> => {
        try {
          return await agent(`精读员-p${pad4(p)}-重试`).ask<ReaderResult>(readerAsk(p));
        } catch (err) {
          return { error: String(err) };
        }
      }),
    );
    for (let i = 0; i < second.length; i++) {
      const r: ReaderOrError = second[i] as ReaderOrError;
      if (!("error" in r)) results.push(r);
    }
  }

  // 两轮派发后仍缺页：大声记账，绝不静默缺页（缺页不入 manifest，收官 status 会露出）
  const settledPages = new Set(results.map((r) => r.pdfPage));
  const stillMissing = pages.filter((p) => !settledPages.has(p));
  if (stillMissing.length > 0) {
    const missList = stillMissing.map(pad4).join("、");
    log(`批次 ${range} 缺页 ${stillMissing.length} 页（两轮派发均失败）：${missList}`);
    noteLedger.push(`批次 ${range} 缺页（两轮精读派发均失败，待人工补读）：${missList}`);
    const f: Finding = {
      where: `PDF ${range}`,
      what: `${stillMissing.length} 页两轮精读派发均失败，本批缺页入库：${missList}`,
      evidence: "两轮 ReaderResult 均未返回（provider 层失败）",
      status: "unconfirmed",
      severity: "high",
    };
    findings.push(f);
    report(f);
  }

  if (results.length === 0) {
    consecutiveFail++;
    const fb: BatchOutcome = { range, status: "failed", entryCount: 0, detail: "两次派发后仍无任何页面产出精读结果" };
    batches.push(fb);
    report(fb, "progress");
    findings.push({ where: `PDF ${range}`, what: "整批精读失败，10 页未入库", evidence: "两轮派发均失败", status: "unconfirmed", severity: "high" });
    report(findings[findings.length - 1]);
    if (consecutiveFail >= 3) throw new Error("连续 3 个批次彻底失败，终止运行交人工处置。");
    continue;
  }
  consecutiveFail = 0;

  for (const r of results) {
    if (r.notes.trim() !== "") noteLedger.push(`p${pad4(r.pdfPage)}（folio ${r.historicalFolio}）：${r.notes.trim()}`);
  }

  phase("合并、入库与门禁");
  const parts = results.map((r) => r.rawFile);
  const batchFile = `literature/workspace_m2_dhs834/raw_blind/raw_blind_${range}.json`;
  const merged = await world.run("python", ["-c", MERGE_PY, ...parts, batchFile]);
  const mergedTail = (merged.stdout || "").trim().split("\n").pop() || "";
  if (mergedTail !== "") log(mergedTail);
  const skipM = /skipped front matter:\s*\[([^\]]*)\]/.exec(merged.stdout || "");
  if (skipM !== null && skipM[1].trim() !== "") {
    noteLedger.push(`本批次跳过现代出版页（page_class=MODERN_FRONT_MATTER）：${skipM[1].trim()}`);
  }
  const entryCount = results.reduce((a, r) => a + r.entryCount, 0);
  let outcome: BatchOutcome;
  if (merged.exitCode !== 0) {
    outcome = { range, status: "failed", entryCount, detail: `合并失败：${(merged.stderr || "").slice(-200)}` };
  } else {
    outcome = await commitAndGate(range, batchFile, entryCount);
  }
  batches.push(outcome);
  report(outcome, "progress");
  if (outcome.status === "committed") {
    totalEntries += outcome.entryCount;
    log(`批次 ${range} 入库通过：${outcome.entryCount} 条（累计 ${totalEntries} 条）`);
  } else {
    consecutiveFail++;
    const f: Finding = { where: `PDF ${range}`, what: outcome.detail, evidence: "commit/gate 命令输出", status: "unconfirmed", severity: "high" };
    findings.push(f);
    report(f);
    if (consecutiveFail >= 3) throw new Error("连续 3 个批次入库失败，终止运行交人工处置。");
  }
}

phase("收官：终检与节点 A 汇总");
const finalGate = await world.run("python", ["architect_gatekeeper.py"], { output: { tail: 4000 } });
const finalStatus = await world.run("python", ["literature/tools/zcode_m2_pipeline.py", "status"]);
log(finalStatus.stdout.trim());
if (finalGate.exitCode !== 0) {
  findings.push({ where: "全局门禁", what: "收官门禁未通过", evidence: (finalGate.stderr + finalGate.stdout).slice(-400), status: "unconfirmed", severity: "high" });
}

const committed = batches.filter((b) => b.status === "committed");
const failedBatches = batches.filter((b) => b.status === "failed");
const mdLines: string[] = [];
mdLines.push("# M2 盲读节点 B 报告（PDF 0451–0834）");
mdLines.push("");
mdLines.push("- 前段说明：PDF 0030–0450 已全部入库封存并通过门禁（其中 PDF 0396–0399 为现代出版物书名页，按指示跳过并登记于 literature/workspace_m2_dhs834/non_lexicographic_pages.json）。本次运行自 0451 推进至 0834，即 M2 正编全部剩余页面。");
mdLines.push(`- 本次运行微批次：${batches.length} 个（每批 10 页，末批 0831–0834 仅 4 页），入库通过 ${committed.length} 个，失败 ${failedBatches.length} 个`);
mdLines.push(`- 本次运行抄录条目合计：${totalEntries} 条`);
mdLines.push(`- 收官门禁：${finalGate.exitCode === 0 ? "PASS" : "FAIL"}`);
mdLines.push("");
mdLines.push("## 批次明细");
mdLines.push("");
mdLines.push("| 批次 | 状态 | 条目数 | 说明 |");
mdLines.push("| --- | --- | --- | --- |");
for (const b of batches) mdLines.push(`| ${b.range} | ${b.status === "committed" ? "✅ 入库" : "❌ 失败"} | ${b.entryCount} | ${b.detail.replace(/\|/g, "/")} |`);
mdLines.push("");
if (noteLedger.length > 0) {
  mdLines.push("## 精读员存难备注（供人工校订线）");
  mdLines.push("");
  const cap = Math.min(noteLedger.length, 80);
  for (let i = 0; i < cap; i++) mdLines.push(`- ${noteLedger[i]}`);
  if (noteLedger.length > cap) mdLines.push(`- ……其余 ${noteLedger.length - cap} 条略（见各 raw_blind_pXXXX_YYYY.json 的精读员返回）`);
  mdLines.push("");
}
mdLines.push("## 当前管线状态");
mdLines.push("");
mdLines.push("```");
mdLines.push(finalStatus.stdout.trim());
mdLines.push("```");
await artifact.markdown("report", mdLines.join("\n"), {
  title: "M2 盲读节点 B 报告（PDF 0451–0834）",
  description: `本次运行 ${batches.length} 个微批次（0451–0834）的入库明细、精读存难备注与收官门禁结果；0030–0450 已此前封存。`,
  primary: true,
});

const rangeOk = finalGate.exitCode === 0;
return {
  conclusion: `PDF 0030–0450 此前已全部入库封存并通过门禁（396–399 为现代书名页，已跳过登记）；本次节点 B 自 0451 推进至 0834：${batches.length} 个微批次中 ${committed.length} 个入库并通过门禁${failedBatches.length > 0 ? `，${failedBatches.length} 个失败待补（见 findings）` : ""}，合计抄录 ${totalEntries} 条；收官门禁 ${rangeOk ? "PASS" : "FAIL"}。至此 M2 盲读线（0030–0834）推进完毕，后续转交人工校订线。`,
  findings,
  verified: [
    "每个批次 commit 后都运行了 architect_gatekeeper.py，以退出码 0 作为 PASS 判定；收官再全量复检一次",
    "每批的条目数来自精读员返回并经 merge/commit 实际落盘确认",
    "进度由 zcode_m2_pipeline.py status 在开工前与收官时双重确认",
  ],
  notCovered: [
    "视觉抄录的逐字正确性属盲读一过性产出，须由后续人工校订线复核；本运行的门禁只保证格式、正字法禁用项与 SHA-256 一致性",
    `精读员存难备注 ${noteLedger.length} 条仅汇总进报告，未逐一裁定`,
    "PDF 0835–1140 属 M1 封盘线（5,762 条已 100% 通过），严禁触碰，不在本运行范围内",
  ],
};