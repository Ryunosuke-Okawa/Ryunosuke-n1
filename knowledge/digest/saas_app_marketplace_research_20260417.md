---
title: SaaS App Marketplace調査（Zoom/kintone/Box/SmartHR/freee/マネーフォワード）
date: 2026-04-17
tags:
  - research
  - marketplace
  - integration
  - OAuth
  - SaaS
---

# SaaS App Marketplace調査

サードパーティSaaSアプリが登録・掲載でき、エンドユーザーがOAuthベースのワンクリック接続を利用できる公開アプリマーケットプレイスの有無を調査。

## 1. Zoom App Marketplace

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり |
| **マーケットプレイスURL** | https://marketplace.zoom.us/ |
| **開発者登録ページ** | https://developers.zoom.us/ |
| **サードパーティ公開掲載** | 可能（Public / Unlisted / Private の3種類） |
| **認証方式** | OAuth 2.0（Unified Build Flowで複数Zoom製品に対応） |
| **審査・要件** | 機能審査、セキュリティ審査、コンプライアンス審査、ブランディング要件あり。全アプリがZoomによる審査を通過する必要あり |
| **承認期間目安** | 初回レスポンスSLA: 72時間以内（平日PT 9-17時）。全体の公開プロセスは4週間以上（レビューバックログ次第）。FIFO方式で処理 |
| **費用** | 無料（開発者アカウント登録無料） |
| **備考** | 2025年にUnified Build Flow導入。1つのアプリでMeetings/Phone/Chat/Contact Center等に対応可能 |

### 主要リンク
- 配布ガイド: https://developers.zoom.us/docs/distribute/
- 審査プロセス: https://developers.zoom.us/docs/distribute/app-review-process/
- 審査ガイドライン: https://developers.zoom.us/docs/distribute/app-review-guidelines/

---

## 2. kintone（サイボウズ）

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（kintone連携サービス一覧 + SmaBiz!プラグインマーケット） |
| **マーケットプレイスURL** | https://kintone-sol.cybozu.co.jp/integrate/ |
| **開発者サイト** | https://cybozu.dev/ja/（日本語）/ https://kintone.dev/en/（英語） |
| **サードパーティ公開掲載** | 可能（「kintone連携サービス認定」を取得すると公式サイトに掲載） |
| **認証方式** | APIトークン認証 / OAuth 2.0（cybozu.comアカウント経由）/ パスワード認証 |
| **審査・要件** | **認定基準あり**: セキュアコーディングガイドライン遵守、公開API のみ使用、導入実績2件以上（自社利用除く）、問い合わせ窓口あり、セキュリティ事故時の報告義務、価格の明示等 |
| **承認期間目安** | 非公開（パートナーネットワーク加入→認定申請→審査の流れ。CyPN加入自体にエントリーシート提出・面談が必要） |
| **費用** | 開発者ライセンスは無料（1年間有効）。パートナー加入は費用要確認 |
| **備考** | SB C&SのSmaBiz!でプラグイン購入も可能。CyPN Report（パートナー評価制度）で星評価あり。2025年11月に認定基準改定 |

### 主要リンク
- 連携サービス認定基準: https://kintone-sol.cybozu.co.jp/integrate/guidelines.html
- パートナー加入: https://partner.cybozu.co.jp/join/system/
- 開発者ライセンス: https://kintone.dev/en/developer-license-registration-form/

---

## 3. Box App Center

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（Box Integrations / Box App Center） |
| **マーケットプレイスURL** | https://cloud.app.box.com/integrations |
| **開発者コンソール** | https://app.box.com/developers/console |
| **サードパーティ公開掲載** | 可能（Dev Consoleの「Publishing」タブから申請） |
| **認証方式** | **OAuth 2.0必須**（App Center掲載にはOAuth 2.0認証が必要。他の認証方式の場合もOAuth 2.0アプリをマーケティング用リスティングとして作成可） |
| **審査・要件** | 提出チェックリストの確認、アプリ情報（カテゴリ、説明文、スクリーンショット、アイコン、サポートリソース）の入力が必要。Boxチームがレビュー後に公開 |
| **承認期間目安** | 非公開（Box Partnersチーム integrate@box.com に問い合わせ） |
| **費用** | 無料（開発者アカウント無料） |
| **備考** | 1,500以上のインテグレーションが掲載。Microsoft、Zoom、Salesforce、Slack等の大手パートナーが参加。Core Boxパッケージに含まれる |

### 主要リンク
- アプリ公開ガイド: https://developer.box.com/guides/getting-started/publish-app
- 開発者ドキュメント: https://developer.box.com/guides
- 問い合わせ先: integrate@box.com

---

