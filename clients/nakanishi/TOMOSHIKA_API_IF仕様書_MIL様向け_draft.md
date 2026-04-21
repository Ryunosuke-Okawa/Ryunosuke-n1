---
title: TOMOSHIKA API I/F仕様書（MIL様向け）
date: 2026-04-21
tags:
  - 中西製作所
  - TOMOSHIKA
  - MIL
  - API仕様
  - draft
status: draft
version: Draft v1.1
---

# TOMOSHIKA API I/F仕様書（MIL様向け）

**バージョン**: Draft v1.1
**発行**: 株式会社エヌイチ
**対象**: 株式会社MIL様
**最終更新**: 2026-04-21

---

## 1. 概要

本仕様書は、MIL様のサーバーから中西製作所様のDify上のTOMOSHIKAマッチングAPIを呼び出す際のインターフェース（入出力）仕様を定めるものです。

```
[MIL様サーバー] ──── HTTPS/JSON ────▶ [Dify API（中西製作所様アカウント）]
                ◀───── HTTPS/JSON ────
```

---

## 2. 接続情報

| 項目 | 値 |
|------|-----|
| エンドポイントURL | `https://api.dify.ai/v1/workflows/run`（※本番切替後に正式URL共有） |
| HTTPメソッド | `POST` |
| 認証方式 | Bearer Token（HTTPヘッダ `Authorization: Bearer {API_KEY}`） |
| Content-Type | `application/json` |
| 文字コード | UTF-8 |
| タイムアウト推奨値 | 30秒 |

> APIキーおよびエンドポイントURLは、中西製作所様のDifyアカウント（Professionalプラン）切替後に、エヌイチよりMIL様へ別途共有いたします。

---

## 3. リクエスト仕様

### 3.1 HTTPヘッダ

```
Authorization: Bearer {API_KEY}
Content-Type: application/json
```

### 3.2 リクエストボディ

```json
{
  "inputs": {
    "R":   8,
    "I":   6,
    "A":   7,
    "S":   18,
    "E":   10,
    "C":   5,
    "Q30": 4,
    "Q31": 4,
    "Q49": 3,
    "Q50": 4,
    "Q51": 4
  },
  "response_mode": "blocking",
  "user": "student-abc123"
}
```

### 3.3 入力項目（`inputs` 配下）

| キー | 型 | 必須 | 範囲 | 説明 |
|------|-----|------|------|------|
| `R`   | number (integer) | ✅ | 4〜20 | R型（現実型）合計点 |
| `I`   | number (integer) | ✅ | 4〜20 | I型（研究型）合計点 |
| `A`   | number (integer) | ✅ | 4〜20 | A型（芸術型）合計点 |
| `S`   | number (integer) | ✅ | 4〜20 | S型（社会型）合計点 |
| `E`   | number (integer) | ✅ | 4〜20 | E型（企業型）合計点 |
| `C`   | number (integer) | ✅ | 4〜20 | C型（慣習型）合計点 |
| `Q30` | number (integer) | ✅ | 1〜5  | 主体性の点数 |
| `Q31` | number (integer) | ✅ | 1〜5  | 変革意欲の点数 |
| `Q49` | number (integer) | ✅ | 1〜5  | L尺度（虚偽回答検知）の点数 |
| `Q50` | number (integer) | ✅ | 1〜5  | BtoB志向の点数 |
| `Q51` | number (integer) | ✅ | 1〜5  | メーカー志向の点数 |

### 3.4 制御項目

| キー | 型 | 必須 | 値 | 説明 |
|------|-----|------|-----|------|
| `response_mode` | string | ✅ | `"blocking"` | 同期実行（推奨） |
| `user` | string | ✅ | 任意文字列 | 学生を識別する一意ID（MIL様側で発行・UUID推奨） |

---

## 4. レスポンス仕様（正常時）

### 4.1 HTTPステータス

`200 OK`

### 4.2 レスポンスボディ

