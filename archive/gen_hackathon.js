const PptxGenJS = require("pptxgenjs");
const pptx = new PptxGenJS();

pptx.layout = "LAYOUT_WIDE";
pptx.title = "商談後1時間以内に、個別最適化された提案書を届ける";

// ─── Color constants ───────────────────────────────────────────
const TEAL      = "0891B2";
const TEAL_DARK = "076A87";
const TEAL_LIGHT= "E0F2F7";
const TEAL_MID  = "B2DFE9";
const DARK      = "1F2937";
const GRAY      = "6B7280";
const LGRAY     = "E5E7EB";
const WHITE     = "FFFFFF";
const BG        = "FAFAFA";

// ─── Helper: slide title + thin top accent bar ─────────────────
function addHeader(slide, title, sub) {
  // Top teal bar
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: "100%", h: 0.12,
    fill: { color: TEAL }
  });
  slide.addText(title, {
    x: 0.45, y: 0.22, w: 8.5, h: 0.55,
    fontSize: 26, bold: true, color: DARK,
    fontFace: "Arial"
  });
  if (sub) {
    slide.addText(sub, {
      x: 0.45, y: 0.78, w: 9, h: 0.3,
      fontSize: 12, color: GRAY, fontFace: "Arial"
    });
  }
}

// ─── Helper: bottom insight bar ────────────────────────────────
function addInsightBar(slide, text) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 6.6, w: 9.1, h: 0.45,
    fill: { color: TEAL_LIGHT },
    line: { color: TEAL, width: 1.5 }
  });
  slide.addText(text, {
    x: 0.6, y: 6.6, w: 8.8, h: 0.45,
    fontSize: 11, color: DARK, bold: true, fontFace: "Arial",
    valign: "middle"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };

  // Top teal bar
  s.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: "100%", h: 0.18, fill: { color: TEAL }
  });
  // Bottom teal bar
  s.addShape(pptx.ShapeType.rect, {
    x: 0, y: 7.02, w: "100%", h: 0.18, fill: { color: TEAL }
  });

  // Decorative left accent
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 1.6, w: 0.08, h: 2.2,
    fill: { color: TEAL }
  });

  // Title
  s.addText("商談後1時間以内に、\n個別最適化された提案書を届ける", {
    x: 0.7, y: 1.5, w: 8.5, h: 2.4,
    fontSize: 34, bold: true, color: DARK, fontFace: "Arial",
    lineSpacingMultiple: 1.3
  });

  // Subtitle
  s.addText("Claude Code Skillによる営業提案の自動化", {
    x: 0.7, y: 4.05, w: 8.5, h: 0.5,
    fontSize: 16, color: GRAY, fontFace: "Arial"
  });

  // Divider line
  s.addShape(pptx.ShapeType.line, {
    x: 0.7, y: 4.7, w: 4.5, h: 0,
    line: { color: LGRAY, width: 1 }
  });

  // Tag
  s.addText("AIハッカソン　｜　新規事業部　大川龍之介", {
    x: 0.7, y: 4.9, w: 8.5, h: 0.35,
    fontSize: 12, color: GRAY, fontFace: "Arial"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 2 — Why proposals matter
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "なぜ「提案資料」が重要なのか", "良いサービスも、伝わらなければ価値がない");

  // Left card
  s.addShape(pptx.ShapeType.roundRect, {
    x: 0.45, y: 1.25, w: 4.3, h: 2.9,
    fill: { color: TEAL_LIGHT },
    line: { color: TEAL, width: 1.2 },
    rectRadius: 0.12
  });
  s.addText("📋  提案資料 = 伝達の核心", {
    x: 0.6, y: 1.45, w: 4.0, h: 0.45,
    fontSize: 13, bold: true, color: TEAL, fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.line, {
    x: 0.6, y: 1.9, w: 3.9, h: 0,
    line: { color: TEAL_MID, width: 0.8 }
  });
  s.addText("良いプロダクト", {
    x: 0.65, y: 2.05, w: 3.9, h: 0.35,
    fontSize: 13, color: DARK, fontFace: "Arial", align: "center"
  });
  s.addText("↓", {
    x: 0.65, y: 2.38, w: 3.9, h: 0.3,
    fontSize: 14, color: TEAL, fontFace: "Arial", align: "center", bold: true
  });
  s.addText("提案資料", {
    x: 0.65, y: 2.66, w: 3.9, h: 0.35,
    fontSize: 13, color: TEAL, bold: true, fontFace: "Arial", align: "center"
  });
  s.addText("↓", {
    x: 0.65, y: 2.99, w: 3.9, h: 0.3,
    fontSize: 14, color: TEAL, fontFace: "Arial", align: "center", bold: true
  });
  s.addText("価値伝達", {
    x: 0.65, y: 3.27, w: 3.9, h: 0.35,
    fontSize: 13, color: DARK, fontFace: "Arial", align: "center"
  });

  // Right card
  s.addShape(pptx.ShapeType.roundRect, {
    x: 5.15, y: 1.25, w: 4.3, h: 2.9,
    fill: { color: TEAL_LIGHT },
    line: { color: TEAL, width: 1.2 },
    rectRadius: 0.12
  });
  s.addText("⏰  リソースの最適配分", {
    x: 5.3, y: 1.45, w: 4.0, h: 0.45,
    fontSize: 13, bold: true, color: TEAL, fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.line, {
    x: 5.3, y: 1.9, w: 3.9, h: 0,
    line: { color: TEAL_MID, width: 0.8 }
  });
  s.addText("作成にかける時間 ↓", {
    x: 5.3, y: 2.1, w: 3.9, h: 0.38,
    fontSize: 13, color: DARK, fontFace: "Arial"
  });
  s.addText("対話・商談にかける時間 ↑", {
    x: 5.3, y: 2.52, w: 3.9, h: 0.38,
    fontSize: 13, color: TEAL, bold: true, fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.line, {
    x: 5.3, y: 3.0, w: 3.9, h: 0,
    line: { color: TEAL_MID, width: 0.8 }
  });
  s.addText("「作成」ではなく\n「商談・関係構築」に時間を使う", {
    x: 5.3, y: 3.08, w: 3.9, h: 0.85,
    fontSize: 11.5, color: GRAY, fontFace: "Arial", lineSpacingMultiple: 1.3
  });

  addInsightBar(s, "示唆：資料作成プロセスこそが、営業活動の隠れたレバレッジポイント");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 3 — Three problems
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "業界に共通する3つの構造的課題", "");

  const cards = [
    { num: "01", title: "スピード不足",    body: "商談後の資料送付は\n「当日〜翌日・次回商談」が業界標準" },
    { num: "02", title: "個別感ゼロ",      body: "テンプレートで対応。クライアント固有の\n課題・ゴールが反映されない" },
    { num: "03", title: "属人的バラつき",  body: "提案ロジックの精度が\n担当者によって異なる" },
  ];

  cards.forEach((c, i) => {
    const x = 0.45 + i * 3.15;
    // Top accent bar
    s.addShape(pptx.ShapeType.rect, {
      x, y: 1.2, w: 2.9, h: 0.1, fill: { color: TEAL }
    });
    // Card body
    s.addShape(pptx.ShapeType.rect, {
      x, y: 1.3, w: 2.9, h: 3.2,
      fill: { color: WHITE },
      line: { color: LGRAY, width: 1 },
      shadow: { type: "outer", blur: 4, offset: 2, angle: 45, color: "CCCCCC", opacity: 0.3 }
    });
    // Number
    s.addText(c.num, {
      x: x + 0.15, y: 1.45, w: 0.7, h: 0.55,
      fontSize: 28, bold: true, color: TEAL_MID, fontFace: "Arial"
    });
    // Title
    s.addText(c.title, {
      x: x + 0.15, y: 2.1, w: 2.6, h: 0.45,
      fontSize: 15, bold: true, color: TEAL, fontFace: "Arial"
    });
    // Body
    s.addText(c.body, {
      x: x + 0.15, y: 2.62, w: 2.65, h: 1.7,
      fontSize: 12, color: DARK, fontFace: "Arial", lineSpacingMultiple: 1.4
    });
  });

  addInsightBar(s, "結果：「どこにでもある資料」として受け取られ、検討が前に進まない");
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 4 — Why existing AI is insufficient
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "なぜ「既存のスライドAI」だけでは不十分か", "Gamma / Manus / Genspark を使うだけでは解決しない");

  // Table header
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 1.2, w: 4.5, h: 0.45, fill: { color: LGRAY }
  });
  s.addText("既存ツールで解決できること", {
    x: 0.45, y: 1.2, w: 4.5, h: 0.45,
    fontSize: 12, bold: true, color: GRAY, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 5.05, y: 1.2, w: 4.5, h: 0.45, fill: { color: TEAL }
  });
  s.addText("解決できないこと（本質的な問題）", {
    x: 5.05, y: 1.2, w: 4.5, h: 0.45,
    fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: "Arial", valign: "middle"
  });

  const rows = [
    ["スライドのデザイン・見た目の生成",    "商談ヒアリング内容の構造化"],
    ["テンプレートからの資料作成",           "髙橋メソッドに基づくロジック設計"],
    ["汎用的な構成の提案",                   "クライアント固有の課題・ゴールの反映"],
  ];

  rows.forEach((r, i) => {
    const y = 1.75 + i * 0.95;
    const bg = i % 2 === 0 ? "F9FAFB" : WHITE;
    s.addShape(pptx.ShapeType.rect, {
      x: 0.45, y, w: 4.5, h: 0.85,
      fill: { color: bg }, line: { color: LGRAY, width: 0.5 }
    });
    s.addText(r[0], {
      x: 0.6, y: y + 0.05, w: 4.2, h: 0.75,
      fontSize: 12.5, color: DARK, fontFace: "Arial", valign: "middle"
    });
    s.addShape(pptx.ShapeType.rect, {
      x: 5.05, y, w: 4.5, h: 0.85,
      fill: { color: bg }, line: { color: LGRAY, width: 0.5 }
    });
    s.addText(r[1], {
      x: 5.2, y: y + 0.05, w: 4.2, h: 0.75,
      fontSize: 12.5, bold: true, color: TEAL_DARK, fontFace: "Arial", valign: "middle"
    });
  });

  // VS divider
  s.addText("VS", {
    x: 4.6, y: 2.3, w: 0.4, h: 1.6,
    fontSize: 14, bold: true, color: GRAY, fontFace: "Arial", align: "center", valign: "middle"
  });

  // Bottom callout
  s.addShape(pptx.ShapeType.roundRect, {
    x: 0.45, y: 5.7, w: 9.1, h: 0.55,
    fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1.5 },
    rectRadius: 0.08
  });
  s.addText("必要なのは「スピード × 個別最適化 × 品質標準化」の同時実現", {
    x: 0.55, y: 5.7, w: 8.9, h: 0.55,
    fontSize: 13, bold: true, color: TEAL_DARK, align: "center", fontFace: "Arial", valign: "middle"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 5 — Logic tree
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "売上への接続ロジック", "提案資料の改善が、売上の2つのドライバーに直結する");

  // Helper: box
  const box = (text, x, y, w, h, fillColor, textColor, fontSize, bold) => {
    s.addShape(pptx.ShapeType.rect, {
      x, y, w, h,
      fill: { color: fillColor },
      line: { color: fillColor === WHITE ? LGRAY : fillColor, width: 1.2 }
    });
    s.addText(text, {
      x, y, w, h,
      fontSize: fontSize || 13, bold: bold !== false, color: textColor || DARK,
      align: "center", valign: "middle", fontFace: "Arial"
    });
  };

  // Level 1
  box("売上高", 3.1, 1.2, 3.8, 0.65, TEAL, WHITE, 17, true);

  // Connector L1→L2
  s.addShape(pptx.ShapeType.line, { x: 5.0, y: 1.85, w: 0, h: 0.35, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 2.2, y: 2.2,  w: 5.6, h: 0, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 2.2, y: 2.2,  w: 0, h: 0.35, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 7.8, y: 2.2,  w: 0, h: 0.35, line: { color: GRAY, width: 1.2 } });

  // Level 2
  box("成約数",   1.1, 2.55, 2.2, 0.58, LGRAY, DARK, 13, true);
  box("受注単価", 6.7, 2.55, 2.2, 0.58, LGRAY, GRAY, 13, false);

  // Connector L2→L3 (from 成約数)
  s.addShape(pptx.ShapeType.line, { x: 2.2, y: 3.13, w: 0, h: 0.35, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 1.1, y: 3.48, w: 2.2, h: 0, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 1.1, y: 3.48, w: 0, h: 0.3, line: { color: GRAY, width: 1.2 } });
  s.addShape(pptx.ShapeType.line, { x: 3.3, y: 3.48, w: 0, h: 0.3, line: { color: GRAY, width: 1.2 } });

  // Level 3 — highlighted
  box("★ 提案数",  0.5, 3.78, 1.8, 0.65, TEAL_LIGHT, TEAL_DARK, 13, true);
  s.addShape(pptx.ShapeType.rect, { x: 0.5, y: 3.78, w: 1.8, h: 0.65, fill: { type: "none" }, line: { color: TEAL, width: 2 } });
  box("★ 成約率",  2.85, 3.78, 1.8, 0.65, TEAL_LIGHT, TEAL_DARK, 13, true);
  s.addShape(pptx.ShapeType.rect, { x: 2.85, y: 3.78, w: 1.8, h: 0.65, fill: { type: "none" }, line: { color: TEAL, width: 2 } });

  // Callout arrows from bottom
  s.addShape(pptx.ShapeType.line, { x: 1.4, y: 4.75, w: 0, h: 0.28, line: { color: TEAL, width: 1.5 } });
  s.addShape(pptx.ShapeType.roundRect, {
    x: 0.3, y: 5.03, w: 2.3, h: 0.55,
    fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1 }, rectRadius: 0.07
  });
  s.addText("作成時間短縮\n→ より多くの案件に対応", {
    x: 0.32, y: 5.03, w: 2.26, h: 0.55,
    fontSize: 10, color: DARK, fontFace: "Arial", align: "center", valign: "middle", lineSpacingMultiple: 1.2
  });

  s.addShape(pptx.ShapeType.line, { x: 3.75, y: 4.75, w: 0, h: 0.28, line: { color: TEAL, width: 1.5 } });
  s.addShape(pptx.ShapeType.roundRect, {
    x: 2.7, y: 5.03, w: 2.3, h: 0.55,
    fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1 }, rectRadius: 0.07
  });
  s.addText("個別最適化\n→ 意思決定を後押し", {
    x: 2.72, y: 5.03, w: 2.26, h: 0.55,
    fontSize: 10, color: DARK, fontFace: "Arial", align: "center", valign: "middle", lineSpacingMultiple: 1.2
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 6 — Quantitative evidence
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "定量根拠：速さと個別最適化が成約率を上げる", "");

  const dataCards = [
    { src: "Harvard Business Review（224万件分析）", stat: "7倍",   body: "商談後1時間以内の接触は\n1時間後より受注率↑" },
    { src: "Google & CEB",                           stat: "35〜50%", body: "B2B商談はファーストレスポンドの\n企業が受注" },
    { src: "McKinsey",                               stat: "+10〜20%", body: "パーソナライズにより\n成約率・売上が向上" },
    { src: "QorusDocs",                              stat: "+25%",   body: "提案書の個別化で\n成約率が中央値で向上" },
  ];

  dataCards.forEach((d, i) => {
    const y = 1.25 + i * 1.3;
    s.addShape(pptx.ShapeType.rect, {
      x: 0.45, y, w: 0.07, h: 1.1,
      fill: { color: TEAL }
    });
    s.addShape(pptx.ShapeType.rect, {
      x: 0.52, y, w: 5.2, h: 1.1,
      fill: { color: "F9FAFB" },
      line: { color: LGRAY, width: 0.5 }
    });
    s.addText(d.src, {
      x: 0.65, y: y + 0.07, w: 4.9, h: 0.28,
      fontSize: 9.5, color: GRAY, fontFace: "Arial"
    });
    s.addText(d.stat, {
      x: 0.65, y: y + 0.32, w: 1.6, h: 0.55,
      fontSize: 26, bold: true, color: TEAL, fontFace: "Arial"
    });
    s.addText(d.body, {
      x: 2.1, y: y + 0.3, w: 3.5, h: 0.65,
      fontSize: 11, color: DARK, fontFace: "Arial", lineSpacingMultiple: 1.3
    });
  });

  // Right: エヌイチ実績
  s.addShape(pptx.ShapeType.roundRect, {
    x: 6.2, y: 1.25, w: 3.3, h: 5.15,
    fill: { color: TEAL_LIGHT },
    line: { color: TEAL, width: 1.5 },
    rectRadius: 0.12
  });
  s.addText("📊  エヌイチ AI-Pax実績", {
    x: 6.35, y: 1.4, w: 3.0, h: 0.4,
    fontSize: 12, bold: true, color: TEAL_DARK, fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.line, {
    x: 6.35, y: 1.85, w: 3.0, h: 0,
    line: { color: TEAL_MID, width: 1 }
  });

  const stats = [
    { label: "着席", val: "12件" },
    { label: "受注見込", val: "5社" },
    { label: "検討中", val: "3社" },
    { label: "想定成約率", val: "≒30%" },
  ];
  stats.forEach((st, i) => {
    const y = 2.05 + i * 1.1;
    s.addText(st.label, {
      x: 6.35, y, w: 3.0, h: 0.3,
      fontSize: 10.5, color: GRAY, fontFace: "Arial"
    });
    s.addText(st.val, {
      x: 6.35, y: y + 0.28, w: 3.0, h: 0.6,
      fontSize: 24, bold: true, color: TEAL_DARK, fontFace: "Arial"
    });
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 7 — Workflow
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "作ったもの：Claude Code Skill「/proposal-outline」", "商談終了から資料送付まで、ほぼ全自動");

  const steps = [
    { n:"1", title:"商談終了",          sub:"Notta\n文字起こし",  dark:false },
    { n:"2", title:"/proposal-outline\n実行", sub:"ファイルを\n1クリック選択", dark:false },
    { n:"3", title:"骨子を自動生成",    sub:"髙橋メソッド\n自動適用",  dark:false },
    { n:"4", title:"「OK」と入力",     sub:"スライド\n自動出力",   dark:false },
    { n:"5", title:"✅ 1時間以内\nに送付完了", sub:"Google Slides\n完成", dark:true },
  ];

  steps.forEach((st, i) => {
    const x = 0.38 + i * 1.96;
    const fill  = st.dark ? TEAL : TEAL_LIGHT;
    const tclr  = st.dark ? WHITE : TEAL_DARK;
    const sclr  = st.dark ? "C0E8F2" : GRAY;

    s.addShape(pptx.ShapeType.rect, {
      x, y: 1.5, w: 1.72, h: 3.2,
      fill: { color: fill },
      line: { color: st.dark ? TEAL_DARK : TEAL, width: 1.2 }
    });
    // Step number circle
    s.addShape(pptx.ShapeType.ellipse, {
      x: x + 0.61, y: 1.6, w: 0.5, h: 0.5,
      fill: { color: st.dark ? TEAL_DARK : TEAL }
    });
    s.addText(st.n, {
      x: x + 0.61, y: 1.6, w: 0.5, h: 0.5,
      fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", fontFace: "Arial"
    });
    s.addText(st.title, {
      x: x + 0.08, y: 2.2, w: 1.56, h: 1.0,
      fontSize: 11.5, bold: true, color: tclr, align: "center", fontFace: "Arial",
      lineSpacingMultiple: 1.3
    });
    s.addText(st.sub, {
      x: x + 0.08, y: 3.28, w: 1.56, h: 1.0,
      fontSize: 10, color: sclr, align: "center", fontFace: "Arial",
      lineSpacingMultiple: 1.3
    });

    // Arrow between steps
    if (i < steps.length - 1) {
      s.addText("→", {
        x: x + 1.72, y: 2.8, w: 0.24, h: 0.4,
        fontSize: 16, bold: true, color: TEAL, align: "center", fontFace: "Arial"
      });
    }
  });

  s.addText("※ 髙橋COOの知見・実績に基づくロジックが全提案に標準装備される", {
    x: 0.45, y: 5.05, w: 9.1, h: 0.35,
    fontSize: 10.5, color: GRAY, fontFace: "Arial", italic: true
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 8 — Time reduction
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "時間短縮の実績：約90%削減", "半日〜1日かかっていた作業が、30〜60分で完結する");

  const MAX_W = 6.5;
  const rows = [
    { label: "骨子作成",  before: "約1時間",           after: "約5分",         ratioB: 0.22, ratioA: 0.03 },
    { label: "スライド化", before: "3〜4時間（深夜作業になることも）", after: "約5〜10分",   ratioB: 1.0,  ratioA: 0.06 },
    { label: "修正・仕上げ", before: "—",              after: "約20〜30分",    ratioB: 0.0,  ratioA: 0.2  },
  ];

  rows.forEach((r, i) => {
    const baseY = 1.4 + i * 1.55;
    s.addText(r.label, {
      x: 0.45, y: baseY, w: 2.0, h: 0.38,
      fontSize: 13, bold: true, color: DARK, fontFace: "Arial", valign: "middle"
    });

    // Before bar
    s.addText("従来", { x: 0.45, y: baseY + 0.42, w: 0.7, h: 0.3, fontSize: 10, color: GRAY, fontFace: "Arial" });
    if (r.ratioB > 0) {
      s.addShape(pptx.ShapeType.rect, {
        x: 1.25, y: baseY + 0.42, w: MAX_W * r.ratioB, h: 0.32,
        fill: { color: LGRAY }, line: { color: LGRAY, width: 0 }
      });
    }
    s.addText(r.before, {
      x: 1.25 + MAX_W * r.ratioB + 0.1, y: baseY + 0.42, w: 3.0, h: 0.32,
      fontSize: 11, color: GRAY, fontFace: "Arial", valign: "middle"
    });

    // After bar
    s.addText("AI活用後", { x: 0.45, y: baseY + 0.85, w: 0.9, h: 0.3, fontSize: 10, color: TEAL, bold: true, fontFace: "Arial" });
    if (r.ratioA > 0) {
      s.addShape(pptx.ShapeType.rect, {
        x: 1.25, y: baseY + 0.85, w: MAX_W * r.ratioA, h: 0.32,
        fill: { color: TEAL }, line: { color: TEAL, width: 0 }
      });
    }
    s.addText(r.after, {
      x: 1.25 + MAX_W * r.ratioA + 0.1, y: baseY + 0.85, w: 3.0, h: 0.32,
      fontSize: 11, bold: true, color: TEAL_DARK, fontFace: "Arial", valign: "middle"
    });
  });

  // Summary box
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 6.3, w: 9.1, h: 0.5,
    fill: { color: TEAL }
  });
  s.addText("合計：半日〜1日　→　30〜60分へ　　生み出した時間を商談・フォローアップに再投資", {
    x: 0.55, y: 6.3, w: 9.0, h: 0.5,
    fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: "Arial", valign: "middle"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 9 — Three values
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "3つの価値の同時実現", "これが、単なるツール活用との違い");

  const cards = [
    { icon: "⚡", title: "スピード",    body: "業界水準（当日〜翌日）を超える\n1時間以内 での送付を実現" },
    { icon: "🎯", title: "個別最適化",  body: "文字起こしからクライアント固有の\n課題・ゴールを自動反映" },
    { icon: "📐", title: "品質標準化",  body: "髙橋COOの知見・実績に基づく\nロジックを全提案に標準装備" },
  ];

  cards.forEach((c, i) => {
    const x = 0.45 + i * 3.18;
    // Top thick border
    s.addShape(pptx.ShapeType.rect, { x, y: 1.25, w: 2.9, h: 0.1, fill: { color: TEAL } });
    // Card
    s.addShape(pptx.ShapeType.rect, {
      x, y: 1.35, w: 2.9, h: 4.5,
      fill: { color: WHITE },
      line: { color: LGRAY, width: 1 },
      shadow: { type: "outer", blur: 5, offset: 2, angle: 45, color: "BBBBBB", opacity: 0.25 }
    });
    // Icon
    s.addText(c.icon, {
      x: x + 0.9, y: 1.6, w: 1.1, h: 0.8,
      fontSize: 32, align: "center", fontFace: "Arial"
    });
    // Title
    s.addText(c.title, {
      x: x + 0.1, y: 2.55, w: 2.7, h: 0.55,
      fontSize: 17, bold: true, color: TEAL, align: "center", fontFace: "Arial"
    });
    // Body
    s.addText(c.body, {
      x: x + 0.1, y: 3.2, w: 2.7, h: 1.6,
      fontSize: 12, color: DARK, align: "center", fontFace: "Arial", lineSpacingMultiple: 1.4
    });
  });

  // Bottom insight
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 6.25, w: 9.1, h: 0.5,
    fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1 }
  });
  s.addText("「ノンコア業務を効率化し、コア業務に時間を使う」を、自分たちが体現する", {
    x: 0.55, y: 6.25, w: 9.0, h: 0.5,
    fontSize: 12, bold: true, color: TEAL_DARK, align: "center", fontFace: "Arial", valign: "middle"
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 10 — Future: Kawaru
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "将来展望①：Kawaruシリーズへの統合", "");

  const levels = [
    { title: "今回の取り組み",         body: "Claude Code Skillで社内実装・実証完了",                        fill: WHITE,      tclr: TEAL_DARK, bclr: TEAL,      w: 5.5, x: 1.0 },
    { title: "Kawaru Team（AI研修）",  body: "「営業提案資料の効率化」を他社への研修として展開",             fill: TEAL_LIGHT, tclr: TEAL_DARK, bclr: TEAL,      w: 6.5, x: 0.5 },
    { title: "Kawaru SaaS（4月1日リリース予定）", body: "このワークフロー自体をSaaSに組み込み、顧客へ提供", fill: TEAL,       tclr: WHITE,     bclr: TEAL_DARK, w: 7.5, x: 0.0 },
  ];

  levels.forEach((lv, i) => {
    const y = 1.3 + i * 1.7;
    s.addShape(pptx.ShapeType.rect, {
      x: lv.x + 0.45, y, w: lv.w, h: 1.3,
      fill: { color: lv.fill },
      line: { color: lv.bclr, width: 1.5 }
    });
    s.addText(lv.title, {
      x: lv.x + 0.65, y: y + 0.1, w: lv.w - 0.25, h: 0.42,
      fontSize: 14, bold: true, color: lv.tclr, fontFace: "Arial"
    });
    s.addText(lv.body, {
      x: lv.x + 0.65, y: y + 0.55, w: lv.w - 0.25, h: 0.6,
      fontSize: 11.5, color: lv.tclr === WHITE ? "D0EEF6" : DARK, fontFace: "Arial"
    });
    if (i < levels.length - 1) {
      s.addText("↓", {
        x: 3.8, y: y + 1.3, w: 0.4, h: 0.4,
        fontSize: 18, bold: true, color: TEAL, align: "center", fontFace: "Arial"
      });
    }
  });

  // Right callout
  s.addShape(pptx.ShapeType.roundRect, {
    x: 8.0, y: 1.3, w: 1.8, h: 5.1,
    fill: { color: "F9FAFB" }, line: { color: LGRAY, width: 1 }, rectRadius: 0.1
  });
  ["自社で実証", "↓", "他社へ展開", "↓", "SaaSに内包", "↓", "売上直結"].forEach((t, i) => {
    s.addText(t, {
      x: 8.05, y: 1.45 + i * 0.65, w: 1.7, h: 0.5,
      fontSize: t === "↓" ? 13 : 11, bold: t !== "↓", color: t === "↓" ? TEAL : TEAL_DARK,
      align: "center", fontFace: "Arial"
    });
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 11 — Future: School division
// ═══════════════════════════════════════════════════════════════
{
  const s = pptx.addSlide();
  s.background = { color: WHITE };
  addHeader(s, "将来展望②：スクール事業部への横展開（私案）", "同じ仕組みが、スクール事業の成約率を上げる可能性がある");

  // LEFT — current
  s.addText("現状", {
    x: 0.45, y: 1.2, w: 3.8, h: 0.35,
    fontSize: 12, bold: true, color: GRAY, align: "center", fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 1.55, w: 3.8, h: 0.7,
    fill: { color: LGRAY }, line: { color: LGRAY, width: 1 }
  });
  s.addText("前半ヒアリング（1〜1.5時間）", {
    x: 0.45, y: 1.55, w: 3.8, h: 0.7,
    fontSize: 12, color: DARK, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addText("↓", {
    x: 0.45, y: 2.25, w: 3.8, h: 0.35,
    fontSize: 16, bold: true, color: GRAY, align: "center", fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 0.45, y: 2.6, w: 3.8, h: 0.7,
    fill: { color: "F3F4F6" },
    line: { color: GRAY, width: 1, dashType: "dash" }
  });
  s.addText("クロージング（同じフォーマット）", {
    x: 0.45, y: 2.6, w: 3.8, h: 0.7,
    fontSize: 12, color: GRAY, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addText("✗ 個別感なし", {
    x: 0.45, y: 3.38, w: 3.8, h: 0.35,
    fontSize: 11.5, bold: true, color: "DC2626", align: "center", fontFace: "Arial"
  });

  // VS
  s.addText("VS", {
    x: 4.4, y: 2.4, w: 0.7, h: 0.5,
    fontSize: 15, bold: true, color: GRAY, align: "center", fontFace: "Arial"
  });

  // RIGHT — proposed
  s.addText("提案", {
    x: 5.25, y: 1.2, w: 4.1, h: 0.35,
    fontSize: 12, bold: true, color: TEAL, align: "center", fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 5.25, y: 1.55, w: 4.1, h: 0.7,
    fill: { color: LGRAY }, line: { color: LGRAY, width: 1 }
  });
  s.addText("前半ヒアリング（1〜1.5時間）", {
    x: 5.25, y: 1.55, w: 4.1, h: 0.7,
    fontSize: 12, color: DARK, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addText("↓", {
    x: 5.25, y: 2.25, w: 4.1, h: 0.35,
    fontSize: 16, bold: true, color: TEAL, align: "center", fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 5.25, y: 2.6, w: 4.1, h: 0.7,
    fill: { color: TEAL }, line: { color: TEAL, width: 1 }
  });
  s.addText("5分で個別提案資料を自動生成", {
    x: 5.25, y: 2.6, w: 4.1, h: 0.7,
    fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addText("↓", {
    x: 5.25, y: 3.3, w: 4.1, h: 0.35,
    fontSize: 16, bold: true, color: TEAL, align: "center", fontFace: "Arial"
  });
  s.addShape(pptx.ShapeType.rect, {
    x: 5.25, y: 3.65, w: 4.1, h: 0.7,
    fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1 }
  });
  s.addText("後半クロージングで投影", {
    x: 5.25, y: 3.65, w: 4.1, h: 0.7,
    fontSize: 12, color: TEAL_DARK, align: "center", fontFace: "Arial", valign: "middle"
  });
  s.addText("✓ インサイトに刺さる提案", {
    x: 5.25, y: 4.43, w: 4.1, h: 0.35,
    fontSize: 11.5, bold: true, color: "059669", align: "center", fontFace: "Arial"
  });

  // Bottom effect boxes
  const effects = ["成約率向上", "AI関心度向上\n（実演効果）", "標準化→\n属人性排除", "商談時間短縮\n→商談数増加"];
  effects.forEach((e, i) => {
    const x = 0.45 + i * 2.38;
    s.addShape(pptx.ShapeType.rect, {
      x, y: 5.3, w: 2.15, h: 0.85,
      fill: { color: TEAL_LIGHT }, line: { color: TEAL, width: 1 }
    });
    s.addText(e, {
      x, y: 5.3, w: 2.15, h: 0.85,
      fontSize: 10.5, bold: true, color: TEAL_DARK, align: "center", fontFace: "Arial",
      valign: "middle", lineSpacingMultiple: 1.2
    });
  });

  // Bottom bar
  s.addShape(pptx.ShapeType.rect, {
    x: 0, y: 6.62, w: "100%", h: 0.55,
    fill: { color: TEAL }
  });
  s.addText("新規事業部での実証　→　スクール事業部へ横展開　→　会社全体の売上貢献へ", {
    x: 0.45, y: 6.62, w: 9.1, h: 0.55,
    fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: "Arial", valign: "middle"
  });
}

// ─── Save ───────────────────────────────────────────────────────
pptx.writeFile({ fileName: "/Users/kyouyuu/cloude/output/hackathon_proposal_skill.pptx" })
  .then(() => console.log("✅ SAVED: hackathon_proposal_skill.pptx"))
  .catch(e => { console.error("❌ ERROR:", e); process.exit(1); });