## 4. SmartHR Plus

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（SmartHR Plus アプリストア） |
| **マーケットプレイスURL** | https://www.smarthr.plus/ |
| **開発者サイト** | https://developer.smarthr.jp/ |
| **サードパーティ公開掲載** | 可能（パートナープログラムに参画→アプリ開発→審査→掲載） |
| **認証方式** | OAuth 2.0（SmartHR APIを利用した認可連携） + APIトークン認証 |
| **審査・要件** | **パートナープログラムへの参画が前提**。連携要件のすり合わせ→連携仕様のすり合わせ→開発→連携機能の審査→リリースの5ステップ。SmartHRが開発環境支援、デザインシステム共有、API仕様案内等を提供 |
| **承認期間目安** | 非公開（5ステップのプロセス全体で数ヶ月が目安と推測。要SmartHRとの個別調整） |
| **費用** | API利用は無料。パートナープログラム参加費用は非公開（要問い合わせ） |
| **備考** | 2023年12月正式リリース。2024年時点で39社パートナー・47アプリ掲載。100〜300アプリへの拡大計画中。SmartHR Plus Partner Award制度あり。SmartHR Labsで実験的アプリも公開。登録社数70,000社以上へのリーチが可能 |

### 主要リンク
- パートナープログラム: https://www.smarthr.plus/partner
- SmartHR API: https://developer.smarthr.jp/api
- サンドボックス環境: https://developer.smarthr.jp/api/about_sandbox

---

## 5. freee アプリストア

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | あり（freeeアプリストア） |
| **マーケットプレイスURL** | https://www.freee.co.jp/appstore/ |
| **開発者ページ** | https://app.secure.freee.co.jp/developers |
| **サードパーティ公開掲載** | 可能（パブリックアプリとして作成→審査→公開） |
| **認証方式** | **OAuth 2.0**（Authorization Code Grant推奨） |
| **審査・要件** | アプリ審査あり: (1) パブリックタイプで作成必須（後から変更不可）、(2) テスト用事業所では公開アプリ作成不可、(3) ヘルプページに連携方法・操作方法・解除方法の記載必須、(4) 権限は最小限に設定、(5) 事業所選択機能の実装、(6) 審査用デモアカウントの提供、(7) アプリ名に「for freee」「by freee」等は使用不可。必要に応じてオンラインデモンストレーションを依頼される場合あり |
| **承認期間目安** | **約1〜2週間**（申請受理からアプリストア公開まで） |
| **費用** | 無料（開発者登録・API利用ともに無料） |
| **備考** | プラン限定アプリ制度あり（高度なワークフロー機能等はアドバンスプラン以上が必要）。6事業所以上への提供にはパブリックアプリ審査が必須。更新公開時も再審査が必要 |

### 主要リンク
- アプリ公開手順: https://developer.freee.co.jp/startguide/deploy-app
- アプリ審査プロセス: https://developer.freee.co.jp/reference/app-review-process
- 開発者コミュニティ: https://developer.freee.co.jp/
- ガイドライン: https://app.secure.freee.co.jp/developers/guidelines/

---

## 6. マネーフォワード クラウド（Money Forward）

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | **なし**（公開アプリマーケットプレイスは存在しない） |
| **連携サービス一覧URL** | https://accounting.moneyforward.com/service_catalog （公式連携サービスカタログ） |
| **開発者サイト** | https://developers.biz.moneyforward.com/ |
| **サードパーティ公開掲載** | **不可**（freeeやSmartHRのような公開アプリストアは未整備。API連携は「アプリポータル」経由で個別設定） |
| **認証方式** | OAuth 2.0 + APIキー認証（ユースケースにより選択） |
| **審査・要件** | 公開マーケットプレイスがないため、公開審査プロセスは存在しない。個別のAPI連携は自由に開発可能。パートナープログラムは販売代理店向け |
| **承認期間目安** | N/A（マーケットプレイス掲載の仕組みがない） |
| **費用** | アプリポータルの登録・利用は無料 |
| **備考** | APIは公開されておりOAuth 2.0/APIキーで連携開発は可能だが、freeeのようなアプリストア型のサードパーティアプリ公開プラットフォームは現時点で存在しない。連携サービスカタログには一部パートナーサービスが掲載されているが、自己申請型のマーケットプレイスではない |

### 主要リンク
- 開発者サイト: https://developers.biz.moneyforward.com/
- API入門: https://developers.biz.moneyforward.com/docs/common/getting-started-moneyforward-cloud-apis/
- パートナー（販売代理店）: https://biz.moneyforward.com/resellers/

---

## サマリー比較表

| サービス | マーケットプレイス | OAuth対応 | セルフ申請 | 審査期間 | 掲載費用 |
|---------|:--:|:--:|:--:|:--:|:--:|
| **Zoom** | あり | OAuth 2.0 | 可 | 4週間+ | 無料 |
| **kintone** | あり | OAuth 2.0 / APIトークン | 要パートナー認定 | 非公開 | 無料（開発者） |
| **Box** | あり | OAuth 2.0必須 | 可 | 非公開 | 無料 |
| **SmartHR** | あり | OAuth 2.0 | 要パートナー契約 | 非公開（数ヶ月） | 要問い合わせ |
| **freee** | あり | OAuth 2.0 | 可 | 1〜2週間 | 無料 |
| **マネーフォワード** | **なし** | OAuth 2.0 / APIキー | N/A | N/A | N/A |
