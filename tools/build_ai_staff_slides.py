"""
AI社員5人 発表スライド生成スクリプト（4月末発表用・13枚構成）
白×紺×Kawaru ブルー基調 / 4サービスカラーは一覧時のみ
視認性重視・装飾要素追加
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE

C = {
    'white':         RGBColor(0xFF, 0xFF, 0xFF),
    'navy':          RGBColor(0x1C, 0x35, 0x57),
    'navy_l':        RGBColor(0x4A, 0x6C, 0x8C),
    'kawaru':        RGBColor(0x25, 0x63, 0xEB),
    'kawaru_l':      RGBColor(0xDB, 0xEA, 0xFE),
    'team':          RGBColor(0xFF, 0x66, 0x00),
    'coach':         RGBColor(0x7C, 0x3A, 0xED),
    'bpo':           RGBColor(0x10, 0xBF, 0x16),
    'gray':          RGBColor(0x6B, 0x72, 0x80),
    'light_gray':    RGBColor(0xF3, 0xF4, 0xF6),
    'border':        RGBColor(0xE5, 0xE7, 0xEB),
}

FONT = 'Noto Sans JP'
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.50)
TOTAL = 13


class Builder:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = SLIDE_W
        self.prs.slide_height = SLIDE_H

    def _slide(self):
        return self.prs.slides.add_slide(self.prs.slide_layouts[6])

    def _bg(self, slide):
        s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
        s.fill.solid()
        s.fill.fore_color.rgb = C['white']
        s.line.fill.background()

    def _block(self, slide, x, y, w, h, text, size, color=None, bg=None,
               bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, rounded=False):
        st = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
        s = slide.shapes.add_shape(st, Inches(x), Inches(y), Inches(w), Inches(h))
        if bg:
            s.fill.solid()
            s.fill.fore_color.rgb = bg
        else:
            s.fill.background()
        s.line.fill.background()
        if rounded and hasattr(s, 'adjustments') and len(s.adjustments) > 0:
            s.adjustments[0] = 0.05

        tf = s.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        tf.vertical_anchor = anchor
        tf.margin_left = Inches(0.10)
        tf.margin_right = Inches(0.10)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)

        for i, line in enumerate(text.split('\n')):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            r = p.add_run()
            r.text = line
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color or C['navy']
        return s

    def _line(self, slide, x, y, w, color, thick=0.05):
        s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(thick))
        s.fill.solid()
        s.fill.fore_color.rgb = color
        s.line.fill.background()
        return s

    def _connector(self, slide, x1, y1, x2, y2, color, weight=2.5):
        """直線コネクタ"""
        line = slide.shapes.add_connector(
            MSO_CONNECTOR_TYPE.STRAIGHT,
            Inches(x1), Inches(y1), Inches(x2), Inches(y2)
        )
        line.line.color.rgb = color
        line.line.width = Pt(weight)
        return line

    def _arrow(self, slide, x, y, w, h, color):
        s = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = color
        s.line.fill.background()
        return s

    def _arrow_right(self, slide, x, y, w, h, color):
        s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = color
        s.line.fill.background()
        return s

    def _circle(self, slide, x, y, w, h, color):
        s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = color
        s.line.fill.background()
        return s

    def _title(self, slide, text, page_num):
        self._block(slide, 12.0, 0.3, 1.1, 0.3, f"{page_num} / {TOTAL}", 11,
                    color=C['gray'], align=PP_ALIGN.RIGHT)
        self._block(slide, 0.5, 0.4, 11.5, 0.7, text, 24, bold=True, color=C['navy'])
        self._line(slide, 0.5, 1.15, 1.8, C['kawaru'], 0.07)

    # ========== Slides ==========

    def s01_cover(self):
        s = self._slide()
        self._bg(s)
        self._line(s, 0, 0, 13.33, C['kawaru'], 0.15)
        self._circle(s, 10.5, 0.5, 2.3, 2.3, C['kawaru_l'])
        self._circle(s, 0.5, 5.5, 1.8, 1.8, C['kawaru_l'])

        self._block(s, 0.5, 2.5, 12.33, 1.6, 'AIハッカソン',
                    60, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._line(s, 5.5, 4.3, 2.33, C['navy'], 0.06)
        self._block(s, 0.5, 4.5, 12.33, 0.8, 'Kawaru事業部',
                    28, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 5.4, 12.33, 0.7, '大川 龍之介',
                    22, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 6.8, 12.33, 0.4, '2026.04',
                    14, color=C['gray'], align=PP_ALIGN.CENTER)

    def s02_premise(self):
        """前提：コストの話がしにくい"""
        s = self._slide()
        self._bg(s)
        self._block(s, 0.5, 0.4, 12.33, 0.5, '前提', 14,
                    color=C['gray'], align=PP_ALIGN.CENTER, bold=True)
        self._line(s, 6.0, 1.0, 1.33, C['kawaru'], 0.06)

        self._block(s, 0.5, 1.6, 12.33, 1.4,
                    'Kawaru事業部は',
                    28, color=C['navy'], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 2.7, 12.33, 1.2,
                    'コストの話がしにくい',
                    44, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        self._block(s, 0.7, 4.6, 5.5, 2.0, '既存事業',
                    18, bold=True, color=C['gray'], bg=C['light_gray'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        self._block(s, 0.7, 5.2, 5.5, 1.4,
                    '固定業務がある\n削減対象が見える',
                    16, color=C['gray'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        self._arrow_right(s, 6.4, 5.3, 0.8, 0.7, C['kawaru'])

        self._block(s, 7.4, 4.6, 5.3, 2.0, 'Kawaru事業部',
                    18, bold=True, color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        self._block(s, 7.4, 5.2, 5.3, 1.4,
                    '業務が毎月変わる\n削減対象がそもそもない',
                    16, color=C['white'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        self._block(s, 12.0, 7.1, 1.1, 0.3, "2 / 13", 11, color=C['gray'], align=PP_ALIGN.RIGHT)

    def s03_status(self):
        """4サービスを2人体制で動かしている"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'Kawaru事業部の現状：4サービスを2人体制で動かしている', 3)

        # 上：4サービス横並び
        services = [
            ('Kawaru', C['kawaru']),
            ('Kawaru Team', C['team']),
            ('Kawaru Coach', C['coach']),
            ('Kawaru BPO', C['bpo']),
        ]
        sw = 3.0
        gap = 0.05
        for i, (name, col) in enumerate(services):
            x = 0.5 + i*(sw + gap)
            self._block(s, x, 1.6, sw, 1.6, name, 24, bold=True,
                        color=C['white'], bg=col, rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 矢印
        self._arrow(s, 6.42, 3.4, 0.5, 0.6, C['kawaru'])

        # 下：2人体制
        self._block(s, 3.5, 4.3, 2.5, 1.4, '髙橋', 28, bold=True,
                    color=C['white'], bg=C['navy'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 6.1, 4.3, 1.0, 1.4, '+', 36, bold=True,
                    color=C['gray'], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 7.2, 4.3, 2.5, 1.4, '大川', 28, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下メッセージ
        self._block(s, 0.5, 6.0, 12.33, 1.0,
                    '現状、Kawaru事業部の重要な4サービスを2人体制でやっている',
                    22, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s04_directing(self):
        """大川がAI社員5人を動かしている（指示構図・放射状の線）"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'すでにAI社員5人を動かしている', 4)

        # 髙橋（最上部）
        self._block(s, 5.67, 1.4, 2.0, 0.7, '髙橋', 18, bold=True,
                    color=C['white'], bg=C['navy'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 髙橋→大川 矢印
        self._connector(s, 6.67, 2.1, 6.67, 2.5, C['gray'], 2.0)

        # 大川（中央）
        ok_x = 5.17
        ok_y = 2.5
        ok_w = 3.0
        ok_h = 1.0
        self._block(s, ok_x, ok_y, ok_w, ok_h, '大川', 28, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ok_cx = ok_x + ok_w/2  # 6.67
        ok_by = ok_y + ok_h    # 3.5

        # 5人のAI（下、横並び）
        labels = ['マーケAI', '営業AI', 'デリバリーAI', '事務法務AI', '戦略AI']
        ai_y = 4.6
        ai_w = 2.3
        ai_h = 1.5
        for i, l in enumerate(labels):
            x = 0.5 + i*2.55
            cx = x + ai_w/2  # AIの中央x
            # 大川の下端中央 → AIの上端中央 へ線を引く
            self._connector(s, ok_cx, ok_by, cx, ai_y, C['kawaru'], 2.5)
            # AIブロック
            self._block(s, x, ai_y, ai_w, ai_h, l, 16, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下メッセージ
        self._block(s, 0.5, 6.4, 12.33, 0.8,
                    '大川主導で AI社員5人 を動かして事業部を回している',
                    20, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s05_concept(self):
        """こういう5人構成を考えています（クッション）"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'こういう5人構成を考えています', 5)

        # 中央：5機能を抽象的に円形配置
        # 上に「事業を回すための5機能」と表示、その下に円5つ
        self._block(s, 0.5, 1.7, 12.33, 0.6,
                    '事業を回すために必要な機能を、5人のAI社員に分けた',
                    18, color=C['navy'], align=PP_ALIGN.CENTER, bold=True)

        # 5機能を円形に
        funcs = ['マーケ', '営業', 'デリバリー', '事務・法務', '戦略']
        cw = 2.2
        gap = 0.3
        total_w = 5*cw + 4*gap  # 13.2
        cx_start = (13.33 - total_w) / 2
        for i, f in enumerate(funcs):
            x = cx_start + i*(cw + gap)
            self._circle(s, x, 3.0, cw, cw, C['kawaru'])
            # 中央テキスト
            self._block(s, x, 3.0, cw, cw, f, 18, bold=True,
                        color=C['white'],
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下メッセージ
        self._block(s, 0.5, 5.7, 12.33, 1.2,
                    'この 5人 で事業を動かす',
                    36, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s06_5agents(self):
        """AI社員5人の構成（詳細・正式名称）"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'AI社員5人の構成', 6)

        roles = [
            ('マーケAI', 'LP / SNS / 展示会 / LINE配信 / 事例記事'),
            ('営業AI', '商談前準備 / 要件ヒアリング / 提案書 / フォロー'),
            ('デリバリーAI', '研修運営 / Dify・n8n・GAS構築 / CSコンサル / PM'),
            ('事務・法務AI', '契約書 / 請求書 / 利用契約書 / プライバシーポリシー / PL'),
            ('戦略・プロダクトAI', '競合調査 / 市場調査 / 料金設計 / データ分析'),
        ]
        y = 1.5
        h = 0.95
        for name, desc in roles:
            self._block(s, 0.5, y, 3.5, h, name, 18, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 4.1, y, 8.7, h, desc, 14, color=C['navy'],
                        bg=C['light_gray'], rounded=True,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            y += 1.05
        self._block(s, 0.5, 6.85, 12.33, 0.4,
                    '4人 = 各領域の戦略 + 実行  /  戦略・プロダクトAI = リサーチ・分析担当',
                    11, color=C['gray'], align=PP_ALIGN.CENTER, bold=True)

    def s07_all_business(self):
        """これが事業でやるべき仕事のすべて"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'これが事業でやるべき仕事のすべて', 7)

        funcs = [
            ('マーケ', '認知獲得'),
            ('営業', '商談・受注'),
            ('デリバリー', '納品'),
            ('事務・法務', '管理・記録'),
            ('戦略', 'リサーチ・分析'),
        ]
        cw = 2.4
        cx = 0.5
        gap = 0.07
        for i, (name, desc) in enumerate(funcs):
            x = cx + i*(cw + gap)
            self._block(s, x, 2.0, cw, 1.6, name, 22, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, x, 3.65, cw, 0.8, desc, 14,
                        color=C['navy'], bg=C['light_gray'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        self._block(s, 0.5, 5.0, 12.33, 1.6,
                    '事業の全部の仕事を 5人で網羅している',
                    26, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s08_how_use(self):
        """今こう使ってます（実例詳細）"""
        s = self._slide()
        self._bg(s)
        self._title(s, '今こう使ってます', 8)

        # 5人のAI社員別に5つずつの具体例
        items = [
            ('マーケAI', [
                '展示会クリエイティブ指示書',
                'LINE配信シナリオ',
                'SNS投稿生成',
                'LP構成案・コピー',
                'YouTube → SNS 転記',
            ]),
            ('営業AI', [
                '商談前ブリーフィング',
                '提案書骨子（髙橋メソッド）',
                'フォローメール（一括）',
                '要件ヒアリング整理',
                '見積書作成',
            ]),
            ('デリバリーAI', [
                'NTT 研修スライド200枚',
                '中西 Dify構築（5h）',
                'キリン 研修PM',
                'ブロードリンク 省エネ運用',
                'カリキュラム設計',
            ]),
            ('事務・法務AI', [
                '契約書チェック',
                'PL自動更新（SUMIFS）',
                '受信トレイ整理',
                '月次レポート生成',
                'ツールコスト最適化',
            ]),
            ('戦略AI', [
                '競合調査',
                '料金設計試算',
                'ローンチ後データ分析',
                'プロダクト改善提案',
                '朝の工程表 / 週次レポート',
            ]),
        ]
        cw = 2.4
        gap = 0.1
        for i, (name, examples) in enumerate(items):
            x = 0.5 + i * (cw + gap)
            self._block(s, x, 1.5, cw, 0.6, name, 14, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            # 例リスト
            ex_text = '\n'.join([f'• {e}' for e in examples])
            self._block(s, x, 2.2, cw, 4.0, ex_text, 11,
                        color=C['navy'], bg=C['kawaru_l'], rounded=True,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)

        self._block(s, 0.5, 6.4, 12.33, 0.8,
                    'いろんな領域で AI社員 を使い倒している',
                    20, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s09_to_results(self):
        """これが売上に直結している（橋渡し）"""
        s = self._slide()
        self._bg(s)
        self._block(s, 0.5, 0.4, 12.33, 0.5, 'そして', 14,
                    color=C['gray'], align=PP_ALIGN.CENTER, bold=True)
        self._line(s, 6.0, 1.0, 1.33, C['kawaru'], 0.06)

        self._block(s, 0.5, 2.2, 12.33, 1.5, 'これが',
                    32, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 3.5, 12.33, 1.6, '売上に直結している',
                    52, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._arrow(s, 6.42, 5.5, 0.5, 0.6, C['kawaru'])
        self._block(s, 12.0, 7.1, 1.1, 0.3, "9 / 13", 11, color=C['gray'], align=PP_ALIGN.RIGHT)

    def s10_results(self):
        """半期¥6,710,000"""
        s = self._slide()
        self._bg(s)
        self._title(s, '半期 ¥6,710,000、4案件すべてにAI社員が動いている', 10)

        cases = [
            ('NTTネクシア', '¥5,000,000'),
            ('中西製作所', '¥1,000,000'),
            ('中部キリンビバレッジ', '¥450,000'),
            ('ブロードリンク', '¥260,000'),
        ]
        y = 1.7
        h = 0.7
        self._block(s, 0.5, y, 5.0, h, '案件', 16, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 5.55, y, 3.0, h, '売上 (税抜)', 16, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.78
        for case, amount in cases:
            self._block(s, 0.5, y, 5.0, h, case, 16, color=C['navy'],
                        bg=C['light_gray'],
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 5.55, y, 3.0, h, amount, 16, color=C['navy'],
                        bg=C['light_gray'],
                        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.78
        self._block(s, 0.5, y, 5.0, h, '半期合計', 18, bold=True,
                    color=C['white'], bg=C['kawaru'],
                    align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 5.55, y, 3.0, h, '¥6,710,000', 18, bold=True,
                    color=C['white'], bg=C['kawaru'],
                    align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

        self._block(s, 9.0, 1.7, 3.83, 4.6,
                    '月換算\n\n¥464,000\n\n=\n\nAI社員\n1.3人分\n稼働中',
                    22, bold=True, color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s11_now_future(self):
        """ここまで現状、ここから今後"""
        s = self._slide()
        self._bg(s)
        self._line(s, 5.5, 1.5, 2.33, C['kawaru'], 0.08)
        self._block(s, 0.5, 2.0, 12.33, 1.2, 'ここまでが現状の話',
                    34, bold=True, color=C['gray'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._arrow(s, 6.17, 3.4, 1.0, 0.8, C['kawaru'])
        self._block(s, 0.5, 4.4, 12.33, 1.5, 'ここから今後の話',
                    50, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 6.0, 12.33, 0.6,
                    '9月末までにAI社員5人を完成させる、その具体ロードマップ',
                    18, color=C['navy'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 12.0, 7.1, 1.1, 0.3, "11 / 13", 11,
                    color=C['gray'], align=PP_ALIGN.RIGHT)

    def s12_roadmap(self):
        """ロードマップ（具体タスク）"""
        s = self._slide()
        self._bg(s)
        self._title(s, '9月末までのロードマップ：何をどうしていくか', 12)

        # 列：月／達成水準／具体タスク／Agent Teams
        rows = [
            ('4月\n(現在)', '1.3人分',
             'NTT・中西デリバリー継続 / 戦略AIで競合・料金リサーチ強化',
             '構造設計の検討', False),
            ('5月', '1.6人分',
             'マーケAI立ち上げ(LP・LINE) / 営業AI立ち上げ(商談前準備テンプレ)',
             '5人の役割分担を設計', False),
            ('6月末\n(中間)', '2人分',
             'Kawaru β版ローンチ実施 / 5人で連携運用テスト開始',
             '初期構築 (3人連携)', True),
            ('7-8月', '3〜4人分',
             'β版運用フィードバック反映 / プロダクト改善ループ確立',
             '連携テスト / デモ実装', False),
            ('8月', '4人分',
             '事務・法務AI追加(契約書/PL/利用規約自動化)',
             '5人連携リハーサル', False),
            ('9月末\n(最終)', '5人分',
             '5人フル稼働 / プロダクト × デリバリー両輪完成',
             '5人協働で事業を動かす', True),
        ]
        y = 1.5
        h = 0.7
        # ヘッダー
        self._block(s, 0.5, y, 1.5, h, '月', 13, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 2.05, y, 1.4, h, '達成水準', 13, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 3.50, y, 6.5, h, '具体タスク', 13, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 10.05, y, 2.78, h, 'Agent Teams', 13, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.78

        for month, level, task, at, emp in rows:
            if emp:
                bg_l = C['kawaru']; bg_r = C['kawaru_l']
                fc_l = C['white']; fc_r = C['navy']
            else:
                bg_l = C['light_gray']; bg_r = C['light_gray']
                fc_l = C['navy']; fc_r = C['navy']
            self._block(s, 0.5, y, 1.5, h, month, 11, bold=emp, color=fc_l, bg=bg_l,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 2.05, y, 1.4, h, level, 14, bold=True, color=fc_l, bg=bg_l,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 3.50, y, 6.5, h, task, 11, color=fc_r, bg=bg_r,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 10.05, y, 2.78, h, at, 11, color=fc_r, bg=bg_r,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.65

        self._block(s, 0.5, 6.85, 12.33, 0.45,
                    '5人を網羅的に同時進行で育てる + Agent Teamsを並走で構築する',
                    14, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s13_close(self):
        """締め"""
        s = self._slide()
        self._bg(s)
        self._line(s, 0, 0, 13.33, C['kawaru'], 0.15)
        self._circle(s, 10.5, 0.8, 2.0, 2.0, C['kawaru_l'])
        self._circle(s, 0.7, 5.5, 1.6, 1.6, C['kawaru_l'])

        self._block(s, 0.5, 1.5, 12.33, 1.5, 'AI社員を動かして、',
                    40, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 2.9, 12.33, 1.6,
                    'Kawaru事業部の事業を推進する',
                    50, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._line(s, 5.5, 4.8, 2.33, C['kawaru'], 0.07)
        self._block(s, 0.5, 5.0, 12.33, 0.6,
                    '2人 + AI社員5人 + Agent Teams で動かす',
                    20, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        self._block(s, 1.0, 6.0, 3.5, 0.8, 'Kawaru', 15, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 4.7, 6.0, 2.6, 0.8, 'Kawaru Team', 14, bold=True,
                    color=C['white'], bg=C['team'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 7.4, 6.0, 2.6, 0.8, 'Kawaru Coach', 14, bold=True,
                    color=C['white'], bg=C['coach'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 10.1, 6.0, 2.4, 0.8, 'Kawaru BPO', 14, bold=True,
                    color=C['white'], bg=C['bpo'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 12.0, 7.1, 1.1, 0.3, '13 / 13', 11,
                    color=C['gray'], align=PP_ALIGN.RIGHT)

    def build(self, output):
        self.s01_cover()
        self.s02_premise()
        self.s03_status()
        self.s04_directing()
        self.s05_concept()
        self.s06_5agents()
        self.s07_all_business()
        self.s08_how_use()
        self.s09_to_results()
        self.s10_results()
        self.s11_now_future()
        self.s12_roadmap()
        self.s13_close()
        self.prs.save(output)
        print(f"Saved: {output}")


if __name__ == '__main__':
    output_path = '/Users/kyouyuu/claude/strategy/AI社員5人_発表_20260426.pptx'
    Builder().build(output_path)
