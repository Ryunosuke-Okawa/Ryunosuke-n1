---
title: Kawaruフライヤー裏面 画像生成AIプロンプト
date: 2026-04-21
tags:
  - 展示会
  - 8EXPO
  - Kawaru
  - デザイン
  - AIプロンプト
---

# Kawaruフライヤー裏面 インフォグラフィック生成プロンプト

## 日本語プロンプト（Imagen / Nano Banana / Firefly 向け）

```
日本のB2B SaaS製品「Kawaru」のA4縦フライヤー裏面デザインを作成。

【テーマ】「チャットで、誰でもかんたんにワークフローが作れる」AIツール。シンプル・モダン・信頼感。

【カラースキーム】
- 背景：白（#FFFFFF）
- メインカラー：青（#1E90FF）
- 見出し色：濃紺（#0F3057）
- カード背景：薄い青（#E8F4FF）
- アクセント：オレンジ（#FF9800、数字強調のみ）
- トリガーノード：緑（#4CAF50）

【レイアウト（上から順）】

1. ヘッダー（上端）
   - 左：Kawaruロゴ（濃紺の角丸スクエアに白文字「K」＋右に「Kawaru」テキスト）
   - 右：青い丸角バッジ「AI Workflow Builder」

2. ヒーロー見出し（大きく、中央寄せ）
   「『チャットで』誰でもかんたんに、
    ワークフローがつくれる。」
   - 「『チャットで』」のみ青（#1E90FF）
   - 残りは濃紺（#0F3057）太ゴシック
   - 下にサブコピー「日本語で話すだけ。AIを学ばなくていい。組まなくていい。」

3. Before→After スクリーンショット比較
   - 左：チャット入力画面モックアップ
     ・タイトル「どんな課題がありますか？」
     ・入力欄＋4つのタグチップ（メール対応／連絡見逃し／議事録／問い合わせ）
     ・キャプション「① 課題をチャットするだけ」
   - 中央：大きな青い矢印 ➔ ＋「自動で」ラベル（青塗り丸角バッジ）
   - 右：ノード型ワークフロー画面モックアップ
     ・縦に6つのノードカード（未読メール監視→返信判定→分岐→下書き→Gmail保存→Slack通知）
     ・各ノード左端に色付きライン（1番目：緑／最終：オレンジ／他：青）
     ・キャプション「② 複数ノードのワークフローが完成」

4. 3つの強みカード（横並び3カラム、薄い青背景カード）
   ・01 専門知識不要：エンジニアリングやAIの専門知識は一切不要
   ・02 構築時間不要：チャットで指示するだけで自動構築
   ・03 人材育成不要：日本語で話せれば誰でも使える

5. 活用事例セクション（左に青い縦棒＋タイトル）
   タイトル「活用事例：ノーコードでワークフローを構築」
   6×4のグリッドに小さなノードアイコンカード24個：
   ・緑＝トリガー（メール受信／会議録画／商談完了／Slackスタンプ／毎朝定時／定期実行）
   ・青＝処理（AI要約／文字起こし／情報抽出 等）
   ・オレンジ＝アクション（下書き保存／Slack通知／SF格納 等）

6. フッター CTA（濃紺→青のグラデ背景、角丸）
   ・左：「まずは無料相談から」（白太字）＋ サブ「30分で、あなたの業務をワークフロー化」
   ・中央：QRコードエリア（白箱）
   ・右：白文字のKawaruロゴ

【スタイル】
- 日本語フォント：Noto Sans JP / ヒラギノ角ゴ系
- ミニマリスト、情報が整理された印象
- 影は控えめ（box-shadow: 0 2px 10px rgba(15,48,87,0.08)相当）
- 角丸は2〜3mm程度
- 全体に余白を確保（詰め込みすぎない）
- 縦横比はA4縦（210:297 ≒ 1:1.414）
```

## 英語プロンプト（Midjourney / DALL-E 向け）

```
Professional A4 portrait flyer back page design for Japanese B2B SaaS "Kawaru" - an AI workflow builder. Clean, modern, trustworthy aesthetic.

Color palette: white background, primary blue #1E90FF, navy #0F3057 for headlines, light blue #E8F4FF for card backgrounds, orange #FF9800 for accents, green #4CAF50 for trigger nodes.

Layout top to bottom:

1. Top header: Kawaru logo (navy square with white K + "Kawaru" text) on left, blue pill badge "AI Workflow Builder" on right.

2. Hero headline (large, centered, Japanese text): 
「『チャットで』誰でもかんたんに、ワークフローがつくれる。」
with "『チャットで』" highlighted in blue, rest in navy bold sans-serif. Small subtitle below.

3. Before→After UI mockup comparison:
- Left: Chat input screen mockup with "どんな課題がありますか？" title, input bar, and 4 clickable tag chips. Caption: "① 課題をチャットするだけ"
- Center: Large blue arrow ➔ with blue pill label "自動で"
- Right: Node-based workflow screen mockup showing 6 vertically stacked node cards (connected pipeline with icons). First node green (trigger), last node orange (action). Caption: "② 複数ノードのワークフローが完成"

4. Three strength cards in a row with light blue backgrounds:
- 01 専門知識不要 (No technical expertise needed)
- 02 構築時間不要 (No build time)
- 03 人材育成不要 (No training needed)

5. Use case showcase: Title "活用事例：ノーコードでワークフローを構築" with blue vertical bar. Grid of 24 mini icon cards (6 columns x 4 rows) showing workflow examples: green=triggers, blue=processes, orange=actions.

6. Bottom CTA bar: navy-to-blue gradient rounded rectangle. Left: "まずは無料相談から" in white bold + subtitle. Center: white QR code box. Right: white Kawaru logo.

Style: minimalist, Japanese B2B SaaS aesthetic, Noto Sans JP font style, clean spacing, subtle shadows, 2-3mm rounded corners, A4 portrait aspect ratio (1:1.414).
```

## 使い方

1. Imagen 3 / Nano Banana：日本語プロンプトをそのまま使う
2. Midjourney / DALL-E 3：英語プロンプトをそのまま使う
3. **HTMLモックアップ** `flyer_kawaru_back_mockup_v1.html` をブラウザで開いて印刷プレビュー → PDF化すれば、デザイナーへの発注資料としても使える
4. ZAPP小畑さんへのデザイン相談時には、HTMLモックアップのスクリーンショット＋上記プロンプトを添付すると意図が伝わりやすい
