---
title: SaaS マーケットプレイス登録手順書（Kawaru掲載用・全14サービス）
date: 2026-04-17
tags:
  - research
  - marketplace
  - integration
  - Kawaru
  - registration
  - procedure
---

# SaaS マーケットプレイス登録手順書（Kawaru掲載用）

Kawaruをサードパーティアプリとして各SaaSマーケットプレイスに掲載するための、具体的な登録手順・必要素材・審査プロセスをまとめた実務ガイド。

---

## 1. Google Workspace Marketplace

### 概要
- **URL**: https://workspace.google.com/marketplace/
- **開発者ページ**: https://developers.google.com/workspace/marketplace
- **費用**: 無料（Google Cloud Projectの維持費のみ）
- **審査期間**: 数日〜数週間（OAuth検証が未完了の場合はさらに数週間〜数ヶ月追加）

### 前提条件
- Google Cloud Projectの作成済み
- OAuth 2.0同意画面の設定・検証完了（公開アプリの場合はOAuth検証必須）
- Google Workspaceの少なくとも1つのアプリケーションを拡張するアプリであること

### 登録手順

**Step 1: Google Cloud Projectの作成**
- Google Cloud Console (https://console.cloud.google.com) でプロジェクトを作成
- 既存のプロジェクトがあればそれを使用

**Step 2: OAuthの設定**
- Google Cloud Console > API & Services > OAuth同意画面を設定
- ユーザータイプを「外部」に設定（内部にするとリジェクトされる）
- パブリッシュステータスを「本番環境」に設定（テスト状態はNG）
- 公開アプリの場合、OAuth検証の申請・完了が必要
- 制限付きスコープを使用する場合、セキュリティ評価も必要

**Step 3: Google Workspace Marketplace SDKの有効化**
- Google Cloud Console > API & Services > Google Workspace Marketplace SDK を有効化
- アプリの可視性（公開/非公開）、インストール設定、拡張するGoogle Workspaceアプリの設定

**Step 4: ストアリスティングの作成**
- Google Cloud Console > API & Services > Google Workspace Marketplace SDK > ストア情報 に移動

### 必要素材

| 素材 | 仕様 | 必須/任意 |
|------|------|----------|
| **アプリ名** | 50文字以内。OAuth同意画面の名前と一致。「Google」の文字使用不可 | 必須 |
| **短い説明** | 200文字以内 | 必須 |
| **詳細説明** | 16,000文字以内 | 必須 |
| **カテゴリ** | 適切なカテゴリを1つ選択 | 必須 |
| **アプリアイコン** | 128x128px と 32x32px の最低2枚（Webアプリの場合96x96と48x48も必要）。正方形、透明背景、カラー | 必須 |
| **リスティングカードバナー** | 220x140px | 必須 |
| **スクリーンショット** | 1280x800px（640x400 or 2560x1600も可）。1〜5枚。角丸なし・枠なし | 必須 |
| **利用規約URL** | 利用規約ページへのリンク | 必須 |
| **プライバシーポリシーURL** | プライバシーポリシーページへのリンク | 必須 |
| **サポートURL** | サポートページへのリンク | 必須 |
| **YouTube動画** | 紹介動画（任意） | 任意 |
| **価格情報** | 無料/有料/無料トライアル/フリーミアム | 任意 |
| **開発者名・Webサイト** | 正確な開発者情報 | 必須 |

**Step 5: 審査提出**
- ストア情報ページで全項目入力後「審査に提出」をクリック
- 非公開アプリは即時公開、公開アプリはGoogle審査後に公開

### 審査基準（主要項目）
- アプリ名がユニーク・バージョン番号なし・50文字以内
- 全リンクが正常動作・正確な情報に遷移
- 明らかなバグなし、全機能が完全動作
- Google商標の不正使用なし
- ワンクリックSSO or ゼロクリックSSO
- 管理者がドメインのOAuth権限を付与済みなら個別ユーザーに再度権限要求しない
- テストアカウントが必要な場合はGoogle審査チームに提供

### 参考URL
- 公開手順: https://developers.google.com/workspace/marketplace/how-to-publish
- 審査プロセス: https://developers.google.com/workspace/marketplace/about-app-review
- リスティング作成: https://developers.google.com/workspace/marketplace/create-listing

---

## 2. Microsoft AppSource

### 概要
- **URL**: https://marketplace.microsoft.com/
- **開発者ダッシュボード**: https://partner.microsoft.com/dashboard/marketplace-offers/overview
- **費用**: 無料（Partner Centerアカウント登録無料）
- **審査期間**: 3〜5営業日（Teams/SPFxアプリは24時間以内）。認証後は約1時間で表示

### 前提条件
- Microsoft Partner Centerの会社アカウント作成・承認完了
- Azure AD（Microsoft Identity Platform）によるOAuth 2.0認証の実装

### 登録手順

**Step 1: Partner Centerアカウントの作成**
- https://partner.microsoft.com/dashboard/account/v3/enrollment/introduction/office にアクセス
- 会社アカウントを作成（承認プロセスあり）
- 必要に応じて支払い情報を追加

**Step 2: オファーの作成**
- Partner Center > Marketplace Offers > Overview から新規オファーを作成
- アプリの種類を選択（Office Add-in、Teams App、Power BI Visual等）

**Step 3: アプリ情報の入力**
- アプリ名、説明、スクリーンショット等のリスティング情報を入力
- テストノートに詳細な情報を記載（サンプルデータ、設定手順、テストアカウント等）

**Step 4: 審査に提出**
- 全情報入力後、Partner Centerから提出

### 必要素材

| 素材 | 仕様 | 必須/任意 |
|------|------|----------|
| **アプリ名** | 明確でわかりやすい名前 | 必須 |
| **説明文** | 正確なスペル・大文字・句読点・文法 | 必須 |
| **スクリーンショット** | アプリの機能を示す画像 | 必須 |
| **テストノート** | サンプルデータ、設定手順、テスト/デモアカウント | 推奨 |
| **プライバシーポリシー** | プライバシーポリシーURL | 必須 |
| **サポートドキュメント** | サポート文書URL | 必須 |
| **ローカライズ対応** | 多言語対応する場合はマニフェスト・サービスの更新 | 任意 |

### 審査プロセス
1. 自動チェック（認証ポリシー準拠確認）
2. バリデーションチーム手動レビュー（3〜5営業日）
3. 承認 or フィードバック（修正依頼）
4. 承認後、約1時間でMicrosoft Marketplaceに表示

### 審査通過後のオプション
- **Microsoft 365 App Compliance Program**（任意）: Publisher Attestation等によるセキュリティ信頼性向上

### 参考URL
- 提出ガイド: https://learn.microsoft.com/en-us/partner-center/marketplace/submit-to-appsource-via-partner-center
- 認証ポリシー: https://learn.microsoft.com/en-us/legal/marketplace/certification-policies
- アカウント開設: https://learn.microsoft.com/en-us/partner-center/marketplace/open-a-developer-account

---

## 3. Slack Marketplace

### 概要
- **URL**: https://slack.com/marketplace
- **開発者ページ**: https://api.slack.com/
- **費用**: 無料
- **審査期間**: 合計 数週間〜3ヶ月（予備審査最大10営業日 + 機能審査最大10週間）

### 前提条件
- Slack APIでアプリを構築済み
- OAuth 2.0認証の実装（SSL必須）
- **5つ以上のアクティブなワークスペースにインストール済み**（過去28日以内に使用）
- 完全に機能するプロダクション品質のアプリ
- アプリの保守・サポート体制が整っていること

### 登録手順

**Step 1: Slackアプリの作成・配布設定**
- https://api.slack.com/apps でアプリを作成
- 配布（Distribution）を有効化
- Unlisted Distributionでまず配布テスト

**Step 2: ガイドライン確認**
- https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements/ を熟読
- 最小権限のスコープ設計
- Enterprise Grid対応（Org App）の検討
- App Homeの構築（オンボーディング情報等）

**Step 3: テスト・フィードバック収集**
- ベータグループを組成して実環境テスト
- インストール→設定→機能利用→アンインストールの全フロー確認
- 開発ワークスペース以外での動作確認必須

**Step 4: Marketplace提出**
- アプリ設定ページの「Submit to the Slack Marketplace」セクションから提出
- 自動テストを通過後、手動提出

### 必要素材

| 素材 | 仕様 | 必須/任意 |
|------|------|----------|
| **アプリリスティング情報** | 名前、説明、カテゴリ等 | 必須 |
| **スコープ一覧と説明** | 各スコープの利用理由 | 必須 |
| **テストアカウント** | サービスへのログイン情報（有料の場合も含む） | 必須 |
| **デモ動画** | インストール・OAuth・セットアップ・機能・アンインストールの全フロー | 強く推奨 |
| **補足情報** | アプリの使い方やテスト手順 | 推奨 |

### 審査プロセス（2段階）

**予備審査（最大10営業日）:**
- リスティング情報、ドキュメント、リンクの確認
- スコープの理由確認
- インストール・OAuthの動作確認
- フィードバック→再提出するとキュー位置リセット

**機能審査（新規: 最大10週間、更新: 最大6週間）:**
- レビュアーが割り当てられ、機能・スコープの詳細テスト
- バグや問題のフィードバック
- 再提出してもキュー位置はリセットされない
- 承認後、任意のタイミングで公開可能

### 注意事項
- coded workflowsはMarketplace掲載不可
- `identity.*`, `admin.*`, `search:read` 等のスコープは使用不可
- 公開後はアプリ設定がロックされ、変更には再審査が必要
- 更新時はステージングアプリの作成を推奨

### 参考URL
- レビューガイド: https://docs.slack.dev/slack-marketplace/slack-marketplace-review-guide/
- ガイドライン: https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements/
- 配布ガイド: https://api.slack.com/start/distributing

---

## 4. Notion Integration Gallery (Marketplace)

### 概要
- **URL**: https://www.notion.so/integrations/all
- **開発者ページ**: https://developers.notion.com/
- **費用**: 無料
- **審査期間**: 5〜10営業日（初回フィードバック）

### 前提条件
- Public Integrationとして作成済み（Internal Integrationは掲載不可）
- Installation scopeが「Any workspace」に設定（作成時に設定、後から変更不可）
- OAuth 2.0フローの実装完了

### 登録手順

**Step 1: Public Integrationの作成**
- https://www.notion.so/profile/integrations でインテグレーションを作成
- タイプを「Public」、スコープを「Any workspace」に設定
- OAuth認可フローを実装

**Step 2: Creator Dashboardでリスティング作成**
- Notion Creator Dashboard > Listings > Integrations に移動
- 新規リスティングを作成

**Step 3: リスティング情報の入力**
- アプリ名、説明、アイコン、スクリーンショット等を入力
- セキュリティ・プライバシー情報の記載

**Step 4: 審査に提出**
- リスティングページから「Submit」をクリック
- Submittedセクションでステータス追跡可能

### 必要素材

| 素材 | 仕様 | 必須/任意 |
|------|------|----------|
| **アプリ名** | わかりやすい名称 | 必須 |
| **説明文** | インテグレーションの機能説明 | 必須 |
| **アイコン** | アプリアイコン | 必須 |
| **スクリーンショット** | 機能を示す画像 | 必須 |
| **セキュリティ・プライバシー情報** | データ取り扱いに関する情報 | 必須 |

### 審査プロセス
- Notionチームによるレビュー（5〜10営業日で初回フィードバック）
- 承認された場合 → Notion Marketplaceに掲載
- 修正が必要な場合 → フィードバックに対応して再提出
- 不承認理由: ブランド/商標問題、品質基準未達、基本要件未満等

### 補足
- Marketplace掲載は任意。掲載なしでもOAuthフローでインテグレーション利用可能
- Technology Partner Program (https://www.notion.com/lp/technology-partner-program) 参加で有利

### 参考URL
- 掲載ガイド: https://developers.notion.com/guides/get-started/publishing-integrations-to-notions-integration-gallery
- ベストプラクティス: https://www.notion.so/notiondevs/Notion-Integration-Gallery-Best-Practices-997825927fd6473e89617ce0c329145c

---

## 5. Chatwork（マーケットプレイスなし / API連携のみ）

### 概要
- **連携サービス紹介ページ**: https://go.chatwork.com/ja/integrate/
- **開発者ページ**: https://developer.chatwork.com/
- **マーケットプレイス**: **なし**（公開アプリストアは存在しない）
- **費用**: 無料（API利用自体は無料）

### 前提条件
- Chatworkアカウント（ビジネスプラン以上推奨）
- 組織管理者へのAPI利用申請（パーソナルプランを除く）
- API利用規約への同意

### API連携セットアップ手順

#### 方法A: APIトークン認証（シンプル）

**Step 1: API利用申請**
- https://www.chatwork.com/service/packages/chatwork/subpackages/api/request.php からAPI利用を申請
- 組織管理者の承認が必要（パーソナルプラン除く）

**Step 2: APIトークンの取得**
- Chatwork画面右上「利用者名」> 「サービス連携」> 「APIトークン」
- APIトークンをコピー

**Step 3: API利用開始**
- リクエストヘッダーに `X-ChatWorkToken: [APIトークン]` を設定してAPIコール

#### 方法B: OAuth 2.0認証（サードパーティアプリ向け・推奨）

**Step 1: OAuthクライアントの登録**
- https://www.chatwork.com/service/packages/chatwork/subpackages/oauth/client_create.php にアクセス
- 以下の情報を登録:

| 項目 | 必須 | 説明 |
|------|------|------|
| クライアント名 | 必須 | アプリの名前 |
| クライアントタイプ | 必須 | コンフィデンシャル（サーバーアプリ）/ パブリック（フロントエンドアプリ） |
| リダイレクトURI | 必須 | 最大5つ。コンフィデンシャルは `https://` のみ |
| スコープ | 必須 | 最低1つ選択 |

**Step 2: 認可フロー実装（Authorization Code Grant）**
- コンセント画面URL: `https://www.chatwork.com/packages/oauth2/login.php`
- 必須パラメータ: `response_type=code`, `client_id`, `scope`
- PKCE対応推奨（パブリッククライアントは必須）

**Step 3: トークン取得**
- トークンエンドポイント: `https://oauth.chatwork.com/token`
- アクセストークン有効期限: 30分
- リフレッシュトークン有効期限: 14日（`offline_access`スコープで無期限）

**Step 4: APIコール**
- `authorization: Bearer [access_token]` ヘッダーでAPIにアクセス
- APIベースURL: `https://api.chatwork.com/v2/`

### 利用可能なスコープ
- `rooms.all:read_write` — ルーム操作
- `contacts.all:read_write` — コンタクト操作
- `users.profile.me:read` — 自分のプロフィール読み取り
- `offline_access` — 永続的アクセス（コンフィデンシャルのみ）

### 注意事項
- 連携サービス紹介ページへの掲載は自動登録の仕組みなし（Chatwork側の裁量）
- IFTTT / Zapier経由の連携も選択肢
- レートリミットあり（`X-RateLimit-*` ヘッダーで確認）
- SAML認証はOAuth専用ログイン画面で非対応

### 参考URL
- APIドキュメント: https://developer.chatwork.com/
- OAuth仕様: https://developer.chatwork.com/docs/oauth
- API利用規約: https://go.chatwork.com/ja/terms/api.html

---

## 6. LINE WORKS App Directory

### 概要
- **URL**: https://line-works.com/appdirectory/
- **開発者ページ**: https://developers.worksmobile.com/jp/
- **マーケットプレイス**: あり（アプリディレクトリ）ただし**招待/審査制**
- **費用**: 不明（パートナー契約による可能性）
- **審査期間**: 不明（パートナーシップ交渉含む、数ヶ月と推定）

### 前提条件
- LINE WORKS Developer Consoleでのアプリ開発実績
- LINE WORKSパートナープログラムへの参加（ソリューションパートナー）
- OAuth 2.0 (API 2.0対応) の実装

### 掲載手順

**Step 1: LINE WORKS Developer Consoleでアプリ開発**
- https://developers.worksmobile.com/jp/ にアクセス
- Developer Consoleでアプリを作成
- OAuth 2.0認証またはService Account認証を実装
- チャットボット、ミニアプリ等の連携機能を開発

**Step 2: パートナープログラムへの参加申請**
- https://line-works.com/partner/partner-program/ からお問い合わせ
- 「サービスパートナープログラム」の「ソリューション」カテゴリが対象
- 連携アプリ、連携ソリューション、関連サービスを提供する企業向け

**Step 3: パートナーランクの取得**
- **Registered**: 連携アプリ提供準備中のパートナー
- **Certified**: 連携アプリ提供実績が認定されたパートナー
- Certifiedになることでアプリディレクトリへの掲載が可能

**Step 4: LINE WORKSとの審査・動作確認**
- LINE WORKS側が審査・動作確認を実施
- 「LINE WORKS公認アプリ」として認定
- アプリディレクトリに掲載

### パートナープログラム構成
| カテゴリ | 対象 |
|---------|------|
| セールス&サポートパートナー | LINE WORKSの販売を行うパートナー（Platinum/Gold/Silver/Registered） |
| サービスパートナー | 業務/ITコンサルテーション、インテグレーション、トレーニング、運用/マネージドサービス、ソリューション |

### 注意事項
- セルフサーブ型の登録フォームは存在しない
- 掲載希望の場合はLINE WORKSの担当部署への直接問い合わせが必要
- 現在100種類以上の連携ソリューションが掲載中

### 参考URL
- アプリディレクトリ: https://line-works.com/appdirectory/
- パートナープログラム: https://line-works.com/partner/partner-program/
- Developer Console: https://developers.worksmobile.com/jp/

---

## 7. Dropbox App Center

### 概要
- **URL**: https://www.dropbox.com/apps
- **開発者ページ**: https://www.dropbox.com/developers
- **マーケットプレイス**: あり（App Center）ただし**パートナー選定制**
- **費用**: 無料（パートナー契約が必要な場合あり）
- **審査期間**: Production Status取得: 数週間。App Center掲載: パートナーシップ交渉が必要（数ヶ月と推定）

### 前提条件
- Dropbox App Consoleでのアプリ作成
- OAuth 2.0 (Scoped Access方式) の実装
- **50ユーザー以上のリンク**（Production Status申請の最低条件）

### 掲載手順（2段階プロセス）

#### Stage 1: Production Statusの取得

**Step 1: アプリの作成**
- https://www.dropbox.com/developers/apps でApp Consoleにアクセス
- 新規アプリを作成、OAuth 2.0認証を設定
- 必要なスコープ（Scoped Access）を設定

**Step 2: 開発・テスト**
- Dropbox APIを利用してアプリを開発
- Developer Guideに沿って実装: https://www.dropbox.com/developers/reference/developer-guide
- ブランディングガイドライン・利用規約への準拠を確認

**Step 3: ユーザー獲得**
- 50ユーザー以上がアプリをリンク（Dropboxアカウントと連携）するまで配布

**Step 4: Production Status申請**
- 50ユーザー到達後、App Consoleからレビュー申請
- Dropboxがアプリをレビュー

#### Stage 2: App Center掲載（招待制）

**Step 5: Technology Partnerへの申請**
- https://www.dropbox.com/business/partners からパートナープログラムに申請
- Dropboxが選定したテクノロジーパートナーのみApp Centerに掲載
- 自動掲載の仕組みはなし

**Step 6: パートナーシップ交渉**
- 専任パートナーマネージャーが割り当て
- トレーニングリソース、技術ドキュメント、製品アップデートへのアクセス
- レベニューシェア、マーケティング開発資金等のインセンティブ

### 注意事項
- App Center掲載はProduction Status取得とは別プロセス
- 現在は招待制で、カテゴリ・適格要件の拡大を検討中
- Production Statusなしでも最大50ユーザーまでは配布可能

### 参考URL
- Developer Guide: https://www.dropbox.com/developers/reference/developer-guide
- App Console: https://www.dropbox.com/developers/apps
- パートナープログラム: https://www.dropbox.com/business/partners

---

## 8. Zoom App Marketplace

### 概要
- **URL**: https://marketplace.zoom.us/
- **開発者ページ**: https://developers.zoom.us/
- **費用**: 無料
- **審査期間**: 初回レスポンスSLA 72時間以内（平日PT 9-17時）。全体で4週間以上（FIFO方式）

### 前提条件
- Zoom管理者アカウント
- OAuth 2.0認証の実装
- 本番環境が稼働中
- テストアカウント（ダミーデータ入り）の準備

### 登録手順

**Step 1: アプリの作成**
- https://marketplace.zoom.us にログイン（管理者アカウント）
- Developドロップダウン > Build App をクリック
- アプリタイプを選択して作成
- Distributionオプションを「ON」に切り替え

**Step 2: OAuth認証の設定**
- OAuth 2.0認証情報の設定
- 必要なスコープの選択（最小権限の原則）
- リダイレクトURL等の設定
- アクセストークンのキャッシュ・リフレッシュトークンフローの実装

**Step 3: 機能開発・テスト**
- Zoom SDKまたはWebhookを使用して機能実装
- デアオーソリゼーションURL（Webhook処理用）の実装必須
- 全機能のend-to-endテスト

**Step 4: ドキュメントの準備**

| ドキュメント | 内容 | 必須 |
|-------------|------|------|
| **テストプラン** | 各スコープの設定・利用手順をステップバイステップで記載。リリースノートにリンクを追加 | 必須 |
| **Technical Design Document (TDD)** | 詳細なセキュリティドキュメント。marketplace.security@zoom.us に送付 | 必須 |
| **サポート/ドキュメントURL** | 整理されたヘルプリソース | 必須 |

**Step 5: アプリメタデータの入力**

| 項目 | 説明 |
|------|------|
| **Short Description** | 1〜2文でコアビジネス目的を説明 |
| **Long Description** | ビジネス価値、主要ユースケース、機能、前提条件、価格/サポートリンクを詳述 |
| **画像** | アプリの視覚的アセット |
| **リソースURL** | 関連リソースへのリンク |
| **Webhookイベントサブスクリプション** | 使用するWebhookイベント |
| **スコープ使用説明** | 各スコープの利用理由 |

**Step 6: 審査提出**
- アプリ設定から審査リクエストを提出
- 提出タイプ: CREATE（新規）、UPDATE（更新）、UNPUBLISH（非公開）、REMOVE（削除）

### 審査プロセス
1. **メタデータレビュー**: Short/Long Description、画像、URL、Webhookイベント、スコープ使用説明
2. **セキュリティレビュー**: TDDに基づくセキュリティ審査
3. **機能・UXテスト**: インストール→設定→機能利用→デアオーソリゼーションの全フロー

### よくあるリジェクト理由（TOP10）
1. テストプラン・テストアカウントの未提供
2. ドキュメントURLの内容不十分
3. デアオーソリゼーションURLが動作しない
4. ロングポーリングをWebhookの代わりに使用
5. 未使用・過剰なAPIスコープの設定
6. アクセストークンの非キャッシュ・リフレッシュトークン未使用
7. アプリ説明が不完全・情報不足
8. インストール体験の不具合
9. 説明と実機能の不一致
10. TDD（Technical Design Document）の未提出

### 参考URL
- 配布ガイド: https://developers.zoom.us/docs/distribute/
- 審査プロセス: https://developers.zoom.us/docs/distribute/app-review-process/
- Build Flow: https://developers.zoom.us/docs/build-flow/

---

## 9. kintone（サイボウズ CyPN プロセス）

### 概要
- **連携サービス一覧**: https://kintone-sol.cybozu.co.jp/integrate/
- **開発者サイト**: https://cybozu.dev/ja/
- **パートナーネットワーク**: https://partner.cybozu.co.jp/
- **費用**: 開発者ライセンス無料。オフィシャルパートナー年会費 10万円（税抜）
- **審査期間**: 非公開（エントリーシート提出→面談→認定の流れで数ヶ月と推定）

### 前提条件
- kintone開発者ライセンス（無料、1年間有効）
- kintone連携サービスの開発完了
- 導入実績2件以上（自社利用除く）
- セキュアコーディングガイドライン遵守

### 掲載手順（プロダクトパートナー認定プロセス）

**Step 1: kintone開発者ライセンスの取得**
- https://kintone.dev/en/developer-license-registration-form/ から申請
- 1年間無料で利用可能
- API開発・テストに使用

**Step 2: 連携サービスの開発**
- cybozu developer network (https://cybozu.dev/ja/) で公開されているAPIのみ使用
- セキュアコーディングガイドライン遵守: https://cybozu.dev/ja/kintone/docs/guideline/secure-coding-guideline/
- DOM操作を利用する場合は先行動作環境で動作確認

**Step 3: 連携サービス認定基準の充足**

| 基準カテゴリ | 主要要件 |
|-------------|---------|
| **製品機能** | 標準機能にない付加価値。公開APIのみ使用。セキュアコーディング遵守 |
| **データ取り扱い** | 外部送信・保存する場合は理由を公開 |
| **顧客対応** | 問い合わせ窓口あり。セキュリティ事故時の速やかな報告義務 |
| **販売** | 導入実績2件以上（自社除く）。価格明示。購入可能な商品単位 |
| **サービス名** | ユーザーに誤解を与えない。既存認定サービスと重複しない |

**Step 4: レジスタード登録**
- https://partner.cybozu.co.jp/join/system/ からレジスタード（パートナー候補企業）に登録
- Registered Portalの利用が可能に
- 法人格をもつ企業のみ（個人事業主不可）

**Step 5: オフィシャルパートナー認定申請**
- 認定条件の充足:
  1. レジスタード登録完了
  2. 実績2件以上
  3. 連携サービス認定基準を満たすプロダクト（プロダクトパートナーの場合）
- エントリーシートの提出
- 担当者面談 → 責任者面談
- 顧客実績、横展開可能なサービス、ビジネス持続可能性をすり合わせ

**Step 6: 認定・年会費支払い**
- 規約に同意しオフィシャルパートナーとして認定
- 年会費10万円（税抜）を支払い
- 各種支援・プロモーションの利用開始

**Step 7: 連携サービス一覧への掲載**
- kintone連携サービスとして公式サイトに掲載
- CyPN Report（パートナー評価制度）での星評価対象に

### ロゴ・商標ルール
- サイボウズ製品ロゴの使用は二次利用ページ確認: https://cybozu.co.jp/logotypes/
- 製品ガイドライン: https://cybozu.co.jp/logotypes/assets/kintone/kintone-visual-identity-guide.pdf

### 認定後の継続条件
- 窓口担当者の配置
- 活動報告の提出（更新時）
- 年会費10万円（税抜）

### 参考URL
- 連携サービス認定基準: https://kintone-sol.cybozu.co.jp/integrate/guidelines.html
- パートナー制度: https://partner.cybozu.co.jp/join/system/
- 開発者ライセンス: https://kintone.dev/en/developer-license-registration-form/

---

## 10. Box App Center

### 概要
- **URL**: https://cloud.app.box.com/integrations
- **開発者コンソール**: https://app.box.com/developers/console
- **費用**: 無料
- **審査期間**: 非公開（integrate@box.com に問い合わせ）

### 前提条件
- Box開発者アカウント（無料）
- **OAuth 2.0認証必須**（App Center掲載にはOAuth 2.0が必要）
  - 他の認証方式を使用している場合でも、マーケティング用リスティングとしてOAuth 2.0アプリを別途作成可

### 登録手順

**Step 1: Box開発者アカウント・アプリ作成**
- https://app.box.com/developers/console にアクセス
- Dev Consoleで新規アプリを作成
- 認証方式にOAuth 2.0を選択
- 必要なスコープを設定

**Step 2: アプリの開発・テスト**
- Box APIを利用して連携機能を開発
- 全機能のテスト完了

**Step 3: 提出チェックリストの確認**
- Dev Console > 対象アプリ > **Publishing** タブを開く
- 提出チェックリストを確認し、全要件を満たしていることを確認
- 確認チェックボックスにチェック

**Step 4: マーケティング情報の入力**

| 項目 | 説明 |
|------|------|
| **General Info** | カテゴリ、対応プラットフォームの選択 |
| **Short Description** | アプリ名の横に表示される短い説明 |
| **Long Description** | アプリ詳細ページに表示。クリック可能なリンクも追加可 |
| **Screenshots** | アプリの見た目・Box連携を示すスクリーンショット |
| **Icon** | アプリアイコン（一覧表示用） |
| **Support Resources** | サポートリンク・補足情報 |

**Step 5: プレビュー・提出**
- プレビューで表示内容を確認
- 問題なければ提出（Submit for approval）

**Step 6: Boxチームレビュー**
- Boxチームがアプリをレビュー
- 承認後、Integrations（App Center）に掲載

### 問い合わせ先
- 質問・問題がある場合: integrate@box.com

### 参考URL
- アプリ公開ガイド: https://developer.box.com/guides/getting-started/publish-app
- 開発者ドキュメント: https://developer.box.com/guides

---

## 11. SmartHR Plus

### 概要
- **URL**: https://www.smarthr.plus/
- **開発者サイト**: https://developer.smarthr.jp/
- **パートナープログラム**: https://www.smarthr.plus/partner
- **費用**: API利用は無料。パートナープログラム参加費は非公開（要問い合わせ）
- **審査期間**: 非公開（5ステッププロセス全体で数ヶ月が目安）

### 前提条件
- SmartHR Plusパートナープログラムへの参画
- SmartHR APIの利用（OAuth 2.0またはAPIトークン）
- 連携開発用のSmartHR環境

### 掲載手順（5ステッププロセス）

**Step 1: 連携要件のすり合わせ**
- SmartHR Plusパートナープログラムに問い合わせ: https://www.smarthr.plus/partner
- SmartHRと連携要件について協議
- ユーザーニーズの共有を受ける

**Step 2: 連携仕様のすり合わせ**
- SmartHR APIの仕様案内を受ける
- OAuth連携仕様の確認
- 開発環境支援、デザインシステム共有
- 連携開発ドキュメントの提供:
  - 開発用SmartHR環境の取得方法
  - SmartHRとのOAuth連携の仕様
  - ユーザーニーズにあった連携開発のポイント
  - FAQ

**Step 3: 貴社にて開発**
- SmartHR APIを利用した連携機能の開発
- サンドボックス環境でのテスト: https://developer.smarthr.jp/api/about_sandbox
- SmartHRからの開発支援・レビューを活用

**Step 4: 連携機能の審査**
- SmartHRによる連携機能の審査
- 品質基準の確認

**Step 5: リリース**
- SmartHR Plusアプリストアに掲載
- プレスリリース配信（SmartHRが対応）
- SmartHR管理画面TOP、メルマガ、オンラインセミナーで告知

### SmartHR Plusの掲載メリット
- 登録社数70,000社以上のSmartHRユーザーへのリーチ
- アプリストア掲載によるプロモーション
- SmartHR管理画面上での告知
- プレスリリース配信
- メルマガでの紹介
- オンラインセミナーでの紹介

### API情報
- SmartHR API: https://developer.smarthr.jp/api
- サンドボックス: https://developer.smarthr.jp/api/about_sandbox
- 認証方式: OAuth 2.0 + APIトークン

### 参考URL
- パートナープログラム: https://www.smarthr.plus/partner
- SmartHR API: https://developer.smarthr.jp/api

---

## 12. freee アプリストア（会計）

### 概要
- **URL**: https://www.freee.co.jp/appstore/
- **開発者ページ**: https://app.secure.freee.co.jp/developers
- **費用**: 無料（開発者登録・API利用ともに無料）
- **審査期間**: 約1〜2週間

### 前提条件
- freeeアカウント（**テスト用事業所・デモ事業所では公開アプリ作成不可**）
- パブリックタイプでアプリを作成（後から変更不可）
- OAuth 2.0 (Authorization Code Grant) の実装

### 登録手順

**Step 1: アプリの作成**
- https://app.secure.freee.co.jp/developers にアクセス
- 「アプリ管理」から新規アプリを作成
- **タイプを「パブリック」に設定**（後から変更不可！）

**Step 2: 基本情報の設定**
- アプリ名: アプリストア・認可画面に反映。「for freee」「by freee」等の使用不可
- アプリ概要: 80文字程度推奨
- コールバックURL: 認可完了後の遷移先URL

**Step 3: 権限設定**
- 「権限設定」タブでAPIとメソッドを選択
- 連携機能に必要な最小限の権限のみを設定

**Step 4: 公開設定（リスティング情報入力）**

| 項目 | 仕様 | 必須 |
|------|------|------|
| **アイコン** | 640px x 640px、jpeg/png/gif | 必須 |
| **アプリ説明文** | テキスト。推奨内容: 対象ユーザー、解決する課題、アプリの特徴 | 必須 |
| **説明画像** | 1200px x 630px、jpeg/png/gif、1〜5枚、5MB以下/枚 | 必須 |
| **ハイライトコンテンツ** | タイトル+説明文+画像を3セットまで | 任意 |
| **動画** | YouTube掲載済み動画。スライド形式で公開 | 任意 |
| **連携ページURL** | freee連携認可画面へのリンクがあるページ | 必須 |
| **ヘルプページURL** | 連携方法・操作方法・解除方法の記載必須 | 必須 |
| **開発者名** | 開発者/企業名 | 必須 |
| **開発者URL** | コーポレートページ or 会社概要ページ | 必須 |
| **問い合わせメールアドレス** | サポート連絡先 | 必須 |
| **事業者正式名称** | 審査用（非公開） | 必須 |
| **代表者名** | 審査用（非公開） | 必須 |
| **審査用デモアカウント** | ID/パスワード（不要な場合は「不要」と記入） | 必須 |
| **カテゴリ** | 適切なカテゴリを選択 | 必須 |

**Step 5: Webhook設定（任意）**
- 利用する場合のみ有効化
- WebhookURL設定、通知条件の選択

**Step 6: 公開申請**
- 「公開設定」タブ > 右上「公開申請」をクリック
- ポップアップで「公開申請」を再度クリック

**Step 7: 審査・公開**
- 約1週間以内に審査結果をメールで通知
- 必要に応じてオンラインデモンストレーションを依頼される場合あり
- 修正が必要な場合はフィードバックに対応し再審査申請
- 公開後の更新も再審査が必要

### 審査時の注意事項
- ヘルプページの記載不十分が最も多いリジェクト理由
- 事業所選択機能の実装が必須（1アカウントで複数事業所利用するケースが多い）
- 権限は最小限に
- プラン限定アプリ制度あり（高度な機能はアドバンスプラン以上のみ）

### 参考URL
- アプリ公開手順: https://developer.freee.co.jp/startguide/deploy-app
- アプリ審査プロセス: https://developer.freee.co.jp/reference/app-review-process
- ガイドライン: https://app.secure.freee.co.jp/developers/guidelines/

---

## 13. freee（人事労務）

### 概要
freee人事労務のアプリ連携は、freee会計と同じ**freeeアプリストア**に統合されている。基本的な手順・プロセスは上記「12. freee アプリストア」と同一。

### 会計との違い

| 項目 | freee会計 | freee人事労務 |
|------|----------|-------------|
| **アプリストア** | 共通（https://www.freee.co.jp/appstore/） | 共通 |
| **APIエンドポイント** | 会計API | 人事労務API（別エンドポイント） |
| **権限スコープ** | 会計関連スコープ | 人事労務関連スコープ（勤怠、給与、従業員情報等） |
| **プラン限定** | アドバンス/エンタープライズ限定機能あり | Webhook利用はプラン限定 |
| **審査プロセス** | 同一 | 同一 |
| **開発者ページ** | 同一 | 同一 |

### 人事労務固有のポイント
- 人事労務APIのスコープは会計とは別
- 勤怠入力、給与明細、従業員情報等のデータにアクセス
- Webhook利用（freee側の操作をトリガーに即時連動）はプラン限定アプリに該当する可能性
- アプリストアの「人事労務」カテゴリから検索可能: https://app.secure.freee.co.jp/applications/search?app_tag_id=1

### API情報
- 開発者サイト: https://developer.freee.co.jp/
- 人事労務APIリファレンス: https://developer.freee.co.jp/docs/hr

---

## 14. マネーフォワード クラウド（Money Forward）

### 概要
- **開発者サイト**: https://developers.biz.moneyforward.com/
- **マーケットプレイス**: **なし**（公開アプリストアは存在しない）
- **費用**: アプリポータルの登録・利用は無料
- **審査**: マーケットプレイスがないため公開審査プロセスなし

### 前提条件
- マネーフォワード クラウドのアカウント
- 「アプリポータル」の利用（必須）

### API連携セットアップ手順

**Step 1: アプリポータルでアプリを登録**
- マネーフォワード クラウドにログイン
- 「API連携（開発者向け）」画面 > 「APIの利用を開始する」
- アプリポータルに切り替わり、新規アプリケーションを作成
- 必要情報:
  - アプリ名称
  - リダイレクトURI
  - クライアント認証方式

**Step 2: 認証情報の取得**
- アプリ作成完了後、以下が発行される:
  - ClientID
  - ClientSecret
- これらを使ってOAuth 2.0認可フローを実装

**Step 3: 認証方式の選択・実装**

| 方式 | 用途 |
|------|------|
| **OAuth 2.0** | ユーザー認可が必要な場面。Authorization Code Grantフロー |
| **APIキー** | サーバー間通信。`/auth/exchange` でJWTを取得 |

**Step 4: アクセストークン取得・API呼び出し**
- OAuth 2.0の場合: 認可コード取得 → トークン交換 → APIコール
- APIキーの場合: APIキーでJWT取得 → APIコール
- APIリファレンス: https://developers.biz.moneyforward.com/docs/api

### 対応プロダクト
- マネーフォワード クラウド会計
- マネーフォワード クラウド請求書
- マネーフォワード クラウド経費
- マネーフォワード クラウド給与
- その他マネーフォワード クラウド各種

### マーケットプレイス非存在に関する補足
- 連携サービスカタログ (https://accounting.moneyforward.com/service_catalog) には一部パートナーサービスが掲載
- ただし自己申請型のマーケットプレイスではない
- パートナープログラムは販売代理店向け (https://biz.moneyforward.com/resellers/)
- 掲載希望の場合はマネーフォワードへの直接問い合わせが必要

### 参考URL
- 開発者サイト: https://developers.biz.moneyforward.com/
- API入門: https://developers.biz.moneyforward.com/docs/common/getting-started-moneyforward-cloud-apis/
- チュートリアル: https://developers.biz.moneyforward.com/docs/tutorials
- APIリファレンス: https://developers.biz.moneyforward.com/docs/api

---

## 総合比較・優先度マトリクス

### 掲載しやすさ順（Kawaru掲載推奨優先度）

| 優先度 | サービス | 登録方式 | 審査期間 | 費用 | 難易度 |
|:------:|---------|---------|---------|------|:------:|
| 1 | **freee** | セルフサーブ | 1〜2週間 | 無料 | 低 |
| 2 | **Microsoft AppSource** | セルフサーブ | 3〜5営業日 | 無料 | 低〜中 |
| 3 | **Notion** | セルフサーブ | 5〜10営業日 | 無料 | 低〜中 |
| 4 | **Box** | セルフサーブ | 非公開 | 無料 | 中 |
| 5 | **Google Workspace** | セルフサーブ | 数日〜数週間+OAuth検証 | 無料 | 中 |
| 6 | **Zoom** | セルフサーブ | 4週間+ | 無料 | 中〜高 |
| 7 | **Slack** | セルフサーブ | 数週間〜3ヶ月 | 無料 | 高 |
| 8 | **SmartHR Plus** | パートナー契約 | 数ヶ月 | 要問い合わせ | 高 |
| 9 | **kintone** | パートナー認定 | 数ヶ月 | 年会費10万円 | 高 |
| 10 | **LINE WORKS** | 招待/審査制 | 不明 | 不明 | 高 |
| 11 | **Dropbox** | パートナー選定制 | 不明 | 不明 | 高 |
| - | **Chatwork** | MPなし（API連携のみ） | N/A | 無料 | 低（API連携のみ） |
| - | **マネーフォワード** | MPなし（API連携のみ） | N/A | 無料 | 低（API連携のみ） |

### 全サービス共通で必要な素材チェックリスト

- [ ] アプリアイコン（各サービスごとにサイズ要件が異なる）
- [ ] スクリーンショット（サービスごとに枚数・サイズ要件あり）
- [ ] アプリ名（短く明確に。各プラットフォームの商標に抵触しないこと）
- [ ] 短い説明文（1〜2文）
- [ ] 詳細説明文
- [ ] プライバシーポリシーURL
- [ ] 利用規約URL
- [ ] サポートページURL
- [ ] ヘルプ/ドキュメントページURL（連携方法・操作方法・解除方法）
- [ ] テストアカウント（審査チーム用）
- [ ] デモ動画（強く推奨されるサービスが多い）
- [ ] OAuth 2.0認証フローの実装
- [ ] 開発者/企業情報（正式名称、代表者名、連絡先）
