"""
中西製作所 TOMOSHIKA Dify コード実行ブロック（v4）

更新日：2026-05-13
更新理由：
- 5/13 津丸様送付PDF「TOMOシリーズ構成案」に従い、企業マスタを5社×1配列に統一
- 各タイプの推薦理由文（40字程度）をPDF確定版に差し替え
- 5/13 MIL松橋様リクエスト対応：primary_type / secondary_type を日本語ラベルで返却
- BtoB/BtoC分岐を廃止（PDFはBtoB版のみ規定のため）
- secondary_companies は常に空配列。1位タイプの5社のみで完結する設計

出力ノードの構成（Dify画面側）は v3 と同一のまま：
  result_type / primary_type / secondary_type
  primary_companies / secondary_companies / message
"""


def main(R: int, I: int, A: int, S: int, E: int, C: int,
         Q30: int, Q31: int, Q49: int, Q50: int, Q51: int) -> dict:

    # ==============================
    # 企業マスタ（PDF確定版・5社×1配列）
    # ==============================
    company_db = {
        "nakanishi": ["中西製作所", "キーエンス", "平田機工", "マクニカ", "ダイフク"],
        "R": ["三菱電機", "村田製作所", "安川電機", "栗田工業", "THK"],
        "I": ["野村総合研究所", "島津製作所", "中外製薬", "オムロン", "ユーザーベース"],
        "A": ["電通", "博報堂", "チームラボ", "Sansan", "乃村工藝社"],
        "S": ["ベネッセ", "リクルートMS", "パソナ", "ワークスA", "LITALICO"],
        "E": ["三菱商事", "伊藤忠商事", "光通信", "サイバーエージェント", "レバレジーズ"],
        "C": ["日本生命", "東京海上日動", "三菱UFJ銀行", "富士通", "オービック"],
    }

    # ==============================
    # 日本語タイプラベル（MIL松橋様リクエスト対応）
    # ==============================
    type_labels = {
        "nakanishi": "中西製作所 親和性型",
        "R": "現実的型",
        "I": "研究的型",
        "A": "芸術的型",
        "S": "社会的型",
        "E": "企業的型",
        "C": "慣習的型",
        "tomocari": "未分化・低スコア層",
    }

    # ==============================
    # タイプ別 推薦理由文（PDF確定版・40字程度）
    # ==============================
    type_messages = {
        "nakanishi": "安定基盤を武器に自ら変化を創り出し、攻めの変革を促す変革者として上記企業を推薦します。",
        "R": "実体重視で成果を追求する職人であり、高い技術で産業の根幹を支えるため上記企業を推薦します。",
        "I": "法則を解明する分析家であり、緻密な論理で複雑な社会課題に解を創出するため上記企業を推薦します。",
        "A": "直感で価値を提示する表現者であり、表現力でビジネスに命を吹き込み実装するため上記企業を推薦します。",
        "S": "調和を尊ぶサポーターであり、対人支援を通じ誰もが輝く社会基盤を築くため上記企業を推薦します。",
        "E": "目標を追求するリーダーであり、圧倒的意欲で巨額の投資や組織を動かすため上記企業を推薦します。",
        "C": "正確性を重んじる管理者であり、揺るぎない信頼で経済基盤を着実に運用するため上記企業を推薦します。",
        "tomocari": "今は特定の型に収まる時期ではありません。焦らず「トモキャリ」を通じて一生使える自分の武器を見つける旅から始めることを推薦します。",
    }

    # ==============================
    # Step 0: L尺度補正
    # ==============================
    scores = {"R": R, "I": I, "A": A, "S": S, "E": E, "C": C}
    if Q49 == 5:
        scores = {k: v * 0.8 for k, v in scores.items()}

    # スコアランキング算出
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_key = sorted_types[0][0]
    secondary_key = sorted_types[1][0]
    max_score = sorted_types[0][1]
    min_score = sorted_types[-1][1]

    # ==============================
    # Step 1: 未分化判定（最優先）
    # ==============================
    if max_score - min_score <= 1.0:
        return {
            "result_type": "tomocari",
            "primary_type": type_labels["tomocari"],
            "secondary_type": "",
            "primary_companies": [],
            "secondary_companies": [],
            "message": type_messages["tomocari"],
        }

    # ==============================
    # Step 2: 行動特性判定（中西親和性型）
    # ==============================
    if Q30 >= 4 and Q31 >= 4 and Q50 >= 3:
        return {
            "result_type": "nakanishi",
            "primary_type": type_labels["nakanishi"],
            "secondary_type": "",
            "primary_companies": company_db["nakanishi"],
            "secondary_companies": [],
            "message": type_messages["nakanishi"],
        }

    # ==============================
    # Step 3: タイプ×志向判定（中西親和性型）
    # ==============================
    nakanishi_types = {"E", "I", "A"}
    top2 = {primary_key, secondary_key}
    q50_q51_avg = (Q50 + Q51) / 2

    if top2 & nakanishi_types and q50_q51_avg >= 3.0 and Q50 >= 3:
        return {
            "result_type": "nakanishi",
            "primary_type": type_labels["nakanishi"],
            "secondary_type": "",
            "primary_companies": company_db["nakanishi"],
            "secondary_companies": [],
            "message": type_messages["nakanishi"],
        }

    # ==============================
    # Step 4: 通常判定（タイプマッチ）
    # ==============================
    return {
        "result_type": "type_match",
        "primary_type": type_labels[primary_key],
        "secondary_type": type_labels[secondary_key],
        "primary_companies": company_db[primary_key],
        "secondary_companies": [],
        "message": type_messages[primary_key],
    }
