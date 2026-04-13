const PptxGenJS = require("pptxgenjs");
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"

// ─── COLORS ────────────────────────────────────────────────────
const C = {
  teal:      "0891B2",
  tealDark:  "076A87",
  tealMid:   "5BB8D4",
  tealLight: "E0F2F7",
  tealPale:  "F0FAFD",
  dark:      "1F2937",
  gray:      "6B7280",
  lgray:     "E5E7EB",
  xlgray:    "F3F4F6",
  white:     "FFFFFF",
  red:       "DC2626",
  green:     "059669",
};

// ─── CONSTANTS ─────────────────────────────────────────────────
const SW = 13.33; // slide width
const SH = 7.5;   // slide height
const MX = 0.5;   // margin x
const CW = SW - MX * 2; // content width = 12.33

// ─── HELPERS ───────────────────────────────────────────────────
function hdr(s, title, sub) {
  s.addShape(pptx.ShapeType.rect, { x:0, y:0, w:SW, h:0.15, fill:{color:C.teal} });
  s.addText(title, { x:MX, y:0.22, w:CW, h:0.62, fontSize:27, bold:true, color:C.dark, fontFace:"Arial" });
  if (sub) s.addText(sub, { x:MX, y:0.84, w:CW, h:0.3, fontSize:12.5, color:C.gray, fontFace:"Arial" });
}

function insightBar(s, txt) {
  s.addShape(pptx.ShapeType.rect, { x:0, y:6.9, w:SW, h:0.52, fill:{color:C.tealLight}, line:{color:C.teal,width:1} });
  s.addText(txt, { x:MX, y:6.9, w:CW, h:0.52, fontSize:12, bold:true, color:C.tealDark, align:"center", fontFace:"Arial", valign:"middle" });
}

function card(s, x, y, w, h, opts={}) {
  s.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    fill: { color: opts.fill || C.white },
    line: { color: opts.line || C.lgray, width: opts.lw || 1 },
    shadow: opts.shadow ? { type:"outer", blur:5, offset:2, angle:45, color:"AAAAAA", opacity:0.2 } : undefined
  });
}

