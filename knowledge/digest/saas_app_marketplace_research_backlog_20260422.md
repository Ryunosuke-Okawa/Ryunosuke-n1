---
title: SaaS App Marketplace リサーチ 補足（Backlog / ヌーラボ）
date: 2026-04-22
tags:
  - research
  - marketplace
  - integration
  - SaaS
  - Kawaru
  - OAuth
  - Backlog
---

# Backlog（ヌーラボ）— マーケットプレイス調査

前回（Vol.1 / Vol.2）のSaaSマーケットプレイス調査で抜けていたBacklogについて、同一フォーマットで追加調査。

---

## API連携状況

| 項目 | 内容 |
| --- | --- |
| ステータス | 連携済み |
| URL | https://nulab.com/ja/login/ |
| ID | kawaru.info@n1-inc.co.jp |
| パスワード | Kawaru260218@ |
| 認証方式 | OAuth 2.0 / APIキー |
| アカウント数 | 1 |
| プラン | フリープラン |

---

## マーケットプレイス

| 項目 | 内容 |
| --- | --- |
| 有無 | **なし**（公開アプリマーケットプレイスは未整備） |
| 連携サービス紹介ページ | https://nulab.com/ja/partner/integrate/ |
| 登録方式 | パートナー選定制（セルフ登録不可） |
| 審査期間 | 非公開 |
| 費用 | 不明（パートナー契約次第。開発者アプリ登録は無料） |

### 位置付け

- **Chatwork / マネーフォワード型**（セルフサーブ型マーケットプレイスが存在しない）
- ただし公式パートナー「拡張サービス・連携アプリパートナー」枠での紹介掲載は可能で、**LINE WORKS / Dropbox型の招待・パートナー選定制**の性質も併せ持つ中間ポジション
- OAuth 2.0連携の開発自体は誰でも可能。ヌーラボ公認として紹介ページに載るにはパートナー契約が前提

### 掲載手順（2段階）

**Stage 1: OAuthアプリ作成・連携機能の開発**

1. ヌーラボアカウントを作成（https://nulab.com/ja/login/）
2. Developer Applicationsでアプリ登録（https://nulab.com/backlog/developer/applications/）— OAuth 2.0設定、`client_id`/`client_secret`取得
3. Backlog API v2を使って連携機能を開発・テスト（Authorization Code Grantフロー実装）
4. ユーザーに対してOAuth連携の提供開始（この時点ではパートナー認定なしでも配布可能）

**Stage 2: ヌーラボ公式パートナー認定 → 連携サービス一覧への掲載**

5. 「公式パートナー加入のご相談」フォームから申請（https://nulab.com/ja/partner/）
6. パートナー種別「拡張サービス・連携アプリパートナー」を選択して個別相談
7. ヌーラボ側の審査・動作確認 → 公式パートナー認定
8. 連携サービス紹介ページ（https://nulab.com/ja/partner/integrate/）に掲載

### 参考

- [ヌーラボ公式パートナー制度](https://nulab.com/ja/partner/)
- [Backlog 連携サービス紹介ページ](https://nulab.com/ja/partner/integrate/)
- [Backlog Developer API（認証）](https://developer.nulab.com/docs/backlog/auth/)
- [Backlog Developer Applications](https://nulab.com/backlog/developer/applications/)
- [Backlog API Overview](https://developer.nulab.com/docs/backlog/)

---

## 既存の比較表への追記

| サービス | マーケットプレイス | セルフサーブ登録 | OAuth 2.0 | レビュー期間 | 掲載の敷居 |
|---------|:--:|:--:|:--:|:--:|:--:|
| **Backlog** | なし（パートナー紹介ページのみ） | 不可（パートナー契約制） | 対応あり | 不明（個別交渉） | 高（公式パートナー加入が前提） |
