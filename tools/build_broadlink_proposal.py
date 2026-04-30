#!/usr/bin/env python3
"""ブロードリンク社向け 2026年度AI研修ご提案書"""
import sys
sys.path.insert(0, '/Users/kyouyuu/claude/tools')
from slide_builder import ProposalBuilder, C, FONT, SLIDE_W, SLIDE_H, M, CW
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

CLIENT = '株式会社ブロードリンク'
DATE_STR = '2026年4月'


class BroadlinkBuilder(ProposalBuilder):

    def section_divider(self, num, title, en_label):
        slide = self._slide(); self._bg(slide)
        self._rect(slide, 0, 0, 0.30, 7.50, C['accent'])
        self._block(slide, 10.50, 0.45, 2.60, 0.35, '株式会社エヌイチ', 13,
                    tc=C['sub'], bold=True, align=PP_ALIGN.RIGHT, rounded=False)
        if num:
            self._block(slide, 0.80, 1.80, 4.0, 2.30, num, 180,
                        tc=C['light_acc'], bold=True, rounded=False, ml=0.08,
                        anchor=MSO_ANCHOR.MIDDLE)
        self._block(slide, 4.80, 2.80, 8.0, 1.00, title, 56,
                    tc=C['title'], bold=True, rounded=False, ml=0.08,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._block(slide, 4.80, 3.95, 8.0, 0.50, en_label, 18,
                    tc=C['accent'], bold=True, rounded=False, ml=0.08,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._rect(slide, 4.80, 4.65, 4.0, 0.05, C['accent'])
        return slide

    def ref_divider(self):
        return self.section_divider('', '参考資料', 'APPENDIX')

    def toc_slide(self, sections):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '目次', 'Contents')
        rh = 0.85
        rg = 0.20
        for i, (num, title, en) in enumerate(sections):
            ry = y + 0.20 + i * (rh + rg)
            self._rect(slide, M, ry, CW, rh, C['white'], rounded=True)
            self._rect(slide, M, ry, 0.06, rh, C['accent'])
            self._block(slide, M + 0.30, ry, 1.30, rh, num, 32,
                        tc=C['accent'], bold=True, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.MIDDLE, rounded=False)
            self._block(slide, M + 1.70, ry + 0.08, 9.0, 0.42, title, 18,
                        tc=C['title'], bold=True, rounded=False, ml=0.04,
                        anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 1.70, ry + 0.50, 9.0, 0.30, en, 11,
                        tc=C['sub'], rounded=False, ml=0.04)
        return slide

    def request_slide(self, requests):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '山道さまから頂いたリクエスト', '振り返り｜4/17商談')
        n = len(requests)
        avail = 7.20 - y
        rh = (avail - 0.10 * (n - 1)) / n
        for i, req in enumerate(requests):
            ry = y + i * (rh + 0.10)
            self._rect(slide, M + 0.80, ry, CW - 0.80, rh, C['card'], rounded=True)
            self._rect(slide, M + 0.80, ry, 0.06, rh, C['accent'])
            self._badge(slide, M + 0.35, ry + rh / 2, 0.26, str(i + 1))
            self._block(slide, M + 1.10, ry, CW - 1.20, rh, req, 14,
                        tc=C['body'], rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.MIDDLE)
        return slide

    def current_state_slide(self, items):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '8年目のISMS研修と、拠点で割れるAI温度', '現状｜事業環境')
        n = len(items)
        avail = 7.20 - y
        rh = (avail - 0.10 * (n - 1)) / n
        for i, item in enumerate(items):
            ry = y + i * (rh + 0.10)
            self._rect(slide, M, ry, CW, rh, C['white'], rounded=True)
            self._rect(slide, M, ry, 0.06, rh, C['accent'])
            self._block(slide, M + 0.30, ry + 0.10, 0.90, rh - 0.20, str(i + 1), 22,
                        bg=C['light_acc'], tc=C['accent'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 1.40, ry, CW - 1.50, rh, item, 14,
                        tc=C['body'], rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.MIDDLE)
        return slide

    def issues_3col(self, issues):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '課題は3つに集約される', '課題｜全体俯瞰')
        cw = 3.85
        gap = 0.39
        for i, (title, desc) in enumerate(issues):
            cx = M + i * (cw + gap)
            ct = y + 0.20
            ch = 5.30
            self._rect(slide, cx, ct, cw, ch, C['white'], rounded=True)
            self._rect(slide, cx, ct, 0.06, ch, C['issue_bar'])
            self._badge(slide, cx + 0.50, ct + 0.50, 0.30, str(i + 1),
                        bg=C['issue_bar'])
            self._block(slide, cx + 0.95, ct + 0.20, cw - 1.10, 0.65, title, 17,
                        tc=C['body'], bold=True, rounded=False, ml=0.04,
                        anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, cx + 0.20, ct + 1.20, cw - 0.40, ch - 1.40, desc, 13,
                        bg=C['issue_bg'], tc=C['body'], bar_color=C['issue_bar'],
                        anchor=MSO_ANCHOR.TOP)
        return slide

    def approach_slide(self, approaches):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '「知る」から「使える」への転換', 'ご要望への回答方針')
        n = len(approaches)
        avail = 7.20 - y
        rh = (avail - 0.10 * (n - 1)) / n
        for i, (title, desc) in enumerate(approaches):
            ry = y + i * (rh + 0.10)
            self._rect(slide, M, ry, CW, rh, C['white'], rounded=True)
            self._rect(slide, M, ry, 0.06, rh, C['accent'])
            self._badge(slide, M + 0.40, ry + rh / 2, 0.26, str(i + 1))
            self._block(slide, M + 0.95, ry + 0.10, 4.30, rh - 0.20, title, 16,
                        bg=C['highlight'], tc=C['accent'], bold=True,
                        anchor=MSO_ANCHOR.MIDDLE, bar_color=C['accent'])
            self._block(slide, M + 5.50, ry, CW - 5.60, rh, desc, 13,
                        tc=C['body'], rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.MIDDLE)
        return slide

    def concept_slide(self):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '体験で腹落ちさせる、実戦研修', '研修コンセプト｜AI実務活用・実戦編')
        self._block(slide, M, y + 0.15, CW, 1.20,
                    '去年は「知る」／今年は「使える」になる研修', 28,
                    bg=C['highlight'], tc=C['title'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bar_color=C['accent'])
        sy = y + 1.65
        story = [
            ('体験', '第3章でラッキーパズル（2人1組で言葉だけで形を伝えるゲーム）を実施'),
            ('伏線回収', 'ゲーム中は目的を伏せ、後半で「実はこれがAIへの指示の出し方」と種明かし'),
            ('腹落ち', '「ガチガチの指示書はいらない、会話するように渡す」をコンテキストエンジとして体得'),
            ('進化', '最新概念（コンテキストエンジ）を、難しい言葉ではなく体験で習得させる構成'),
        ]
        n = len(story)
        avail = 7.30 - sy
        rh = (avail - 0.10 * (n - 1)) / n
        for i, (label, desc) in enumerate(story):
            ry = sy + i * (rh + 0.10)
            self._rect(slide, M, ry, CW, rh, C['card'], rounded=True)
            self._rect(slide, M, ry, 0.06, rh, C['accent'])
            self._block(slide, M + 0.20, ry + 0.10, 1.80, rh - 0.20, label, 15,
                        bg=C['light_acc'], tc=C['accent'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 2.20, ry, CW - 2.30, rh, desc, 13,
                        tc=C['body'], rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.MIDDLE)
        return slide

    def timeline_slide(self, items):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '2時間で5章を駆け抜ける', 'アジェンダ｜全体タイムライン')
        hy = y + 0.10
        cols = [
            (M, 2.00, '時間'),
            (M + 2.10, 1.30, '章'),
            (M + 3.50, 7.50, '内容'),
            (M + 11.10, 1.23, '時間'),
        ]
        for cx, cwd, h in cols:
            self._block(slide, cx, hy, cwd, 0.45, h, 12,
                        bg=C['dark_head'], tc=C['white'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ry = hy + 0.55
        rh = 0.78
        for i, (time, ch, content, dur, highlight) in enumerate(items):
            bg = C['highlight'] if highlight else (C['card'] if i % 2 == 0 else C['white'])
            tc_main = C['accent'] if highlight else C['body']
            self._block(slide, M, ry, 2.00, rh, time, 13,
                        bg=bg, tc=C['body'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 2.10, ry, 1.30, rh, ch, 13,
                        bg=bg, tc=tc_main, bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 3.50, ry, 7.50, rh, content, 13,
                        bg=bg, tc=C['body'], bold=highlight,
                        anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 11.10, ry, 1.23, rh, dur, 13,
                        bg=bg, tc=tc_main, bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            ry += rh + 0.05
        return slide

    def chapter_highlights(self, title, sub, chapters):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, title, sub)
        n = len(chapters)
        avail = 7.30 - y
        rh = (avail - 0.15 * (n - 1)) / n
        for i, (ch_title, ch_desc) in enumerate(chapters):
            ry = y + i * (rh + 0.15)
            self._rect(slide, M, ry, CW, rh, C['white'], rounded=True)
            self._rect(slide, M, ry, 0.06, rh, C['accent'])
            self._block(slide, M + 0.20, ry + 0.10, 4.50, 0.50, ch_title, 16,
                        bg=C['info_bg'], tc=C['body'], bold=True,
                        bar_color=C['info_bar'], anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 0.20, ry + 0.65, CW - 0.40, rh - 0.75, ch_desc, 12,
                        tc=C['body'], rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.TOP)
        return slide

    def location_handson(self, locations):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '本社とTCで、中身を差し替える', '第4章｜拠点別実践（25分）')
        cw = 6.05
        gap = 0.23
        for i, (loc, level, content, aim) in enumerate(locations):
            cx = M + i * (cw + gap)
            ct = y + 0.10
            ch = 5.50
            self._rect(slide, cx, ct, cw, ch, C['white'], rounded=True)
            self._rect(slide, cx, ct, 0.06, ch, C['accent'])
            self._block(slide, cx + 0.20, ct + 0.10, cw - 0.40, 0.50, loc, 18,
                        tc=C['body'], bold=True, rounded=False, ml=0.10,
                        anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, cx + 0.20, ct + 0.65, cw - 0.40, 0.35, level, 11,
                        bg=C['highlight'], tc=C['accent'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._section_head(slide, cx + 0.20, ct + 1.15, cw - 0.40, '内容', 12)
            self._block(slide, cx + 0.20, ct + 1.50, cw - 0.40, 2.50, content, 12,
                        bg=C['card'], tc=C['body'], bar_color=C['accent'])
            self._section_head(slide, cx + 0.20, ct + 4.15, cw - 0.40, 'ねらい', 12)
            self._block(slide, cx + 0.20, ct + 4.50, cw - 0.40, 0.90, aim, 12,
                        bg=C['ok_bg'], tc=C['body'], bar_color=C['ok_bar'])
        return slide

    def implementation_slide(self, items):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '2拠点 × 2時間、2026年7月実施', '実施概要')
        n = len(items)
        avail = 7.20 - y
        rh = (avail - 0.10 * (n - 1)) / n
        for i, (label, val) in enumerate(items):
            ry = y + i * (rh + 0.10)
            self._block(slide, M, ry, 2.80, rh, label, 13,
                        bg=C['light_acc'], tc=C['accent'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._block(slide, M + 2.90, ry, CW - 2.90, rh, val, 14,
                        bg=C['card'], tc=C['body'], bar_color=C['accent'],
                        anchor=MSO_ANCHOR.MIDDLE)
        return slide

    def pricing_simple(self):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '税込286,000円（税抜260,000円）据え置き', 'お見積り')
        cx = 2.0
        cw = 9.33
        ct = y + 0.40
        ch = 4.20
        self._rect(slide, cx, ct, cw, ch, C['highlight'], rounded=True)
        self._rect(slide, cx, ct, 0.10, ch, C['accent'])
        self._block(slide, cx + 0.30, ct + 0.30, cw - 0.50, 0.45, '売上（税抜）', 16,
                    tc=C['sub'], bold=True, rounded=False, ml=0.10)
        self._block(slide, cx + 0.30, ct + 0.80, cw - 0.50, 0.85, '260,000円', 44,
                    tc=C['body'], bold=True, rounded=False, ml=0.10,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._rect(slide, cx + 0.30, ct + 1.85, cw - 0.60, 0.025, C['divider'])
        self._block(slide, cx + 0.30, ct + 2.05, cw - 0.50, 0.45, '売上（税込）', 16,
                    tc=C['accent'], bold=True, rounded=False, ml=0.10)
        self._block(slide, cx + 0.30, ct + 2.55, cw - 0.50, 1.10, '286,000円', 56,
                    tc=C['accent'], bold=True, rounded=False, ml=0.10,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._block(slide, M, 6.40, CW, 0.50, '前年同額（据え置き）', 18,
                    bg=C['ok_bg'], tc=C['ok_text'], bold=True,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    bar_color=C['ok_bar'])
        return slide

    def next_steps_4(self, steps):
        slide = self._slide(); self._bg(slide)
        y = self._title_bar(slide, '5月末から7月実施までの動き', 'NEXT STEP')
        n = len(steps)
        cw = (CW - (n - 1) * 0.20) / n
        for i, (step_label, time, action) in enumerate(steps):
            cx = M + i * (cw + 0.20)
            ct = y + 0.30
            ch = 5.20
            self._block(slide, cx, ct, cw, 0.55, step_label, 14,
                        bg=C['accent'], tc=C['white'], bold=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._rect(slide, cx, ct + 0.65, cw, ch - 0.65, C['white'], rounded=True)
            self._rect(slide, cx, ct + 0.65, 0.06, ch - 0.65, C['accent'])
            self._block(slide, cx + 0.15, ct + 0.85, cw - 0.30, 0.70, time, 24,
                        tc=C['accent'], bold=True, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.MIDDLE, rounded=False)
            self._rect(slide, cx + 0.40, ct + 1.65, cw - 0.80, 0.025, C['divider'])
            self._block(slide, cx + 0.15, ct + 1.85, cw - 0.30, 2.50, action, 14,
                        tc=C['body'], bold=True, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.TOP, ml=0.10)
            if i < n - 1:
                ax = cx + cw + 0.02
                self._block(slide, ax, y + 2.80, 0.18, 0.40, '→', 22,
                            tc=C['accent'], bold=True, align=PP_ALIGN.CENTER,
                            anchor=MSO_ANCHOR.MIDDLE, rounded=False)
        return slide

    def closing_simple(self):
        slide = self._slide(); self._bg(slide)
        self._rect(slide, 0, 0, 0.30, 7.50, C['accent'])
        self._block(slide, 1.0, 2.50, 11.33, 1.50,
                    '"使える" が、定着する研修へ', 48,
                    tc=C['title'], bold=True, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE, rounded=False)
        self._rect(slide, 5.0, 4.20, 3.33, 0.05, C['accent'])
        self._block(slide, 1.0, 4.80, 11.33, 0.50, '株式会社エヌイチ', 22,
                    tc=C['body'], bold=True, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE, rounded=False)
        self._block(slide, 1.0, 5.40, 11.33, 0.40, 'AI（アイ）ある社会に', 14,
                    tc=C['accent'], align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE, rounded=False)
        return slide


def main():
    b = BroadlinkBuilder(CLIENT, DATE_STR)

    # 1. 表紙
    b.cover()

    # 2. 目次
    b.toc_slide([
        ('01', '振り返り｜前回商談のご要望', 'RECAP'),
        ('02', '現状｜御社のAI活用環境', 'CURRENT STATE'),
        ('03', '課題｜弊社で抽出した3点', 'ISSUES'),
        ('04', '弊社方針｜「使える」へのシフト', 'OUR APPROACH'),
        ('05', '研修内容｜AI実務活用・実戦編', 'PROGRAM'),
    ])

    # 3. 区切り 01
    b.section_divider('01', '振り返り', 'RECAP')

    # 4. 前回ご要望
    b.request_slide([
        '基礎より「実戦」へ — 「こういう使い方ができる」という方向性が伝わればOK',
        '2時間 × 2拠点（本社／本部TC）でオンライン実施',
        'ISMS要素は2割マックス（ハルシネーション・情報漏洩を短く）',
        'スプレッドシート活用を重点化したい',
        '金額は前回据え置きを希望（税込30万円ボーダー）',
    ])

    # 5. 区切り 02
    b.section_divider('02', '現状', 'CURRENT STATE')

    # 6. 御社の現状
    b.current_state_slide([
        'ISMS年次研修は8年目。「もう飽きちゃってる」（山道さまご発言）',
        '本社・大阪支店：Google Workspace導入済み／Gemini日常使い／副社長はGAS活用',
        '本部TC・大阪TC：ほぼAI未使用／業務はキッティング・報告書・マニュアル作成中心',
        'Google Workspace導入済み。ただし慣れたExcelを使い続ける社員が多く、スプレッドシート活用が浅い',
    ])

    # 7. 区切り 03
    b.section_divider('03', '課題', 'ISSUES')

    # 8. 抽出した課題（順序：マンネリ化／温度差／AI活用）
    b.issues_3col([
        ('研修のマンネリ化',
         '8年連続のISMS研修で「やらされ感」が蔓延。\n同じ枠の継続では参加者の集中が持続しない'),
        ('拠点間温度差',
         '本社（高リテラシー）／TC（低リテラシー）の二極化。\n一律研修では「物足りない／ついていけない」が同時発生'),
        ('AIを活かしきれていない',
         'GWS・Geminiは導入済みだが業務に落ちていない。\nAIコンサルは特定部署のみで全社底上げにつながっていない'),
    ])

    # 9. 区切り 04
    b.section_divider('04', '弊社方針', 'OUR APPROACH')

    # 10. 弊社方針
    b.approach_slide([
        ('実戦シフト', '座学は最小限。ハンズオン50分を中心に据える'),
        ('拠点別差替え', '本社（スプシ×Gemini×GAS）／TC（業務別Gem量産）で温度差を吸収'),
        ('ISMSは"濃く・短く"', 'セキュリティ要素は事例ベースで凝縮し、研修全体の20%以内に収める'),
        ('金額据え置き', '税込286,000円（税抜260,000円）／前年同額'),
    ])

    # 11. 区切り 05
    b.section_divider('05', '研修内容', 'PROGRAM')

    # 12. プログラムコンセプト
    b.concept_slide()

    # 13. タイムライン
    b.timeline_slide([
        ('0:00 - 0:05', '第1章', '導入', '5分', False),
        ('0:05 - 0:20', '第2章', 'AI基礎＋セキュリティ', '15分', False),
        ('0:20 - 0:50', '第3章', 'ゲーム → 伏線回収 → プロンプト', '30分', True),
        ('0:50 - 1:00', '—', '☕ 休憩', '10分', False),
        ('1:00 - 1:50', '第4章', 'ハンズオン実践', '50分', True),
        ('1:50 - 2:00', '第5章', 'まとめ＋質疑', '10分', False),
    ])

    # 14. 章別前半
    b.chapter_highlights(
        '前半｜AIを"体で"腹落ちさせる', '第1〜3章',
        [
            ('第1章 導入（5分）',
             '・講師紹介\n・この1年のAI進化（GPT-5・Gemini 3・推論モデル・エージェント化）\n・ゴール3本柱（理解する／任せる／実践する）'),
            ('第2章 AI基礎＋セキュリティ（15分）',
             '・LLMの仕組み（予測変換の超強力版）\n・ハルシネーションと企業実例\n・セキュリティ × ISMS（入力禁止情報・GWS版Geminiの安全性）'),
            ('第3章 ゲーム→伏線回収→プロンプト（30分）',
             '・ラッキーパズル20分（2人1組・言葉だけで形を伝える）\n・伏線回収「実はこれがコンテキストエンジ」\n・プロンプトの考え方（役割・目的・対象・制約）'),
        ]
    )

    # 15. 章別後半
    b.chapter_highlights(
        '後半｜手を動かして"使える"に変える', '第4〜5章',
        [
            ('第4章 ハンズオン実践（50分）',
             '① Gemini基本＋Google Workspace連携（10分）\n② Gems基礎：自分専用の"部下"を作る（15分）\n③ 拠点別実践（25分／本社・TCで内容を差替え）'),
            ('第5章 まとめ＋質疑（10分）',
             '・5トピック（セキュリティ／AI基礎／プロンプト・コンテキスト／Gemini／GWS）を1枚で振り返り\n・質疑応答'),
        ]
    )

    # 16. 拠点別ハンズオン
    b.location_handson([
        ('本社・大阪支店',
         '高リテラシー層',
         'スプレッドシート × Gemini × GAS\n\n・関数をAIに作らせる\n・汚いデータをAIで整形する\n・GAS紹介（Gmail自動送信／シート連動）',
         'Excel脳からスプシへの移行促進。\n副社長が使うGAS活用を全社に広げる'),
        ('本部TC・大阪TC',
         '低リテラシー層',
         '業務別Gem量産ワーク\n\n・講師デモ（マニュアル作成Gem）\n・各自作成（メール／マニュアル／日報から1つ選んでGem化）\n・発表（2-3名）',
         '「口頭でOK」の体感。\n自分のGemを1個持ち帰る成功体験'),
    ])

    # 17. 実施規模
    b.implementation_slide([
        ('実施形式', 'オンライン研修（Google Meet）'),
        ('実施拠点', '本社（大阪支店オンライン接続）／本部TC（大阪TCオンライン接続）'),
        ('1拠点あたり', '2時間 × 1回'),
        ('参加人数', '各拠点 15〜20名／最大40名（合計）'),
        ('実施時期', '2026年7月（第1〜2週 or 7/21-31）'),
        ('講師', '大川 龍之介（株式会社エヌイチ）'),
    ])

    # 18. 費用
    b.pricing_simple()

    # 19. ネクストアクション
    b.next_steps_4([
        ('STEP 1', '5月末', '事前アンケート\n（Googleフォーム）\n実施'),
        ('STEP 2', '5月末', '実施日程の\n確定'),
        ('STEP 3', '6月', '研修資料作成\n・準備'),
        ('STEP 4', '7月', '研修実施'),
    ])

    # 20. 締め
    b.closing_simple()

    # 21. 参考資料区切り
    b.ref_divider()

    # 22. 会社概要
    b.company_overview()

    # 23. 導入実績
    b.case_studies()

    out = '/Users/kyouyuu/claude/output/proposal_broadlink_20260430.pptx'
    b.save(out)
    print(f'Saved: {out}')
    print(f'Slides: {len(b.prs.slides)}')


if __name__ == '__main__':
    main()