```json
{
  "workflow_run_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
  "task_id": "f9c7a8b1-2d3e-4f5a-9b0c-1d2e3f4a5b6c",
  "data": {
    "id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
    "workflow_id": "abcdef12-3456-7890-abcd-ef1234567890",
    "status": "succeeded",
    "outputs": {
      "result_type": "nakanishi",
      "primary_type": "S",
      "secondary_type": "E",
      "primary_companies": [
        "中西製作所（厨房機器）",
        "キーエンス（自動制御）",
        "平田機工（生産システム）",
        "マクニカ（半導体商社）",
        "ダイフク（物流システム）"
      ],
      "primary_reasons": [
        "業界シェア1位の盤石な基盤。安定した環境で「攻め」のビジネスを展開したいあなたに最適。",
        "圧倒的な付加価値を生むロジック。若いうちから「稼ぐ本質」を学びたい野心家へ。",
        "世界の製造現場を支える技術力。オーダーメイドの課題解決で「一品モノ」を創る醍醐味。",
        "最先端技術の目利き。商社でありながら技術力で世界を動かすスピード感を求める方へ。",
        "Eコマースを支える物流自動化の旗手。巨大なインフラを変革する達成感がある。"
      ],
      "secondary_companies": [],
      "secondary_reasons": [],
      "message": "あなたの主体性と変革意欲は、安定基盤×ベンチャー志向の企業で大きく花開きます。"
    },
    "error": null,
    "elapsed_time": 0.85,
    "total_steps": 4,
    "created_at":  1745123400,
    "finished_at": 1745123401
  }
}
```

### 4.3 出力項目（`data.outputs` 配下）

| キー | 型 | 値の例 | 説明 |
|------|-----|--------|------|
| `result_type`        | string          | `"nakanishi"` / `"type_match"` / `"tomocari"` | 判定カテゴリ |
| `primary_type`       | string          | `"R"` / `"I"` / `"A"` / `"S"` / `"E"` / `"C"` | 第1位タイプ |
| `secondary_type`     | string          | 同上 | 第2位タイプ |
| `primary_companies`  | array of string | `["中西製作所（厨房機器）", "キーエンス（自動制御）", ...]` | メイン推薦企業（最大5社） |
| `primary_reasons`    | array of string | `["業界シェア1位の盤石な基盤...", ...]` | メイン推薦理由（`primary_companies`と同順・同数） |
| `secondary_companies`| array of string | `["三菱電機 / 村田製作所", ...]` / `[]` | 補足推薦企業（`result_type="type_match"`時のみ値あり、それ以外は空配列） |
| `secondary_reasons`  | array of string | 同上 / `[]` | 補足推薦理由（同上） |
| `message`            | string          | 1文のメッセージ | 結果画面用の一言 |

> `primary_companies` と `primary_reasons` は**同じ順序・同じ要素数**で返されます（`primary_companies[0]` に対応する理由が `primary_reasons[0]`）。`secondary_*` も同様。

### 4.4 `result_type` 別の出力パターン

| result_type | primary_companies | secondary_companies | message |
|---|---|---|---|
| `nakanishi`   | 中西製作所＋同系統企業（配列） | 空配列 `[]` | 中西向けメッセージ |
| `type_match`  | 1位タイプの企業群（配列） | 2位タイプの企業群（配列） | タイプ別メッセージ |
| `tomocari`    | 空配列 `[]` | 空配列 `[]` | トモキャリ誘導文 |

---

## 5. サンプルコード（Python）

```python
import requests

API_KEY  = "{発行されたAPIキー}"
ENDPOINT = "https://api.dify.ai/v1/workflows/run"

payload = {
    "inputs": {
        "R": 8, "I": 6, "A": 7, "S": 18, "E": 10, "C": 5,
        "Q30": 4, "Q31": 4, "Q49": 3, "Q50": 4, "Q51": 4,
    },
    "response_mode": "blocking",
    "user": "student-abc123",
}

res = requests.post(
    ENDPOINT,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=30,
)
res.raise_for_status()
outputs = res.json()["data"]["outputs"]

# primary_companies は配列（array of string）で返される
print(outputs["result_type"])            # 例: "nakanishi"
for company, reason in zip(outputs["primary_companies"], outputs["primary_reasons"]):
    print(f"- {company}: {reason}")
```

---

## 6. 動作保証範囲

- 本APIは、中西製作所様のDifyアカウント（Professionalプラン）上で稼働します
- 月間リクエスト上限：5,000件/月（Professionalプラン標準）
- 同時接続数：Dify側の標準値に準拠

---

## 7. お問い合わせ

本仕様に関するご質問・ご相談は下記までご連絡ください。

- **株式会社エヌイチ**　大川 龍之介
  - Mail：r.okawa@n1-inc.co.jp
  - TEL：080-2646-2420
