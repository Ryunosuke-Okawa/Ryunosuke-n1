---
title: SaaS料金体系ベンチマーク調査（AI時代の設計指針）
date: 2026-04-22
tags:
  - research
  - SaaS
  - pricing
  - kawaru
  - benchmark
status: final
related:
  - "[[Yoom_pricing_analysis_20260416]]"
  - "[[kawaru_lp_plan_comparison_20260420]]"
---

# SaaS料金体系ベンチマーク調査（AI時代の設計指針）

**目的**：Kawaru料金体系設計のため、世の中のSaaSツール（特にAI系）の料金体系を網羅的に調査し、設計原理を抽出する
**調査対象**：主要SaaS 35サービス／約80プラン（2026年4月時点）
**現行Kawaru料金案**：TRIAL（無料14日／1名）｜PERSONAL（¥9,000／月・1名）｜TEAM（¥14,900／人・月／5名〜）

---

## 用語の定義（冒頭でまとめて）

本レポートで出てくる課金方式の日本語定義。

| 用語 | 意味 | 代表例 |
|------|------|--------|
| **座席課金**（1人あたり課金、いわゆる per-seat） | 利用人数に比例して料金が決まる。1アカウント=1席の発想 | Notion、Slack、Kawaru現行TEAM |
| **従量課金**（使った分だけ課金、いわゆる usage-based） | タスク実行数・トークン数・ワークフロー実行回数など、使った量で料金が決まる | Zapier、Make、Yoom（2026/5〜） |
| **定額制**（一律料金、いわゆる flat-rate） | 人数や利用量に関係なく、組織単位で同じ料金 | SHIFT AI、Kawaru現行PERSONAL |
| **成果課金**（いわゆる outcome-based） | 「解決したチケット数」「削減した工数」など、プロダクトが生んだ成果に対して課金 | Intercom Fin（$0.99／解決1件） |
| **複合型**（いわゆる hybrid） | 基本料金＋従量など2軸以上を組み合わせた方式 | Yoom新体系、Cursor Business |
| **PLG**（プロダクト主導型成長） | 営業ではなくプロダクト体験そのものが顧客獲得・拡大を牽引する事業モデル | Notion、Slack、Zapier |
| **無料プラン無期限**（いわゆる Free tier） | 機能や利用量に制限はあるが、期間無制限で無料で使える層 | Notion Free、Slack Free |
| **閲覧専用アカウント**（いわゆる View-Only Seat） | 読み取りだけ可能な無料または低価格アカウント。情報共有の摩擦を下げる役割 | HubSpot、Figma |

---

## 🎯 エグゼクティブサマリー

世の中のSaaS料金体系は、AI時代の到来で**構造変化の只中**にある。キーワードは3つ。

1. **座席課金からの脱却**：座席課金の採用率は2024年64% → 2025年57%に低下。業務自動化系（Zapier／Make／n8n／Yoom／IFTTT）は全社「ユーザー無制限＋従量課金」に移行済み。
2. **無料プラン（無期限）が標準装備**：調査34サービス中28で無期限無料プランあり。「14日トライアルのみ」は業界と逆行するリスク。
3. **「何人から」下限表現は少数派**：調査34プラン中わずか4件（12%）。多数派は「1名から／座席課金」または「人数無制限／定額制」。

**Kawaru料金案の位置づけ**：PERSONAL ¥9,000（約$60相当）はグローバル上位26%。TEAM ¥14,900／人（約$100相当）は座席課金系で上位10%。**価格帯は高めに振れており、座席課金 × 下限設定（5名〜）× 高単価という設計は業界トレンドの真逆に立っている**。

ただし、これは単純に「間違い」ではない。**Kawaruが「AIが自動化してくれる業務量」と「ワークフローを作る／管理する人数」のどちらに価値の軸を置くかで、最適な料金表は変わる**。本レポートは判断材料を提供する。

---

## 1. 世の中のSaaS料金体系：事実ベースの全体像

### 1.1 人数表現パターン（34プラン集計）

| パターン | 件数 | 割合 | 代表例 |
|----------|------|------|--------|
| **人数無制限**（定額制） | 11 | 32% | Zapier全プラン、Make全プラン、Yoomサクセス、IFTTT、n8n Cloud |
| **1名あたり課金**（座席課金） | 14 | 41% | Notion／Slack／Figma／HubSpot／Asana／Salesforce／Zoom／Perplexity |
| **「〜名まで」上限表記** | 5 | 15% | Yoom ミニ20名・チーム100名、Dify Pro 3・Team 50 |
| **「〜名から」下限表記** | 4 | 12% | ChatGPT Business（2名〜）、Claude Team（5名〜）、Dropbox（3名〜）、**Kawaru TEAM（5名〜）** |

