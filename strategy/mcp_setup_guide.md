# MCP外部ツール連携 セットアップガイド

最終更新: 2026-03-03

## 現在のステータス

| サービス | 登録状況 | 認証方式 | 残作業 |
|---------|---------|--------|--------|
| Notion | ✅ 登録済み | OAuthリモートMCP | 初回使用時にブラウザ認証 |
| Zoom | ✅ 登録済み | OAuthブラウザフロー | 初回使用時にブラウザ認証 |
| Google Drive | ✅ 登録済み | OAuth2ファイル方式 | Googleキー取得→auth実行 |
| Google Calendar | ✅ 登録済み | OAuth2ファイル方式 | Googleキー取得→auth実行 |
| Slack | ✅ 登録済み | Bot Token | setup_slack.sh実行 |

設定ファイル: `~/.claude.json`（mcpServers セクション）

---

## 残作業A: Google認証（Drive / Docs / Sheets / Slides / Calendar）

### 手順

1. **Google Cloud Consoleでプロジェクト作成**
   - https://console.cloud.google.com/ にアクセス
   - 新しいプロジェクトを作成（例: `claude-mcp`）

2. **必要なAPIを有効化**（左メニュー「APIとサービス」→「ライブラリ」）
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API
   - Google Calendar API

3. **OAuth同意画面を設定**
   - 「APIとサービス」→「OAuth同意画面」
   - ユーザーの種類: 外部
   - アプリ名・メールを入力
   - スコープは後で追加でもOK
   - テストユーザーに自分のGmailを追加

4. **OAuthクライアントIDを作成**
   - 「認証情報」→「認証情報を作成」→「OAuthクライアントID」
   - アプリの種類: **デスクトップアプリ**
   - 作成後、「JSONをダウンロード」

5. **JSONファイルを配置**
   ```bash
   mv ~/Downloads/client_secret_*.json ~/.config/claude-mcp/gcp-oauth.keys.json
   ```

6. **認証スクリプトを実行**
   ```bash
   bash ~/.config/claude-mcp/setup_google_auth.sh
   ```
   ブラウザが開くのでGoogleアカウントでログインして許可。

---

## 残作業B: Slack Bot Token取得

1. https://api.slack.com/apps → 「Create New App」→「From scratch」
2. アプリ名を入力（例: `Claude MCP`）、ワークスペースを選択
3. 「OAuth & Permissions」→「Bot Token Scopes」に追加:
   ```
   channels:read
   channels:history
   chat:write
   files:read
   users:read
   groups:read
   groups:history
   ```
4. 「Install to Workspace」でインストール
5. **Bot User OAuth Token**（`xoxb-...`）をコピー
6. Team IDは SlackのブラウザURLから確認: `https://app.slack.com/client/TXXXXXXXX/`
7. セットアップスクリプト実行:
   ```bash
   bash ~/.config/claude-mcp/setup_slack.sh
   ```

---

## 残作業C: Notion（初回使用時）

Claudeで最初にNotionの操作をリクエストすると自動的にブラウザが開いてOAuth認証が行われます。
事前の設定は不要です。

---

## 残作業D: Zoom（初回使用時）

Claudeで最初にZoomの操作をリクエストすると自動的にブラウザが開いてOAuth認証が行われます。
事前の設定は不要です。

---

## 認証完了後の確認

Claude Codeを再起動して以下を実行:
```
/mcp
```
各サーバーが `connected` 状態であることを確認する。

---

## ファイル構成

```
~/.config/claude-mcp/
├── setup_google_auth.sh      # Google認証スクリプト
├── setup_slack.sh            # Slack設定スクリプト
├── gcp-oauth.keys.json       # ← ここに配置（未作成）
├── gdrive-credentials.json   # 認証後に自動生成
└── gcal-credentials.json     # 認証後に自動生成（Calendarのみ）

~/.claude.json                # MCPサーバー設定（登録済み）
```

---

## トラブルシューティング

| 問題 | 対処法 |
|-----|--------|
| Google「403: access_denied」 | OAuth同意画面のテストユーザーに自分のGmailを追加 |
| Google認証後すぐ期限切れ | テストモードのため1週間で期限切れ。再度 auth スクリプトを実行 |
| Notion「401 Unauthorized」 | `/mcp` でNotionのOAuth再認証を実行 |
| Slackの「not_authed」 | setup_slack.shで正しいBot TokenとTeam IDを再設定 |
| MCPサーバーが表示されない | `claude --mcp-debug` でログ確認 |
