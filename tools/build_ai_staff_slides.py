"""
AI社員5人 発表スライド生成スクリプト（4月末発表用・11枚構成）
白×紺×Kawaru ブルー基調 / 4サービスカラーは一覧時のみ
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

C = {
    'white':         RGBColor(0xFF, 0xFF, 0xFF),
    'navy':          RGBColor(0x1C, 0x35, 0x57),  # 紺（メイン文字色）
    'navy_l':        RGBColor(0x4A, 0x6C, 0x8C),
    'kawaru':        RGBColor(0x25, 0x63, 0xEB),  # Kawaru ブルー（アクセント）
    'kawaru_l':      RGBColor(0xDB, 0xEA, 0xFE),
    'team':          RGBColor(0xFF, 0x66, 0x00),  # Kawaru Team
    'coach':         RGBColor(0x7C, 0x3A, 0xED),  # Kawaru Coach
    'bpo':           RGBColor(0x10, 0xBF, 0x16),  # Kawaru BPO
    'gray':          RGBColor(0x6B, 0x72, 0x80),
    'light_gray':    RGBColor(0xF3, 0xF4, 0xF6),
    'border':        RGBColor(0xE5, 0xE7, 0xEB),
}

FONT = 'Noto Sans JP'
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.50)
TOTAL = 11


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
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.08)

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

    def _title(self, slide, text, page_num):
        # ページ番号
        self._block(slide, 12.0, 0.3, 1.1, 0.3, f"{page_num} / {TOTAL}", 10,
                    color=C['gray'], align=PP_ALIGN.RIGHT)
        # タイトル
        self._block(slide, 0.5, 0.4, 11.5, 0.7, text, 22, bold=True, color=C['navy'])
        # アクセントライン
        self._line(slide, 0.5, 1.15, 1.5, C['kawaru'], 0.06)

    # ========== Slides ==========

    def s01_cover(self):
        """表紙"""
        s = self._slide()
        self._bg(s)
        # アクセントライン上
        self._line(s, 5.5, 2.3, 2.33, C['kawaru'], 0.08)
        # メインタイトル
        self._block(s, 0.5, 2.5, 12.33, 1.4, 'AIハッカソン',
                    48, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 区切り
        self._line(s, 5.5, 4.0, 2.33, C['border'], 0.04)
        # 事業部
        self._block(s, 0.5, 4.2, 12.33, 0.7, 'Kawaru事業部',
                    24, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 名前
        self._block(s, 0.5, 5.0, 12.33, 0.7, '大川 龍之介',
                    20, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 日付
        self._block(s, 0.5, 6.5, 12.33, 0.4, '2026.04',
                    13, color=C['gray'],
                    align=PP_ALIGN.CENTER)

    def s02_intro(self):
        """コストダウンの話ができない"""
        s = self._slide()
        self._bg(s)
        self._block(s, 0.5, 2.0, 12.33, 1.5,
                    '私たちは「コストダウン」の話ができません',
                    36, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 3.5, 12.33, 0.5,
                    'Kawaru事業部の前提',
                    14, color=C['gray'], align=PP_ALIGN.CENTER)
        # 対比
        self._block(s, 1.5, 4.7, 4.5, 1.5,
                    '既存事業\n固定業務がある\n削減対象が見える',
                    16, color=C['gray'], bg=C['light_gray'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 6.0, 4.7, 1.33, 1.5, '←→', 28, color=C['kawaru'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 7.33, 4.7, 4.5, 1.5,
                    'Kawaru事業部\n業務が毎月変わる\n削減対象がない',
                    16, color=C['navy'], bg=C['kawaru_l'], rounded=True, bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # ページ番号
        self._block(s, 12.0, 7.1, 1.1, 0.3, "2 / 11", 10, color=C['gray'], align=PP_ALIGN.RIGHT)

    def s03_4services(self):
        """Kawaru事業部の4サービス（田の字）"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'Kawaru事業部の4サービス', 3)

        # 田の字レイアウト
        # 左上：Kawaru、右上：Team、左下：Coach、右下：BPO
        cell_w = 5.5
        cell_h = 2.4
        gap = 0.3
        cx1 = 0.7
        cx2 = cx1 + cell_w + gap
        cy1 = 1.6
        cy2 = cy1 + cell_h + gap

        self._block(s, cx1, cy1, cell_w, cell_h, 'Kawaru', 36, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, cx2, cy1, cell_w, cell_h, 'Kawaru Team', 36, bold=True,
                    color=C['white'], bg=C['team'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, cx1, cy2, cell_w, cell_h, 'Kawaru Coach', 36, bold=True,
                    color=C['white'], bg=C['coach'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, cx2, cy2, cell_w, cell_h, 'Kawaru BPO', 36, bold=True,
                    color=C['white'], bg=C['bpo'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下メッセージ
        self._block(s, 0.5, 6.85, 12.33, 0.5,
                    'この4つのサービスを動かしている',
                    16, bold=True, color=C['navy'], align=PP_ALIGN.CENTER)

    def s04_2people(self):
        """2人だけ、だからAI社員5人"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'でもフルコミットは2人だけ。だからAI社員5人で動かす', 4)

        # 上：髙橋と大川
        self._block(s, 3.5, 1.7, 2.5, 1.0, '髙橋', 22, bold=True,
                    color=C['white'], bg=C['navy'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 7.33, 1.7, 2.5, 1.0, '大川', 22, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 矢印
        self._block(s, 0.5, 3.0, 12.33, 0.6,
                    '↓ AI社員に動いてもらう ↓',
                    16, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下：5人のAI社員
        labels = ['マーケAI', '営業AI', 'デリバリーAI', '事務法務AI', '戦略AI']
        for i, l in enumerate(labels):
            x = 0.7 + i*2.5
            self._block(s, x, 3.9, 2.3, 1.4, l, 14, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下強調
        self._block(s, 0.5, 5.7, 12.33, 1.1,
                    '2人で4サービスは難しい。AI社員5人で動かす',
                    22, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s05_5agents(self):
        """AI社員5人の構成"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'AI社員5人の構成', 5)

        roles = [
            ('マーケAI', 'LP / SNS / 展示会 / LINE配信 / 事例記事'),
            ('営業AI', '商談前準備 / 要件ヒアリング / 提案書 / フォロー'),
            ('デリバリーAI', '研修運営 / Dify・N8N・GAS構築 / CSコンサル / PM'),
            ('事務・法務AI', '契約 / 請求 / PL / 利用規約'),
            ('戦略・プロダクトAI', '競合・市場・料金・データ分析(リサーチ・分析担当)'),
        ]
        y = 1.5
        h = 0.85
        for name, desc in roles:
            self._block(s, 0.5, y, 3.5, h, name, 16, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 4.1, y, 8.7, h, desc, 14, color=C['navy'],
                        bg=C['light_gray'], rounded=True,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.95
        self._block(s, 0.5, 6.55, 12.33, 0.4,
                    '4人 = 各領域の戦略 + 実行  /  戦略・プロダクトAI = リサーチ・分析担当',
                    11, color=C['gray'], align=PP_ALIGN.CENTER, bold=True)

    def s06_all_business(self):
        """これが事業でやるべき仕事のすべて"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'これが事業でやるべき仕事のすべて', 6)

        # 5機能を横並び
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
            self._block(s, x, 2.2, cw, 1.4, name, 18, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, x, 3.65, cw, 0.7, desc, 13,
                        color=C['navy'], bg=C['light_gray'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下メッセージ
        self._block(s, 0.5, 5.0, 12.33, 1.4,
                    'マーケから戦略まで、事業の全部の仕事を 5人 で網羅している',
                    22, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s07_how_use(self):
        """AI社員をこう使っているイメージ"""
        s = self._slide()
        self._bg(s)
        self._title(s, 'AI社員をこう使っているイメージ', 7)

        # 左：Kawaru プロダクト作り
        self._block(s, 0.5, 1.5, 6.0, 0.55, 'Kawaru プロダクト作り', 16, bold=True,
                    color=C['white'], bg=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        prod = [
            ('プロダクト改善の提案たたき', '戦略AI'),
            ('ローンチPM・LP・LINE配信', 'マーケAI + 戦略AI'),
            ('競合・料金・データ分析', '戦略AI'),
        ]
        y = 2.15
        for biz, ai in prod:
            self._block(s, 0.5, y, 4.0, 0.85, biz, 13, color=C['navy'],
                        bg=C['kawaru_l'],
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 4.55, y, 1.95, 0.85, ai, 11, bold=True,
                        color=C['kawaru'], bg=C['white'],
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.93

        # 右：Kawaru Team / Coach / BPO
        self._block(s, 6.83, 1.5, 6.0, 0.55, 'Kawaru Team / Coach / BPO',
                    16, bold=True, color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        deliv = [
            ('展示会設計・クリエイティブ', 'マーケAI'),
            ('提案書骨子作成', '営業AI'),
            ('Dify / N8N / GAS構築', 'デリバリーAI'),
        ]
        y = 2.15
        for biz, ai in deliv:
            self._block(s, 6.83, y, 4.0, 0.85, biz, 13, color=C['navy'],
                        bg=C['light_gray'],
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 10.88, y, 1.95, 0.85, ai, 11, bold=True,
                        color=C['navy'], bg=C['white'],
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.93

        # 下メッセージ
        self._block(s, 0.5, 5.5, 12.33, 1.0,
                    'いろんな領域で AI社員を使っている',
                    22, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s08_results(self):
        """半期¥6,710,000、4案件すべてにAI社員"""
        s = self._slide()
        self._bg(s)
        self._title(s, '半期 ¥6,710,000、4案件すべてにAI社員が動いている', 8)

        cases = [
            ('NTTネクシア', '¥5,000,000'),
            ('中西製作所', '¥1,000,000'),
            ('中部キリンビバレッジ', '¥450,000'),
            ('ブロードリンク', '¥260,000'),
        ]
        y = 1.7
        h = 0.7
        # ヘッダー
        self._block(s, 0.5, y, 5.0, h, '案件', 14, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 5.55, y, 3.0, h, '売上 (税抜)', 14, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.75
        for case, amount in cases:
            self._block(s, 0.5, y, 5.0, h, case, 14, color=C['navy'],
                        bg=C['light_gray'],
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 5.55, y, 3.0, h, amount, 14, color=C['navy'],
                        bg=C['light_gray'],
                        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.75
        self._block(s, 0.5, y, 5.0, h, '半期合計', 16, bold=True,
                    color=C['white'], bg=C['kawaru'],
                    align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 5.55, y, 3.0, h, '¥6,710,000', 16, bold=True,
                    color=C['white'], bg=C['kawaru'],
                    align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

        # 右強調枠
        self._block(s, 9.0, 1.7, 3.83, 4.55,
                    '月換算\n¥464,000\n\n=\n\nAI社員\n1.3人分\n稼働中',
                    20, bold=True, color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s09_now_future(self):
        """ここまで現状、ここから今後"""
        s = self._slide()
        self._bg(s)
        # ライン
        self._line(s, 5.5, 1.5, 2.33, C['kawaru'], 0.06)
        # 中央タイトル
        self._block(s, 0.5, 2.0, 12.33, 1.2, 'ここまでが現状の話',
                    32, bold=True, color=C['gray'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 矢印
        self._block(s, 0.5, 3.3, 12.33, 0.7, '↓',
                    36, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 下：今後
        self._block(s, 0.5, 4.2, 12.33, 1.5, 'ここから今後の話',
                    44, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # サブ
        self._block(s, 0.5, 5.9, 12.33, 0.6,
                    '9月末までにAI社員5人を完成させる、その道筋',
                    16, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # ページ番号
        self._block(s, 12.0, 7.1, 1.1, 0.3, "9 / 11", 10,
                    color=C['gray'], align=PP_ALIGN.RIGHT)

    def s10_roadmap(self):
        """6月末2人分→9月末5人分"""
        s = self._slide()
        self._bg(s)
        self._title(s, '6月末2人分 → 9月末5人分、Agent Teams も並走で構築', 10)

        rows = [
            ('4月 (現在)', '1.3人分', 'デリバリーAI + 戦略AI が稼働中', False),
            ('6月末 (中間発表)', '2人分', '5人全員が同時進行で立ち上がり / Agent Teams 初期構築', True),
            ('7-8月', '3〜4人分', '各領域で深化 / Agent Teams 連携テスト', False),
            ('9月末 (最終)', '5人分', '5人フル稼働 + Agent Teams で協働', True),
        ]
        y = 1.5
        h = 0.7
        # ヘッダー
        self._block(s, 0.5, y, 2.5, h, '月', 14, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 3.05, y, 2.0, h, '達成水準', 14, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 5.10, y, 7.7, h, '動き', 14, bold=True,
                    color=C['white'], bg=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += 0.8
        for month, level, action, emp in rows:
            if emp:
                bg_l = C['kawaru']
                bg_r = C['kawaru_l']
                fc_l = C['white']
                fc_r = C['navy']
            else:
                bg_l = C['light_gray']
                bg_r = C['light_gray']
                fc_l = C['navy']
                fc_r = C['navy']
            self._block(s, 0.5, y, 2.5, h, month, 13, bold=emp, color=fc_l, bg=bg_l,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 3.05, y, 2.0, h, level, 16, bold=True, color=fc_l, bg=bg_l,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(s, 5.10, y, 7.7, h, action, 12, color=fc_r, bg=bg_r,
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
            y += 0.8

        self._block(s, 0.5, 6.0, 12.33, 0.9,
                    '5人を網羅的に同時進行で育てる',
                    18, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s11_close(self):
        """締め"""
        s = self._slide()
        self._bg(s)
        # 大メッセージ
        self._block(s, 0.5, 1.4, 12.33, 1.4,
                    'AI社員を動かして、',
                    36, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 2.7, 12.33, 1.5,
                    'Kawaru事業部の事業を推進する',
                    44, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._line(s, 5.5, 4.4, 2.33, C['kawaru'], 0.06)
        self._block(s, 0.5, 4.9, 12.33, 0.6,
                    '2人 + AI社員5人 + Agent Teams で、Kawaru事業部を動かす',
                    18, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 4サービス
        self._block(s, 1.0, 5.8, 3.5, 0.8, 'Kawaru', 14, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 4.7, 5.8, 2.6, 0.8, 'Kawaru Team', 13, bold=True,
                    color=C['white'], bg=C['team'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 7.4, 5.8, 2.6, 0.8, 'Kawaru Coach', 13, bold=True,
                    color=C['white'], bg=C['coach'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 10.1, 5.8, 2.4, 0.8, 'Kawaru BPO', 13, bold=True,
                    color=C['white'], bg=C['bpo'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # ページ番号
        self._block(s, 12.0, 7.1, 1.1, 0.3, '11 / 11', 10,
                    color=C['gray'], align=PP_ALIGN.RIGHT)

    def build(self, output):
        self.s01_cover()
        self.s02_intro()
        self.s03_4services()
        self.s04_2people()
        self.s05_5agents()
        self.s06_all_business()
        self.s07_how_use()
        self.s08_results()
        self.s09_now_future()
        self.s10_roadmap()
        self.s11_close()
        self.prs.save(output)
        print(f"Saved: {output}")


if __name__ == '__main__':
    output_path = '/Users/kyouyuu/claude/strategy/AI社員5人_発表_20260426.pptx'
    Builder().build(output_path)