> **観察**：「〜名から」下限表記は少数派（12%）。採用しているChatGPT Business・Claude Teamはいずれも大手LLM本家で、**「セールス主導で取りに行く層」を明示的に絞っている**商品。Dropboxの「3名〜」はビジネスプランの伝統的設計。Kawaruが並ぶのはこの4社のみ。
>
> 大川さんの「『何人以上』って見せ方ってあんまりしてない」という感覚は**データで裏付けられる**（ただし、大手LLMが採用しているのは事実）。

### 1.2 課金方式のパターン

| 課金方式 | 件数 | 代表例 | 特徴 |
|----------|------|--------|------|
| **座席課金**（純粋型） | 11 | 汎用SaaS全般、Perplexity | 予測可能性が高い、AIと相性が悪い |
| **従量課金** | 7 | Zapier／Make／n8n／Yoom／Dify／IFTTT／Adobe | 価値と連動、変動コストを顧客に転嫁できる |
| **複合型**（座席＋クレジット等） | 3 | Cursor Business、ChatGPT Business、Claude Team | 新世代の主流 |
| **成果課金** | 1 | Intercom Fin（1解決あたり$0.99） | ROI透明だが「成功するほど請求増」のパラドックス |
| **定額制**（人数無制限） | 2 | SHIFT AI、Cursor個人 | シンプルさで訴求 |

**トレンドデータ**（Gartner／IDC／a16z／Bessemer 複数出典）：
- 座席課金の採用率：64%（2024）→ 57%（2025）
- 従量課金の採用率：45%（2021）→ 61%（2025）
- 純粋な座席課金の採用率：21% → 15%（1年で-6ポイント）
- **2026年までに70%の企業が座席課金より従量課金を選好**（Gartner予測）
- **2028年までに70%のSaaSベンダーが純粋な座席課金から脱却**（IDC予測）

### 1.3 主要プランの価格分布（最安有料プラン、月額USD換算）

| 価格帯 | 件数 | 代表例 |
|--------|------|--------|
| $3-5 | 1 | IFTTT Pro |
| $6-9 | 4 | MS365 Basic、Otter、ChatGPT Go、Make Core |
| $10-15 | 7 | Copilot、Notion Plus、Asana、Figma、MS365 Std、Zoom、Granola |
| $16-20 | 10 | Cursor、Dropbox、Zapier、ChatGPT Plus、Claude Pro、Perplexity、Notion Biz |
| $21-30 | 4 | MS365 Premium、ChatGPT Biz、Salesforce Starter、Asana Adv |
| $40-69 | 4 | Cursor Biz、Perplexity Ent、Zapier Team、Dify Pro |
| $100+ | 4 | HubSpot Pro、Salesforce Pro、Cursor Ultra、Perplexity Max |

**Kawaru換算**（$1=¥150）：
- PERSONAL ¥9,000 ≒ $60 → Dify Pro帯、全体で上位26%
- TEAM ¥14,900／人 ≒ $100 → HubSpot Pro／Salesforce Pro相当、座席課金系では上位10%

### 1.4 主要ツール別 料金早見表

#### カテゴリA：LLM本家
| サービス | 料金構造 | 人数扱い |
|---------|---------|---------|
| ChatGPT | Free／Go $8／Plus $20／Pro $200／Business $25-30／Enterprise要相談 | 個人1名、Business **2名〜** |
| Claude | Free／Pro $20／Max $100-200／Team Standard $20-25・Premium $100-125／Ent要相談 | Team **5名〜** |
| Gemini×Workspace | Starter $9.20／Std $18.40／Plus $22 | 1名あたり課金 |

#### カテゴリB：業務自動化ツール（Kawaruに最も近い）
| サービス | 料金構造 | 人数扱い |
|---------|---------|---------|
| Zapier | Free／Pro $20／Team $69／Ent要相談 | **全プラン人数無制限** |
| Make | Free／Core $9／Pro $16／Teams $29／Ent要相談 | **全プラン人数無制限** |
| n8n Cloud | Starter €24／Pro €60／Business €667／Ent要相談 | 実質人数無制限 |
| Dify Cloud | Sandbox $0／Pro $59／Team $159／Ent要相談 | **1名／3名まで／50名まで** |
| **Yoom新体系** | Free／Personal ¥2,400／Mini ¥16,000／Team ¥40,000／Success ¥80,000 | 1／1／**20まで**／**100まで**／**人数無制限** |
| IFTTT | Free／Pro $3.49／Pro+ $14.99 | 1名 |

