---
title: 中西製作所TOMOSHIKA Dify修正引き継ぎ（MILリクエスト対応）
date: 2026-04-28
status: in-progress
client: 中西製作所
project: TOMOSHIKA
tags:
  - clients
  - nakanishi
  - dify
  - handover
---

# 中西製作所TOMOSHIKA Dify修正 引き継ぎ書

> **このドキュメントを新しいチャットの冒頭で読み込めば、コールドスタートで作業継続できる構成にしてあります。**

---

## 🎯 ゴール（このタスクの目的）

MIL（実装担当）から来たリクエストに従い、Difyワークフローの出力から `primary_reasons` / `secondary_reasons` を削除する。スマホで結果ページが縦長になりすぎる問題への対応。

## 📍 現在の進捗

- ✅ **MILの依頼内容を整理済み**（4論点に分解）
- ✅ **進め方を決定済み**：「reasons削除だけ即対応 → その後3論点を確認」の二段構え
- ✅ **修正版コードを作成済み**（このドキュメント末尾に貼付）
- ⏸ **未完了**：以下4つの作業
  1. Difyコード実行ブロックを修正版に差し替え
  2. Dify出力ノードから `primary_reasons` / `secondary_reasons` の2変数を削除
  3. テスト実行で動作確認（解答例は本書末尾）
  4. MILへの返信送付（残3論点の確認）

---

## 📦 プロジェクト前提

### 案件概要
- **クライアント**：中西製作所（厨房機器業界シェア1位）
- **プロジェクト名**：TOMOSHIKA
- **内容**：RIASEC適性診断ツール。学生がアンケート回答→AIが企業候補を提示する仕組み
- **実装担当**：MIL（フロントエンド実装会社）
- **窓口**：津丸様（MIL）
- **エンジニア**：木村さん（中西社内）／**Dify構築は大川さん自身が担当**、木村さんはレビュー役
- **大川さんの役割**：Difyワークフロー設計・コード実装

### Difyワークフロー構成
```
[ユーザー入力] → [コード実行] → [出力]
   11変数      Pythonロジック    8変数（→修正後6変数）
```

#### 入力変数（11個）
| 変数 | 内容 |
|---|---|
| R / I / A / S / E / C | RIASECの6タイプ各スコア |
| Q30, Q31 | 行動特性（主体性・変革意欲）1〜5 |
| Q49 | L尺度（社会的望ましさ）→ 5なら全スコア×0.8 |
| Q50 | BtoB志向（≥3でBtoB、＜3でBtoC） |
| Q51 | インフラ志向 |

#### 判定ロジック（4ステップ）
| Step | 条件 | result_type | 出力企業 |
|---|---|---|---|
| 1 | max-min ≤ 1.0（未分化） | `tomocari` | なし |
| 2 | Q30≥4 & Q31≥4 & Q50≥3 | `nakanishi` | 中西BtoB 5社 |
| 3 | top2に{E,I,A}含む & avg(Q50,Q51)≥3.0 & Q50≥3 | `nakanishi` | 中西BtoB 5社 |
| 4 | それ以外 | `type_match` | primary 2社＋secondary 2社 |

---

## 📨 MILからの修正依頼（2026/04/28受領）

### 依頼内容（要旨）
- スマホで結果ページが縦長になり見づらい
- 当初イメージは「会社名リスト＋全体メッセージ1文」だった
- 各社ごとの理由文（`primary_reasons`）は**表示しない**ことにしたい

### 表示の対比
**Before（当初イメージ）**
```
A社／B社／C社／D社／E社
─────────────
選んだ理由は、、、（全体で1文）
```

**Now（現状アウトプット）**
```
A社 → 選んだ理由は、、、
B社 → 選んだ理由は、、、
…
全体メッセージ、、、
```
→ MIL要望は **Before** に戻す

### MILスクショの指示
- ✅ 使う：`primary_companies` ＋ `message`
- ❌ 使わない：`primary_reasons`（「ここの要素を入れない」と明記）

---

## 🛠️ 進め方の方針（合意済み）

「即対応する範囲」と「確認に回す範囲」を分けた二段構え。

| 対応 | 内容 | 理由 |
|---|---|---|
| ✅ 即修正 | `primary_reasons` / `secondary_reasons` を出力dictから削除 | MILが明示 |
| ✅ 即修正 | Dify出力ノードからも該当2変数を削除 | 上記とセット |
| ⏸ 確認後 | `secondary_companies` の扱い | 通常判定時の言及なし → **残す** |
| ⏸ 確認後 | `message` の文言変更 | 役割が変わる可能性は推測なので触らない |
| ⏸ 確認後 | `tomocari` 時の表示仕様 | フロント側実装で吸収可能 |

