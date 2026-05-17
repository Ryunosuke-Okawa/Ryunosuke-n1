---
title: 法人向け3LP 公開マニュアル（XServer デプロイ手順）
date: 2026-05-17
tags:
  - marketing
  - lp
  - deploy
  - hosting
  - xserver
  - 3lp
aliases:
  - 3LP公開手順
  - サブドメイン公開
---

# 法人向け 3LP 公開マニュアル

> [!info] このマニュアルでできること
> 3 つの法人向け LP（Claude Code/Codex 研修・AI 社員構築研修・AI 社員構築 代行）を、XServer のサブドメインに公開する手順を**順番通りに**まとめたもの。
> **対象**：HTML・サーバーの専門知識がない人。コマンド操作なし、すべてブラウザ・XServer ファイルマネージャで完結。

> [!tip] 汎用マニュアルとの違い
> 汎用版：[claudecode_lp_deploy_guide.md](claudecode_lp_deploy_guide.md)（XServer サブドメイン作成の手順全般）
> このマニュアル：**今回の 3LP を実際に公開するための、具体的なファイル所在・順番・チェックリスト**

---

## 0. 全体像

3LP それぞれが独立した 1 ファイル＋画像フォルダで完結しています。各 LP は別々のサブドメインに置きます。

```
[ローカル]                                    [公開 URL（サブドメイン）]
marketing/claudecode_codex_training_lp/   →   ①Claude Code/Codex 研修
marketing/ai_staff_training_lp/           →   ②AI 社員構築研修
marketing/ai_staff_bpo_lp/                →   ③AI 社員構築 代行
```

公開は **1 LP ずつ** 進めるのが安全。順序は **① → ② → ③** を推奨（既存 `claudecode.n1-inc.co.jp` の差し替えがある場合は最後）。

---

## 1. 事前準備（最初に揃えるもの）

| 項目 | 値・取得方法 |
|---|---|
| XServer サーバーパネル URL | https://www.xserver.ne.jp/login_server.php |
| サーバーID | `xs842147` |
| サーバーパスワード | 1Password 等で管理（大川） |
| 親ドメイン | `n1-inc.co.jp`（XServer に登録済み） |
| 公開 LP の HTML | `marketing/各LPフォルダ/index.html`（既に完成済） |
| 公開 LP の画像 | `marketing/各LPフォルダ/images/`（hero_team.png / support_team.png / cta_team.png） |

> [!warning] パスワード共有時の注意
> XServer ログイン情報は **Slack やメール本文に直接書かない**。1Password 等のパスワード共有機能を使う。

---

## 2. サブドメイン候補（決定が必要）

各 LP のサブドメイン名は **大川さんが決定**してください。以下は候補：

| LP | 候補A（短め） | 候補B（説明的） |
|---|---|---|
| ①Claude Code/Codex 研修 | `claudecode-codex.n1-inc.co.jp` | `cc-training.n1-inc.co.jp` |
| ②AI 社員構築研修 | `aistaff.n1-inc.co.jp` | `ai-staff-training.n1-inc.co.jp` |
| ③AI 社員構築 代行 | `bpo.n1-inc.co.jp` | `ai-staff-bpo.n1-inc.co.jp` |

> [!note] 既存サブドメインの扱い
> `claudecode.n1-inc.co.jp`（Claude Code 単体の旧 LP）は別物として運用中。①の新 LP を別サブドメインで公開するか、既存を差し替えるかは要判断。

> [!tip] サブドメイン命名のコツ
> - 短く覚えやすく（チラシ・メールで案内するため）
> - 半角英数字とハイフンのみ
> - 用途終了時に削除しないと「使われていない住所」が残るので命名規則は揃える

---

## 3. ローカルのファイル所在まとめ

各 LP の構造は同じ。`index.html` ＋ `images/` フォルダの 2 点セット。

### ①Claude Code/Codex 研修
```
marketing/claudecode_codex_training_lp/
├── index.html
└── images/
    ├── hero_team.png
    ├── support_team.png
    └── cta_team.png
```

### ②AI 社員構築研修
```
marketing/ai_staff_training_lp/
├── index.html
└── images/
    ├── hero_team.png
    ├── support_team.png
    └── cta_team.png
```

### ③AI 社員構築 代行
```
marketing/ai_staff_bpo_lp/
├── index.html
└── images/
    ├── hero_team.png
    ├── support_team.png
    └── cta_team.png
```

> [!warning] フォルダ構造はそのままサーバーに移す
> サーバー上も `index.html` ＋ `images/` の構造を維持。違うフォルダに散らすと画像リンクが切れる。

---

## 4. 公開作業の流れ（1 LP あたり）

### Phase 1：サブドメインを作る（5分操作 + 反映待ち 5〜30分）

