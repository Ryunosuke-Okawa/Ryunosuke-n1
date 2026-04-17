---
title: SaaS App Marketplace リサーチ Vol.2（Google/Microsoft/Slack/Notion/Chatwork/LINE WORKS/Dropbox）
date: 2026-04-17
tags:
  - research
  - marketplace
  - integration
  - SaaS
  - Kawaru
  - OAuth
---

# SaaS App Marketplace リサーチ Vol.2

サードパーティSaaSアプリがOAuthベースのワンクリック接続を提供するために、各プラットフォームの公開マーケットプレイスに登録・掲載できるかを調査。

---

## 1. Google Workspace Marketplace

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり |
| **マーケットプレイスURL** | https://workspace.google.com/marketplace/ |
| **開発者ページ** | https://developers.google.com/workspace/marketplace |
| **サードパーティ公開掲載** | 可能（公開アプリとして誰でも申請可能） |
| **認証方式** | OAuth 2.0（必須。Google Cloud Projectの作成とOAuth同意画面の設定が前提） |
| **審査・要件** | Google Workspace Marketplace SDK有効化、OAuth検証の完了、アプリ名・説明・スクリーンショット・アイコン等の品質基準、機能性・UX・ブランディング・グラフィック等の多岐にわたる審査項目、テストアカウント提供が必要な場合あり |
| **承認期間目安** | 数日〜数週間（提出時の品質やキューの状況次第。OAuth検証が別途必要な場合はさらに数週間〜数ヶ月追加） |
| **費用** | Google Cloud Projectの維持費のみ（マーケットプレイス掲載自体は無料） |

### 参考URL
- 公開手順: https://developers.google.com/workspace/marketplace/how-to-publish
- レビュープロセス: https://developers.google.com/workspace/marketplace/about-app-review

---

## 2. Microsoft 365 (Microsoft AppSource / Teams App Store)

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（Microsoft Marketplace / AppSource） |
| **マーケットプレイスURL** | https://marketplace.microsoft.com/ |
| **開発者ページ** | https://partner.microsoft.com/dashboard/marketplace-offers/overview |
| **サードパーティ公開掲載** | 可能（Partner Centerアカウント作成後に申請） |
| **認証方式** | OAuth 2.0（Azure AD / Microsoft Identity Platform） |
| **審査・要件** | Partner Centerアカウント作成（会社アカウント、承認プロセスあり）、認証ポリシー準拠、ウイルスフリー・安定性・機能性、テストアカウント提供推奨。Microsoft 365 App Compliance Program（オプション） |
| **承認期間目安** | 3〜5営業日（自動チェック＋バリデーションチーム）。Teams/SPFxアプリは24時間以内。認証後は約1時間で表示 |
| **費用** | 無料（Partner Centerアカウント登録無料） |

### 参考URL
- 提出ガイド: https://learn.microsoft.com/en-us/partner-center/marketplace/submit-to-appsource-via-partner-center
- 認証ポリシー: https://learn.microsoft.com/en-us/legal/marketplace/certification-policies
- 概要: https://learn.microsoft.com/en-us/partner-center/marketplace/overview

---

## 3. Slack (Slack Marketplace)

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（Slack Marketplace、旧 Slack App Directory） |
| **マーケットプレイスURL** | https://slack.com/marketplace |
| **開発者ページ** | https://api.slack.com/ |
| **サードパーティ公開掲載** | 可能（レビュー通過後に公開リスト化） |
| **認証方式** | OAuth 2.0（必須。配布アプリは全ワークスペースでOAuthフロー必要。SSL必須） |
| **審査・要件** | Unlisted Distribution → Marketplace申請の2段階。ガイドライン・要件への準拠。予備審査（最大10営業日）→ 機能審査（新規: 最大10週間、再提出: 最大6週間）。再提出でキューリセット |
| **承認期間目安** | 合計: 数週間〜3ヶ月程度（予備審査10営業日 + 機能審査最大10週間。複数ラウンドのフィードバック可能性あり） |
| **費用** | 無料 |

### 参考URL
- 配布ガイド: https://api.slack.com/start/distributing
- レビューガイド: https://docs.slack.dev/slack-marketplace/slack-marketplace-review-guide/
- ガイドライン: https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements/

---

## 4. Notion (Notion Integration Gallery / Marketplace)

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（Notion Marketplace / Integration Gallery） |
| **マーケットプレイスURL** | https://www.notion.so/integrations/all |
| **開発者ページ** | https://developers.notion.com/ |
| **サードパーティ公開掲載** | 可能（セルフサーブ申請が可能になった。以前は招待制） |
| **認証方式** | OAuth 2.0（Public Integration必須。Internal Integrationは掲載不可。installation scopeが「Any workspace」のみ対象） |
| **審査・要件** | Notion Creator DashboardからListing作成・提出。セキュリティ・プライバシーレビュー通過が必要。ブランド/トレードマーク問題、品質基準への適合。Technology Partner Program参加で有利 |
| **承認期間目安** | 5〜10営業日（初回フィードバック）。不承認の場合は修正・再提出可能 |
| **費用** | 無料 |

