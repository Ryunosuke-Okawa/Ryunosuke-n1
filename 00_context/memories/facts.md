# 事実・データメモリ

## 2026-03-18
- 定期実行タスクの状態
  - `morning-daily-schedule`: 毎朝8時（月〜金）工程表生成 → ✅ 稼働中 【唯一必要な定期タスク】
    - ⚠️ 祝日除外は未実装 → 次回改修で対応予定
  - `slack-task-check-noon`: 毎日12時（月〜金）→ ❌ 不要（無効化すべき）
  - `slack-task-check-evening`: 毎日17時（月〜金）→ ❌ 不要（無効化すべき）
  - 決定: 2026-03-18にユーザーが朝8時のみでOKと明言
- 「おはよう」トリガーと定期実行の関係
  - 「おはよう」→ /daily-schedule スキルが手動起動（会話内で実行）
  - 毎朝8時 → morning-daily-schedule が自動起動（定期実行）
  - 両方とも同じ工程表生成を行う
- 祝日判定の実装方針（未実装、次回改修で対応）
  - 方法: スキル実行冒頭でGoogle Calendar APIを呼び、今日が祝日かチェック
  - 判定ソース:
    1. Google Calendar「日本の祝日」カレンダーに当日の予定があるか
    2. primaryカレンダーに「祝日ブロック」「祝日」等の記載があるか
  - いずれかに該当 → 工程表生成をスキップ

## 2026-04-24
- Claude Codeライブイベント用アンケート（最終版・5問構成）
  - 詳細ファイル: `marketing/claudecode_live_survey_draft.md`
  - Q1: お立場は？（単一・5択）エンジニア／非エンジニア／マネージャー・経営層／情シス・DX／その他
  - Q2: Claude Codeの利用状況は？（単一・5択）まだ使っていない／検討中／試した／個人で活用／チーム・組織で導入
  - Q3: Claude Codeで気になることは？（複数可・6択）何ができるか／学習コスト／セキュリティ／非エンジニア／チームで使う仕組み／費用感
  - Q4: Claude Codeをどう活用したい？（複数可・7択）個人／チーム／部署・部門／新規事業・特定プロジェクト／非エンジニア部門／全社／未検討 ← 展開スケール軸
  - Q5: 自由記述（一番聞きたいこと）
  - 設計意図: 回答内容から参加者層・AI成熟度・営業提案シナリオを自動仕分け
  - 実装先候補: Google Forms + QRコード、Mentimeter、Slido
  - 関連: `https://claudecode.n1-inc.co.jp/`（LP公開済み）
- Claude Code法人向けLP 公開情報
  - URL: `https://claudecode.n1-inc.co.jp/`
  - ホスティング: XServer（n1-inc.co.jpのサブドメイン）
  - CTA: TimeRex予約（https://timerex.net/s/r.okawa_54e9_ded1/a9ae1912）＋ LINE（https://liff.line.me/2007309014-D4N3WV34/landing?follow=%40172ilyxr&lp=WevSoA&liff_id=2007309014-D4N3WV34）の2パス
  - ローカルソース: `marketing/claudecode_training_lp.html`
  - デプロイログ: `marketing/claudecode_lp_deploy_log.md`

## 2026-04-26
- Claude Code LP Challenges 3カード設計（最終版）
  - **設計ロジック**: Claude Code導入ジャーニー3段階の壁（Technology Acceptance Modelに準拠）
    - 触り始め → 学習 → 業務適用 の3ドロップオフポイント
  - **CASE 01 SETUP STUCK**: 「そもそも、インストールや設定で詰まる」（Node.js/ターミナル/APIキーの壁）
  - **CASE 02 JARGON OVERLOAD**: 「専門用語ばかりで、何が何だか分からない」（CLI/npm/git/MCP/API等）
  - **CASE 03 NO USE-CASE**: 「動かせるけど、仕事で何に使えばいいか分からない」（ツールと業務の深い溝）
  - **レイアウト**: テキスト（タグ・CASE No・タイトル・本文）を上、イラスト（240px）を下
  - **イラスト**: 各カード大きなSVGイラスト
    - CASE 01: コーラル色の鍵（Padlock）＋ 周辺に技術用語タグ（Node.js / ターミナル / APIキー / npm）
    - CASE 02: 困惑顔（バツ目）＋ 飛び交う用語タグ（CLI / npm / MCP / git / API / トークン / フック / リポジトリ）
    - CASE 03: 左にClaude Codeターミナル、右に書類＋ブリーフケース、間に深い溝＋大きな「？」
  - **背景**: SNS・YouTube・ブログでよく言及される「経営課題」レベルではなく、実際にツールを触った人がぶつかる「身近で泥臭いつまずき」に焦点
  - **関連ファイル**: `marketing/claudecode_training_lp.html`