#### カテゴリC：AI研修系（Kawaru直接競合）
| サービス | 料金構造 | 備考 |
|---------|---------|------|
| SHIFT AI | ¥21,780／月（税込）／一括¥547,800 | 個人向け定額制 |
| Jinba | Free＋要問合せ | ワークフロー自動化寄り |
| UOOM | 公開価格なし | 要問合せ商慣習 |
| exaBase DX | 要問合せ（2名×2週間トライアル） | 法人向け |

> 日本のAI研修系SaaSは**要問合せ型が商慣習**。Kawaruが公開価格＋セルフサインアップで入れれば、この市場で透明性の差別化要因になり得る。

#### カテゴリD：AIネイティブ
Cursor Hobby $0／Pro $20／Pro+ $60／Ultra $200／Business $40・Ent要相談（料金＝AIクレジット額）／GitHub Copilot Free／Pro $10／Pro+ $39／Business・Ent要相談／Perplexity Free／Pro $20／Max $200／Ent Pro $40・Max $325／Notion AI統合（$20／ユーザー）／Granola Free／Individual $18／Business $14・Ent $35／Otter Pro $8.33／Business $19.99／Ent要相談

#### カテゴリE：汎用SaaS（比較基準）
Notion Plus $10／Business $20／Ent $25-30（ゲスト無料）／Slack Pro $7.25／Biz+ $12.50／Grid要相談／Figma Pro $12／Org $45／Ent $90（アカウント種別4種、閲覧専用無料）／HubSpot Starter $15／Pro $100／Ent $150（閲覧専用無料）／Asana Starter $10.99／Adv $24.99／Ent $35／Ent+ $45／Zoom Pro $13.33／Business $18.33／Biz+ $29／Salesforce Starter $25／Pro $100／Ent $175／Unlimited $350／Agentforce1 $550／Dropbox Standard $18／Advanced $30（**3名〜**）／MS365 Basic $6／Standard $12.50／Premium $22

---

## 2. 論考：SaaS料金設計の3つの原理（弁証法的分析）

### 論点1：「階段設計」の本質は"段の数"ではなく"越える壁の最小化"

**業界通説**：無料 → 個人 → チーム → エンタープライズ の4段構造がPLG（プロダクト主導型成長）の定石。境界線は「顧客価値が非連続に跳ね上がる点」に引く。

**反論**：4段設計は「産業慣習」であって「原理」ではない。AIが価値の大半を生むプロダクトでは、機能・人数・サポートの3軸同時進行モデルは破綻する。

**結論**：階段設計の本質は、**段ごとに顧客が超える意思決定の壁を最小化すること**。壁は3つ — ①「試す壁」（認知→体験）②「払う壁」（体験→個人契約）③「広げる壁」（個人→組織契約）。各段の壁を一つずつ下げる設計になっているか？が評価軸。

### 論点2：「人数表現」は事業モデルの哲学の表出

| 表現 | 発信メッセージ | 商品観 |
|------|---------------|--------|
| 「〜名まで」（上限表記） | 「ここまでは面倒見る」 | パッケージ商品 |
| 「〜名から」（下限表記） | 「ここから取引開始」 | 法人営業商品 |
| 「1名あたり」（座席課金） | 「人数に比例して課金」 | 席売りツール |
| 「人数無制限」（定額制） | 「組織価値を提供」 | プラットフォーム |

「〜名から」下限表記は、**法人営業商品の発信**。LP主導の自己完結型購買導線とは構造的に相性が悪い。日本企業の稟議文化（小さく始めて効果検証→拡大）とも齟齬がある。

同じ価格を実現する表現の選択肢として：
- 「5名〜・¥14,900／人・月」→ 最低¥74,500 のコミットを最初に見せる（減算的）
- 「チームプラン基本料¥49,000／月（5席込み）、追加1名¥9,900」→ パッケージ＋追加席で同額を実現（加算的）

