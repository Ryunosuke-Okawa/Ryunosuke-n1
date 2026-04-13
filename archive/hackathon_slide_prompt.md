# PPTX再現プロンプト
## AIハッカソン発表資料「資料作成の効率化が、新規事業の売上を最大化させる」

---

## 指示

以下の仕様に従い、`pptxgenjs` を使ってPPTXを生成するNode.jsスクリプトを作成し、実行してください。
出力先: `/Users/kyouyuu/claude/output/hackathon_v2.pptx`
生成後、`/Users/kyouyuu/Downloads/` にコピーし、Google Drive（account: main）にアップロードしてGoogle Slidesに変換してください。

---

## 技術仕様

```
ライブラリ: pptxgenjs（npm install pptxgenjs）
レイアウト: LAYOUT_WIDE（13.33" × 7.5"）
座標単位: インチ（"）
```

---

## デザインシステム

### カラーパレット
```js
const C = {
  teal:      "0891B2",  // メインアクセント（ティール）
  tealDark:  "076A87",  // ティール濃
  tealMid:   "5BB8D4",  // ティール中間
  tealLight: "E0F2F7",  // ティール薄（カード背景）
  tealPale:  "F0FAFD",  // ティール極薄
  dark:      "1F2937",  // 本文テキスト（ダークグレー）
  gray:      "6B7280",  // サブテキスト
  lgray:     "E5E7EB",  // ボーダー・区切り線
  xlgray:    "F3F4F6",  // テーブル背景・薄グレー
  white:     "FFFFFF",
  red:       "DC2626",
  green:     "059669",
};
```

### レイアウト定数
```js
const SW = 13.33;         // スライド幅
const SH = 7.5;           // スライド高さ
const MX = 0.5;           // 左右マージン
const CW = SW - MX * 2;  // コンテンツ幅 = 12.33
```

### 共通ヘルパー関数

**hdr(s, title, sub)**
- 上部ティールバー: x=0, y=0, w=SW, h=0.15, fill=teal
- タイトル: x=MX, y=0.22, w=CW, h=0.62, fontSize=27, bold, color=dark
- サブタイトル（任意）: x=MX, y=0.84, w=CW, h=0.3, fontSize=12.5, color=gray

**insightBar(s, txt)**
- バー: x=0, y=6.9, w=SW, h=0.52, fill=tealLight, border=teal
- テキスト: fontSize=12, bold, color=tealDark, align=center, valign=middle

**card(s, x, y, w, h, opts)**
- opts: fill, line(border color), lw(border width), shadow(boolean)
- shadow設定: type=outer, blur=5, offset=2, angle=45, color=AAAAAA, opacity=0.2

### フォント・タイポグラフィ
- fontFace: "Arial"（全スライド統一）
- スライドタイトル: 27pt, bold, color=dark
- セクションタイトル: 15〜17pt, bold, color=teal or tealDark
- 本文: 11.5〜13pt, color=dark
- キャプション・注記: 10〜11pt, color=gray, italic

### 背景
- 全スライド: 白（FFFFFF）
- 濃色背景・グラデーション禁止

---

## スライド仕様（全11枚）

---

### SLIDE 1 — タイトル

**構成要素:**
- 上部ティールバー: x=0, y=0, w=SW, h=0.22
- 下部ティールバー: x=0, y=7.22, w=SW, h=0.28
- 左アクセントバー（縦）: x=0.5, y=1.6, w=0.1, h=2.6, fill=teal
- メインタイトル: `"資料作成の効率化が、\n新規事業の売上を最大化させる"` x=0.82, y=1.5, w=11.2, h=2.8, fontSize=38, bold, color=dark, lineSpacingMultiple=1.35
- サブタイトル: `"提案資料作成の変革による営業力強化"` x=0.82, y=4.45, w=10, h=0.55, fontSize=17, color=gray
- 区切り線: x=0.82, y=5.15, w=5.5, h=0, color=lgray
- タグ: `"AIハッカソン　｜　新規事業部　大川龍之介"` x=0.82, y=5.3, w=10, h=0.38, fontSize=13.5, color=gray

---

### SLIDE 2 — なぜ「提案資料」が重要なのか