---

## ❓ MILへの確認事項（修正後に送付）

修正完了後、MIL（津丸様）に以下3点を返信で確認する。

> ご依頼の通り、結果ページに表示しない `primary_reasons` / `secondary_reasons` をDify出力から削除しました。動作確認の上、3点だけ実装方針を確認させてください。
>
> 1. **secondary（2位タイプ）の企業表示**：通常判定パターン（`type_match`）では現状primary 2社＋secondary 2社で計4社出ています。今回の表示方針はprimaryのみでよろしいでしょうか？それとも合算して表示しますか？
> 2. **未分化パターン（`tomocari`）**：会社名は空配列、メッセージのみとなります。この場合は会社リスト枠を非表示にしてメッセージのみ表示で問題ないでしょうか？
> 3. **`message`文の役割**：当初イメージの「選んだ理由は、、、」は「なぜこの5社が選ばれたか」の説明文と理解しております。現状の `message` はタイプ特性のサマリー文になっているため、内容を「企業選定理由のサマリー」に書き換える必要があるかご確認ください。

---

## 📋 残作業の手順

### Step 1：コード実行ブロックを修正版に差し替え（コピペ可）

下記コードを Dify の「コード実行」ブロックに**まるごと貼り付けて置き換える**。

```python
def main(R: int, I: int, A: int, S: int, E: int, C: int,
         Q30: int, Q31: int, Q49: int, Q50: int, Q51: int) -> dict:

    # ==============================
    # 企業マスタ
    # ==============================
    company_db = {
        "nakanishi": {
            "BtoB": [
                {"group": "中西製作所（厨房機器）", "reason": "業界シェア1位の盤石な基盤。安定した環境で「攻め」のビジネスを展開したいあなたに最適。"},
                {"group": "キーエンス（自動制御）", "reason": "圧倒的な付加価値を生むロジック。若いうちから「稼ぐ本質」を学びたい野心家へ。"},
                {"group": "平田機工（生産システム）", "reason": "世界の製造現場を支える技術力。オーダーメイドの課題解決で「一品モノ」を創る醍醐味。"},
                {"group": "マクニカ（半導体商社）", "reason": "最先端技術の目利き。商社でありながら技術力で世界を動かすスピード感を求める方へ。"},
                {"group": "ダイフク（物流システム）", "reason": "Eコマースを支える物流自動化の旗手。巨大なインフラを変革する達成感がある。"},
            ],
            "BtoC": [
                {"group": "ソニー（総合電機）", "reason": "テクノロジーとクリエイティビティの融合。既存の枠を超えた新しい「遊び」を創れる。"},
                {"group": "リクルート（人材/IT）", "reason": "「自ら機会を創り出し、機会によって自らを変えよ」。圧倒的な主体性を試せる環境。"},
                {"group": "メルカリ（フリマアプリ）", "reason": "「Go Bold（大胆にやろう）」。日本発のグローバルベンチャーで社会実装に挑める。"},
                {"group": "カヤック（面白法人）", "reason": "斬新なアイデアを即座に形にする文化。面白さをビジネスに変える創造性が必要。"},
                {"group": "マネーフォワード（Fintech）", "reason": "お金の概念を変える。個人の生活を支えるプラットフォームを自ら構築したい方へ。"},
            ],
        },
        "R": {
            "BtoB": [
                {"group": "三菱電機 / 村田製作所", "reason": "世界を支える高い技術精度。確かな「物作り」の最高峰で自分の腕を磨ける。"},
                {"group": "安川電機 / 栗田工業 / THK", "reason": "産業の根幹を成す装置や水処理。目立たずとも「無くてはならない」実益を支える。"},
            ],
            "BtoC": [
                {"group": "トヨタ自動車 / 任天堂", "reason": "圧倒的な製品クオリティ。手に取れる「最高の結果」を世界中に届ける手応え。"},
                {"group": "スノーピーク / ヤマハ / マキタ", "reason": "こだわりのある道具作り。ユーザーの熱量を感じながら、実用性を極められる環境。"},
            ],
        },
        "I": {
            "BtoB": [
                {"group": "野村総合研究所 / 島津製作所", "reason": "緻密な分析と論理。日本の知性を牽引し、複雑な社会課題を解き明かす知的興奮。"},
                {"group": "中外製薬 / オムロン / ユーザーベース", "reason": "R&Dや情報分析。根拠に基づいた意思決定で、業界に新たなスタンダードを創る。"},
            ],
            "BtoC": [
                {"group": "Google / 武田薬品工業", "reason": "世界規模のデータと知見。人々の生活を根本から変える「解」を研究し続ける場。"},
                {"group": "コーセー / エーザイ / メルカリ(データ部門)", "reason": "科学的根拠に基づく美や健康。個人のQOLを高めるための深い洞察が可能。"},
            ],
        },
        "A": {
            "BtoB": [
                {"group": "電通 / 博報堂", "reason": "クリエイティブで企業を変える。表現の力でビジネスに新しい命を吹き込める。"},
                {"group": "チームラボ / Sansan / 乃村工藝社", "reason": "空間やITのデザイン。形のないアイデアを社会に実装する、表現者としての挑戦。"},
            ],
            "BtoC": [
                {"group": "サンリオ / オリエンタルランド", "reason": "世界観の構築。人々の感情を揺さぶり、日常に魔法をかける体験価値の創造。"},
                {"group": "資生堂 / 集英社 / 無印良品", "reason": "独自の美学やストーリー。個々のライフスタイルに寄り添う、新しい価値の提案。"},
            ],
        },
        "S": {
            "BtoB": [
                {"group": "ベネッセ / リクルートマネジメント", "reason": "組織や人の教育。企業という集団がより良く機能するための、対人的な支援。"},
                {"group": "パソナ / ワークスアプリケーションズ / LITALICO", "reason": "働く環境の改善や福祉。誰もが活躍できる社会基盤を、BtoBの視点で構築。"},
            ],
            "BtoC": [
                {"group": "日本赤十字社 / 損害保険ジャパン", "reason": "有事の際の支え。人々の生活に安心を与え、困っている人を救う使命感。"},
                {"group": "星野リゾート / Zoff / クラシコム", "reason": "顧客体験の向上。日々の暮らしを豊かにし、一人ひとりの笑顔を直接つくる喜び。"},
            ],
        },
        "E": {
            "BtoB": [
                {"group": "三菱商事 / 伊藤忠商事", "reason": "ビジネスの最前線。巨額の投資と交渉で、世界のエネルギーや食糧を動かす。"},
                {"group": "光通信 / サイバーエージェント(営業) / レバレジーズ", "reason": "圧倒的な達成意欲。若いうちから組織を率い、マーケットを切り拓くバイタリティ。"},
            ],
            "BtoC": [
                {"group": "ソフトバンク / 楽天グループ", "reason": "スピード感ある事業展開。生活インフラを次々と刷新し、勝負し続ける環境。"},
                {"group": "ファーストリテイリング / ZOZO", "reason": "圧倒的な顧客開拓。既成の小売りやサービスを破壊し、新しい市場を統治する。"},
            ],
        },
        "C": {
            "BtoB": [
                {"group": "日本生命 / 東京海上日動", "reason": "揺るぎない信頼。膨大な契約とデータを正確に管理し、社会のセーフティネットを守る。"},
                {"group": "三菱UFJ銀行 / 富士通 / オービック", "reason": "経済の血流を支えるシステム。一寸のミスも許されない環境で、着実に基盤を運用。"},
            ],
            "BtoC": [
                {"group": "JR東日本 / ANA", "reason": "運行の正確性と安全。多くの人々の日常を、寸分の狂いなく守り抜くプロ意識。"},
                {"group": "日本郵便 / ゆうちょ銀行", "reason": "地域社会の基盤。ルールと手順を守り、全ての人に公平で正確なサービスを提供。"},
            ],
        },
    }

    # ==============================
    # Step 0: L尺度補正
    # ==============================
    scores = {"R": R, "I": I, "A": A, "S": S, "E": E, "C": C}

    if Q49 == 5:
        scores = {k: v * 0.8 for k, v in scores.items()}

    # ==============================
    # スコアのランキング算出
    # ==============================
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_type = sorted_types[0][0]
    primary_score = sorted_types[0][1]
    secondary_type = sorted_types[1][0]
    secondary_score = sorted_types[1][1]
    min_score = sorted_types[-1][1]
    max_score = sorted_types[0][1]

    # BtoB / BtoC 判定
    btob_flag = "BtoB" if Q50 >= 3 else "BtoC"

    # ==============================
    # Step 1: 未分化判定（最優先）
    # ==============================
    if max_score - min_score <= 1.0:
        return {
            "result_type": "tomocari",
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "primary_companies": [],
            "secondary_companies": [],
            "message": "今はまだ、特定のタイプに収まる時期ではありません。焦って就職先を決める前に、トモキャリで「一生使える自分の武器」を見つける旅を始めましょう。",
        }

    # ==============================
    # Step 2: 行動特性判定
    # ==============================
    if Q30 >= 4 and Q31 >= 4 and Q50 >= 3:
        companies = company_db["nakanishi"]["BtoB"]
        return {
            "result_type": "nakanishi",
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "primary_companies": [c["group"] for c in companies],
            "secondary_companies": [],
            "message": "あなたの主体性と変革意欲は、安定基盤×ベンチャー志向の企業で大きく花開きます。",
        }

    # ==============================
    # Step 3: タイプ×志向判定
    # ==============================
    nakanishi_types = {"E", "I", "A"}
    top2 = {primary_type, secondary_type}
    q50_q51_avg = (Q50 + Q51) / 2

    if top2 & nakanishi_types and q50_q51_avg >= 3.0 and Q50 >= 3:
        companies = company_db["nakanishi"]["BtoB"]
        return {
            "result_type": "nakanishi",
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "primary_companies": [c["group"] for c in companies],
            "secondary_companies": [],
            "message": "あなたの志向性とBtoB・インフラへの適性は、社会基盤を支える企業で活かされます。",
        }

    # ==============================
    # Step 4: 通常判定
    # ==============================
    p_companies = company_db[primary_type][btob_flag]
    s_companies = company_db[secondary_type][btob_flag]

    return {
        "result_type": "type_match",
        "primary_type": primary_type,
        "secondary_type": secondary_type,
        "primary_companies": [c["group"] for c in p_companies],
        "secondary_companies": [c["group"] for c in s_companies],
        "message": f"あなたは{primary_type}型の特性が最も強く、{secondary_type}型の側面も備わっています。",
    }
```