**支払総額は同じだが、稟議書の表題が「5名契約」から「チームプラン導入」に変わる**。これはただのフレーミングではなく、プロダクトの商品観の宣言。

### 論点3：座席課金 vs 従量課金 vs 定額制 の使い分け原理

課金方式は「プロダクトの価値創出メカニズムと一致させよ」という第一原理に帰着する。

| 課金方式 | 適合条件 | Kawaruへの適合度 |
|---------|---------|-----------------|
| 座席課金（1人あたり） | 人が操作することで価値が出る／予測可能性重視 | 部分適合 |
| 従量課金（使った分だけ） | 利用量と価値が線形／コスト変動を転嫁したい | 高適合（ワークフロー実行数） |
| 成果課金（削減工数等） | 成果が明確に測定可能／性能に自信がある | 中適合（削減工数） |
| 定額制（人数無制限） | 原価が急速に低下／単純さで差別化 | 中適合（シンプルさで日本市場に刺さる） |

2026年のコンセンサスは**複合型**（基本サブスク＋従量／成果アドオン）。純粋単一モデル比+21%の成長率（Monetizely 2026）。Yoomの2026年5月改定（ライセンス課金廃止＋タスク課金強化）も同じ構造転換。

**Kawaruの核心問い**：
> **「Kawaruは『席を売る』のか、『業務成果を売る』のか？」**
>
> この一問への答えが、料金表の全ての表現・数字・軸を規定する。

---

## 3. Kawaru現行案への批判的視点（Devil's Advocate）

### 3.1 盲点ベスト3（リサーチャーC判定）

#### 1位：座席課金 × 高単価のAI時代リスク
業界全体が座席課金から脱却に動く中、2026年ローンチの新規SaaSが座席課金で¥14,900／人は**構造的に逆行**。Yoomが2026年5月に座席課金（ライセンス課金）廃止へ動いた事例を見れば、Kawaruも遠からず同じ修正を迫られる可能性が高い。**既存契約との整合性問題が後から発生する**リスクを今から認識しておくべき。

#### 2位：PERSONAL→TEAMの8.3倍ジャンプ
¥9,000 → ¥74,500（最低）の飛躍は業界標準の3〜5倍を大幅に超える。**PLGの拡大経路（個人→チーム展開）が物理的に断絶**。TRIALはTEAM機能を体験させる設計だが1名のみ=組織内共有の核心価値が体験不可能という矛盾。

#### 3位：競合との異常な価格差
| サービス | 5名チーム月額 | 1名あたり | Kawaru比 |
|---------|-------------|----------|---------|
| Zapier Team | 約¥10,400（$69、人数無制限） | 約¥2,080 | **1/7** |
| Yoom Team | ¥40,000（100名まで） | ¥400 | **1/37** |
| **Kawaru TEAM** | **¥74,500（5名）** | **¥14,900** | **1倍** |

Yoom比37倍、Zapier比7倍。稟議で必ず作られる比較表で独自価値の強い訴求がないと即脱落。

### 3.2 その他の盲点

- **下限5名のFAQ地獄**：「4名でも契約できますか？」「6人目追加は？」「5名分まとめて誰が払う？」がLP公開初週から殺到する予測
- **TEAM限定機能の価値説明不足**：「組織内テンプレ共有」は組織1度の実装で済む機能なのに、人数×¥5,900上乗せは過剰感
- **比較表の×印配置矛盾**：「TEAMだけセミナー×」は組織導入者が「TEAMにセミナー付けないのはなぜ？」と混乱
- **税抜表記の罠**：¥14,900（税抜）→¥16,390（税込）、5名で¥81,950／月、年¥983,400。LP一瞥時と契約時金額の乖離で信頼毀損リスク

---

## 4. 具体的事例研究（設計ヒント集）

### 事例1：Zapierのタスク課金（座席課金完全廃止）
Team $69／月で人数無制限。タスク実行数＝価値提供量と連動。社内展開の摩擦ゼロが最大の武器。

### 事例2：Yoom 2026年5月 改定
ライセンス課金（人数課金）廃止（ミニ3→20、チーム10→100、サクセス20→無制限）、基本料金+67%。Free→ミニ¥9,600の断崖をPersonal¥2,400で埋めた（有料転換率改善狙い）。

### 事例3：Intercom Fin の成果課金
1解決あたり$0.99。AIが解決したときだけ課金＝ROI透明。年間経常収益（ARR）$1M→$100M+に急伸。ただし「成功するほど請求が増える」パラドックス。