### 参考URL
- 掲載ガイド: https://developers.notion.com/guides/get-started/publishing-integrations-to-notions-integration-gallery
- Technology Partner Program: https://www.notion.com/lp/technology-partner-program

---

## 5. Chatwork

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | **なし**（公開マーケットプレイスは存在しない） |
| **連携サービス紹介ページ** | https://go.chatwork.com/ja/integrate/ |
| **開発者ページ** | https://developer.chatwork.com/ |
| **サードパーティ公開掲載** | **不可**（自由に登録・掲載できる仕組みなし） |
| **認証方式** | OAuth 2.0対応あり + APIトークン認証 + Webhook |
| **審査・要件** | N/A（マーケットプレイスがないため公開審査プロセスなし） |
| **承認期間目安** | N/A |
| **費用** | N/A |
| **備考** | 連携サービス紹介ページに一部パートナーが掲載されているが、自動登録の仕組みはない。IFTTT / Zapier経由の連携が推奨。API利用には組織管理者への申請が必要（ビジネス/エンタープライズプラン） |

### 参考URL
- APIドキュメント: https://developer.chatwork.com/
- 連携サービス一覧: https://go.chatwork.com/ja/integrate/

---

## 6. LINE WORKS（アプリディレクトリ）

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（**アプリディレクトリ**） |
| **マーケットプレイスURL** | https://line-works.com/appdirectory/ |
| **開発者ページ** | https://developers.worksmobile.com/jp/ |
| **サードパーティ公開掲載** | 可能だが**招待/審査制**（LINE WORKS公認アプリとしての審査・動作確認が必要） |
| **認証方式** | OAuth 2.0 (API 2.0対応) + Service Account認証 / User Account認証 |
| **審査・要件** | LINE WORKS側の審査・動作確認が必要。「LINE WORKS公認アプリ」として配信。自由申請型ではなくパートナーシップ的位置付け。100種類以上の連携ソリューションが現在掲載 |
| **承認期間目安** | 不明（公式に明示なし。パートナーシップ交渉を含むため数ヶ月と推定） |
| **費用** | 不明（パートナー契約による可能性） |

### 結論
アプリディレクトリは存在するが、セルフサーブで自由に登録できる仕組みではない。掲載希望の場合はLINE WORKSの担当部署への直接問い合わせが必要。

### 参考URL
- アプリディレクトリ: https://line-works.com/appdirectory/
- Developer Console: https://developers.worksmobile.com/jp/

---

## 7. Dropbox (Dropbox App Center)

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（**Dropbox App Center**） |
| **マーケットプレイスURL** | https://www.dropbox.com/apps |
| **開発者ページ** | https://www.dropbox.com/developers |
| **サードパーティ公開掲載** | **限定的**（App Centerへの掲載は招待制/パートナー選定制） |
| **認証方式** | OAuth 2.0（Scoped Access方式。App Console でアプリ作成、スコープ設定） |
| **審査・要件** | **Production Statusの取得が第一段階**: 50ユーザー以上リンク後にレビュー開始、ブランディングガイドライン・利用規約準拠。**App Center掲載はProduction Status取得とは別**: Dropboxが選定したテクノロジーパートナーのみ掲載。自動掲載なし |
| **承認期間目安** | Production Status: 50ユーザー到達後、申請から数週間。App Center掲載: パートナーシップ交渉が必要なため不明（数ヶ月と推定） |
| **費用** | 無料（ただしパートナー契約が必要な場合あり） |

### 参考URL
- Developer Guide: https://www.dropbox.com/developers/reference/developer-guide
- App Console: https://www.dropbox.com/developers/apps
- パートナープログラム: https://www.dropbox.com/business/partners

---

## 比較サマリー

| サービス | マーケットプレイス | セルフサーブ登録 | OAuth 2.0 | レビュー期間 | 掲載の敷居 |
|---------|:--:|:--:|:--:|:--:|:--:|
| **Google Workspace** | あり | 可能 | 必須 | 数日〜数週間 | 中（OAuth検証含む） |
| **Microsoft 365** | あり | 可能 | 必須 | 3〜5営業日 | 中 |
| **Slack** | あり | 可能 | 必須 | 数週間〜3ヶ月 | 高（審査が厳格） |
| **Notion** | あり | 可能 | 必須 | 5〜10営業日 | 中 |
| **Chatwork** | **なし** | 不可 | 対応あり | N/A | N/A |
| **LINE WORKS** | あり（審査制） | **不可**（招待制） | 対応あり | 不明 | 高（パートナー交渉） |
| **Dropbox** | あり（選定制） | **不可**（招待制） | 必須 | 不明 | 高（パートナー選定） |

### 推奨優先順位（掲載しやすさ順）
1. **Microsoft 365** — レビューが最速（3〜5日）、Partner Centerも無料
2. **Notion** — セルフサーブ化済み、5〜10営業日
3. **Google Workspace** — 標準的だがOAuth検証が追加ステップ
4. **Slack** — 最も時間がかかる（最大3ヶ月）が、影響力大
5. **LINE WORKS** — アプリディレクトリ存在するが招待制
6. **Dropbox** — App Center掲載はパートナー選定制
7. **Chatwork** — マーケットプレイス自体が存在しない