**ヘッダー:**
- title: `"なぜ「提案資料」が重要なのか"`
- sub: `"良いプロダクトも、顧客に伝わらなければ価値がない"`

**本体: 2カラムカード（各 cY=1.2, cH=5.45, cW=5.85）**

**左カード（x=MX）: 顧客との接点最大化**
- fill=tealLight, border=teal, lw=1.5
- 上部ティールバー: h=0.12
- カードタイトル: `"顧客との接点最大化"` y=cY+0.2, fontSize=15, bold, color=tealDark
- フロー図（縦3段、y=cY+0.85から1.35間隔）:
  - Box1: `"良いプロダクト"` fill=white, border=tealMid, h=0.72
  - 矢印↓: fontSize=18, color=teal
  - Box2: `"提案資料"` fill=teal, text=white（ハイライト）, h=0.72
  - 矢印↓
  - Box3: `"価値伝達"` fill=white, border=tealMid, h=0.72

**右カード（x=MX+cW+0.63）: リソースの最適配分**
- fill=tealLight, border=teal, lw=1.5
- 上部ティールバー: h=0.12
- カードタイトル: `"リソースの最適配分"` fontSize=15, bold, color=tealDark
- 項目1（y=cY+1.1）: 矢印↓（color=gray）+`"作成にかける時間 ↓"` fontSize=14, color=gray
- 区切り線
- 項目2（y=cY+3.2）: 矢印↑（color=teal）+`"商談・関係構築の時間 ↑"` fontSize=14, bold, color=teal
- 補足テキスト（y=cY+5.0）: `"「作成」ではなく「対話」に時間を使う必要がある"` fill=tealLight, fontSize=10.5

**インサイトバー:** `"示唆：資料作成プロセスこそが、営業活動の隠れたレバレッジポイント"`

---

### SLIDE 3 — 営業現場を縛る「資料作成の課題」

**ヘッダー:**
- title: `"営業現場を縛る「資料作成の課題」"`
- sub: `"1案件 半日〜1日の資料作成が、営業の行動量を制限している"`

**本体: 3カラムカード（cY=1.2, cH=5.45, cW=3.9, gap=0.265）**

各カード共通構造（x = MX + i*(cW+gap)）:
- 上部アクセントバー: h=0.1, fill=teal
- カード本体: fill=white, border=lgray, shadow=true

**カード01 — スピード不足（x=MX）**
- 番号`"01"`: fontSize=32, bold, color=tealLight
- タイトル`"スピード不足"`: fontSize=17, bold, color=teal, y=cY+0.95
- 区切り線
- 本文:
  ```
  商談後の提案資料は
  「当日〜翌日・次回商談」が業界標準

  商談直後の検討意欲が最も高いタイミングに
  資料が届かない
  ```
  fontSize=11.5, lineSpacingMultiple=1.45
- 補足: `"コア業務の時間減\nノンコア業務が増え、本来注力すべき業務に\n取りかかれない"` fontSize=10, gray, italic

**カード02 — 個別感ゼロ（x=MX+3.9+0.265）**
- 番号`"02"`
- タイトル`"個別感ゼロ"`
- 本文:
  ```
  決まったテンプレートで対応するため
  クライアント固有の課題・ゴールが
  資料に反映されない

  「どこにでもある資料」として受け取られ
  検討が前に進まない
  ```

**カード03 — 属人的バラつき（x=MX+(3.9+0.265)*2）**
- 番号`"03"`
- タイトル`"属人的バラつき"`
- 本文:
  ```
  テンプレ化されていない場合
  提案ロジックの精度が担当者によって大きく異なる

  トップ営業の思考・ロジックが
  組織に蓄積されない
  ```
- 補足: `"（現在は標準化対応済み）"` color=gray, italic

**インサイトバー:** `"示唆：資料作成の工数削減が、営業力解放の第一歩"`

---

### SLIDE 4 — 売上構造のロジックツリー（全体像）

**ヘッダー:**
- title: `"売上構造のロジックツリー（全体像）"`
- sub: `"売上を上げる打ち手は、構造的に特定できる"`

**本体: 5層のロジックツリー（startY=1.3, rH=0.62, rGap=0.32）**

各ボックスはrect shape + テキストの組み合わせ。