1. **XServer サーバーパネル**にログイン（サーバーID：`xs842147`）
2. 「**ドメイン**」→「**サブドメイン設定**」
3. `n1-inc.co.jp` を「**選択する**」
4. タブを「**サブドメイン設定追加**」に切り替え
5. サブドメイン名を入力（例：`aistaff`）
6. コメント欄に用途を記載（例：「AI 社員構築研修 LP」）
7. **無料独自SSLを利用する**：✅ ON のまま
8. 「確認画面へ進む」→「追加する」
9. 5〜30分待つ（DNS 反映待ち）
10. ブラウザで `https://〇〇〇.n1-inc.co.jp/` にアクセス → XServer 初期ページが見えれば OK

### Phase 2：HTML と画像をローカルで準備

> [!warning] 元ファイルを直接いじらない
> 必ず**コピー**してから `~/Desktop/lp_deploy_〇〇/` 等の作業フォルダにまとめる。Vault の元ファイルが壊れると再編集が大変。

1. Finder で `marketing/各LPフォルダ/` を開く
2. `index.html` と `images/` フォルダの **2 つをコピー**
3. デスクトップに `lp_deploy_aistaff/` のような作業フォルダを作って中に貼り付け
4. フォルダ構造が以下になっていることを確認：

```
~/Desktop/lp_deploy_aistaff/
├── index.html
└── images/
    ├── hero_team.png
    ├── support_team.png
    └── cta_team.png
```

> [!info] ファイル名はそのままで OK
> 各 LP の HTML は既に `index.html` というファイル名なので、リネーム不要。

### Phase 3：サーバーにアップロード

1. XServer サーバーパネルから「**ファイル**」→「**ファイルマネージャ**」
2. 以下の順にダブルクリックで降りていく：

```
n1-inc.co.jp
  └─ public_html
       └─ 〇〇〇.n1-inc.co.jp     ← Phase 1で作ったサブドメインのフォルダ
```

3. このフォルダの中に入った状態で、「**ファイルのアップロード**」をクリック
4. ローカルの `index.html` を選択 → アップロード
5. 続けて「**フォルダの作成**」で `images` フォルダを作る
6. `images` フォルダに入り、「ファイルのアップロード」で 3 枚の画像をまとめてアップロード
7. 最終的にサーバー側が以下になっていることを確認：

```
〇〇〇.n1-inc.co.jp/
├── index.html
└── images/
    ├── hero_team.png
    ├── support_team.png
    └── cta_team.png
```

> [!warning] フォルダの取り違えに注意
> `public_html/` の直下には他のサブドメイン用フォルダが並びます。**必ず今回作ったサブドメインの名前のフォルダ**で作業。違うフォルダに上書きすると別サイトを壊します。

### Phase 4：公開を確認

1. ブラウザで `https://〇〇〇.n1-inc.co.jp/` にアクセス
2. **ハード再読み込み**（Mac：`Cmd + Shift + R`／Win：`Ctrl + Shift + R`）
3. 以下のチェックリストを全てクリアすればOK：

#### 公開チェックリスト（各 LP 共通）

- [ ] LP が想定通りに表示されている（崩れていない）
- [ ] アドレスバーに **鍵マーク** が付いている（SSL 有効）
- [ ] Hero の人物写真が表示されている
- [ ] サポート/CTA セクションの人物写真も表示されている
- [ ] AI 社員カタログ（②③）のアイコンが正しい色で出ている
- [ ] スマホで開いても崩れていない
- [ ] 「無料相談はこちら」「LINE で質問する」ボタンをクリックして、想定先に飛ぶ
- [ ] FAQ のアコーディオン（▾）が開閉する

---

## 5. 公開後の URL 管理

各 LP の公開 URL が確定したら、`marketing/articles/lp_3services_master_20260516.md` に追記しておく。

| LP | 公開 URL（公開後に記入） |
|---|---|
| ①Claude Code/Codex 研修 | https://〇〇〇.n1-inc.co.jp/ |
| ②AI 社員構築研修 | https://〇〇〇.n1-inc.co.jp/ |
| ③AI 社員構築 代行 | https://〇〇〇.n1-inc.co.jp/ |

---

## 6. 2 回目以降の更新フロー

初回公開後の修正は **Phase 2〜4 のみ** でOK。

### STEP A — ローカルで `marketing/各LPフォルダ/index.html` を編集

### STEP B — 既存ファイルをバックアップ（必須）
1. ファイルマネージャでサブドメインのフォルダに入る
2. 既存の `index.html` を右クリック → 「**ダウンロード**」
3. PC に落ちてきたファイルを `index_backup_YYYYMMDD.html` にリネームして保管

### STEP C — 新版 `index.html` をアップロード
1. ファイルマネージャの「ファイルのアップロード」で新版を選択
2. 「**同名のファイルを上書きしますか？**」→「**はい**」
3. ファイル一覧の `index.html` の更新日時が今に変わっていれば OK