> 💡 `company_db` 内の `"reason"` データは**残してある**（後で復活させたい時のため）。

### Step 2：Dify 出力ノードの修正

画面右の「出力」ノードから、以下2つを**ゴミ箱アイコンで削除**：

- ❌ `primary_reasons`（コード実行 / Array[String]）
- ❌ `secondary_reasons`（コード実行 / Array[String]）

修正後の出力変数（6個）：
| 変数名 | 型 |
|---|---|
| result_type | String |
| primary_type | String |
| secondary_type | String |
| primary_companies | Array[String] |
| secondary_companies | Array[String] |
| message | String |

### Step 3：テスト実行で動作確認

中西判定にならないテストパターン（`type_match` と `tomocari` の両方を確認）。

#### パターン①：通常判定（type_match）／R型主軸・BtoC
```
R=5, I=2, A=3, S=4, E=1, C=2
Q30=3, Q31=3, Q49=2, Q50=2, Q51=2
```
**期待結果**：
- `result_type` = `type_match`
- `primary_type` = `R` / `secondary_type` = `S`
- `primary_companies` = ["トヨタ自動車 / 任天堂", "スノーピーク / ヤマハ / マキタ"]
- `secondary_companies` = ["日本赤十字社 / 損害保険ジャパン", "星野リゾート / Zoff / クラシコム"]
- `reasons`系フィールドが**存在しない**ことを確認