**ROW 1: 売上高**
- x=MX, y=startY, w=CW, h=rH
- fill=dark, text=white, fontSize=17, bold

**ROW 1→2 コネクター:**
- 中心から下へ垂直線、左右に水平線、両端から垂直線

**ROW 2: 成約数 | 受注単価**
- r2w=(CW-0.18)/2
- `"成約数"`: x=MX, fill=xlgray, color=dark, bold
- `"受注単価"`: x=MX+r2w+0.18, fill=xlgray, color=gray（グレーアウト）

**ROW 2→3 コネクター（成約数のみ）:**
- 成約数中心から分岐して3列へ

**ROW 3: ★提案数 | ★成約率 | （単価）（今回の注力ポイント★）**
- r3wはr2wの1/3
- `"★ 提案数"`: fill=tealLight, border=teal lw=2, color=tealDark, bold（ハイライト）
- `"★ 成約率"`: fill=tealLight, border=teal lw=2, color=tealDark, bold（ハイライト）
- `"（単価）"`: fill=xlgray, color=gray（グレーアウト）

**ROW 3→4 コネクター**

**ROW 4: 商談数 | 提案率 | 成約率 | （単価）**
- r4wActual=(r2w-0.27)/4
- fill=xlgray, color=dark（単価のみgray）, fontSize=12

**ROW 4→5 コネクター**

**ROW 5: リード数 | 商談化率 | 提案率 | 成約率 | （単価）**
- r5wActual=(r2w-0.32)/5
- fill=xlgray, color=dark（単価のみgray）, fontSize=11.5

**インサイトバー:** `"示唆：売上向上の打ち手は構造的に特定できる"`

---

### SLIDE 5 — 売上を最大化させる2つの変数

**ヘッダー:**
- title: `"売上を最大化させる2つの変数"`
- sub: `"「提案の数」を増やし、同時に「成約率」を上げる"`

**構成:**

**上部フォーミュラBOX（x=MX, y=1.25, w=CW, h=0.85）:**
- fill=xlgray, border=lgray
- テキスト: `"売上　＝　成約数　×　受注単価"` fontSize=20, bold, center

**矢印テキスト:** `"↓　注力ポイント"` y=2.15, fontSize=15, bold, color=teal, center

**2つのハイライトBOX（by=2.72, bH=1.9, bW=5.5）:**

左BOX（b1x=MX+0.5）:
- fill=tealLight, border=teal lw=2.5
- タイトル`"提案数"`: fontSize=30, bold, color=teal, center
- 説明: `"作成時間を半日→1時間に短縮\n1日複数案件の対応が可能になる"` fontSize=12.5, center

中央: `"×"` fontSize=26, bold, color=gray

右BOX（b2x=SW-MX-0.5-bW）:
- fill=tealLight, border=teal lw=2.5
- タイトル`"成約率"`: fontSize=30, bold, color=teal
- 説明: `"スピード × 個別最適化 × 品質標準化\nによる意思決定の後押し"`

**補足説明BOX（x=MX, y=4.75, w=CW, h=1.95, fill=xlgray）:**
2行:
- `"提案数↑の根拠"` + `"資料作成が半日〜1日から30〜60分に短縮 → 1日あたりの対応案件数が増加"`
- `"成約率↑の根拠"` + `"商談直後の送付（業界標準を大幅に超えるスピード）× ヒアリング内容の個別反映 × 髙橋COOのメソッドによる提案品質の標準化"`

**インサイトバー:** `"示唆：2つの変数を同時に改善することで売上最大化を実現"`

---

### SLIDE 6 — 定量根拠：速さと個別最適化が成約率を上げる

**ヘッダー:**
- title: `"定量根拠：速さと個別最適化が成約率を上げる"`
- sub: `"仮説ではなく、データが証明している"`

**本体: 左右分割（leftW=7.8, rightW=4.2, gap=0.33, startY=1.25）**

**左側: 4つのデータカード（縦積み）**
各カード高さ: (SH - startY - 0.7) / 4 - 0.12