### 事例4：Adobe 生成クレジット
AIの計算費用を既存SaaS料金に内包、月次付与＋繰越なし（使用圧力＝アップセル機会）。

### 事例5：Cursor「プラン料金＝AIクレジット額」
Pro $20＝月$20分のプレミアムモデル利用枠。Auto modeは無制限。支払額とAIコストが1:1。透明性で信頼獲得。

### 事例6：Claude Team のStandard/Premium混在
最小5アカウント、Standard $20＋Premium $100を混在可能。パワーユーザーとカジュアルユーザーを1契約で運用できる柔軟性。

### 事例7：HubSpot 閲覧専用 / Figma 閲覧専用アカウント
閲覧専用は無料・人数無制限。情報共有の摩擦を下げる＝導入拡大の潤滑油。Kawaruでも「閲覧専用メンバー」の概念導入で組織内展開の摩擦を下げる余地あり。

### 事例8：Dropboxの「3名から」
下限設定型座席課金の数少ない採用例。ただしDropboxは「ファイル共有が本質＝3名以上で意味を持つ」という機能的理由があり、下限設定の正当性がプロダクト側に内在している。Kawaruが下限を設けるなら同等の機能的正当性の説明が必要。

---

## 5. Kawaru料金設計への示唆（判断材料）

※ ここは「こうすべき」ではなく「判断のための論点」として整理。

### Q1：Kawaruの価値軸は「席」か「業務量」か？
- 「席」を軸にするなら → 座席課金は整合的。ただし業界トレンドと逆行する説明責任を負う
- 「業務量」を軸にするなら → ワークフロー実行数／タスク数ベースの従量課金を検討すべき
- 「複合型」なら → 基本料金＋従量の2階建て設計（Yoom、Cursor型）

### Q2：「5名から」を維持するか、別のフレーミングにするか？
- 維持する → 「なぜ5名？」の機能的正当性を明示する必要（Dropbox型の説明責任）
- 基本料＋追加席にする → 支払総額同じでも心理ハードルと稟議摩擦が下がる（¥49,000基本＋¥9,900追加など）
- 1名から座席課金にする → Notion／Slack／Asana型。ただしTEAM独自価値（組織内共有・専任CS）の位置づけを機能差で説明する必要

### Q3：PERSONAL→TEAMの間に中間層が必要か？
- 2名／3名／4名チームの受け皿：業界的には必ずしも必要ない（Slack等は1名→人数無制限）が、現行案は8.3倍ジャンプなので緩衝材がないと個人複数契約に流れる
- Yoomが採ったのは「Personal→Mini（20名まで）」の拡張型。「下限なし」で人数拡張に応じて次プランに自動遷移する設計

### Q4：無料プランはTRIAL（14日）のみで十分か？
- 業界標準は「無期限無料＋機能制限」（調査34社中28社）
- 14日トライアルのみは業界と逆行。業務に定着する前に切れるリスク
- 代替案：「月◯回のワークフロー実行まで無料」型の無期限無料プラン

### Q5：β版期間の料金に期間限定の明示が必要か？
- 将来改定の摩擦を避けるなら「β版価格は期間限定、正式版で改定予定」と最初から明示するのが定石
- 現行案のまま固定するなら、6ヶ月後の改定時に既存契約の救済が必要

---

## 6. 結論：3つの問いに答えることが料金表をつくる

1. **Kawaruは『席を売る』のか、『業務成果を売る』のか？**
2. **『5名から』は機能的必然か、それとも営業的都合か？**
3. **β版の料金は"正式版まで暫定"か、"最終形"か？**

これらの答えが、下記を一意に規定する：
- 課金方式（座席課金／従量課金／定額制／複合型）
- 人数表現（上限表記／下限表記／座席課金／人数無制限）
- 階段の段数と境界
- 無料プランの設計
- 改定前提の有無

一般論としての「ベストプラクティス」は存在する。ただし**それを無批判に踏襲するのは、プロダクトの思想を料金表に反映するチャンスを逃すこと**。大川さんがまず決めるべきは、価格の数字ではなく、Kawaruが立つ思想的立ち位置。

---

## 関連資料

- [[Yoom_pricing_analysis_20260416]] — Yoom 2026年5月料金改定の背景分析（座席課金脱却トレンドの起点）
- [[kawaru_lp_plan_comparison_20260420]] — 現行Kawaru LPプラン比較表（Notion貼付用）
- [[kawaru_launch_plan_20260409]] — β版ローンチ計画
- [[kawaru_cs_設計_20260418]] — CS体制設計（TEAM専任CSの位置づけ根拠）

