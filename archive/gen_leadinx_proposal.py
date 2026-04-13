"""
リードインクス株式会社 向け提案書生成スクリプト
"""
import sys
sys.path.insert(0, '/Users/kyouyuu/cloude/output')

from slide_builder import ProposalBuilder, C, FONT, M, CW, SLIDE_W, SLIDE_H
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

CLIENT = 'リードインクス株式会社'
DATE = '2026年3月24日'
OUTPUT = '/Users/kyouyuu/cloude/output/proposal_leadinx_20260324.pptx'

b = ProposalBuilder(CLIENT, DATE)

# ======================================================
# スライド1: 表紙
# ======================================================
b.cover()

# ======================================================
# スライド2: 会社概要
# ======================================================
b.company_overview()

# ======================================================
# スライド3: 導入実績
# ======================================================
b.case_studies()

# ======================================================
# スライド4: 前回の振り返り
# ======================================================
b.status_issues(
    review_items=[
        ('日時',   '2026年2月27日（約46分）/ オンライン'),
        ('参加者', '呉振宇様（SaaS本部長） / 大川・髙橋（エヌイチ）'),
        ('経緯',   '年会エクスポーでの名刺交換後 初回商談'),
        ('内容',   'エヌイチ4サービス紹介 → LINX社AI活用課題ヒアリング'),
        ('反応',   'Kawaru Teamに強い関心。費用・形式・言語対応を深掘り'),
    ],
    conclusion='社長との1on1（翌週木曜）で研修の件を相談 → OKが出たら研修設計に着手',
    issues=[
        ('呉様 → 社長1on1で研修を相談', '来週木曜の定例1on1で研修の件を持ち上げる'),
        ('エヌイチ → 商談概要メール送付', '当日の商談内容をメールで送付済み ✅'),
        ('本日のゴール', '提案内容を確認し、社長への稟議を通すための材料を揃える'),
    ],
    right_title='合意ネクストアクション',
    right_bar_color=C['accent'],
    right_item_bg=C['highlight'],
    right_item_bar=C['accent'],
)