各カードの構成:
- 左端ティールバー: w=0.1, fill=teal
- カード本体: fill=F9FAFB, border=lgray
- 出典テキスト: fontSize=10.5, color=gray
- 統計数値（大きく）: fontSize=30, bold, color=teal
- 単位ラベル: fontSize=13, bold, color=tealDark
- 説明文: fontSize=11.5, color=dark

| # | 出典 | 数値 | 単位 | 説明 |
|---|------|------|------|------|
| 1 | Harvard Business Review（224万件分析） | 7倍 | 受注率↑ | 商談後1時間以内の接触は\n1時間後より受注率が7倍高い |
| 2 | Google & CEB | 35〜50% | が受注 | B2B商談はファーストレスポンドした\n企業が受注する |
| 3 | McKinsey | +10〜20% | 成約率↑ | パーソナライズにより\n成約率・売上が向上する |
| 4 | QorusDocs（第7回年次調査） | +25% | 成約率↑ | 提案書の個別化で成約率が中央値+25%\n商談進捗速度+37%向上 |

**右側: エヌイチ実績BOX**
- fill=tealLight, border=teal lw=1.5
- 上部ティールバー: h=0.12
- タイトル: `"エヌイチ　AI-Pax実績"` fontSize=13.5, bold, color=tealDark
- サブ: `"2026年2月18〜19日 出展"` fontSize=10.5, gray
- 区切り線
- 4つの統計（縦積み、各高さ1.2"):

| ラベル | 数値 | 補足 |
|--------|------|------|
| 商談確定 | 19社 | （実質着席12件） |
| 受注見込み | 5社 | |
| 検討中 | 3社 | |
| 想定成約率 | ≒30% | |

数値: fontSize=28, bold, color=tealDark

---

### SLIDE 7 — 特定されたボトルネックと、既存AIでは解決できない理由

**ヘッダー:**
- title: `"特定されたボトルネックと、既存AIでは解決できない理由"`
- sub: `"「資料作成の都度カスタマイズ」が提案数・成約率向上を阻害している"`

**本体: 左右2分割（縦区切り線: x=6.15）**

**左側（lW=5.5）: ボトルネック構造**

セクションタイトル: `"ボトルネックの構造"` fontSize=13.5, bold, color=tealDark, y=1.25

フロー図（縦3段）:
1. `"提案資料の都度カスタマイズ"` fill=xlgray, border=lgray, h=0.65
2. 矢印↓
3. `"準備に 半日〜1日\n（ボトルネック）"` fill=teal, text=white, h=0.9（強調）
4. 矢印↓
5. `"提案数・成約率の向上　✗"` fill=FEF2F2, text=red, border=red, h=0.65

補足箇条書き（y=4.5）:
```
• コア業務の時間減：本来注力すべき商談・関係構築に取りかかれない
• 都度カスタマイズ：毎回ゼロから作り直す工数と精神的負荷
• 物理的限界：準備時間が重くのしかかり、商談数を増やせない
```
fontSize=11.5, lineSpacingMultiple=1.5

**縦区切り線:** x=6.15, y=1.25, h=5.45, color=lgray

**右側（rX=6.45）: 既存AIでは不十分な理由**

タイトル: `"なぜ既存スライドAIだけでは不十分か"` fontSize=13.5, bold, color=tealDark
サブ: `"Gamma / Manus / Genspark を使うだけでは解決しない"` fontSize=11, gray

**比較テーブル（tStartY=2.0）:**
- ヘッダー行:
  - 左: `"既存ツールで解決できること"` fill=lgray, color=gray, bold
  - 右: `"解決できないこと（本質）"` fill=teal, color=white, bold
- データ行（交互背景 F9FAFB / white）:

| 既存ツールで解決できること | 解決できないこと（本質）|
|--------------------------|------------------------|
| スライドのデザイン・見た目 | 商談ヒアリング内容の構造化 |
| テンプレートからの資料作成 | 髙橋メソッドに基づくロジック設計 |
| 汎用的な構成の提案 | クライアント固有の課題・ゴールの反映 |

右列テキスト: bold, color=tealDark

**下部コールアウトBOX（y=5.75, h=0.62）:**
fill=tealLight, border=teal lw=1.5
テキスト: `"必要なのは\nスピード × 個別最適化 × 品質標準化 の同時実現"`
fontSize=12, bold, color=tealDark, center