---

## 情報ソース

### トレンド・論考
- [MindStudio: SaaS Pricing Is Breaking — Per-Seat in AI Era](https://www.mindstudio.ai/blog/saas-pricing-ai-agent-era)
- [Pilot: New Economics of AI Pricing 2026](https://pilot.com/blog/ai-pricing-economics-2026)
- [Monetizely: 2026 Guide to SaaS, AI, Agentic Pricing](https://www.getmonetizely.com/blogs/the-2026-guide-to-saas-ai-and-agentic-pricing-models)
- [a16z: AI Is Driving Shift to Outcome-Based Pricing](https://a16z.com/newsletter/december-2024-enterprise-newsletter-ai-is-driving-a-shift-towards-outcome-based-pricing/)
- [Bessemer: AI Pricing & Monetization Playbook](https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook)
- [ProductLed: PLG Predictions 2026](https://productled.com/blog/plg-predictions-for-2026)
- [PipelineRoad: SaaS Pricing Page Best Practices 2026](https://pipelineroad.com/agency/blog/saas-pricing-page-best-practices)
- [Schematic HQ: Seat-Based Pricing 101](https://schematichq.com/blog/seat-based-pricing-101-the-classic-saas-model-that-still-works-sometimes)
- [The Register: Salesforce Seat-Based AI Licensing](https://www.theregister.com/2025/12/12/ai_agents_salesforce_pricing/)
- [PinkLime: The Death of Per-Seat Pricing](https://pinklime.io/blog/future-saas-pricing-ai-era)
- [Rejoicehub: Agent-First Pricing in 2026](https://rejoicehub.com/blogs/agent-first-pricing-why-per-seat-saas-pricing-is-broken)
- [SaaS Mag: Hybrid Pricing in SaaS 2026](https://www.saasmag.com/hybrid-pricing-saas-growth-2026/)
- [Monetizely: The Anchoring Effect in SaaS Pricing](https://www.getmonetizely.com/articles/the-anchoring-effect-in-saas-pricing-using-high-prices-to-drive-sales)

### LLM本家
- [ChatGPT Pricing](https://chatgpt.com/pricing/)
- [Claude Pricing](https://claude.com/pricing)
- [Claude Team Plan](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)
- [Google Workspace Pricing](https://workspace.google.com/pricing)

### 業務自動化ツール
- [Zapier Pricing](https://zapier.com/pricing)
- [Make Pricing](https://www.make.com/en/pricing)
- [n8n Pricing](https://n8n.io/pricing/)
- [n8n New Pricing Blog](https://blog.n8n.io/build-without-limits-everything-you-need-to-know-about-n8ns-new-pricing/)
- [Dify Pricing](https://dify.ai/pricing)
- [IFTTT Plans](https://ifttt.com/plans)

### AI研修系
- [SHIFT AI](https://shift-ai.co.jp/)
- [Jinba Pricing](https://jinba.io/ja/pricing)
- [exaBase DX](https://exawizards.com/eai/)

### AIネイティブ
- [Cursor Pricing](https://cursor.com/pricing)
- [GitHub Copilot Plans](https://github.com/features/copilot/plans)
- [Perplexity Enterprise](https://www.perplexity.ai/enterprise/pricing)
- [Granola Pricing](https://www.granola.ai/pricing)
- [Otter Pricing](https://otter.ai/pricing)

### 汎用SaaS
- [Notion Pricing](https://www.notion.com/pricing)
- [Slack Pricing](https://slack.com/pricing)
- [Figma Pricing](https://www.figma.com/pricing/)
- [Asana Pricing](https://asana.com/pricing)
- [Zoom Pricing](https://zoom.us/pricing)
- [Salesforce Pricing](https://www.salesforce.com/pricing/)
- [Dropbox Business](https://www.dropbox.com/business/plans-comparison)
- [HubSpot Pricing](https://cargas.com/software/hubspot/pricing/)

### 特殊事例
- [Intercom Pricing](https://www.intercom.com/pricing)
- [Fin.ai Pricing](https://fin.ai/pricing)
- [Adobe Generative Credits FAQ](https://helpx.adobe.com/creative-cloud/apps/generative-ai/generative-credits-faq.html)