### STEP D — ブラウザでハード再読み込みして確認

> [!tip] 画像も更新する場合
> 画像も `images/` フォルダ内の同名ファイルとして上書きすればOK。HTML 修正は不要。

---

## 7. トラブルシューティング

### 「サブドメインを作ったのに、ブラウザで表示されない」
- DNS 反映待ち：作成から 30 分以内なら待つ
- URL のスペルミス：`https://` で始めているか、サブドメイン名にタイポがないか
- SSL 反映待ち：「保護されていません」警告だけならアクセス自体はできる

### 「変更が反映されない」
- ハード再読み込みをやったか？（`Cmd+Shift+R`）
- アップロード先のフォルダは正しいサブドメインのフォルダか？
- ファイル名は `index.html`（小文字・拡張子.html）か？

### 「画像が表示されない／壊れた画像アイコンが出る」
- `images/` フォルダがサーバーに存在しているか？
- フォルダ名は `images`（小文字）か？（`Images` `IMAGES` はNG）
- 画像ファイル名が HTML 内の `src` と完全一致しているか？
- ブラウザのアドレスバーに `https://〇〇〇.n1-inc.co.jp/images/hero_team.png` を直接入力して画像が見えるか？
  - 見える → HTML の src のスペルミス
  - 404 → 画像未アップロード or フォルダ違い

### 「ページが真っ白／崩れている」
バックアップの `index_backup_YYYYMMDD.html` を `index.html` にリネームして上書きアップロードで元に戻す。

### 「ログインできない」
- サーバーID は `xs842147`
- パスワードは 1Password で再確認
- それでもダメなら大川（r.okawa@n1-inc.co.jp）に連絡

---

## 8. やってはいけないこと

> [!danger] NG リスト
> - ❌ **作ったサブドメイン以外のフォルダにアップロードする**（他サイトを壊す）
> - ❌ **`index.html` 以外の名前でアップする**（公開 URL に表示されない）
> - ❌ **バックアップを取らずに上書きする**（戻せなくなる）
> - ❌ **XServer のログイン情報をメール／Slack で平文共有する**
> - ❌ **サーバーパネルの「ドメイン削除」「サーバー初期化」をいじる**（取り返しがつかない）
> - ❌ **SSL を「無効」に切り替える**（公開 LP が警告まみれになる）
> - ❌ **3LP のローカル元ファイル（`marketing/各LPフォルダ/index.html`）を直接リネームする**（再編集できなくなる）

---

## 9. 関連ドキュメント

- **汎用 LP 公開ガイド**：[claudecode_lp_deploy_guide.md](claudecode_lp_deploy_guide.md)（XServer の基礎説明・画像入れ方詳細）
- **3LP マスター索引**：[articles/lp_3services_master_20260516.md](articles/lp_3services_master_20260516.md)
- **既存 LP 公開ログ**：[claudecode_lp_deploy_log.md](claudecode_lp_deploy_log.md)（claudecode.n1-inc.co.jp の構成）
- **メモリ**：`project_3lp_corporate.md`（3LP 完成状態・確定事項）

---

## 10. 早見表（印刷用）

```
━━━ 1 LP を新規公開するときの全工程 ━━━

[Phase 1] サブドメインを作る（XServerサーバーパネル）
  1. https://www.xserver.ne.jp/login_server.php にログイン（ID: xs842147）
  2. ドメイン → サブドメイン設定 → n1-inc.co.jp を選択
  3. サブドメイン名を入力（例：aistaff）→ SSL ON → 追加
  4. 5〜30分待つ → ブラウザで初期ページが見えればOK
        ↓
[Phase 2] ローカルで準備
  1. marketing/各LPフォルダ/ の index.html + images/ をコピー
  2. ~/Desktop/lp_deploy_〇〇/ にまとめる
        ↓
[Phase 3] サーバーにアップロード（ファイルマネージャ）
  1. n1-inc.co.jp/public_html/〇〇〇.n1-inc.co.jp/ に入る
  2. index.html をアップロード
  3. images フォルダを作って、画像3枚をアップロード
        ↓
[Phase 4] 公開確認
  1. https://〇〇〇.n1-inc.co.jp/ を Cmd+Shift+R で開く
  2. SSL鍵マーク・画像・CTAリンクをチェック
        ↓
       ✅ 完了

━━━ 2 回目以降の更新 ━━━
A. ローカルで編集
B. サーバーの既存 index.html をダウンロード → バックアップ
C. 新 index.html をアップロード（上書き「はい」）
D. ハード再読み込みで確認
```

---

> [!success] このマニュアルの位置づけ
> - 3 LP それぞれを公開・更新するときの **作業手順書**
> - サブドメイン名と公開 URL は公開後に「5. 公開後の URL 管理」に追記してください
> - 困ったら汎用版マニュアルか、大川さんに連絡
