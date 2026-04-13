# Antigravity で Claude Code を使う

## 前提条件

- Antigravity: インストール済み（`/Applications/Antigravity.app`）
- Claude Code: インストール済み（`~/.npm-global/bin/claude`）
- Claude Pro/Max または API キー: 必要

---

## セットアップ手順

### 1. Antigravity を起動してプロジェクトを開く

```
Antigravity.app を起動
→ 「Open Folder」で ~/claude を開く
```

### 2. 統合ターミナルを開く

```
Ctrl + `（バッククォート）
```

### 3. claude コマンドを起動

```bash
claude
```

これだけで完了。`~/claude` を作業ディレクトリとして Claude Code が起動する。

---

## 動作確認

ターミナルで以下を実行してバージョンが表示されれば OK:

```bash
claude --version
```

---

## トラブルシューティング

### `claude: command not found` が出る場合

ターミナルで以下を実行して PATH を確認:

```bash
echo $PATH | grep npm-global
```

表示されない場合は手動で追加:

```bash
export PATH=~/.npm-global/bin:$PATH
claude
```

恒久的な修正は `~/.zshrc` を確認する:

```bash
cat ~/.zshrc
# → export PATH=~/.npm-global/bin:$PATH が含まれているか確認
```

### ログイン画面が出る場合

Claude Pro/Max に契約しているアカウントでサインイン、または API キーを入力する。

---

## おすすめワークフロー

| 場面 | ツール |
|------|--------|
| 計画・設計 | Antigravity の AI エージェント（Gemini） |
| 実装・コーディング | Claude Code（ターミナル） |
| Gemini のレート制限に当たったとき | Claude Code に切り替え |

---

## 注意事項

- Claude Code の使用には Claude Pro/Max サブスクリプションまたは API クレジットが必要
- Antigravity のモデルを Claude Code に流用するプロキシツールは ToS 違反のリスクあり（非推奨）