**インサイトバー:** `"示唆：ボトルネック解消が売上向上の最短ルート"`

---

### SLIDE 8 — AIがもたらす「時間の再定義」

**ヘッダー:**
- title: `"AIがもたらす「時間の再定義」"`
- sub: `"資料作成時間を 半日〜1日 から 30〜60分 へ短縮できる"`

**バーグラフ（MAX_BAR=7.5, barSX=3.8, labelX=MX, labelW=3.1）:**
各行の高さ間隔: 1.65, 開始y=1.35

**3行のデータ:**

| フェーズ | 従来 | AI活用後 | ratioB | ratioA |
|---------|------|---------|--------|--------|
| 骨子作成\n（構成・ロジック） | 約1時間 | 約5分 | 0.22 | 0.02 |
| スライド化 | 3〜4時間\n（深夜作業も） | 約5〜10分 | 1.0 | 0.05 |
| 修正・仕上げ | — | 約20〜30分 | 0.0 | 0.17 |

各行の構成:
- フェーズラベル（x=labelX）: fontSize=13, bold, color=dark
- 「従来」ラベル（右寄せ, x=barSX-0.55）: fontSize=10, color=gray
- 従来バー: fill=lgray, w=MAX_BAR*ratioB
- 従来値テキスト（バー右）: fontSize=12, color=gray
- 「AI後」ラベル（右寄せ）: fontSize=10, bold, color=teal
- AI後バー: fill=teal, w=MAX_BAR*ratioA
- AI後値テキスト（バー右）: fontSize=12, bold, color=tealDark
- 区切り線（最終行以外）

**3つの効果ボックス（y=5.6）:**

タイトル `"3つの効果"` fontSize=13, bold, y=5.58

各エフェクトBOX（efW=(CW-0.4)/3、高さ1.25、fill=tealLight、border=teal）:

| アイコン+タイトル | 説明 |
|-----------------|------|
| ⏱ 作成工数90%削減 | 半日〜1日 → 30〜60分\n圧倒的な時間創出 |
| 📐 質の標準化 | 髙橋COOのメソッドで属人化防止\n常に高い提案品質 |
| 🔄 作業から選択へ | ゼロから作らず\nAIの提案を選択・修正する |

---

### SLIDE 9 — 次世代資料作成ワークフロー

**ヘッダー:**
- title: `"次世代資料作成ワークフロー"`
- sub: `"商談終了から資料送付まで、ほぼ全自動"`

**5ステップ横並びフロー（sW=(CW-0.6)/5, sH=3.5, sY=1.35）:**
各ボックス幅: (12.33-0.6)/5 = 約2.35"
間隔: 0.15"

| ステップ | タイトル | サブ | 背景 |
|---------|---------|------|------|
| ① | 商談終了 | Notta文字起こし\nGoogle Driveに自動保存 | tealLight |
| ② | /proposal-outline\n実行 | ファイルを\n1クリック選択 | tealLight |
| ③ | 骨子を自動生成 | 髙橋メソッド自動適用\nロジック設計完了 | tealLight |
| ④ | 「OK」と入力 | スライド\n自動出力（5〜10分） | tealLight |
| ⑤ | ✅ 1時間以内\n送付完了 | Google Slides\n完成・送付 | teal（dark, text=white） |

各ボックスの構成:
- 円形ステップ番号（fill=teal dark版はtealDark）: fontSize=15, white
- タイトル（y=sY+1.0）: fontSize=12, bold
- 区切り線
- サブテキスト（y=sY+2.1）: fontSize=11
- ボックス間の矢印→: fontSize=16, bold, color=tealMid

注記（y=5.05）: `"※ 髙橋COO（事業部責任者）の知見・実績・提案ロジックが全提案に標準装備される"` italic, gray

**比較BOX（y=5.48）:**
- 左（w=CW/2-0.2）: fill=xlgray, `"従来：「作業」　ゼロから毎回作り直す"` color=gray
- 右（x=MX+CW/2+0.1）: fill=tealLight, border=teal, `"現在：「選択」　AIの提案から選ぶだけ"` bold, color=tealDark

---

### SLIDE 10 — 将来展望①：Kawaruシリーズへの統合