#### パターン②：未分化判定（tomocari）／全タイプ均等
```
R=3, I=3, A=3, S=3, E=3, C=3
Q30=3, Q31=3, Q49=2, Q50=3, Q51=3
```
**期待結果**：
- `result_type` = `tomocari`
- `primary_companies` = `[]` / `secondary_companies` = `[]`
- `message` = 「今はまだ、特定のタイプに収まる時期ではありません。…」

### Step 4：「公開する」を押して反映

画面右上の「公開する」ボタンを押す。

### Step 5：MILへ返信

上記「❓ MILへの確認事項」のテンプレを使ってメール返信。

---

## 📚 参考ファイル（同ディレクトリ）

- `dify_code_v3.py` — 既存のコード（修正前のバックアップ的存在）
- `TOMOSHIKA_API_IF仕様書_MIL様向け_draft.md` — MIL向けAPI仕様書
- `TOMOSHIKA_APIエラーコード一覧_MIL様向け_draft.md` — エラーコード一覧
- `TOMOSHIKA_ロジック整理_三者会議用.md` — ロジック議論ログ
- `api_output_explanation.md` — API出力の説明書

> ⚠️ `dify_code_v3.py` も整合性を取るため**修正後のコードに更新する必要あり**（このタスクに含める）。

---

## 🔗 メモリ参照

- [中西製作所エンジニア木村さん](memory:reference_nakanishi_engineer.md)

---

## ⏰ 期日感

MIL曰く「今週から実装対応を進めてまいりますため、なるべく早いお返事をお待ちしております」。
→ **2026/04/28〜04/30 中に修正＋返信完了**が望ましい。