function arrow(s, x1, y1, x2, y2) {
  s.addShape(pptx.ShapeType.line, { x:x1, y:y1, w:x2-x1, h:y2-y1, line:{color:C.gray,width:1.2} });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 1 — TITLE
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };

  // Top bar
  s.addShape(pptx.ShapeType.rect, { x:0, y:0, w:SW, h:0.22, fill:{color:C.teal} });
  // Bottom bar
  s.addShape(pptx.ShapeType.rect, { x:0, y:7.22, w:SW, h:0.28, fill:{color:C.teal} });
  // Left accent
  s.addShape(pptx.ShapeType.rect, { x:MX, y:1.6, w:0.1, h:2.6, fill:{color:C.teal} });

  // Main title
  s.addText("資料作成の効率化が、\n新規事業の売上を最大化させる", {
    x:0.82, y:1.5, w:11.2, h:2.8,
    fontSize:38, bold:true, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.35
  });
  // Subtitle
  s.addText("提案資料作成の変革による営業力強化", {
    x:0.82, y:4.45, w:10, h:0.55,
    fontSize:17, color:C.gray, fontFace:"Arial"
  });
  // Divider
  s.addShape(pptx.ShapeType.line, { x:0.82, y:5.15, w:5.5, h:0, line:{color:C.lgray,width:1} });
  // Tag
  s.addText("AIハッカソン　｜　新規事業部　大川龍之介", {
    x:0.82, y:5.3, w:10, h:0.38,
    fontSize:13.5, color:C.gray, fontFace:"Arial"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 2 — WHY PROPOSALS MATTER
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "なぜ「提案資料」が重要なのか", "良いプロダクトも、顧客に伝わらなければ価値がない");

  const cY = 1.2, cH = 5.45, cW = 5.85;

  // ── LEFT card ──
  card(s, MX, cY, cW, cH, { fill:C.tealLight, line:C.teal, lw:1.5 });
  s.addShape(pptx.ShapeType.rect, { x:MX, y:cY, w:cW, h:0.12, fill:{color:C.teal} });
  s.addText("顧客との接点最大化", { x:MX+0.2, y:cY+0.2, w:cW-0.4, h:0.45, fontSize:15, bold:true, color:C.tealDark, fontFace:"Arial" });

  // Flow diagram inside left card
  const flowItems = ["良いプロダクト", "提案資料", "価値伝達"];
  flowItems.forEach((item, i) => {
    const fy = cY + 0.85 + i * 1.35;
    const isTeal = i === 1;
    s.addShape(pptx.ShapeType.rect, {
      x:MX+0.35, y:fy, w:cW-0.7, h:0.72,
      fill:{color: isTeal ? C.teal : C.white},
      line:{color: isTeal ? C.teal : C.tealMid, width:1.5}
    });
    s.addText(item, {
      x:MX+0.35, y:fy, w:cW-0.7, h:0.72,
      fontSize:15, bold:true, color: isTeal ? C.white : C.dark,
      align:"center", valign:"middle", fontFace:"Arial"
    });
    if (i < 2) {
      s.addText("↓", {
        x:MX+0.35, y:fy+0.72, w:cW-0.7, h:0.63,
        fontSize:18, bold:true, color:C.teal, align:"center", fontFace:"Arial", valign:"middle"
      });
    }
  });

  // ── RIGHT card ──
  const rX = MX + cW + 0.63;
  card(s, rX, cY, cW, cH, { fill:C.tealLight, line:C.teal, lw:1.5 });
  s.addShape(pptx.ShapeType.rect, { x:rX, y:cY, w:cW, h:0.12, fill:{color:C.teal} });
  s.addText("リソースの最適配分", { x:rX+0.2, y:cY+0.2, w:cW-0.4, h:0.45, fontSize:15, bold:true, color:C.tealDark, fontFace:"Arial" });

  // Balance visual
  const bars = [
    { label:"作成にかける時間", arrow:"↓", color:C.gray,  size:28 },
    { label:"商談・関係構築の時間", arrow:"↑", color:C.teal, size:28 },
  ];
  bars.forEach((b, i) => {
    const by = cY + 1.1 + i * 2.1;
    s.addText(b.arrow, { x:rX+0.3, y:by, w:0.6, h:0.8, fontSize:b.size, bold:true, color:b.color, align:"center", fontFace:"Arial", valign:"middle" });
    s.addText(b.label, { x:rX+1.0, y:by+0.1, w:cW-1.2, h:0.6, fontSize:14, bold:i===1, color:b.color, fontFace:"Arial", valign:"middle" });
    if (i === 0) {
      s.addShape(pptx.ShapeType.line, { x:rX+0.2, y:by+1.05, w:cW-0.4, h:0, line:{color:C.lgray,width:1} });
    }
  });
  s.addShape(pptx.ShapeType.rect, { x:rX+0.2, y:cY+5.0, w:cW-0.4, h:0.3, fill:{color:C.tealLight}, line:{color:C.tealMid,width:0} });
  s.addText("「作成」ではなく「対話」に時間を使う必要がある", {
    x:rX+0.2, y:cY+5.0, w:cW-0.4, h:0.3, fontSize:10.5, color:C.tealDark, fontFace:"Arial", valign:"middle"
  });

  insightBar(s, "示唆：資料作成プロセスこそが、営業活動の隠れたレバレッジポイント");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 3 — THREE PROBLEMS
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "営業現場を縛る「資料作成の課題」", "1案件 半日〜1日の資料作成が、営業の行動量を制限している");

  const cY=1.2, cH=5.45, cW=3.9, gap=0.265;
  const cards2 = [
    {
      num:"01", title:"スピード不足",
      body:"商談後の提案資料は\n「当日〜翌日・次回商談」が業界標準\n\n商談直後の検討意欲が最も高いタイミングに\n資料が届かない",
      sub:"コア業務の時間減\nノンコア業務が増え、本来注力すべき業務に\n取りかかれない"
    },
    {
      num:"02", title:"個別感ゼロ",
      body:"決まったテンプレートで対応するため\nクライアント固有の課題・ゴールが\n資料に反映されない\n\n「どこにでもある資料」として受け取られ\n検討が前に進まない",
      sub:""
    },
    {
      num:"03", title:"属人的バラつき",
      body:"テンプレ化されていない場合\n提案ロジックの精度が担当者によって大きく異なる\n\nトップ営業の思考・ロジックが\n組織に蓄積されない",
      sub:"（現在は標準化対応済み）"
    },
  ];

  cards2.forEach((c, i) => {
    const x = MX + i * (cW + gap);
    // Top accent bar
    s.addShape(pptx.ShapeType.rect, { x, y:cY, w:cW, h:0.1, fill:{color:C.teal} });
    card(s, x, cY+0.1, cW, cH-0.1, { fill:C.white, line:C.lgray, shadow:true });
    // Number
    s.addText(c.num, { x:x+0.2, y:cY+0.22, w:1.0, h:0.7, fontSize:32, bold:true, color:C.tealLight, fontFace:"Arial" });
    // Title
    s.addText(c.title, { x:x+0.2, y:cY+0.95, w:cW-0.4, h:0.5, fontSize:17, bold:true, color:C.teal, fontFace:"Arial" });
    s.addShape(pptx.ShapeType.line, { x:x+0.2, y:cY+1.5, w:cW-0.4, h:0, line:{color:C.lgray,width:1} });
    // Body
    s.addText(c.body, { x:x+0.2, y:cY+1.6, w:cW-0.4, h:3.2, fontSize:11.5, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.45 });
    if (c.sub) {
      s.addText(c.sub, { x:x+0.2, y:cY+4.85, w:cW-0.4, h:0.4, fontSize:10, color:C.gray, fontFace:"Arial", italic:true });
    }
  });

  insightBar(s, "示唆：資料作成の工数削減が、営業力解放の第一歩");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 4 — LOGIC TREE
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "売上構造のロジックツリー（全体像）", "売上を上げる打ち手は、構造的に特定できる");

  const startY = 1.3;
  const rH = 0.62;
  const rGap = 0.32;

  // Helper: draw a box
  const bx = (txt, x, y, w, h, fill, txtColor, fs, bold, border) => {
    s.addShape(pptx.ShapeType.rect, { x, y, w, h, fill:{color:fill}, line:{color: border||fill, width: border?2:1} });
    s.addText(txt, { x, y, w, h, fontSize:fs||13, bold:bold!==false, color:txtColor||C.dark, align:"center", valign:"middle", fontFace:"Arial" });
  };

  // ── ROW 1: 売上高 ──
  const r1y = startY;
  bx("売上高", MX, r1y, CW, rH, C.dark, C.white, 17, true);

  // connector down
  const r1bot = r1y + rH;
  const r2y = r1bot + rGap;
  s.addShape(pptx.ShapeType.line, { x:SW/2, y:r1bot, w:0, h:rGap/2, line:{color:C.gray,width:1.2} });
  s.addShape(pptx.ShapeType.line, { x:MX+1.5, y:r1bot+rGap/2, w:CW-3.0, h:0, line:{color:C.gray,width:1.2} });
  s.addShape(pptx.ShapeType.line, { x:MX+1.5, y:r1bot+rGap/2, w:0, h:rGap/2, line:{color:C.gray,width:1.2} });
  s.addShape(pptx.ShapeType.line, { x:MX+CW-1.5, y:r1bot+rGap/2, w:0, h:rGap/2, line:{color:C.gray,width:1.2} });

  // ── ROW 2: 成約数 | 受注単価 ──
  const r2w = (CW - 0.18) / 2;
  bx("成約数",   MX,          r2y, r2w, rH, C.xlgray, C.dark, 14, true);
  bx("受注単価", MX+r2w+0.18, r2y, r2w, rH, C.xlgray, C.gray, 14, false);

  // connector from 成約数 down
  const r2bot = r2y + rH;
  const r3y = r2bot + rGap;
  const cx2 = MX + r2w/2;
  s.addShape(pptx.ShapeType.line, { x:cx2, y:r2bot, w:0, h:rGap/2, line:{color:C.gray,width:1.2} });
  const r3w = (r2w - 0.12) / 3;
  const r3x1 = MX;
  const r3x2 = MX + r3w + 0.12;
  const r3x3 = MX + (r3w + 0.12) * 2;
  s.addShape(pptx.ShapeType.line, { x:r3x1+r3w/2, y:r2bot+rGap/2, w:r3x3+r3w/2-(r3x1+r3w/2), h:0, line:{color:C.gray,width:1.2} });
  [r3x1, r3x2, r3x3].forEach(rx => {
    s.addShape(pptx.ShapeType.line, { x:rx+r3w/2, y:r2bot+rGap/2, w:0, h:rGap/2, line:{color:C.gray,width:1.2} });
  });

  // ── ROW 3: 提案数★ | 成約率★ | (単価) ── HIGHLIGHTED
  bx("★ 提案数", r3x1, r3y, r3w, rH, C.tealLight, C.tealDark, 14, true, C.teal);
  bx("★ 成約率", r3x2, r3y, r3w, rH, C.tealLight, C.tealDark, 14, true, C.teal);
  bx("（単価）",  r3x3, r3y, r3w, rH, C.xlgray,    C.gray,     13, false);

  // connector from row3 left 2 boxes down
  const r3bot = r3y + rH;
  const r4y = r3bot + rGap;
  const r4w = (r2w - 0.18) / 3;
  [0,1,2].forEach(j => {
    const rx = MX + j*(r4w+0.09);
    const cx3 = r3x1 + r3w/2 + (j > 0 ? j*r3w/2 : 0);
  });
  // simpler: just draw lines from centers of rows 3 boxes
  s.addShape(pptx.ShapeType.line, { x:r3x1+r3w/2, y:r3bot, w:0, h:rGap/2, line:{color:C.gray,width:1} });
  s.addShape(pptx.ShapeType.line, { x:r3x2+r3w/2, y:r3bot, w:0, h:rGap/2, line:{color:C.gray,width:1} });
  const r4x1 = MX, r4x2 = MX + r4w*1+0.09, r4x3 = MX + r4w*2+0.18, r4x4 = MX + r4w*3+0.27;
  const r4wActual = (r2w - 0.27) / 4;
  const ra = [
    {x: MX,                      lbl:"商談数"},
    {x: MX+r4wActual+0.09,       lbl:"提案率"},
    {x: MX+(r4wActual+0.09)*2,   lbl:"成約率"},
    {x: MX+(r4wActual+0.09)*3,   lbl:"（単価）"},
  ];
  s.addShape(pptx.ShapeType.line, { x:ra[0].x+r4wActual/2, y:r3bot+rGap/2, w:ra[2].x+r4wActual/2-(ra[0].x+r4wActual/2), h:0, line:{color:C.gray,width:1} });
  ra.slice(0,3).forEach(r => {
    s.addShape(pptx.ShapeType.line, { x:r.x+r4wActual/2, y:r3bot+rGap/2, w:0, h:rGap/2, line:{color:C.gray,width:1} });
  });

  // ── ROW 4 ──
  ra.forEach((r, i) => {
    bx(r.lbl, r.x, r4y, r4wActual, rH, i===3?C.xlgray:C.xlgray, i===3?C.gray:C.dark, 12, i!==3);
  });

  // connector to row5
  const r4bot = r4y + rH;
  const r5y = r4bot + rGap;
  const r5wActual = (r2w - 0.32) / 5;
  const rb = [
    {x: MX,                      lbl:"リード数"},
    {x: MX+(r5wActual+0.08)*1,   lbl:"商談化率"},
    {x: MX+(r5wActual+0.08)*2,   lbl:"提案率"},
    {x: MX+(r5wActual+0.08)*3,   lbl:"成約率"},
    {x: MX+(r5wActual+0.08)*4,   lbl:"（単価）"},
  ];
  s.addShape(pptx.ShapeType.line, { x:rb[0].x+r5wActual/2, y:r4bot+rGap/2, w:rb[3].x+r5wActual/2-(rb[0].x+r5wActual/2), h:0, line:{color:C.gray,width:0.8} });
  rb.slice(0,4).forEach(r => {
    s.addShape(pptx.ShapeType.line, { x:ra[0].x+r4wActual/2, y:r4bot, w:0, h:rGap/2, line:{color:C.gray,width:0.8} });
    s.addShape(pptx.ShapeType.line, { x:r.x+r5wActual/2, y:r4bot+rGap/2, w:0, h:rGap/2, line:{color:C.gray,width:0.8} });
  });

  // ── ROW 5 ──
  rb.forEach((r, i) => {
    bx(r.lbl, r.x, r5y, r5wActual, rH, C.xlgray, i===4?C.gray:C.dark, 11.5, i!==4);
  });

  insightBar(s, "示唆：売上向上の打ち手は構造的に特定できる");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 5 — TWO VARIABLES
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "売上を最大化させる2つの変数", "「提案の数」を増やし、同時に「成約率」を上げる");

  // Top formula
  s.addShape(pptx.ShapeType.rect, { x:MX, y:1.25, w:CW, h:0.85, fill:{color:C.xlgray}, line:{color:C.lgray,width:1} });
  s.addText("売上　＝　成約数　×　受注単価", {
    x:MX, y:1.25, w:CW, h:0.85, fontSize:20, bold:true, color:C.dark, align:"center", valign:"middle", fontFace:"Arial"
  });

  // Arrow down
  s.addText("↓　注力ポイント", {
    x:MX, y:2.15, w:CW, h:0.52, fontSize:15, bold:true, color:C.teal, align:"center", fontFace:"Arial", valign:"middle"
  });

  // Two highlighted boxes
  const bW = 5.5;
  const b1x = MX + 0.5, b2x = SW - MX - 0.5 - bW;
  const by = 2.72, bH = 1.9;

  s.addShape(pptx.ShapeType.rect, { x:b1x, y:by, w:bW, h:bH, fill:{color:C.tealLight}, line:{color:C.teal,width:2.5} });
  s.addText("提案数", { x:b1x, y:by+0.15, w:bW, h:0.7, fontSize:30, bold:true, color:C.teal, align:"center", fontFace:"Arial" });
  s.addText("作成時間を半日→1時間に短縮\n1日複数案件の対応が可能になる", {
    x:b1x+0.2, y:by+0.9, w:bW-0.4, h:0.85,
    fontSize:12.5, color:C.dark, align:"center", fontFace:"Arial", lineSpacingMultiple:1.35
  });

  s.addText("×", { x:b1x+bW, y:by+0.55, w:b2x-b1x-bW, h:0.8, fontSize:26, bold:true, color:C.gray, align:"center", fontFace:"Arial" });

  s.addShape(pptx.ShapeType.rect, { x:b2x, y:by, w:bW, h:bH, fill:{color:C.tealLight}, line:{color:C.teal,width:2.5} });
  s.addText("成約率", { x:b2x, y:by+0.15, w:bW, h:0.7, fontSize:30, bold:true, color:C.teal, align:"center", fontFace:"Arial" });
  s.addText("スピード × 個別最適化 × 品質標準化\nによる意思決定の後押し", {
    x:b2x+0.2, y:by+0.9, w:bW-0.4, h:0.85,
    fontSize:12.5, color:C.dark, align:"center", fontFace:"Arial", lineSpacingMultiple:1.35
  });

  // Sub explanation
  s.addShape(pptx.ShapeType.rect, { x:MX, y:4.75, w:CW, h:1.95, fill:{color:C.xlgray}, line:{color:C.lgray,width:1} });
  const points = [
    { label:"提案数↑の根拠", body:"資料作成が半日〜1日から30〜60分に短縮 → 1日あたりの対応案件数が増加" },
    { label:"成約率↑の根拠", body:"商談直後の送付（業界標準を大幅に超えるスピード）× ヒアリング内容の個別反映 × 髙橋COOのメソッドによる提案品質の標準化" },
  ];
  points.forEach((p, i) => {
    const py = 4.88 + i * 0.82;
    s.addText("▶  " + p.label, { x:MX+0.3, y:py, w:2.8, h:0.35, fontSize:12, bold:true, color:C.tealDark, fontFace:"Arial" });
    s.addText(p.body, { x:MX+3.1, y:py, w:CW-2.8, h:0.55, fontSize:11.5, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.3 });
  });

  insightBar(s, "示唆：2つの変数を同時に改善することで売上最大化を実現");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 6 — QUANTITATIVE EVIDENCE
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "定量根拠：速さと個別最適化が成約率を上げる", "仮説ではなく、データが証明している");

  const leftW = 7.8, rightW = 4.2, gap = 0.33;
  const startY = 1.25;

  // ── LEFT: 4 data cards ──
  const dataCards = [
    { src:"Harvard Business Review（224万件分析）", stat:"7倍", unit:"受注率↑", body:"商談後1時間以内の接触は\n1時間後より受注率が7倍高い" },
    { src:"Google & CEB", stat:"35〜50%", unit:"が受注", body:"B2B商談はファーストレスポンドした\n企業が受注する" },
    { src:"McKinsey", stat:"+10〜20%", unit:"成約率↑", body:"パーソナライズにより\n成約率・売上が向上する" },
    { src:"QorusDocs（第7回年次調査）", stat:"+25%", unit:"成約率↑", body:"提案書の個別化で成約率が中央値+25%\n商談進捗速度+37%向上" },
  ];
  const cardH = (SH - startY - 0.7) / 4 - 0.12;
  dataCards.forEach((d, i) => {
    const cy = startY + i * (cardH + 0.12);
    s.addShape(pptx.ShapeType.rect, { x:MX, y:cy, w:0.1, h:cardH, fill:{color:C.teal} });
    card(s, MX+0.1, cy, leftW-0.1, cardH, { fill:"F9FAFB", line:C.lgray });
    s.addText(d.src, { x:MX+0.35, y:cy+0.1, w:leftW-0.5, h:0.3, fontSize:10.5, color:C.gray, fontFace:"Arial" });
    s.addText(d.stat, { x:MX+0.35, y:cy+0.38, w:2.5, h:0.75, fontSize:30, bold:true, color:C.teal, fontFace:"Arial", valign:"middle" });
    s.addText(d.unit, { x:MX+2.85, y:cy+0.38, w:1.2, h:0.75, fontSize:13, bold:true, color:C.tealDark, fontFace:"Arial", valign:"middle" });
    s.addText(d.body, { x:MX+4.1, y:cy+0.2, w:leftW-4.2, h:cardH-0.25, fontSize:11.5, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.3, valign:"middle" });
  });

  // ── RIGHT: エヌイチ実績 ──
  const rx = MX + leftW + gap;
  card(s, rx, startY, rightW, SH-startY-0.72, { fill:C.tealLight, line:C.teal, lw:1.5 });
  s.addShape(pptx.ShapeType.rect, { x:rx, y:startY, w:rightW, h:0.12, fill:{color:C.teal} });
  s.addText("エヌイチ　AI-Pax実績", { x:rx+0.2, y:startY+0.2, w:rightW-0.4, h:0.42, fontSize:13.5, bold:true, color:C.tealDark, fontFace:"Arial" });
  s.addText("2026年2月18〜19日 出展", { x:rx+0.2, y:startY+0.6, w:rightW-0.4, h:0.3, fontSize:10.5, color:C.gray, fontFace:"Arial" });
  s.addShape(pptx.ShapeType.line, { x:rx+0.2, y:startY+0.95, w:rightW-0.4, h:0, line:{color:C.tealMid,width:1} });

  const stats = [
    { lbl:"商談確定", val:"19社", sub:"（実質着席12件）" },
    { lbl:"受注見込み", val:"5社", sub:"" },
    { lbl:"検討中", val:"3社", sub:"" },
    { lbl:"想定成約率", val:"≒30%", sub:"" },
  ];
  stats.forEach((st, i) => {
    const sy = startY + 1.1 + i * 1.2;
    s.addText(st.lbl, { x:rx+0.2, y:sy, w:rightW-0.4, h:0.3, fontSize:11, color:C.gray, fontFace:"Arial" });
    s.addText(st.val, { x:rx+0.2, y:sy+0.28, w:rightW-0.4, h:0.62, fontSize:28, bold:true, color:C.tealDark, fontFace:"Arial" });
    if (st.sub) s.addText(st.sub, { x:rx+0.2, y:sy+0.88, w:rightW-0.4, h:0.28, fontSize:10, color:C.gray, fontFace:"Arial" });
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 7 — BOTTLENECK + WHY EXISTING AI ISN'T ENOUGH
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "特定されたボトルネックと、既存AIでは解決できない理由", "「資料作成の都度カスタマイズ」が提案数・成約率向上を阻害している");

  // LEFT: Bottleneck flow
  const lW = 5.5;
  s.addText("ボトルネックの構造", { x:MX, y:1.25, w:lW, h:0.38, fontSize:13.5, bold:true, color:C.tealDark, fontFace:"Arial" });

  const flowB = [
    { txt:"提案資料の都度カスタマイズ", fill:C.xlgray, tc:C.dark, h:0.65 },
    { txt:"準備に 半日〜1日\n（ボトルネック）", fill:C.teal, tc:C.white, h:0.9 },
    { txt:"提案数・成約率の向上　✗", fill:"FEF2F2", tc:C.red, h:0.65 },
  ];
  let fy = 1.7;
  flowB.forEach((f, i) => {
    s.addShape(pptx.ShapeType.rect, { x:MX+0.3, y:fy, w:lW-0.6, h:f.h, fill:{color:f.fill}, line:{color:f.fill===C.xlgray?C.lgray:f.fill,width:f.fill===C.teal?0:1} });
    s.addText(f.txt, { x:MX+0.3, y:fy, w:lW-0.6, h:f.h, fontSize:13, bold:true, color:f.tc, align:"center", valign:"middle", fontFace:"Arial", lineSpacingMultiple:1.3 });
    if (i < 2) {
      fy += f.h;
      s.addText("↓", { x:MX+0.3, y:fy, w:lW-0.6, h:0.42, fontSize:18, bold:true, color:C.tealMid, align:"center", fontFace:"Arial", valign:"middle" });
      fy += 0.42;
    }
  });

  // Sub note
  s.addText("• コア業務の時間減：本来注力すべき商談・関係構築に取りかかれない\n• 都度カスタマイズ：毎回ゼロから作り直す工数と精神的負荷\n• 物理的限界：準備時間が重くのしかかり、商談数を増やせない", {
    x:MX, y:4.5, w:lW, h:1.65,
    fontSize:11.5, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.5
  });

  // Vertical divider
  s.addShape(pptx.ShapeType.line, { x:6.15, y:1.25, w:0, h:5.45, line:{color:C.lgray,width:1.2} });

  // RIGHT: Why existing AI isn't enough
  const rX = 6.45, rW = SW - rX - MX;
  s.addText("なぜ既存スライドAIだけでは不十分か", { x:rX, y:1.25, w:rW, h:0.38, fontSize:13.5, bold:true, color:C.tealDark, fontFace:"Arial" });
  s.addText("Gamma / Manus / Genspark を使うだけでは解決しない", { x:rX, y:1.63, w:rW, h:0.28, fontSize:11, color:C.gray, fontFace:"Arial" });

  // Comparison table
  const tStartY = 2.0, rowH = 0.88, tW = rW;
  const cols = ["既存ツールで解決できること", "解決できないこと（本質）"];
  const colW = [tW*0.47, tW*0.53];
  // Header
  s.addShape(pptx.ShapeType.rect, { x:rX, y:tStartY, w:colW[0], h:0.42, fill:{color:C.lgray} });
  s.addText(cols[0], { x:rX, y:tStartY, w:colW[0], h:0.42, fontSize:11, bold:true, color:C.gray, align:"center", valign:"middle", fontFace:"Arial" });
  s.addShape(pptx.ShapeType.rect, { x:rX+colW[0]+0.05, y:tStartY, w:colW[1]-0.05, h:0.42, fill:{color:C.teal} });
  s.addText(cols[1], { x:rX+colW[0]+0.05, y:tStartY, w:colW[1]-0.05, h:0.42, fontSize:11, bold:true, color:C.white, align:"center", valign:"middle", fontFace:"Arial" });

  const rows = [
    ["スライドのデザイン・見た目",  "商談ヒアリング内容の構造化"],
    ["テンプレートからの資料作成",  "髙橋メソッドに基づくロジック設計"],
    ["汎用的な構成の提案",          "クライアント固有の課題・ゴールの反映"],
  ];
  rows.forEach((r, i) => {
    const ry = tStartY + 0.42 + i * rowH;
    const bg = i%2===0 ? "F9FAFB" : C.white;
    s.addShape(pptx.ShapeType.rect, { x:rX, y:ry, w:colW[0], h:rowH, fill:{color:bg}, line:{color:C.lgray,width:0.5} });
    s.addText(r[0], { x:rX+0.1, y:ry, w:colW[0]-0.2, h:rowH, fontSize:11.5, color:C.dark, fontFace:"Arial", valign:"middle", lineSpacingMultiple:1.3 });
    s.addShape(pptx.ShapeType.rect, { x:rX+colW[0]+0.05, y:ry, w:colW[1]-0.05, h:rowH, fill:{color:bg}, line:{color:C.lgray,width:0.5} });
    s.addText(r[1], { x:rX+colW[0]+0.15, y:ry, w:colW[1]-0.2, h:rowH, fontSize:11.5, bold:true, color:C.tealDark, fontFace:"Arial", valign:"middle", lineSpacingMultiple:1.3 });
  });

  // Bottom callout
  s.addShape(pptx.ShapeType.rect, { x:rX, y:5.75, w:rW, h:0.62, fill:{color:C.tealLight}, line:{color:C.teal,width:1.5} });
  s.addText("必要なのは\nスピード × 個別最適化 × 品質標準化 の同時実現", {
    x:rX+0.15, y:5.75, w:rW-0.3, h:0.62,
    fontSize:12, bold:true, color:C.tealDark, align:"center", fontFace:"Arial", valign:"middle", lineSpacingMultiple:1.3
  });

  insightBar(s, "示唆：ボトルネック解消が売上向上の最短ルート");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 8 — TIME REDUCTION
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "AIがもたらす「時間の再定義」", "資料作成時間を 半日〜1日 から 30〜60分 へ短縮できる");

  const MAX_BAR = 7.5;
  const barSX = 3.8, labelX = MX, labelW = 3.1;
  const rows = [
    { phase:"骨子作成\n（構成・ロジック）", before:"約1時間",           after:"約5分",       ratioB:0.22, ratioA:0.02 },
    { phase:"スライド化",                   before:"3〜4時間\n（深夜作業も）", after:"約5〜10分", ratioB:1.0,  ratioA:0.05 },
    { phase:"修正・仕上げ",                 before:"—",                 after:"約20〜30分",  ratioB:0.0,  ratioA:0.17 },
  ];

  rows.forEach((r, i) => {
    const baseY = 1.35 + i * 1.65;
    // Phase label
    s.addText(r.phase, { x:labelX, y:baseY+0.1, w:labelW, h:0.9, fontSize:13, bold:true, color:C.dark, fontFace:"Arial", valign:"middle", lineSpacingMultiple:1.3 });

    // Before bar
    s.addText("従来", { x:barSX-0.55, y:baseY+0.05, w:0.5, h:0.4, fontSize:10, color:C.gray, fontFace:"Arial", align:"right" });
    if (r.ratioB > 0) {
      s.addShape(pptx.ShapeType.rect, { x:barSX, y:baseY+0.05, w:MAX_BAR*r.ratioB, h:0.42, fill:{color:C.lgray} });
    }
    s.addText(r.before, {
      x: barSX + MAX_BAR*r.ratioB + 0.15, y:baseY+0.05, w:2.5, h:0.42,
      fontSize:12, color:C.gray, fontFace:"Arial", valign:"middle", lineSpacingMultiple:1.2
    });

    // After bar
    s.addText("AI後", { x:barSX-0.55, y:baseY+0.65, w:0.5, h:0.4, fontSize:10, bold:true, color:C.teal, fontFace:"Arial", align:"right" });
    if (r.ratioA > 0) {
      s.addShape(pptx.ShapeType.rect, { x:barSX, y:baseY+0.65, w:MAX_BAR*r.ratioA, h:0.42, fill:{color:C.teal} });
    }
    s.addText(r.after, {
      x: barSX + MAX_BAR*r.ratioA + 0.15, y:baseY+0.65, w:2.5, h:0.42,
      fontSize:12, bold:true, color:C.tealDark, fontFace:"Arial", valign:"middle"
    });

    if (i < rows.length-1) {
      s.addShape(pptx.ShapeType.line, { x:MX, y:baseY+1.3, w:CW, h:0, line:{color:C.lgray,width:0.8} });
    }
  });

  // Three effects row
  const efY = 5.6;
  s.addText("3つの効果", { x:MX, y:efY-0.02, w:CW, h:0.35, fontSize:13, bold:true, color:C.dark, fontFace:"Arial" });
  const effs = [
    { icon:"⏱", title:"作成工数90%削減", body:"半日〜1日 → 30〜60分\n圧倒的な時間創出" },
    { icon:"📐", title:"質の標準化",       body:"髙橋COOのメソッドで属人化防止\n常に高い提案品質" },
    { icon:"🔄", title:"作業から選択へ",   body:"ゼロから作らず\nAIの提案を選択・修正する" },
  ];
  const efW = (CW - 0.4) / 3;
  effs.forEach((e, i) => {
    const ex = MX + i*(efW+0.2);
    card(s, ex, efY+0.42, efW, 1.25, { fill:C.tealLight, line:C.teal, lw:1 });
    s.addText(e.icon+" "+e.title, { x:ex+0.15, y:efY+0.52, w:efW-0.3, h:0.38, fontSize:12.5, bold:true, color:C.tealDark, fontFace:"Arial" });
    s.addText(e.body, { x:ex+0.15, y:efY+0.9, w:efW-0.3, h:0.65, fontSize:11, color:C.dark, fontFace:"Arial", lineSpacingMultiple:1.3 });
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 9 — WORKFLOW
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "次世代資料作成ワークフロー", "商談終了から資料送付まで、ほぼ全自動");

  const steps = [
    { n:"①", title:"商談終了",               sub:"Notta文字起こし\nGoogle Driveに自動保存",  dark:false },
    { n:"②", title:"/proposal-outline\n実行", sub:"ファイルを\n1クリック選択",              dark:false },
    { n:"③", title:"骨子を自動生成",          sub:"髙橋メソッド自動適用\nロジック設計完了",   dark:false },
    { n:"④", title:"「OK」と入力",           sub:"スライド\n自動出力（5〜10分）",            dark:false },
    { n:"⑤", title:"✅ 1時間以内\n送付完了", sub:"Google Slides\n完成・送付",               dark:true  },
  ];

  const sW = (CW - 0.6) / 5, sH = 3.5, sY = 1.35;
  steps.forEach((st, i) => {
    const sx = MX + i*(sW+0.15);
    const fill = st.dark ? C.teal : C.tealLight;
    const tc   = st.dark ? C.white : C.tealDark;
    const sc   = st.dark ? "C0EBF5" : C.gray;

    // Card
    card(s, sx, sY, sW, sH, { fill, line: st.dark ? C.tealDark : C.teal, lw:1.5 });

    // Step circle
    s.addShape(pptx.ShapeType.ellipse, { x:sx+sW/2-0.32, y:sY+0.2, w:0.64, h:0.64, fill:{color: st.dark ? C.tealDark : C.teal} });
    s.addText(st.n, { x:sx+sW/2-0.32, y:sY+0.2, w:0.64, h:0.64, fontSize:15, bold:true, color:C.white, align:"center", valign:"middle", fontFace:"Arial" });

    // Title
    s.addText(st.title, { x:sx+0.1, y:sY+1.0, w:sW-0.2, h:0.95, fontSize:12, bold:true, color:tc, align:"center", fontFace:"Arial", lineSpacingMultiple:1.3 });

    // Divider
    s.addShape(pptx.ShapeType.line, { x:sx+0.2, y:sY+2.0, w:sW-0.4, h:0, line:{color: st.dark ? "5BB8D4" : C.tealMid, width:0.8} });

    // Sub
    s.addText(st.sub, { x:sx+0.1, y:sY+2.1, w:sW-0.2, h:1.2, fontSize:11, color:sc, align:"center", fontFace:"Arial", lineSpacingMultiple:1.35 });

    // Arrow
    if (i < steps.length-1) {
      s.addText("→", { x:sx+sW+0.01, y:sY+sH/2-0.25, w:0.14, h:0.5, fontSize:16, bold:true, color:C.tealMid, align:"center", fontFace:"Arial" });
    }
  });

  // Note
  s.addText("※ 髙橋COO（事業部責任者）の知見・実績・提案ロジックが全提案に標準装備される", {
    x:MX, y:5.05, w:CW, h:0.35, fontSize:11, color:C.gray, fontFace:"Arial", italic:true
  });

  // Bottom comparison
  s.addShape(pptx.ShapeType.rect, { x:MX, y:5.48, w:CW/2-0.2, h:0.62, fill:{color:C.xlgray}, line:{color:C.lgray,width:1} });
  s.addText("従来：「作業」　ゼロから毎回作り直す", { x:MX+0.2, y:5.48, w:CW/2-0.4, h:0.62, fontSize:12, color:C.gray, fontFace:"Arial", valign:"middle", bold:false });
  s.addShape(pptx.ShapeType.rect, { x:MX+CW/2+0.1, y:5.48, w:CW/2-0.2, h:0.62, fill:{color:C.tealLight}, line:{color:C.teal,width:1.5} });
  s.addText("現在：「選択」　AIの提案から選ぶだけ", { x:MX+CW/2+0.3, y:5.48, w:CW/2-0.4, h:0.62, fontSize:12, bold:true, color:C.tealDark, fontFace:"Arial", valign:"middle" });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 10 — FUTURE: KAWARU
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "将来展望①：Kawaruシリーズへの統合", "今回の取り組みは、サービスそのものになる");

  const levels = [
    {
      title: "今回の取り組み",
      body: "Claude Code Skillで社内実装・実証完了\nエヌイチ新規事業部にて商談→提案資料作成を全自動化",
      fill: C.white, tc: C.dark, bc: C.teal, w: 8.5, offset: 1.5, h: 1.2
    },
    {
      title: "Kawaru Team（AI研修）",
      body: "「営業部門：提案資料作成効率化」を他社への研修として展開\n※ Kawaru Teamの研修カスタマイズ例として既に設計済み",
      fill: C.tealLight, tc: C.tealDark, bc: C.teal, w: 10.5, offset: 0.5, h: 1.2
    },
    {
      title: "Kawaru SaaS（4月1日リリース予定）",
      body: "このワークフロー自体をSaaSに組み込み、顧客へ提供\n「営業の資料自動化をしたい」という需要をKawaruが叶えられるようになる",
      fill: C.teal, tc: C.white, bc: C.tealDark, w: 12.33, offset: 0, h: 1.3
    },
  ];

  let lY = 1.3;
  levels.forEach((lv, i) => {
    const lx = MX + lv.offset;
    card(s, lx, lY, lv.w, lv.h, { fill:lv.fill, line:lv.bc, lw:1.8 });
    s.addText(lv.title, {
      x:lx+0.25, y:lY+0.1, w:lv.w-0.5, h:0.42,
      fontSize:15, bold:true, color:lv.tc, fontFace:"Arial"
    });
    s.addText(lv.body, {
      x:lx+0.25, y:lY+0.52, w:lv.w-0.5, h:0.58,
      fontSize:11.5, color: lv.fill===C.teal ? "D0EEF6" : C.dark, fontFace:"Arial", lineSpacingMultiple:1.3
    });
    lY += lv.h;
    if (i < levels.length-1) {
      s.addText("↓", { x:MX, y:lY, w:CW, h:0.38, fontSize:20, bold:true, color:C.teal, align:"center", fontFace:"Arial", valign:"middle" });
      lY += 0.38;
    }
  });

  // Summary flow (right side after slide 10 content)
  const sumY = 5.6, sumItems = ["自社で実証", "→", "研修で他社へ展開", "→", "SaaSに内包", "→", "売上直結"];
  const sumW = CW / sumItems.length;
  sumItems.forEach((t, i) => {
    const isArrow = t === "→";
    s.addText(t, {
      x: MX + i * sumW, y: sumY, w: sumW, h: 0.55,
      fontSize: isArrow ? 18 : 12, bold: !isArrow,
      color: isArrow ? C.tealMid : C.tealDark,
      align:"center", fontFace:"Arial", valign:"middle"
    });
  });
  s.addShape(pptx.ShapeType.rect, { x:MX, y:sumY, w:CW, h:0.55, fill:{color:C.tealLight}, line:{color:C.tealMid,width:1} });
  sumItems.forEach((t, i) => {
    const isArrow = t === "→";
    s.addText(t, {
      x: MX + i * sumW, y: sumY, w: sumW, h: 0.55,
      fontSize: isArrow ? 18 : 12.5, bold: !isArrow,
      color: isArrow ? C.tealMid : C.tealDark,
      align:"center", fontFace:"Arial", valign:"middle"
    });
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 11 — FUTURE: SCHOOL DIVISION
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: C.white };
  hdr(s, "将来展望②：スクール事業部への横展開（私案）", "同じ仕組みが、スクール事業の成約率を上げる可能性がある");

  const colW = 5.5, gap2 = 0.83;
  const lx = MX, rx = MX + colW + gap2;
  const topY = 1.25;

  // Column labels
  s.addShape(pptx.ShapeType.rect, { x:lx, y:topY, w:colW, h:0.4, fill:{color:C.lgray} });
  s.addText("現状", { x:lx, y:topY, w:colW, h:0.4, fontSize:13, bold:true, color:C.gray, align:"center", valign:"middle", fontFace:"Arial" });
  s.addShape(pptx.ShapeType.rect, { x:rx, y:topY, w:colW, h:0.4, fill:{color:C.teal} });
  s.addText("提案", { x:rx, y:topY, w:colW, h:0.4, fontSize:13, bold:true, color:C.white, align:"center", valign:"middle", fontFace:"Arial" });

  // VS
  s.addText("VS", { x:colW+MX+0.15, y:topY+1.2, w:gap2-0.3, h:0.55, fontSize:16, bold:true, color:C.gray, align:"center", fontFace:"Arial" });

  // LEFT flow
  const flowL = [
    { txt:"前半ヒアリング（1〜1.5時間）", fill:C.xlgray, tc:C.dark, h:0.7 },
    { txt:"クロージング\n（全員が同じフォーマット）", fill:"FEF2F2", tc:C.red, h:0.9 },
  ];
  let lfY = topY + 0.5;
  flowL.forEach((f, i) => {
    card(s, lx+0.3, lfY, colW-0.6, f.h, { fill:f.fill, line: f.fill==="FEF2F2"?C.red:C.lgray, lw:1 });
    s.addText(f.txt, { x:lx+0.3, y:lfY, w:colW-0.6, h:f.h, fontSize:12.5, bold:i===1, color:f.tc, align:"center", valign:"middle", fontFace:"Arial", lineSpacingMultiple:1.3 });
    if (i < flowL.length-1) {
      lfY += f.h;
      s.addText("↓", { x:lx+0.3, y:lfY, w:colW-0.6, h:0.38, fontSize:18, bold:true, color:C.gray, align:"center", fontFace:"Arial", valign:"middle" });
      lfY += 0.38;
    }
  });
  s.addText("✗ 個別感なし → 検討が前に進まない", { x:lx+0.3, y:topY+2.7, w:colW-0.6, h:0.35, fontSize:11, bold:true, color:C.red, align:"center", fontFace:"Arial" });

  // RIGHT flow
  const flowR = [
    { txt:"前半ヒアリング（1〜1.5時間）", fill:C.xlgray, tc:C.dark, h:0.7 },
    { txt:"5分で個別提案資料を自動生成", fill:C.teal, tc:C.white, h:0.7 },
    { txt:"後半クロージングで投影", fill:C.tealLight, tc:C.tealDark, h:0.7 },
  ];
  let rfY = topY + 0.5;
  flowR.forEach((f, i) => {
    card(s, rx+0.3, rfY, colW-0.6, f.h, { fill:f.fill, line: f.fill===C.teal?C.tealDark:C.teal, lw:1.5 });
    s.addText(f.txt, { x:rx+0.3, y:rfY, w:colW-0.6, h:f.h, fontSize:12.5, bold:true, color:f.tc, align:"center", valign:"middle", fontFace:"Arial" });
    if (i < flowR.length-1) {
      rfY += f.h;
      s.addText("↓", { x:rx+0.3, y:rfY, w:colW-0.6, h:0.38, fontSize:18, bold:true, color:C.teal, align:"center", fontFace:"Arial", valign:"middle" });
      rfY += 0.38;
    }
  });
  s.addText("✓ インサイトに刺さる提案で意思決定を後押し", { x:rx+0.3, y:topY+3.38, w:colW-0.6, h:0.35, fontSize:11, bold:true, color:C.green, align:"center", fontFace:"Arial" });

  // Four effect boxes
  const efY2 = 3.95, efH = 1.35;
  const effs2 = [
    { title:"成約率向上",        body:"ヒアリング内容を反映した\n提案で意思決定を後押し" },
    { title:"AI関心度向上",      body:"目の前でリアルタイム生成\n実演効果で関心が高まる" },
    { title:"標準化",            body:"トップ営業のロジックを全員に\n属人性を排除" },
    { title:"商談数増加",        body:"商談時間の短縮により\n1日の対応件数が増える" },
  ];
  const efW2 = (CW - 0.45) / 4;
  effs2.forEach((e, i) => {
    const ex = MX + i*(efW2+0.15);
    card(s, ex, efY2, efW2, efH, { fill:C.tealLight, line:C.teal, lw:1 });
    s.addShape(pptx.ShapeType.rect, { x:ex, y:efY2, w:efW2, h:0.1, fill:{color:C.teal} });
    s.addText(e.title, { x:ex+0.1, y:efY2+0.15, w:efW2-0.2, h:0.38, fontSize:13, bold:true, color:C.tealDark, align:"center", fontFace:"Arial" });
    s.addShape(pptx.ShapeType.line, { x:ex+0.1, y:efY2+0.57, w:efW2-0.2, h:0, line:{color:C.tealMid,width:0.8} });
    s.addText(e.body, { x:ex+0.1, y:efY2+0.65, w:efW2-0.2, h:0.6, fontSize:11, color:C.dark, align:"center", fontFace:"Arial", lineSpacingMultiple:1.3 });
  });

  // Challenge note
  s.addShape(pptx.ShapeType.rect, { x:MX, y:5.4, w:CW, h:0.4, fill:{color:C.xlgray}, line:{color:C.lgray,width:1} });
  s.addText("⚠ 実現課題：文字起こしと録画の同時進行によるPC負荷、録画停止タイミングの調整など　→ 実現可能性は十分にあると判断", {
    x:MX+0.2, y:5.4, w:CW-0.4, h:0.4, fontSize:10.5, color:C.gray, fontFace:"Arial", valign:"middle"
  });

  // Bottom bar
  s.addShape(pptx.ShapeType.rect, { x:0, y:5.92, w:SW, h:0.58, fill:{color:C.teal} });
  s.addText("新規事業部での実証　→　スクール事業部へ横展開　→　会社全体の売上貢献へ", {
    x:MX, y:5.92, w:CW, h:0.58, fontSize:14, bold:true, color:C.white, align:"center", fontFace:"Arial", valign:"middle"
  });
}

// ─── SAVE ───────────────────────────────────────────────────────
pptx.writeFile({ fileName: "/Users/kyouyuu/cloude/output/hackathon_v2.pptx" })
  .then(() => console.log("✅ SAVED: hackathon_v2.pptx"))
  .catch(e => { console.error("❌", e); process.exit(1); });