**ヘッダー:**
- title: `"将来展望①：Kawaruシリーズへの統合"`
- sub: `"今回の取り組みは、サービスそのものになる"`

**3層縦フロー（下に広がるピラミッド型）:**

| 層 | タイトル | 本文 | fill | w | offset |
|----|---------|------|------|---|--------|
| 1 | 今回の取り組み | Claude Code Skillで社内実装・実証完了\nエヌイチ新規事業部にて商談→提案資料作成を全自動化 | white | 8.5 | 1.5 |
| 2 | Kawaru Team（AI研修） | 「営業部門：提案資料作成効率化」を他社への研修として展開\n※ Kawaru Teamの研修カスタマイズ例として既に設計済み | tealLight | 10.5 | 0.5 |
| 3 | Kawaru SaaS（4月1日リリース予定） | このワークフロー自体をSaaSに組み込み、顧客へ提供\n「営業の資料自動化をしたい」という需要をKawaruが叶えられるようになる | teal（text=white） | 12.33 | 0 |

各層: h=1.2、間にティール矢印↓

**サマリーフロー（y=5.6, fill=tealLight）:**
`"自社で実証　→　研修で他社へ展開　→　SaaSに内包　→　売上直結"`
テキストを均等分割して横並び、fontSize=12.5, color=tealDark

---

### SLIDE 11 — 将来展望②：スクール事業部への横展開（私案）

**ヘッダー:**
- title: `"将来展望②：スクール事業部への横展開（私案）"`
- sub: `"同じ仕組みが、スクール事業の成約率を上げる可能性がある"`

**本体: 左右比較（colW=5.5, gap=0.83）**

**列ヘッダー（y=1.25, h=0.4）:**
- 左: `"現状"` fill=lgray, color=gray
- 右: `"提案"` fill=teal, color=white

**VS ラベル:** 中央（x=colW+MX+0.15）, fontSize=16, bold, color=gray

**左カラム（現状フロー）:**
1. `"前半ヒアリング（1〜1.5時間）"` fill=xlgray, h=0.7
2. 矢印↓（gray）
3. `"クロージング\n（全員が同じフォーマット）"` fill=FEF2F2, border=red, color=red, h=0.9
4. `"✗ 個別感なし → 検討が前に進まない"` color=red, bold, center

**右カラム（提案フロー）:**
1. `"前半ヒアリング（1〜1.5時間）"` fill=xlgray, h=0.7
2. 矢印↓（teal）
3. `"5分で個別提案資料を自動生成"` fill=teal, text=white, h=0.7
4. 矢印↓（teal）
5. `"後半クロージングで投影"` fill=tealLight, border=teal, color=tealDark, h=0.7
6. `"✓ インサイトに刺さる提案で意思決定を後押し"` color=green, bold, center

**4つの効果BOX（y=3.95, h=1.35, 横均等配置）:**

| タイトル | 説明 |
|---------|------|
| 成約率向上 | ヒアリング内容を反映した\n提案で意思決定を後押し |
| AI関心度向上 | 目の前でリアルタイム生成\n実演効果で関心が高まる |
| 標準化 | トップ営業のロジックを全員に\n属人性を排除 |
| 商談数増加 | 商談時間の短縮により\n1日の対応件数が増える |

各BOX: fill=tealLight, 上部バーh=0.1 fill=teal, border=teal

**課題注記（y=5.4, fill=xlgray）:**
`"⚠ 実現課題：文字起こしと録画の同時進行によるPC負荷、録画停止タイミングの調整など　→ 実現可能性は十分にあると判断"`
fontSize=10.5, color=gray

**下部フルティールバー（x=0, y=5.92, w=SW, h=0.58, fill=teal）:**
`"新規事業部での実証　→　スクール事業部へ横展開　→　会社全体の売上貢献へ"`
fontSize=14, bold, white, center

---

## 出力後の処理

1. ファイルを `/Users/kyouyuu/Downloads/` にコピー
2. `mcp__google-workspace__uploadFileToDrive` で Google Drive にアップロード
   - account: `main`
   - convertToGoogleFormat: `true`
   - fileName: `【AIハッカソン】提案資料自動化_新規事業部_大川龍之介`
3. アップロード完了後、Google SlidesのURLを返す