# ======================================================
# スライド5: 現状① 組織構造
# ======================================================
def slide_org_structure(b):
    slide = b._slide(); b._bg(slide)
    y = b._title_bar(slide, '2本部・50〜60名のエンジニア組織', '現状①  組織構造')

    # 左パネル: 数値バッジ + 組織概要
    lw = 5.80
    b._rect(slide, M, y, lw, 5.60, C['white'], rounded=True)
    b._rect(slide, M, y, 0.06, 5.60, C['accent'])

    b._section_head(slide, M + 0.20, y + 0.15, lw - 0.30, '会社・事業概要')
    iy = y + 0.60
    rows = [
        ('会社名', 'リードインクス株式会社'),
        ('グループ', 'ソフトバンクグループ会社'),
        ('事業', '保険業界向けSaaSプロダクト（保険会社・代理店向け）'),
        ('顧客', '保険会社 / 保険代理店'),
        ('現状', '伝統的フォーム形式のSaaSを提供。AI機能対応が急務'),
    ]
    for label, val in rows:
        b._block(slide, M + 0.20, iy, 1.20, 0.30, label, 10,
                 bg=C['light_acc'], tc=C['accent'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.03)
        b._block(slide, M + 1.50, iy, lw - 1.80, 0.30, val, 12,
                 bg=C['card'], tc=C['body'], rounded=False, ml=0.10)
        iy += 0.42

    # 右パネル: 2本部構成
    rx = M + lw + 0.25
    rw = CW - lw - 0.25
    b._rect(slide, rx, y, rw, 5.60, C['white'], rounded=True)
    b._rect(slide, rx, y, 0.06, 5.60, C['info_bar'])
    b._section_head(slide, rx + 0.20, y + 0.15, rw - 0.30, 'エンジニア組織構成')

    # 合計バッジ
    by = y + 0.60
    b._block(slide, rx + 0.20, by, rw - 0.40, 0.55,
             '両本部エンジニア　合計 50〜60名', 18,
             bg=C['highlight'], tc=C['body'], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, bar_color=C['accent'])
    by += 0.75

    depts = [
        ('SaaS本部（呉様）', '保険業界向けSaaSプロダクト開発・運営', C['accent']),
        ('SI本部', '伝統的なカスタマイズシステム開発', C['info_bar']),
    ]
    for name, desc, bar_c in depts:
        b._rect(slide, rx + 0.20, by, rw - 0.40, 0.90, C['card'], rounded=True)
        b._rect(slide, rx + 0.20, by, 0.06, 0.90, bar_c)
        b._block(slide, rx + 0.35, by + 0.08, rw - 0.70, 0.30, name, 13,
                 tc=C['body'], bold=True, rounded=False)
        b._block(slide, rx + 0.35, by + 0.45, rw - 0.70, 0.30, desc, 11,
                 tc=C['sub'], rounded=False)
        by += 1.10

    # 言語制約ハイライト
    by += 0.10
    b._block(slide, rx + 0.20, by, rw - 0.40, 0.70,
             '⚠  エンジニアの約半数（25〜30名）が中国語話者\n　  日本語研修だけでは対応困難【事実】',
             12, bg=C['issue_bg'], tc=C['body'], bold=True, bar_color=C['issue_bar'])

slide_org_structure(b)

# ======================================================
# スライド6: 現状② AI活用の現状
# ======================================================
def slide_ai_status(b):
    slide = b._slide(); b._bg(slide)
    y = b._title_bar(slide, 'AI活用は「個人の我流」のままで止まっている', '現状②  AI活用の現状')

    pw = 5.80; gap = 0.73
    rx = M + pw + gap
    rw = CW - pw - gap

    # 左: 現状（個人ベース）
    b._rect(slide, M, y, pw, 5.60, C['white'], rounded=True)
    b._rect(slide, M, y, 0.06, 5.60, C['issue_bar'])
    b._section_head(slide, M + 0.20, y + 0.15, pw - 0.30, '現在の状況', 13)

    items_l = [
        ('個人活用', 'ChatGPT・Claudeを各自の判断で利用\nベストプラクティス・共有ルールなし', C['issue_bg'], C['issue_bar']),
        ('AI開発', '海外ベンダーへのBPO委託でPOCを推進\n本番運用は海外ベンダー利用が法規制上困難', C['issue_bg'], C['issue_bar']),
        ('知識レベル', '一般的なIT知識あり\nただしAI開発プロセスは「一切わからない」', C['issue_bg'], C['issue_bar']),
    ]
    iy = y + 0.60
    for label, txt, ibg, ibar in items_l:
        b._block(slide, M + 0.20, iy, 1.20, 0.30, label, 10,
                 bg=C['light_acc'], tc=C['accent'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.03)
        b._block(slide, M + 1.50, iy, pw - 1.80, 0.68, txt, 11,
                 bg=ibg, tc=C['body'], bar_color=ibar)
        iy += 0.90

    # 引用ブロック
    iy += 0.10
    b._block(slide, M + 0.20, iy, pw - 0.40, 0.90,
             '「みんな我流でやってるんですね。\nベストプラクティスという知識は\nみんな持っていなくて」\n— 呉様（商談での発言）',
             10, bg=C['warn_bg'], tc=C['warn_text'], bar_color=C['warn_bar'])

    # 右: 組織の課題
    b._rect(slide, rx, y, rw, 5.60, C['white'], rounded=True)
    b._rect(slide, rx, y, 0.06, 5.60, C['accent'])
    b._section_head(slide, rx + 0.20, y + 0.15, rw - 0.30, '組織としての課題', 13)

    items_r = [
        ('ツール利用', 'ChatGPT Enterpriseのみ\n会社資産アップロード可（近日契約予定）'),
        ('開発体制', 'AI開発ノウハウが社内に蓄積されていない\n外部BPO依存で知見が残らない'),
        ('標準化', '社内の標準プロセスなし\n本番運用移行のための体制が未整備'),
    ]
    iy = y + 0.60
    for label, txt in items_r:
        b._block(slide, rx + 0.20, iy, 1.20, 0.30, label, 10,
                 bg=C['light_acc'], tc=C['accent'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.03)
        b._block(slide, rx + 1.50, iy, rw - 1.80, 0.68, txt, 11,
                 bg=C['card'], tc=C['body'])
        iy += 0.90

slide_ai_status(b)

# ======================================================
# スライド7: 現状③ 三重制約
# ======================================================
b.detail_3col(
    title='ChatGPT縛り・金融規制・言語の三重制約',
    subtitle='現状③  AI活用環境',
    columns=[
        ('制約①　ツール',
         'ChatGPT Enterprise\nのみ使用可',
         [
             'ソフトバンク方針によりGPT中心',
             '会社資産アップロードはChatGPT Enterpriseのみ許可',
             'Copilot・Claude等は業務利用不可',
             '近日ChatGPT Enterprise契約予定',
         ]),
        ('制約②　法規制',
         '本番運用で\n海外ベンダー利用が困難',
         [
             '金融規制（個人情報保護）が適用',
             'POCは海外ベンダーで可能',
             '本番運用は日本国内ベンダー必須',
             '外部AI人材依存を継続できない',
         ]),
        ('制約③　言語',
         'エンジニアの約半数が\n中国語話者',
         [
             '日本語不可のエンジニアが25〜30名',
             '日本語研修では半数に届かない',
             '翻訳ツール活用は意味は伝わるが',
             '研修効果（熱量）が薄れるリスク',
         ]),
    ]
)

# ======================================================
# スライド8: 課題① ロジックツリー
# ======================================================
b.logic_tree(
    title='課題は3層構造',
    root_text='AIを活用できる組織・プロダクトへ転換できない',
    branches=[
        ('① エンジニアの\nAI開発力が\n不足', [
            ('AI開発プロセス（要件→タスク分解→実装）が分からない', True),
            ('AIエージェント作成・活用の基礎知識がない', True),
            ('各自の我流どまり、組織的ベストプラクティスがゼロ', True),
        ]),
        ('② AI活用環境に\n三重の制約', [
            ('ツール制約：ChatGPT Enterprise以外は会社資産アップロード不可', True),
            ('法規制：金融規制により本番運用で海外ベンダー利用が不可', True),
            ('言語制約：エンジニアの約半数が中国語話者で日本語研修に参加困難', True),
        ]),
        ('③ 組織的な\nAI推進体制\nがない', [
            ('AIノウハウが社内蓄積されず外部BPO依存が続く', True),
            ('3月末の親会社企画書通過のために社内AI体制整備の具体策が必要', False),
            ('研修・予算の社内承認プロセスがまだ動いていない', True),
        ]),
    ]
)

# ======================================================
# スライド9: 課題② AI開発力不足
# ======================================================
b.proposal_overview(
    items=[
        ('現在地',
         '「使う」だけで止まっている',
         [
             'ChatGPTをチャットとして使用',
             'ビジネス要件にどう応えるか不明',
             '「ピンと来ない」状態',
             '伝統開発の手法しか知らない',
         ]),
        ('ギャップ',
         'AI開発プロセスが\n分からない',
         [
             '要件→タスク分解→実装の流れ不明',
             'AIエージェントの設計方法が不明',
             'ユースケースが社内にゼロ',
             '「どの道に進むか、誰も正解を知らない」',
         ]),
        ('目指す場所',
         '「作れる」エンジニアへ',
         [
             '課題→タスク分解→AI実装を自走',
             'AIエージェントを構築・活用',
             '保険金請求AI-OCRを自社で実装',
             '支払い判断自動化を社内開発',
         ]),
    ]
)

# ======================================================
# スライド10: 課題③ 市場リスク
# ======================================================
def slide_market_risk(b):
    slide = b._slide(); b._bg(slide)
    y = b._title_bar(slide, 'AI非対応プロダクトは競争力を失う', '課題③  市場リスク')

    pw = 5.80; gap = 0.73
    rx = M + pw + gap
    rw = CW - pw - gap

    # 左: 保険業界トレンド
    b._rect(slide, M, y, pw, 5.60, C['white'], rounded=True)
    b._rect(slide, M, y, 0.06, 5.60, C['issue_bar'])
    b._section_head(slide, M + 0.20, y + 0.15, pw - 0.30, '保険業界のAI化の現状', 13)

    bullets = [
        '保険会社・代理店がAI活用による\nUX向上を顧客に求められている',
        'メインフレームからAI移行の\nPOCが業界全体で加速',
        'LINX社顧客も既にAI活用POCを\n複数進めている',
        '「伝統的なフォーム形式では\n古くなるリスク」（呉様）',
    ]
    iy = y + 0.60
    for bull in bullets:
        b._block(slide, M + 0.20, iy, pw - 0.40, 0.80,
                 f'●  {bull}', 11,
                 bg=C['issue_bg'], tc=C['body'], bar_color=C['issue_bar'])
        iy += 0.95

    # 右: タイムラインと示唆
    b._rect(slide, rx, y, rw, 5.60, C['white'], rounded=True)
    b._rect(slide, rx, y, 0.06, 5.60, C['warn_bar'])
    b._section_head(slide, rx + 0.20, y + 0.15, rw - 0.30, '今動かないとどうなるか', 13)

    timeline = [
        ('3月末', '親会社（ソフトバンク）への\nAIプロダクト企画書提出期限'),
        ('〜半年', 'POCから本番運用フェーズへ\n社内AI人材がいないと前進できない'),
        ('1年後〜', '競合他社がAI機能搭載SaaSで\n市場シェアを拡大'),
    ]
    iy = y + 0.60
    for timing, desc in timeline:
        b._block(slide, rx + 0.20, iy, 1.20, 0.75, timing, 14,
                 bg=C['warn_bg'], tc=C['warn_bar'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        b._block(slide, rx + 1.50, iy, rw - 1.80, 0.75, desc, 12,
                 bg=C['card'], tc=C['body'])
        iy += 0.95

    # 結論ブロック
    iy += 0.10
    b._block(slide, rx + 0.20, iy, rw - 0.40, 0.70,
             '今こそ、社内AI開発体制を整備するタイミング',
             14, bg=C['highlight'], tc=C['body'], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, bar_color=C['accent'])

slide_market_risk(b)

# ======================================================
# スライド11: 目指す姿 Before/After
# ======================================================
def slide_before_after(b):
    slide = b._slide(); b._bg(slide)
    y = b._title_bar(slide, '3ヶ月後、エンジニアはAIで開発できる', '目指す姿  Before / After')

    pw = (CW - 0.60) / 2

    # Before
    b._rect(slide, M, y, pw, 5.55, C['white'], rounded=True)
    b._rect(slide, M, y, 0.06, 5.55, C['issue_bar'])
    b._block(slide, M + 0.15, y + 0.08, pw - 0.30, 0.35, 'Before  現在', 13,
             bg=C['issue_bg'], tc=C['issue_bar'], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    befores = [
        ('AI開発プロセス', '伝統的な開発手法しか分からない'),
        ('エージェント活用', 'ChatGPTをチャットとして使うだけ'),
        ('ベストプラクティス', '各自の我流。知見の共有なし'),
        ('プロダクト展開', 'ビジネス要件にAIをどう組み込むか不明'),
    ]
    iy = y + 0.55
    for label, desc in befores:
        b._block(slide, M + 0.20, iy, 1.30, 0.30, label, 10,
                 bg=C['light_acc'], tc=C['accent'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.03)
        b._block(slide, M + 1.60, iy, pw - 1.85, 0.65, desc, 12,
                 bg=C['issue_bg'], tc=C['body'])
        iy += 0.85

    # Arrow
    ax = M + pw + 0.10
    b._block(slide, ax, y + 2.50, 0.40, 0.40, '→', 24,
             tc=C['accent'], bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, rounded=False)

    # After
    afterx = M + pw + 0.60
    b._rect(slide, afterx, y, pw, 5.55, C['white'], rounded=True)
    b._rect(slide, afterx, y, 0.06, 5.55, C['ok_bar'])
    b._block(slide, afterx + 0.15, y + 0.08, pw - 0.30, 0.35, 'After  研修後', 13,
             bg=C['ok_bg'], tc=C['ok_text'], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    afters = [
        ('AI開発プロセス', '課題→タスク分解→AI実装まで自走できる'),
        ('エージェント活用', 'AIエージェントを構築・活用できる'),
        ('ベストプラクティス', '組織共通の標準プロセスが確立される'),
        ('プロダクト展開', 'POC→本番運用への移行を社内で推進できる'),
    ]
    iy = y + 0.55
    for label, desc in afters:
        b._block(slide, afterx + 0.20, iy, 1.30, 0.30, label, 10,
                 bg=C['highlight'], tc=C['accent'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ml=0.03)
        b._block(slide, afterx + 1.60, iy, pw - 1.85, 0.65, desc, 12,
                 bg=C['ok_bg'], tc=C['body'])
        iy += 0.85

slide_before_after(b)

# ======================================================
# スライド12: 成果指標 KPI
# ======================================================
b.detail_3col(
    title='達成すべき3つの状態',
    subtitle='成果指標  KPI',
    columns=[
        ('KPI 1',
         'AI開発プロセスの\n習得',
         [
             '研修内ワークで「業務課題→AIタスク分解」が自力でできた参加者の割合',
             '目標：参加者の80%以上が達成',
             '測定：研修内ワーク成果で確認',
             '参考：キリングループ満足度8.5点',
         ]),
        ('KPI 2',
         '受講者満足度\n4.0以上（5点満点）',
         [
             '「業務でAIを活用できそう」回答率 90%以上',
             '測定：受講後アンケート',
             '参考：キリングループ「AIを活用できそう」100%回答',
             '中国語話者への対応評価も含める',
         ]),
        ('KPI 3',
         '実践展開\n30日以内に1件以上',
         [
             '研修後30日以内に学んだ手法を実業務に適用',
             '測定：1ヶ月後フォローアップ',
             '目標：参加者の60%以上が実業務適用',
             '保険金請求AI化等での実践を期待',
         ]),
    ]
)

# ======================================================
# スライド13: 提案根拠① 比較
# ======================================================
def slide_comparison(b):
    slide = b._slide(); b._bg(slide)
    y = b._title_bar(slide, '汎用研修では御社の課題に届かない', '提案根拠①  他との違い')

    headers = ['比較項目', '汎用AI研修', 'Kawaru Team']
    rows = [
        ('カリキュラム', '固定コンテンツ', '御社専用にゼロから設計'),
        ('課題対応', '一般的な業務効率化', '保険業界×エンジニア×AI開発プロセス'),
        ('言語対応', '日本語のみ', '中国語話者への対応設計可'),
        ('ツール', '汎用ツール前提', 'ChatGPT Enterprise縛り前提で設計'),
        ('講師', '研修会社インストラクター', 'AI開発の実践者（自社でAI開発を実施）'),
    ]
    col_x = [M, M + 2.20, M + 6.50]
    col_w = [2.00, 4.10, 5.73]
    row_h = 0.65
    header_h = 0.40

    # ヘッダー行
    hy = y + 0.10
    for i, (hdr, cx, cw) in enumerate(zip(headers, col_x, col_w)):
        hbg = C['accent'] if i == 2 else C['dark_head']
        b._block(slide, cx, hy, cw, header_h, hdr, 13,
                 bg=hbg, tc=C['white'], bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # データ行
    for r_idx, row in enumerate(rows):
        ry = hy + header_h + 0.08 + r_idx * (row_h + 0.06)
        for i, (cell, cx, cw) in enumerate(zip(row, col_x, col_w)):
            if i == 0:
                b._block(slide, cx, ry, cw, row_h, cell, 12,
                         bg=C['light_acc'], tc=C['accent'], bold=True,
                         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            elif i == 1:
                b._block(slide, cx, ry, cw, row_h, cell, 12,
                         bg=C['card'], tc=C['sub'], bar_color=C['divider'])
            else:
                b._block(slide, cx, ry, cw, row_h, cell, 12,
                         bg=C['highlight'], tc=C['body'], bold=True,
                         bar_color=C['accent'])

slide_comparison(b)

# ======================================================
# スライド14: 提案根拠② エヌイチの強み
# ======================================================
b.steps_3(
    title='「AI開発の実践者」が教える研修',
    subtitle='提案根拠②  エヌイチならではの強み',
    steps=[
        ('強み①',
         'AI開発を\n日常的に実践',
         [
             'エヌイチ自身がAI SaaS（Kawaru）を開発・運営',
             'AIエージェントを日常業務で活用',
             '教科書ではなく実務ノウハウを提供',
             'GPT中心での開発知見を保有',
         ]),
        ('強み②',
         '完全\nフルカスタマイズ',
         [
             '御社の業務・課題・制約に合わせてゼロ設計',
             'GPT縛り・言語問題も研修内容に反映',
             '保険業界のユースケースで事例を構成',
             '「0から全部フルカスタマイズ」が他社との最大の違い',
         ]),
        ('強み③',
         '実績に基づく\n設計力',
         [
             'キリングループ：満足度8.5点',
             'ミズカラ：月283時間→85時間へ削減',
             'BIRDY：商談件数1.5倍・バックオフィス効率化',
             '業界・規模を問わず導入実績多数',
         ]),
    ]
)

# ======================================================
# スライド15: 提案詳細① 研修内容
# ======================================================
b.detail_3col(
    title='御社専用カリキュラムの設計方針',
    subtitle='提案詳細①  研修内容（ヒアリング後に確定）',
    columns=[
        ('テーマ 1',
         'AIエージェント基礎',
         [
             'エージェントとは何か・仕組み',
             '作成方法と活用パターン',
             'ChatGPT Enterpriseを使った実装',
             '「チャットツールじゃなくてエージェントを」（呉様）',
         ]),
        ('テーマ 2',
         'ビジネス課題×\nAIタスク分解',
         [
             'ビジネス要件をAIで解決する思考法',
             'できること・できないことの整理',
             '保険金請求AI-OCRの実装イメージ',
             '小額短期保険の支払い判断自動化',
         ]),
        ('テーマ 3',
         'AI開発プロセス\n実践',
         [
             'AI版の要件定義→設計→実装の流れ',
             'POC→本番運用への移行方法',
             'ChatGPT Enterprise前提の開発標準',
             '「伝統的開発とAI開発の違いを学びたい」',
         ]),
    ]
)

# ======================================================
# スライド16: 提案詳細② 実施形式
# ======================================================
b.steps_3(
    title='ヒアリング2時間でカリキュラムをゼロ設計',
    subtitle='提案詳細②  実施形式・スケジュール',
    steps=[
        ('STEP 1',
         'ヒアリング\n（約2時間）',
         [
             '課題・現場業務・ゴールを確認',
             '中国語話者への対応方針を決定',
             'ChatGPT Enterprise活用方針を確認',
             '参加人数・日程を確定',
         ]),
        ('STEP 2',
         'カリキュラム設計\n（1〜2週間）',
         [
             '御社専用コンテンツをゼロから作成',
             '保険業界ユースケースで事例を構成',
             'GPT縛り前提のカリキュラムに調整',
             '多言語対応の教材設計',
         ]),
        ('STEP 3',
         '研修実施\n（10〜15時間）',
         [
             '平日9〜18時（助成金適用条件対応）',
             '1回あたり15〜25名・両本部交代制',
             '3〜4日間で完結',
             '修了後1ヶ月でフォローアップ',
         ]),
    ]
)

# ======================================================
# スライド17: 提案詳細③ 費用
# ======================================================
b.pricing(
    price_main='1人あたり  150,000円',
    price_detail='研修時間：10〜15時間  /  3〜4日間\n対象：15〜25名（交代制で両本部をカバー）',
    subsidy_price='助成金活用で実質 37,500〜60,000円 / 人',
    subsidy_detail='● 助成金還元率：60〜75%（平日9〜18時の条件で適用）\n'
                   '● 25名参加の場合 総額3,750,000円 → 実質約937,500〜1,500,000円\n'
                   '● 条件：平日9〜18時での実施（対応可能）\n'
                   '● 申請手続きはエヌイチがサポート',
    schedule=[
        ('社内承認', '呉様→社長との1on1で承認取得'),
        ('ヒアリング', '承認後すぐ（約2時間）'),
        ('カリキュラム確定', 'ヒアリングから1〜2週間'),
        ('研修実施', '日程調整後・平日3〜4日間'),
        ('フォローアップ', '修了後1ヶ月'),
    ]
)

# ======================================================
# スライド18: 提案詳細④ 進め方
# ======================================================
b.steps_3(
    title='今後の進め方',
    subtitle='提案詳細④  ネクストステップ',
    steps=[
        ('STEP 1',
         '社内承認\n（呉様→社長）',
         [
             '本提案資料を社長説明にご活用ください',
             '助成金で実質負担が大幅削減の点を訴求',
             '3月末の親会社企画書とも連動',
             '承認結果をエヌイチへご連絡ください',
         ]),
        ('STEP 2',
         '研修設計\nキックオフ',
         [
             '承認後すぐにヒアリング日程を調整',
             '課題・ゴール・言語対応を確定',
             'ChatGPT Enterprise活用方針を確認',
             'カリキュラム設計（1〜2週間）',
         ]),
        ('STEP 3',
         '研修実施\n→ フォローアップ',
         [
             '15〜25名×交代制で実施',
             '平日9〜18時（助成金適用）',
             '10〜15時間・3〜4日間で完結',
             '修了後1ヶ月でKPI達成確認',
         ]),
    ]
)

# ======================================================
# スライド19: ネクストアクション
# ======================================================
b.next_actions([
    ('社内承認（呉様→社長）を完了',
     '来週の社長1on1で研修の件を相談 → 承認結果をエヌイチへご連絡ください'),
    ('承認結果の連絡',
     '承認後すぐにエヌイチへご連絡。研修設計キックオフの日程を調整します'),
    ('研修設計キックオフ（ヒアリング）',
     '承認連絡後3営業日以内に日程を確定。ヒアリング約2時間で設計に着手します'),
])

# ======================================================
# スライド20: 締め
# ======================================================
b.closing()

# 保存
b.save(OUTPUT)
print(f'✅ 保存完了: {OUTPUT}')
print(f'   スライド枚数: {len(b.prs.slides)}枚')
