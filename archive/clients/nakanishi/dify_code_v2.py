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
            "primary_companies": "該当なし",
            "primary_reasons": "該当なし",
            "secondary_companies": "該当なし",
            "secondary_reasons": "該当なし",
            "message": "今はまだ、特定のタイプに収まる時期ではありません。焦って就職先を決める前に、トモキャリで「一生使える自分の武器」を見つける旅を始めましょう。",
        }

    # ==============================
    # Step 2: 行動特性判定
    # 【変更】Q50 >= 3（BtoB志向）を条件に追加。
    #         BtoC寄りの学生には中西を案内せず、Step 4で通常判定に回す。
    # ==============================
    if Q30 >= 4 and Q31 >= 4 and Q50 >= 3:
        companies = company_db["nakanishi"]["BtoB"]
        names = " / ".join([c["group"] for c in companies])
        reasons = " | ".join([c["reason"] for c in companies])
        return {
            "result_type": "nakanishi",
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "primary_companies": names,
            "primary_reasons": reasons,
            "secondary_companies": "該当なし",
            "secondary_reasons": "該当なし",
            "message": "あなたの主体性と変革意欲は、安定基盤×ベンチャー志向の企業で大きく花開きます。",
        }

    # ==============================
    # Step 3: タイプ×志向判定
    # 【変更】Q50 >= 3（BtoB志向）を条件に追加。
    #         BtoC寄りの学生には中西を案内せず、Step 4で通常判定に回す。
    # ==============================
    nakanishi_types = {"E", "I", "A"}
    top2 = {primary_type, secondary_type}
    q50_q51_avg = (Q50 + Q51) / 2

    if top2 & nakanishi_types and q50_q51_avg >= 3.0 and Q50 >= 3:
        companies = company_db["nakanishi"]["BtoB"]
        names = " / ".join([c["group"] for c in companies])
        reasons = " | ".join([c["reason"] for c in companies])
        return {
            "result_type": "nakanishi",
            "primary_type": primary_type,
            "secondary_type": secondary_type,
            "primary_companies": names,
            "primary_reasons": reasons,
            "secondary_companies": "該当なし",
            "secondary_reasons": "該当なし",
            "message": "あなたの志向性とBtoB・インフラへの適性は、社会基盤を支える企業で活かされます。",
        }

    # ==============================
    # Step 4: 通常判定
    # ==============================
    # 1位タイプの企業グループ
    p_companies = company_db[primary_type][btob_flag]
    p_names = " / ".join([c["group"] for c in p_companies])
    p_reasons = " | ".join([c["reason"] for c in p_companies])

    # 2位タイプの企業グループ（補足）
    s_companies = company_db[secondary_type][btob_flag]
    s_names = " / ".join([c["group"] for c in s_companies])
    s_reasons = " | ".join([c["reason"] for c in s_companies])

    return {
        "result_type": "type_match",
        "primary_type": primary_type,
        "secondary_type": secondary_type,
        "primary_companies": p_names,
        "primary_reasons": p_reasons,
        "secondary_companies": s_names,
        "secondary_reasons": s_reasons,
        "message": f"あなたは{primary_type}型の特性が最も強く、{secondary_type}型の側面も備わっています。",
    }
