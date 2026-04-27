"""
AI社員5人 発表スライド生成スクリプト（4月末発表用・9枚構成）
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

    def _title(self, slide, text, page_num, total=9):
        # ページ番号
        self._block(slide, 12.3, 0.3, 0.8, 0.3, f"{page_num} / {total}", 10,
                    color=C['gray'], align=PP_ALIGN.RIGHT)
        # タイトル
        self._block(slide, 0.5, 0.4, 12.0, 0.7, text, 22, bold=True, color=C['navy'])
        # アクセントライン
        self._line(slide, 0.5, 1.15, 1.5, C['kawaru'], 0.06)

    # ========== Slides ==========

    def s1(self):
        s = self._slide()
        self._bg(s)
        # メインタイトル
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
        # ページ番号（下）
        self._block(s, 12.3, 7.1, 0.8, 0.3, "1 / 9", 10, color=C['gray'], align=PP_ALIGN.RIGHT)

    def s2(self):
        s = self._slide()
        self._bg(s)
        self._title(s, 'AI社員を動かして、Kawaruプロダクト作りを前に進める', 2)

        # フォーカス：Kawaru プロダクト作り
        self._block(s, 4.0, 1.7, 5.33, 1.4,
                    'Kawaru プロダクト作り\n★ フォーカス ★',
                    20, bold=True, color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 矢印
        self._block(s, 4.0, 3.2, 5.33, 0.5, '↓ AI社員を動かす ↓', 16,
                    color=C['navy'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 同時進行
        self._block(s, 0.5, 3.9, 12.33, 0.4, '─ 同時進行 ─', 13,
                    color=C['gray'], align=PP_ALIGN.CENTER)
        # 3サービス
        self._block(s, 0.7, 4.5, 3.9, 1.5, 'Kawaru Team', 20, bold=True,
                    color=C['white'], bg=C['team'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 4.72, 4.5, 3.9, 1.5, 'Kawaru Coach', 20, bold=True,
                    color=C['white'], bg=C['coach'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 8.74, 4.5, 3.9, 1.5, 'Kawaru BPO', 20, bold=True,
                    color=C['white'], bg=C['bpo'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 0.5, 6.2, 12.33, 0.5,
                    '3つのデリバリーサービスも動かす',
                    14, color=C['gray'], align=PP_ALIGN.CENTER)
        self._block(s, 0.5, 6.7, 12.33, 0.4,
                    'プロダクト作りとデリバリーは同時進行、フォーカスはプロダクト作り',
                    11, color=C['gray'], align=PP_ALIGN.CENTER)

    def s3(self):
        s = self._slide()
        self._bg(s)
        self._title(s, 'AI社員5人の構成', 3)

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
        # キャプション
        self._block(s, 0.5, 6.55, 12.33, 0.4,
                    'マーケから事務までの4人 = 各領域の戦略 + 実行  /  戦略・プロダクトAI = 全体のリサーチ・分析担当',
                    11, color=C['gray'], align=PP_ALIGN.CENTER, bold=True)

    def s4(self):
        s = self._slide()
        self._bg(s)
        self._title(s, 'なぜこの構成にしたか', 4)

        # 縦軸：コア能力
        self._block(s, 0.5, 1.7, 2.5, 0.4, '【縦軸】コア能力', 13,
                    bold=True, color=C['kawaru'])
        self._block(s, 0.5, 2.2, 2.5, 2.2, '作る\n調べる\n設計する\n整理する\n考える',
                    15, color=C['navy'], bg=C['kawaru_l'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 横軸：機能
        self._block(s, 3.5, 1.7, 9.3, 0.4, '【横軸】機能でMECEに網羅', 13,
                    bold=True, color=C['kawaru'])
        funcs = ['マーケ', '営業', 'デリバリー', '事務法務', '戦略']
        cw = 1.78
        cx = 3.5
        for i, f in enumerate(funcs):
            self._block(s, cx + i*cw, 2.2, cw - 0.1, 2.2, f, 16, bold=True,
                        color=C['navy'], bg=C['light_gray'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 下部メッセージ
        self._block(s, 0.5, 5.0, 12.33, 1.2,
                    '案件が変わっても、5人それぞれが受け止められる設計',
                    22, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s5(self):
        s = self._slide()
        self._bg(s)
        self._title(s, 'Kawaru事業部のフルコミットは2人。AI社員5人で動かす', 5)

        # 髙橋COO
        self._block(s, 5.17, 1.5, 3.0, 0.7, '髙橋COO', 18, bold=True,
                    color=C['white'], bg=C['navy'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 6.17, 2.25, 1.0, 0.4, '↓', 18, color=C['gray'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 大川
        self._block(s, 5.17, 2.7, 3.0, 0.7, '大川', 18, bold=True,
                    color=C['white'], bg=C['kawaru'], rounded=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self._block(s, 6.17, 3.45, 1.0, 0.4, '↓', 18, color=C['gray'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 5人のAI社員
        labels = ['マーケ', '営業', 'デリバリー', '事務法務', '戦略']
        for i, l in enumerate(labels):
            x = 0.7 + i*2.5
            self._block(s, x, 3.95, 2.3, 1.2, f'AI社員\n{l}', 14, bold=True,
                        color=C['white'], bg=C['kawaru'], rounded=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # 注記
        self._block(s, 0.5, 5.5, 12.33, 0.4,
                    '業務委託は別途活用、フルコミットはこの2人',
                    12, color=C['gray'], align=PP_ALIGN.CENTER)
        # 強調
        self._block(s, 0.5, 6.1, 12.33, 0.9,
                    '2人だけだから、AI社員5人で事業部を動かす',
                    20, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s6(self):
        s = self._slide()
        self._bg(s)
        self._title(s, '半期 ¥6,710,000、4案件すべてにAI社員が動いている', 6)

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
        # 合計
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

    def s7(self):
        s = self._slide()
        self._bg(s)
        self._title(s, '上流業務でAI社員を使い倒す', 7)

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
        self._block(s, 6.83, 1.5, 6.0, 0.55, 'Kawaru Team / Coach / BPO のデリバリー',
                    14, bold=True, color=C['white'], bg=C['navy'],
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

        # 下強調
        self._block(s, 0.5, 5.5, 12.33, 1.1,
                    '時給 3,000〜5,000円帯の上流領域で AI を使い倒している',
                    22, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bg=C['kawaru_l'], rounded=True)

    def s8(self):
        s = self._slide()
        self._bg(s)
        self._title(s, '6月末2人分 → 9月末5人分、Agent Teams も並走で構築', 8)

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

        # 下強調
        self._block(s, 0.5, 6.0, 12.33, 0.9,
                    '特定の1人を完成させるのではなく、5人を網羅的に育てる',
                    18, bold=True, color=C['kawaru'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def s9(self):
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
        # アクセントライン
        self._line(s, 5.5, 4.4, 2.33, C['kawaru'], 0.06)
        # フッター
        self._block(s, 0.5, 4.9, 12.33, 0.6,
                    '2人 + AI社員5人 + Agent Teams で、Kawaru事業部を動かす',
                    18, bold=True, color=C['navy'],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # 4サービス
        self._block(s, 1.0, 5.8, 3.5, 0.8, 'Kawaru プロダクト', 14, bold=True,
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
        self._block(s, 12.3, 7.1, 0.8, 0.3, '9 / 9', 10,
                    color=C['gray'], align=PP_ALIGN.RIGHT)

    def build(self, output):
        self.s1()
        self.s2()
        self.s3()
        self.s4()
        self.s5()
        self.s6()
        self.s7()
        self.s8()
        self.s9()
        self.prs.save(output)
        print(f"Saved: {output}")


if __name__ == '__main__':
    output_path = '/Users/kyouyuu/claude/strategy/AI社員5人_発表_20260426.pptx'
    Builder().build(output_path)
