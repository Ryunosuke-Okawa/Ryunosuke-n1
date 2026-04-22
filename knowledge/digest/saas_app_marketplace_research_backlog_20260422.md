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

# SaaS App Marketplace リサーチ 補足 — Backlog

前回（Vol.1 / Vol.2）のマーケットプレイス調査で抜けていたBacklog（ヌーラボ）について、同一フォーマットで追加調査。サードパーティSaaSがOAuthベースの連携アプリとして公開マーケットプレイスに登録・掲載できるかを確認。

---

## Backlog（株式会社ヌーラボ）

| 項目 | 内容 |
|------|------|
| **マーケットプレイス有無** | **なし**（セルフサーブ型の公開アプリマーケットプレイスは存在しない） |
| **連携サービス紹介ページ** | https://nulab.com/ja/partner/integrate/ （ヌーラボ公式パートナーの連携サービス一覧） |
| **開発者ページ** | https://developer.nulab.com/docs/backlog/ / https://nulab.com/backlog/developer/applications/ |
| **サードパーティ公開掲載** | **不可（招待制/パートナー契約制）**。自由に申請・自動掲載される仕組みはなく、「拡張サービス・連携アプリパートナー」として公式パートナープログラムに加入する必要がある |
| **認証方式** | OAuth 2.0（Authorization Code Grant、RFC 6749準拠） + APIキー認証。Developer Siteでアプリ登録→`client_id`/`client_secret`取得。アクセストークン有効期限3600秒、リフレッシュトークン対応 |
| **審査・要件** | **公式な公開審査プロセスなし**。パートナー加入はフォームからの個別相談ベース。種別は「技術支援」「コンサルティング」「拡張サービス・連携アプリ」の3種。加入要件・審査基準は非公開 |
| **承認期間目安** | 不明（パートナー契約交渉次第、数ヶ月と推定） |
| **費用** | 不明（パートナー契約による可能性。Developer Siteへのアプリ登録自体は無料） |
| **備考** | 連携サービス紹介ページに掲載されているのは厳選された公式パートナーのみ（6社程度）。サードパーティがセルフサーブで連携アプリを公開する仕組みはChatwork/マネーフォワードと同様に未整備。OAuth 2.0連携自体は誰でも開発可能だが、「Backlog公認」として紹介ページに載るにはパートナー契約が前提 |

### 参考URL
- 公式パートナー制度: https://nulab.com/ja/partner/
- 連携サービス一覧: https://nulab.com/ja/partner/integrate/
- API認証ドキュメント: https://developer.nulab.com/docs/backlog/auth/
- アプリケーション登録: https://nulab.com/backlog/developer/applications/
- API概要: https://developer.nulab.com/docs/backlog/

---

## 結論

Backlogには**セルフサーブ型のアプリマーケットプレイスは存在しない**。Chatwork/マネーフォワードと同じく「公開連携アプリを自由に掲載できる仕組みなし」型に分類される。ただし、ヌーラボ公式パートナープログラムの「拡張サービス・連携アプリパートナー」枠に加入すれば、連携サービス紹介ページに掲載される可能性はある（LINE WORKS/Dropbox型に近い招待・パートナー選定制）。

掲載の敷居としては**高**（パートナー交渉ベース、セルフサーブ不可）。

---

## 既存の比較表への追記（位置付け）

| サービス | マーケットプレイス | セルフサーブ登録 | OAuth 2.0 | レビュー期間 | 掲載の敷居 |
|---------|:--:|:--:|:--:|:--:|:--:|
| **Backlog** | **なし**（パートナー紹介ページのみ） | **不可**（パートナー契約制） | 対応あり | 不明（個別交渉） | 高（公式パートナー加入が前提） |

Chatwork・マネーフォワードと同じ「マーケットプレイスなし」グループ、または掲載自体はあるが招待制のLINE WORKS・Dropboxに近い中間ポジション。
