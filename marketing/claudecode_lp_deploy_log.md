---
title: Claude Code 法人向けLP 公開ログ
date: 2026-04-24
tags:
  - marketing
  - lp
  - claudecode
  - deploy
---

# Claude Code 法人研修・コンサルティング LP

## 公開URL
https://claudecode.n1-inc.co.jp/

## 構成概要
- ポジショニング：Claude Codeの法人向け研修＋コンサルティング（Kawaruブランドは非表示）
- 訴求：煽らず、抽象度高め
- カラー：白ベース＋Claudeコーラル（`#D97757`）
- ビジュアル：ヒーローにClaude Codeターミナル風モック、Programsに別タイプのビジュアル

## セクション
1. Hero（非対称2カラム：コピー＋ターミナル）
2. Meta Strip（4つの訴求バー）
3. Challenges（3カード）
4. Programs（Training / Consulting の2プログラム＋両方セットも可）
5. Process（4ステップ）
6. FAQ（6問）
7. CTA（Googleフォーム連携・要差し替え）
8. Footer

## インフラ
- ホスティング：エックスサーバー（XServer レンタルサーバー）
- サーバーID：xs842147
- ドメイン：n1-inc.co.jp のサブドメイン `claudecode`
- ドキュメントルート：`/home/xs842147/n1-inc.co.jp/public_html/claudecode.n1-inc.co.jp/`
- SSL：無料独自SSL（Let's Encrypt）有効

## ファイル構造（サーバー側）
```
claudecode.n1-inc.co.jp/
├── index.html             # LP本体（ローカルでは marketing/claudecode_training_lp.html）
└── assets/
    └── n1-logo.jpg        # エヌイチロゴ
```

## ローカルのソースファイル
- `marketing/claudecode_training_lp.html`（編集元）
- `marketing/assets/n1-logo.jpg`
- デプロイ用：`~/Desktop/claudecode_lp_deploy/`（rename to index.html）

## 更新方法
1. ローカルで `marketing/claudecode_training_lp.html` を編集
2. `index.html` としてリネーム or コピー
3. XServerファイルマネージャで `claudecode.n1-inc.co.jp/` に上書きアップロード
4. ブラウザで Cmd+Shift+R ハード再読み込み

## CTA設計（2026-04-24 更新）
GoogleフォームはやめてCTAを2パスに変更：
1. **TimeRex予約**：即商談に持ち込む導線
   - URL：https://timerex.net/s/r.okawa_54e9_ded1/a9ae1912
   - 配置：ヒーロー Primaryボタン、#contact 左カード
2. **LINE流入**：気軽な質問→チャット対応
   - URL：https://liff.line.me/2007309014-D4N3WV34/landing?follow=%40172ilyxr&lp=WevSoA&liff_id=2007309014-D4N3WV34
   - 配置：ヒーロー Secondaryボタン（LINE緑アウトライン）、#contact 右カード（LINE緑）

## 残タスク
- [ ] （任意）ターミナルのダミー題材を実研修題材に差し替え
- [ ] （任意）`default_page.png` の削除（XServer初期ファイル、表示には影響なし）
- [ ] （運用）TimeRex予約数・LINE追加数のトラッキング方法を検討
