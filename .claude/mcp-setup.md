# MCP セットアップ手順

## 設定ファイルの場所

Claude Code のグローバルMCP設定: `~/.claude/settings.json`

## 接続予定ツール

### 1. Notion

```json
"notion": {
  "command": "npx",
  "args": ["-y", "@notionhq/notion-mcp-server"],
  "env": {
    "NOTION_API_KEY": "secret_xxxxxxxxxxxx"
  }
}
```

**取得先**: https://www.notion.so/my-integrations

---

### 2. Google Calendar

```json
"google-calendar": {
  "command": "npx",
  "args": ["-y", "@cocal/google-calendar-mcp"],
  "env": {
    "GOOGLE_CLIENT_ID": "xxxxxxxx.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "GOCSPX-xxxxxxxx"
  }
}
```

**取得先**: https://console.cloud.google.com/ → APIとサービス → 認証情報

---

### 3. Google Sheets

```json
"google-sheets": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-google-sheets"],
  "env": {
    "GOOGLE_CLIENT_ID": "xxxxxxxx.apps.googleusercontent.com",
    "GOOGLE_CLIENT_SECRET": "GOCSPX-xxxxxxxx"
  }
}
```

**取得先**: Google Calendar と同じOAuthクライアントを使用可能

---

## 設定完了後の手順

1. `~/.claude/settings.json` の `mcpServers` に上記を追記
2. Claude Code を再起動
3. 各ツールの接続テストを実施
4. `CLAUDE.md` の「外部ツール連携」セクションを更新
