#!/usr/bin/env python3
"""展示会準備ガントチャート生成 — Eight EXPO 2026 夏"""

import os, json, datetime as dt
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ══════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════
SSID  = '1iLmAUAayRM_cdFPZF2YXow7spbe-ZwYemTJmUdJQKek'
SID   = 0
SNAME = 'ガントチャート'
MASTER_SID   = 999
MASTER_SNAME = 'マスター'
ENTRY_SID    = 998
ENTRY_SNAME  = '出展情報_入力管理'
START = dt.date(2026, 4, 9)
END   = dt.date(2026, 6, 11)
C0    = 8   # first date column index (I) — A:WBS B:タスク C:担当 D:責任者 E:開始 F:期限 G:優先度 H:ステータス
HDROWS = 5  # header rows (0-4)

DOW_JA = '月火水木金土日'
HOLIDAYS = {dt.date(2026,4,29), dt.date(2026,5,3), dt.date(2026,5,4),
            dt.date(2026,5,5), dt.date(2026,5,6)}

# ══════════════════════════════════════════════════════════════════════
# COLORS
# ══════════════════════════════════════════════════════════════════════
def hx(h):
    h = h.lstrip('#')
    return {'red': int(h[:2],16)/255, 'green': int(h[2:4],16)/255, 'blue': int(h[4:6],16)/255}

WHITE     = hx('#FFFFFF')
BLACK     = hx('#333333')
TITLE_BG  = hx('#0D1B2A')
HDR_BG    = hx('#1B2A4A')
WEEK_BG   = hx('#34495E')
WKEND_BG  = hx('#F0F0F0')
WKEND_HDR = hx('#546E7A')
DL_RED    = hx('#E53935')
EXPO_GOLD = hx('#FF6F00')

CAT = {
    '出展情報登録':      dict(h=hx('#0D47A1'), r=hx('#E3F2FD'), b=hx('#42A5F5'), m=hx('#0D47A1')),
    '4/24 事務局申請':   dict(h=hx('#1565C0'), r=hx('#E8EAF6'), b=hx('#5C6BC0'), m=hx('#1A237E')),
    '制作：共通':                         dict(h=hx('#BF360C'), r=hx('#FBE9E7'), b=hx('#FF8A65'), m=hx('#BF360C')),
    '制作：パネル（W4910×H2050）':        dict(h=hx('#E65100'), r=hx('#FFF3E0'), b=hx('#FFA726'), m=hx('#E65100')),
    '制作：フライヤー（Kawaru / Kawaru Team）': dict(h=hx('#F57F17'), r=hx('#FFFDE7'), b=hx('#FFD54F'), m=hx('#F57F17')),
    '制作：サービス資料（4プロダクト統合版）':    dict(h=hx('#FF6F00'), r=hx('#FFF8E1'), b=hx('#FFCA28'), m=hx('#FF6F00')),
    '制作：デモ動画':                      dict(h=hx('#E64A19'), r=hx('#FBE9E7'), b=hx('#FF7043'), m=hx('#D84315')),
    '集客・営業':        dict(h=hx('#2E7D32'), r=hx('#E8F5E9'), b=hx('#66BB6A'), m=hx('#1B5E20')),
    'ロジ・当日運営':     dict(h=hx('#6A1B9A'), r=hx('#F3E5F5'), b=hx('#AB47BC'), m=hx('#4A148C')),
    'フォローアップ':     dict(h=hx('#37474F'), r=hx('#ECEFF1'), b=hx('#78909C'), m=hx('#263238')),
}

STATUS_COLORS = {
    '未着手': hx('#F5F5F5'), '進行中': hx('#E3F2FD'), '完了': hx('#E8F5E9'),
    '要検討': hx('#FFF8E1'), '保留':  hx('#FFEBEE'), '要確認': hx('#E8EAF6'),
}

# ══════════════════════════════════════════════════════════════════════
# MASTER DATA
# ══════════════════════════════════════════════════════════════════════
MEMBERS = ['大川', '髙橋悠', '髙橋美優', '柳沼', '果歩', '外部デザイナー', '社内']
STATUSES = ['未着手', '進行中', '完了', '要検討', '保留', '要確認']

# ══════════════════════════════════════════════════════════════════════
# TASK DATA
# ══════════════════════════════════════════════════════════════════════
def D(m, d): return dt.date(2026, m, d)

# (wbs, name, owner, responsible, start, end, priority, status, is_milestone)
# priority: 高/中/低
TASKS = [
    ('出展情報登録', [
        ('1.1',  '掲載サービス数の確定（全5枠 or 絞り込み）', '大川', '髙橋悠',  D(4,9),  D(4,14), '高', '未着手', False),
        ('1.2',  'サービスロゴ ファイル形式確認（RGB/ai/png）','大川', '髙橋美優',D(4,9),  D(4,14), '高', '未着手', False),
        ('1.3',  'サービス名・フリガナ（各サービス40字）',     '大川', '大川',    D(4,9),  D(4,14), '中', '未着手', False),
        ('1.4',  'キャッチコピー（各30字以内）',              '大川', '髙橋悠',  D(4,9),  D(4,14), '高', '未着手', False),
        ('1.5',  'サービス紹介文（各130字以内）',             '大川', '大川',    D(4,9),  D(4,18), '高', '未着手', False),
        ('1.6',  'サービスイメージ画像（675×1200px）',        '髙橋美優','大川', D(4,9),  D(4,18), '高', '未着手', False),
        ('1.7',  'ピックアップポイント①②③（各20字）',        '大川', '大川',    D(4,9),  D(4,18), '高', '未着手', False),
        ('1.8',  'こんな課題はありませんか？①②③（各40字）',   '大川', '大川',    D(4,9),  D(4,18), '高', '未着手', False),
        ('1.9',  'サービス対象（50字以内）',                  '大川', '大川',    D(4,9),  D(4,18), '中', '未着手', False),
        ('1.10', 'ブース訪問特典（30字以内）',                '大川', '髙橋悠',  D(4,14), D(4,18), '中', '未着手', False),
        ('1.11', 'マッチング対象設定（属性選択）',             '大川', '大川',    D(4,14), D(4,18), '低', '未着手', False),
        ('1.12', '検索条件キーワード（3つ）・フリーワード',     '大川', '大川',    D(4,14), D(4,18), '低', '未着手', False),
        ('1.13', '動画・資料アップロード（任意）',             '大川', '大川',    D(5,7),  D(5,15), '低', '未着手', False),
        ('1.14', '商談枠数設定',                             '大川', '大川',    D(4,14), D(4,18), '低', '要確認', False),
        ('1.15', '◆ 出展情報登録 全項目入力完了（4/18〆切）',   '大川', '大川',    D(4,18), D(4,18), '高', '未着手', True),
        ('1.16', '担当者アカウント申請（管理画面付与）',         '大川', '大川',    D(4,10), D(4,17), '高', '未着手', False),
    ]),
    ('4/24 事務局申請', [
        ('2.1', '基礎装飾確認申請（パネル入稿）',        '大川', '大川', D(4,23), D(4,24), '高', '未着手', False),
        ('2.2', '名刺交換担当者申請（Eight QR読取）',    '大川', '大川', D(4,21), D(4,24), '中', '未着手', False),
        ('2.3', '課題解決キーワード申請（3つ選択）',      '大川', '大川', D(4,21), D(4,24), '中', '未着手', False),
        ('2.4', '出展社パス枚数申請',                   '大川', '大川', D(4,21), D(4,24), '中', '未着手', False),
        ('2.5', '共有アカウント申請（名刺画像作成含む）',  '大川', '大川', D(4,14), D(4,24), '高', '未着手', False),
        ('2.6', '搬入出車輌申請（想定最大で入力）',       '大川', '大川', D(4,21), D(4,24), '中', '未着手', False),
        ('2.7', 'オプション備品申込（モニター等）',       '大川', '大川', D(4,21), D(4,24), '低', '要検討', False),
        ('2.8', '◆ 4/24 全申請提出完了',               '大川', '大川', D(4,24), D(4,24), '高', '未着手', True),
    ]),
    ('制作：共通', [
        ('3.0', '前回素材確認・修正箇所リストアップ',    '大川', '大川', D(4,9), D(4,11), '高', '未着手', False),
        ('3.9', '◆ 印刷発注（パネル・フライヤー・資料）', '大川', '大川', D(5,25),D(5,25), '高', '未着手', True),
    ]),
    ('制作：パネル（W4910×H2050）', [
        ('3.1.1', '内容決め（コピー・構成・方針）',    '大川',     '髙橋悠', D(4,9),  D(4,14), '高', '未着手', False),
        ('3.1.2', 'デザイナーに発注',               '大川',     '大川',   D(4,14), D(4,15), '高', '未着手', False),
        ('3.1.3', '初稿上がり',                    '髙橋美優', '大川',   D(4,15), D(4,18), '高', '未着手', False),
        ('3.1.4', 'FB・修正',                      '大川',     '大川',   D(4,18), D(4,23), '高', '未着手', False),
        ('3.1.5', '◆ 最終FIX・入稿（ai形式）',      '髙橋美優', '大川',   D(4,23), D(4,23), '高', '未着手', True),
    ]),
    ('制作：フライヤー（Kawaru / Kawaru Team）', [
        ('3.2.1', '内容決め（前回ベース・修正方針）',  '大川',     '髙橋悠', D(4,9),  D(4,14), '高', '未着手', False),
        ('3.2.2', 'デザイナーに発注',               '大川',     '大川',   D(4,15), D(4,15), '中', '未着手', False),
        ('3.2.3', '初稿上がり',                    '髙橋美優', '大川',   D(4,15), D(5,2),  '中', '未着手', False),
        ('3.2.4', 'FB・修正',                      '大川',     '大川',   D(5,2),  D(5,16), '中', '未着手', False),
        ('3.2.5', '◆ 最終FIX',                    '髙橋美優', '大川',   D(5,20), D(5,20), '中', '未着手', True),
    ]),
    ('制作：サービス資料（4プロダクト統合版）', [
        ('3.3.1', '内容決め（構成・掲載サービス）',    '大川',     '髙橋悠', D(5,7),  D(5,9),  '中', '未着手', False),
        ('3.3.2', 'デザイナーに発注',               '大川',     '大川',   D(5,9),  D(5,9),  '中', '未着手', False),
        ('3.3.3', '初稿上がり',                    '髙橋美優', '大川',   D(5,9),  D(5,16), '中', '未着手', False),
        ('3.3.4', 'FB・修正',                      '大川',     '大川',   D(5,14), D(5,20), '中', '未着手', False),
        ('3.3.5', '◆ 最終FIX',                    '大川',     '大川',   D(5,22), D(5,22), '中', '未着手', True),
    ]),
    ('制作：デモ動画', [
        ('3.4.1', '内容決め（構成・シナリオ）',        '大川', '大川', D(4,14), D(4,18), '中', '未着手', False),
        ('3.4.2', '撮影依頼・実施',                  '社内', '大川', D(4,21), D(4,22), '中', '未着手', False),
        ('3.4.3', '初稿上がり（編集完了）',           '社内', '大川', D(4,22), D(5,2),  '中', '未着手', False),
        ('3.4.4', 'FB・修正',                       '大川', '大川', D(5,2),  D(5,8),  '中', '未着手', False),
        ('3.4.5', '◆ 最終FIX・掲載',               '大川', '大川', D(5,9),  D(5,9),  '中', '未着手', True),
    ]),
    ('集客・営業', [
        ('4.1', '来訪リクエスト配信文面作成',    '大川', '大川',   D(4,9),  D(4,18), '中', '未着手', False),
        ('4.2', '配信リスト整備',              '大川', '大川',   D(4,21), D(5,9),  '中', '未着手', False),
        ('4.3', '商談予約特典 内容確定',        '大川', '髙橋悠', D(4,14), D(4,24), '中', '未着手', False),
        ('4.4', '出展社ページ素材アップロード',  '大川', '大川',   D(5,7),  D(5,15), '中', '未着手', False),
        ('4.5', '◆ 来訪リクエスト配信',        '大川', '大川',   D(5,12), D(5,23), '中', '未着手', True),
        ('4.6', '事前TELスクリプト作成',        '大川', '大川',   D(5,7),  D(5,15), '低', '未着手', False),
        ('4.7', '◆ 事前TEL実施',              '大川', '大川',   D(5,19), D(5,30), '低', '未着手', True),
    ]),
    ('ロジ・当日運営', [
        ('5.1', 'リード管理フロー設計（前回改善）', '大川', '大川', D(4,14), D(5,15), '低', '未着手', False),
        ('5.2', 'iPad準備・設定',                '大川', '大川', D(5,19), D(5,30), '低', '未着手', False),
        ('5.3', '車手配',                       '大川', '大川', D(5,19), D(5,30), '低', '未着手', False),
        ('5.4', '🎌 展示会当日',                 '大川', '大川', D(6,3),  D(6,4),  '中', '未着手', True),
    ]),
    ('フォローアップ', [
        ('6.1', 'サンクスメールテンプレ作成',       '大川', '大川', D(5,7),  D(5,15), '低', '未着手', False),
        ('6.2', '架電フロー・テンプレ設計',         '大川', '大川', D(5,7),  D(5,15), '低', '未着手', False),
        ('6.3', 'リード情報ダウンロード',           '大川', '大川', D(6,4),  D(6,11), '低', '未着手', False),
        ('6.4', '◆ フォロー実施（メール・架電）',    '大川', '大川', D(6,5),  D(6,11), '低', '未着手', True),
    ]),
]

# ══════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════
def rng(r0, r1, c0, c1):
    return {'sheetId': SID, 'startRowIndex': r0, 'endRowIndex': r1,
            'startColumnIndex': c0, 'endColumnIndex': c1}

def fc(r0, r1, c0, c1, **kw):
    """repeatCell format request."""
    cf, fl = {}, []
    if 'bg' in kw:
        cf['backgroundColor'] = kw['bg']; fl.append('userEnteredFormat.backgroundColor')
    tf = {}
    if 'fg' in kw: tf['foregroundColor'] = kw['fg']
    if 'bold' in kw: tf['bold'] = kw['bold']
    if 'sz' in kw: tf['fontSize'] = kw['sz']
    if tf:
        cf['textFormat'] = tf; fl.append('userEnteredFormat.textFormat')
    if 'ha' in kw:
        cf['horizontalAlignment'] = kw['ha']; fl.append('userEnteredFormat.horizontalAlignment')
    if 'va' in kw:
        cf['verticalAlignment'] = kw['va']; fl.append('userEnteredFormat.verticalAlignment')
    if 'wrap' in kw:
        cf['wrapStrategy'] = 'WRAP'; fl.append('userEnteredFormat.wrapStrategy')
    return {'repeatCell': {'range': rng(r0, r1, c0, c1),
            'cell': {'userEnteredFormat': cf}, 'fields': ','.join(fl)}}

def mg(r0, r1, c0, c1):
    return {'mergeCells': {'range': rng(r0, r1, c0, c1), 'mergeType': 'MERGE_ALL'}}

def rh(row, h):
    return {'updateDimensionProperties': {
        'range': {'sheetId': SID, 'dimension': 'ROWS', 'startIndex': row, 'endIndex': row+1},
        'properties': {'pixelSize': h}, 'fields': 'pixelSize'}}

def colw(c0, c1, w):
    return {'updateDimensionProperties': {
        'range': {'sheetId': SID, 'dimension': 'COLUMNS', 'startIndex': c0, 'endIndex': c1},
        'properties': {'pixelSize': w}, 'fields': 'pixelSize'}}

def dv(r0, r1, c0, c1, vals, strict=True):
    return {'setDataValidation': {'range': rng(r0, r1, c0, c1),
        'rule': {'condition': {'type': 'ONE_OF_LIST',
                 'values': [{'userEnteredValue': v} for v in vals]},
                 'showCustomUi': True, 'strict': strict}}}

def cf_rule(r0, r1, c0, c1, text, bg, idx=0):
    return {'addConditionalFormatRule': {
        'rule': {'ranges': [rng(r0, r1, c0, c1)],
                 'booleanRule': {'condition': {'type': 'TEXT_EQ',
                    'values': [{'userEnteredValue': text}]},
                    'format': {'backgroundColor': bg}}}, 'index': idx}}

def gen_dates():
    dates, d = [], START
    while d <= END:
        dates.append(d); d += dt.timedelta(days=1)
    return dates

def week_groups(dates):
    groups, cm, cd = [], None, []
    for d in dates:
        m = d - dt.timedelta(days=d.weekday())
        if m != cm:
            if cd: groups.append((cm, cd))
            cm, cd = m, [d]
        else:
            cd.append(d)
    if cd: groups.append((cm, cd))
    return groups

def week_label(monday):
    m = monday.month
    first, n, d = monday.replace(day=1), 0, monday.replace(day=1)
    while d <= monday:
        if d.weekday() == 0: n += 1
        d += dt.timedelta(days=1)
    lbl = f'{m}月{n}週目'
    ann = {
        D(4,13): ' ★4/17-18登録〆',
        D(4,20): ' ★4/24申請〆',
        D(4,27): ' GW⚠',
        D(5,25): ' ★印刷発注',
        D(6,1):  ' 🎌展示会',
    }
    return lbl + ann.get(monday, '')

# ══════════════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════════════
def get_svc():
    with open(os.path.expanduser('~/.google-mcp/tokens/main.json')) as f:
        td = json.load(f)
    c = Credentials(
        token=None, refresh_token=td.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=td.get('client_id'), client_secret=td.get('client_secret'))
    c.refresh(Request())
    return build('sheets', 'v4', credentials=c)

# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    svc = get_svc()
    dates = gen_dates()
    nd = len(dates)
    tc = C0 + nd

    # ── Build row layout ──
    row_data = []
    for ci, (cn, tasks) in enumerate(TASKS):
        row_data.append(('cat', cn, None))
        for t in tasks:
            row_data.append(('task', cn, t))
        if ci < len(TASKS) - 1:
            row_data.append(('sep', None, None))
    row_data.append(('sep', None, None))
    row_data.append(('legend', None, None))

    tr = HDROWS + len(row_data)

    # ── Build value grid ──
    grid = []

    # Row 0: Title
    grid.append(['展示会準備ガントチャート｜Eight EXPO 2026 夏（2回目出展）'] + ['']*(tc-1))

    # Row 1: Info
    r1 = ['担当者', '大川 龍之介', '', '会社', '株式会社エヌイチ', '', '作成日', '2026/4/9']
    grid.append(r1 + ['']*(tc - len(r1)))

    # Row 2: Empty
    grid.append([''] * tc)

    # Row 3: Week labels
    wgs = week_groups(dates)
    r3 = [''] * C0
    dl = [''] * nd
    for mon, grp in wgs:
        off = (grp[0] - dates[0]).days
        dl[off] = week_label(mon)
    grid.append(r3 + dl)

    # Row 4: Column headers + dates
    r4 = ['WBS', 'タスク名', '担当者', '責任者', '開始日', '期限', '優先度', 'ステータス']
    for d in dates:
        r4.append(f'{d.month}/{d.day}\n{DOW_JA[d.weekday()]}')
    grid.append(r4)

    # Content rows
    for rtype, cn, task in row_data:
        if rtype == 'cat':
            r = [f'■ {cn}'] + [''] * (tc - 1)
        elif rtype == 'task':
            wbs, nm, ow, rsp, s, e, pri, st, ms = task
            r = [wbs, nm, ow, rsp, f'{s.month}/{s.day}', f'{e.month}/{e.day}', pri, st]
            for d in dates:
                if s <= d <= e and ms and s == e:
                    r.append('◆')
                else:
                    r.append('')
        elif rtype == 'legend':
            r = ['【凡例】', '━ タスク期間', '', '◆ マイルストーン', '',
                 '🔴 4/24 Sansan提出締切', '', ''] + [''] * (tc - 8)
        else:
            r = [''] * tc
        grid.append(r)

    # ══════════════════════════════════════════════════════════════════
    # API CALLS
    # ══════════════════════════════════════════════════════════════════
    # ── マスターシート準備 ──
    print('📊 シート準備...')
    # Get existing sheets
    ss_meta = svc.spreadsheets().get(spreadsheetId=SSID, fields='sheets.properties').execute()
    existing_ids = {s['properties']['sheetId'] for s in ss_meta['sheets']}

    init_reqs = [
        # Unmerge ALL cells first (old merges persist across runs)
        {'unmergeCells': {'range': {'sheetId': SID,
            'startRowIndex': 0, 'endRowIndex': 1000,
            'startColumnIndex': 0, 'endColumnIndex': 200}}},
        # Clear main sheet
        {'updateCells': {'range': {'sheetId': SID},
         'fields': 'userEnteredValue,userEnteredFormat,dataValidation'}},
        {'updateSheetProperties': {
            'properties': {'sheetId': SID, 'title': SNAME}, 'fields': 'title'}},
        {'updateSheetProperties': {
            'properties': {'sheetId': SID,
                           'tabColorStyle': {'rgbColor': hx('#1565C0')}},
            'fields': 'tabColorStyle'}},
        # Ensure sheet has enough columns
        {'updateSheetProperties': {
            'properties': {'sheetId': SID,
                           'gridProperties': {'columnCount': max(tc + 5, 100)}},
            'fields': 'gridProperties.columnCount'}},
    ]

    # Create or clear master sheet
    if MASTER_SID in existing_ids:
        init_reqs.append({'updateCells': {'range': {'sheetId': MASTER_SID},
            'fields': 'userEnteredValue,userEnteredFormat'}})
    else:
        init_reqs.append({'addSheet': {'properties': {
            'sheetId': MASTER_SID, 'title': MASTER_SNAME,
            'gridProperties': {'rowCount': 50, 'columnCount': 10},
            'tabColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}}})

    svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': init_reqs}).execute()

    # ── マスターシートにデータ書き込み ──
    print('📋 マスターシート書き込み...')
    master_data = [
        ['メンバー', '状態'],
    ]
    max_rows = max(len(MEMBERS), len(STATUSES))
    for i in range(max_rows):
        master_data.append([
            MEMBERS[i] if i < len(MEMBERS) else '',
            STATUSES[i] if i < len(STATUSES) else '',
        ])

    svc.spreadsheets().values().update(
        spreadsheetId=SSID, range=f'{MASTER_SNAME}!A1',
        valueInputOption='RAW', body={'values': master_data}
    ).execute()

    # マスターシートの書式
    svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': [
        fc(0, 1, 0, 2, bg=HDR_BG, fg=WHITE, bold=True, sz=10, ha='CENTER',
           **{'va': 'MIDDLE'}),  # header row of master
        colw(0, 1, 120),
        colw(1, 2, 120),
        # Override sheetId for master sheet
    ]}).execute()
    # Fix: the fc/colw helpers use SID=0, need to patch for master
    # We'll do a separate batch with explicit sheetId
    m_reqs = [
        {'repeatCell': {'range': {'sheetId': MASTER_SID,
            'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 2},
            'cell': {'userEnteredFormat': {
                'backgroundColor': HDR_BG,
                'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 10},
                'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': MASTER_SID, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': MASTER_SID, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
            'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
    ]
    svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': m_reqs}).execute()

    # ══════════════════════════════════════════════════════════════════
    # 出展情報_入力管理シート
    # ══════════════════════════════════════════════════════════════════
    print('📄 出展情報_入力管理シート作成...')
    if ENTRY_SID in existing_ids:
        svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': [
            {'updateCells': {'range': {'sheetId': ENTRY_SID},
             'fields': 'userEnteredValue,userEnteredFormat,dataValidation'}},
        ]}).execute()
    else:
        svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': [
            {'addSheet': {'properties': {
                'sheetId': ENTRY_SID, 'title': ENTRY_SNAME,
                'gridProperties': {'rowCount': 100, 'columnCount': 15},
                'tabColor': {'red': 0.0, 'green': 0.35, 'blue': 0.7}}}},
        ]}).execute()

    # ── 出展情報データ ──
    ENTRY_ITEMS = [
        # (WBS, 項目, 仕様・条件, 文字数, サービス1案, 担当, 状態)
        ('1.1', '掲載サービス数', '全5枠 or 絞り込み。複数掲載で接触面UP（商談枠は増えない）', '—', '', '大川', '未着手'),
        ('1.2', 'サービスロゴ（RGB）', '背景白で使用できるロゴ。ai/png/jpeg。RGB形式', '—', '', '髙橋美優', '未着手'),
        ('1.2', 'サービスロゴガイドライン', 'ガイドラインがある場合アップロード', '—', '', '髙橋美優', '未着手'),
        ('1.3', 'サービス名', 'サービスの正式名称。キャッチコピーは入れない', '40字', '', '大川', '未着手'),
        ('1.3', 'サービス名（フリガナ）', '', '80字', '', '大川', '未着手'),
        ('1.4', 'キャッチコピー', 'サービス名を含めない', '30字', '', '大川', '未着手'),
        ('1.5', 'サービス紹介文', 'ブース詳細に掲載。絵文字不可', '130字', '', '大川', '未着手'),
        ('1.6', 'サービスイメージ画像', '推奨：縦675px×横1200px（16:9）。端に重要情報を入れない', '—', '', '髙橋美優', '未着手'),
        ('1.7', 'ピックアップポイント①', '「サービスの3つのポイント」として来場ガイドブック等に掲載', '20字', '', '大川', '未着手'),
        ('1.7', 'ピックアップポイント②', '', '20字', '', '大川', '未着手'),
        ('1.7', 'ピックアップポイント③', '', '20字', '', '大川', '未着手'),
        ('1.8', 'こんな課題はありませんか？①', 'サービスが解決できる課題を掲載（①のみ必須）', '40字', '', '大川', '未着手'),
        ('1.8', 'こんな課題はありませんか？②', '', '40字', '', '大川', '未着手'),
        ('1.8', 'こんな課題はありませんか？③', '', '40字', '', '大川', '未着手'),
        ('1.9', 'サービス対象', 'おすすめしたい対象者', '50字', '', '大川', '未着手'),
        ('1.10', 'ブース訪問特典', '来場者に特典があれば記入', '30字', '', '大川', '未着手'),
        ('1.11', 'マッチング対象', '職種/役職/従業員規模/業種/業態/ツール/決定権/業務課題/IT/AI活用状況等', '選択式', '', '大川', '未着手'),
        ('1.12', '検索キーワード', '3つまで選択', '選択式', '', '大川', '未着手'),
        ('1.12', 'フリーワード', '「／」で区切って複数指定可', '50字', '', '大川', '未着手'),
        ('1.13', '動画アップロード', '来場ガイドブックに掲載。トラッキング機能なし', '任意', '', '大川', '未着手'),
        ('1.13', '資料アップロード（最大3つ）', 'PDF資料。トラッキング機能なし', '任意', '', '大川', '未着手'),
        ('1.14', '商談枠数', '小間数に応じて自動設定。減らしたい場合のみ変更', '—', '', '大川', '未着手'),
    ]

    entry_header = ['WBS', '項目', '仕様・条件', '文字数',
                    'サービス1\n入力内容', 'サービス2\n入力内容', 'サービス3\n入力内容',
                    'サービス4\n入力内容', 'サービス5\n入力内容',
                    '担当', '状態', 'FB①', 'FB②', 'FB③']

    entry_grid = [
        ['出展情報 入力管理シート｜Eight EXPO 2026 夏'],
        ['※ 各サービスごとに入力内容を記入 → FBを受けて修正 → 最終FIXしたら出展管理システムに登録'],
        [],
        entry_header,
    ]
    for item in ENTRY_ITEMS:
        wbs, name, spec, chars, val, owner, status = item
        entry_grid.append([f"'{wbs}", name, spec, chars, val, '', '', '', '', owner, status, '', '', ''])

    svc.spreadsheets().values().update(
        spreadsheetId=SSID, range=f'{ENTRY_SNAME}!A1',
        valueInputOption='USER_ENTERED', body={'values': entry_grid}
    ).execute()

    # ── 出展情報シート書式 ──
    ES = ENTRY_SID
    e_hdr = hx('#0D47A1')
    e_reqs = [
        # Freeze
        {'updateSheetProperties': {
            'properties': {'sheetId': ES,
                           'gridProperties': {'frozenRowCount': 4, 'frozenColumnCount': 2}},
            'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'}},
        # Title row (merge within frozen + merge outside frozen)
        {'mergeCells': {'range': {'sheetId': ES, 'startRowIndex': 0, 'endRowIndex': 1,
                                   'startColumnIndex': 0, 'endColumnIndex': 2}, 'mergeType': 'MERGE_ALL'}},
        {'mergeCells': {'range': {'sheetId': ES, 'startRowIndex': 0, 'endRowIndex': 1,
                                   'startColumnIndex': 2, 'endColumnIndex': 14}, 'mergeType': 'MERGE_ALL'}},
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 0, 'endRowIndex': 1,
                                   'startColumnIndex': 0, 'endColumnIndex': 14},
            'cell': {'userEnteredFormat': {
                'backgroundColor': TITLE_BG, 'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 13},
                'verticalAlignment': 'MIDDLE'}},
            'fields': 'userEnteredFormat'}},
        # Note row
        {'mergeCells': {'range': {'sheetId': ES, 'startRowIndex': 1, 'endRowIndex': 2,
                                   'startColumnIndex': 0, 'endColumnIndex': 2}, 'mergeType': 'MERGE_ALL'}},
        {'mergeCells': {'range': {'sheetId': ES, 'startRowIndex': 1, 'endRowIndex': 2,
                                   'startColumnIndex': 2, 'endColumnIndex': 14}, 'mergeType': 'MERGE_ALL'}},
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 1, 'endRowIndex': 2,
                                   'startColumnIndex': 0, 'endColumnIndex': 14},
            'cell': {'userEnteredFormat': {
                'backgroundColor': hx('#FFF8E1'), 'textFormat': {'fontSize': 9, 'italic': True}}},
            'fields': 'userEnteredFormat'}},
        # Header row
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 3, 'endRowIndex': 4,
                                   'startColumnIndex': 0, 'endColumnIndex': 14},
            'cell': {'userEnteredFormat': {
                'backgroundColor': e_hdr, 'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 9},
                'horizontalAlignment': 'CENTER', 'verticalAlignment': 'MIDDLE', 'wrapStrategy': 'WRAP'}},
            'fields': 'userEnteredFormat'}},
        # サービス入力列（E-I）を薄い青背景
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 4, 'endRowIndex': 4 + len(ENTRY_ITEMS),
                                   'startColumnIndex': 4, 'endColumnIndex': 9},
            'cell': {'userEnteredFormat': {'backgroundColor': hx('#E3F2FD'), 'wrapStrategy': 'WRAP'}},
            'fields': 'userEnteredFormat'}},
        # FB列（L-N）を薄い黄色背景
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 4, 'endRowIndex': 4 + len(ENTRY_ITEMS),
                                   'startColumnIndex': 11, 'endColumnIndex': 14},
            'cell': {'userEnteredFormat': {'backgroundColor': hx('#FFF8E1'), 'wrapStrategy': 'WRAP'}},
            'fields': 'userEnteredFormat'}},
        # Column widths
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 55}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
            'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3},
            'properties': {'pixelSize': 280}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4},
            'properties': {'pixelSize': 65}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 9},
            'properties': {'pixelSize': 180}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 9, 'endIndex': 10},
            'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 10, 'endIndex': 11},
            'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'COLUMNS', 'startIndex': 11, 'endIndex': 14},
            'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
        # Row heights
        {'updateDimensionProperties': {'range': {'sheetId': ES, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 38}, 'fields': 'pixelSize'}},
        # Thin borders for all data
        {'repeatCell': {'range': {'sheetId': ES, 'startRowIndex': 3, 'endRowIndex': 4 + len(ENTRY_ITEMS),
                                   'startColumnIndex': 0, 'endColumnIndex': 14},
            'cell': {'userEnteredFormat': {'borders': {
                'top': {'style': 'SOLID', 'color': hx('#E0E0E0')},
                'bottom': {'style': 'SOLID', 'color': hx('#E0E0E0')},
                'left': {'style': 'SOLID', 'color': hx('#E0E0E0')},
                'right': {'style': 'SOLID', 'color': hx('#E0E0E0')}}}},
            'fields': 'userEnteredFormat.borders'}},
        # Status dropdown
        {'setDataValidation': {'range': {'sheetId': ES, 'startRowIndex': 4, 'endRowIndex': 4 + len(ENTRY_ITEMS),
                                          'startColumnIndex': 10, 'endColumnIndex': 11},
            'rule': {'condition': {'type': 'ONE_OF_LIST',
                     'values': [{'userEnteredValue': v} for v in ['未着手', '下書き中', 'FB待ち', '修正中', 'FIX済']]},
                     'showCustomUi': True, 'strict': True}}},
        # Owner dropdown
        {'setDataValidation': {'range': {'sheetId': ES, 'startRowIndex': 4, 'endRowIndex': 4 + len(ENTRY_ITEMS),
                                          'startColumnIndex': 9, 'endColumnIndex': 10},
            'rule': {'condition': {'type': 'ONE_OF_LIST',
                     'values': [{'userEnteredValue': v} for v in MEMBERS]},
                     'showCustomUi': True, 'strict': True}}},
    ]
    svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': e_reqs}).execute()

    print('📝 データ書き込み...')
    # Use updateCells with explicit stringValue for ALL cells (including empty)
    rows_payload = []
    for row in grid:
        cells = []
        for v in row:
            sv = str(v) if v != '' else ''
            # Always set stringValue, even for empty strings
            cells.append({'userEnteredValue': {'stringValue': sv}})
        rows_payload.append({'values': cells})

    # Write in batches of 20 rows to avoid request size limits
    batch_sz = 20
    for i in range(0, len(rows_payload), batch_sz):
        batch = rows_payload[i:i+batch_sz]
        svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': [
            {'updateCells': {
                'rows': batch,
                'range': rng(i, i + len(batch), 0, tc),
                'fields': 'userEnteredValue'}}
        ]}).execute()
    print(f'   → {len(rows_payload)}行書き込み完了')

    # ══════════════════════════════════════════════════════════════════
    # FORMATTING
    # ══════════════════════════════════════════════════════════════════
    print('🎨 書式設定...')
    reqs = []

    # ── Force text format on WBS column (A) and date columns (E-F) to prevent number interpretation ──
    text_fmt = {'numberFormat': {'type': 'TEXT'}}
    for col_start, col_end in [(0, 1), (4, 6)]:
        reqs.append({'repeatCell': {
            'range': rng(0, tr, col_start, col_end),
            'cell': {'userEnteredFormat': text_fmt},
            'fields': 'userEnteredFormat.numberFormat'}})

    # ── Column widths ──
    for c, w in [(0,55), (1,300), (2,100), (3,85), (4,70), (5,70), (6,60), (7,90)]:
        reqs.append(colw(c, c+1, w))
    reqs.append(colw(C0, C0 + nd, 38))

    # ── Freeze panes ──
    reqs.append({'updateSheetProperties': {
        'properties': {'sheetId': SID,
                       'gridProperties': {'frozenRowCount': HDROWS, 'frozenColumnCount': C0}},
        'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'}})

    # ── Row 0: Title ──
    reqs.append(mg(0, 1, 0, C0))  # Merge within frozen columns only
    reqs.append(fc(0, 1, 0, tc, bg=TITLE_BG, fg=WHITE, bold=True, sz=14, va='MIDDLE'))
    reqs.append(rh(0, 44))

    # ── Row 1: Info ──
    reqs.append(fc(1, 2, 0, tc, bg=hx('#F5F5F5'), sz=9, va='MIDDLE'))
    reqs.append(fc(1, 2, 0, 1, bold=True))
    reqs.append(fc(1, 2, 3, 4, bold=True))
    reqs.append(fc(1, 2, 6, 7, bold=True))
    reqs.append(rh(1, 26))

    # ── Row 2: Spacer ──
    reqs.append(rh(2, 6))

    # ── Row 3: Week labels ──
    reqs.append(mg(3, 4, 0, C0))
    reqs.append(fc(3, 4, 0, C0, bg=HDR_BG, fg=WHITE, bold=True, sz=9, ha='CENTER', va='MIDDLE'))
    for mon, grp in wgs:
        cs = C0 + (grp[0] - dates[0]).days
        ce = C0 + (grp[-1] - dates[0]).days + 1
        reqs.append(mg(3, 4, cs, ce))
        # Deadline week gets special color
        if mon == D(4, 20):
            reqs.append(fc(3, 4, cs, ce, bg=hx('#B71C1C'), fg=WHITE, bold=True, sz=8, ha='CENTER', va='MIDDLE'))
        elif mon == D(6, 1):
            reqs.append(fc(3, 4, cs, ce, bg=EXPO_GOLD, fg=WHITE, bold=True, sz=8, ha='CENTER', va='MIDDLE'))
        else:
            reqs.append(fc(3, 4, cs, ce, bg=WEEK_BG, fg=WHITE, bold=True, sz=8, ha='CENTER', va='MIDDLE'))
    reqs.append(rh(3, 28))

    # ── Row 4: Column headers ──
    reqs.append(fc(4, 5, 0, C0, bg=HDR_BG, fg=WHITE, bold=True, sz=9, ha='CENTER', va='MIDDLE'))
    reqs.append(fc(4, 5, C0, C0 + nd, bg=HDR_BG, fg=WHITE, sz=7, ha='CENTER', va='MIDDLE', wrap=True))
    reqs.append(rh(4, 40))

    # Weekend/holiday date headers
    for i, d in enumerate(dates):
        if d.weekday() >= 5 or d in HOLIDAYS:
            reqs.append(fc(4, 5, C0+i, C0+i+1, bg=WKEND_HDR))

    # 4/24 deadline header
    dl_idx = (D(4,24) - dates[0]).days
    reqs.append(fc(4, 5, C0 + dl_idx, C0 + dl_idx + 1, bg=DL_RED, fg=WHITE, bold=True))

    # Exhibition day headers
    for expo_d in [D(6,3), D(6,4)]:
        if START <= expo_d <= END:
            ei = (expo_d - dates[0]).days
            reqs.append(fc(4, 5, C0+ei, C0+ei+1, bg=EXPO_GOLD, fg=WHITE, bold=True))

    # ── Weekend/holiday backgrounds for all content rows ──
    for i, d in enumerate(dates):
        if d.weekday() >= 5 or d in HOLIDAYS:
            reqs.append(fc(HDROWS, tr, C0+i, C0+i+1, bg=WKEND_BG))

    # ── Category & task formatting ──
    ri = HDROWS
    task_row_ranges = []  # (start, end) for continuous task rows
    cur_task_start = None

    for rtype, cn, task in row_data:
        if rtype == 'cat':
            if cur_task_start is not None:
                task_row_ranges.append((cur_task_start, ri))
                cur_task_start = None
            cc = CAT[cn]
            reqs.append(fc(ri, ri+1, 0, tc, bg=cc['h'], fg=WHITE, bold=True, sz=10, va='MIDDLE'))
            reqs.append(mg(ri, ri+1, 0, C0))
            reqs.append(rh(ri, 30))

        elif rtype == 'task':
            if cur_task_start is None:
                cur_task_start = ri
            cc = CAT[cn]
            wbs, nm, ow, rsp, s, e, pri, st, ms = task

            # Info columns
            reqs.append(fc(ri, ri+1, 0, C0, bg=cc['r'], sz=9, va='MIDDLE'))
            reqs.append(fc(ri, ri+1, 0, 1, ha='CENTER'))  # WBS center
            reqs.append(fc(ri, ri+1, 2, C0, ha='CENTER'))  # C-H center

            # Gantt bar
            bar_s = max(0, (s - dates[0]).days)
            bar_e = min(nd - 1, (e - dates[0]).days) + 1
            if bar_s < bar_e:
                bar_c = cc['m'] if ms else cc['b']
                reqs.append(fc(ri, ri+1, C0 + bar_s, C0 + bar_e, bg=bar_c))
                if ms:
                    reqs.append(fc(ri, ri+1, C0 + bar_s, C0 + bar_e,
                                   fg=WHITE, bold=True, sz=8, ha='CENTER'))

            reqs.append(rh(ri, 26))

        elif rtype == 'sep':
            if cur_task_start is not None:
                task_row_ranges.append((cur_task_start, ri))
                cur_task_start = None
            reqs.append(rh(ri, 8))
            reqs.append(fc(ri, ri+1, 0, tc, bg=hx('#FAFAFA')))

        elif rtype == 'legend':
            if cur_task_start is not None:
                task_row_ranges.append((cur_task_start, ri))
                cur_task_start = None
            reqs.append(fc(ri, ri+1, 0, tc, bg=hx('#F5F5F5'), sz=8, va='MIDDLE'))
            reqs.append(rh(ri, 24))

        ri += 1

    if cur_task_start is not None:
        task_row_ranges.append((cur_task_start, ri))

    # ── 4/24 deadline vertical line ──
    dl_col = C0 + dl_idx
    reqs.append({'repeatCell': {
        'range': rng(HDROWS, tr, dl_col, dl_col + 1),
        'cell': {'userEnteredFormat': {'borders': {
            'right': {'style': 'SOLID_THICK', 'color': DL_RED}}}},
        'fields': 'userEnteredFormat.borders.right'}})

    # ── Data validation (dropdowns) ──
    PRIORITIES = ['高', '中', '低']
    for r0, r1 in task_row_ranges:
        reqs.append(dv(r0, r1, 2, 3, MEMBERS))       # 担当者
        reqs.append(dv(r0, r1, 3, 4, MEMBERS))       # 責任者
        reqs.append(dv(r0, r1, 6, 7, PRIORITIES))    # 優先度
        reqs.append(dv(r0, r1, 7, 8, STATUSES))      # ステータス

    # ── Conditional formatting ──
    all_task_min = min(r[0] for r in task_row_ranges)
    all_task_max = max(r[1] for r in task_row_ranges)
    # ステータス列 (H = col 7)
    for i, (st, bg) in enumerate(STATUS_COLORS.items()):
        reqs.append(cf_rule(all_task_min, all_task_max, 7, 8, st, bg, i))
    # 優先度列 (G = col 6) — 高=赤、中=黄、低=グレー
    pri_colors = {'高': hx('#FFCDD2'), '中': hx('#FFF9C4'), '低': hx('#F5F5F5')}
    for j, (p, bg) in enumerate(pri_colors.items()):
        reqs.append(cf_rule(all_task_min, all_task_max, 6, 7, p, bg, len(STATUS_COLORS) + j))

    # ── Thin borders for info area ──
    thin_border = {'style': 'SOLID', 'color': hx('#E0E0E0')}
    reqs.append({'repeatCell': {
        'range': rng(HDROWS, tr, 0, C0),
        'cell': {'userEnteredFormat': {'borders': {
            'top': thin_border, 'bottom': thin_border,
            'left': thin_border, 'right': thin_border}}},
        'fields': 'userEnteredFormat.borders'}})

    # ══════════════════════════════════════════════════════════════════
    # EXECUTE
    # ══════════════════════════════════════════════════════════════════
    batch_size = 500
    total_reqs = len(reqs)
    for i in range(0, total_reqs, batch_size):
        batch = reqs[i:i+batch_size]
        print(f'   → 書式バッチ {i//batch_size + 1}/{(total_reqs-1)//batch_size + 1} ({len(batch)}件)...')
        svc.spreadsheets().batchUpdate(spreadsheetId=SSID, body={'requests': batch}).execute()

    total_tasks = sum(len(t[1]) for t in TASKS)
    print()
    print(f'✅ ガントチャート生成完了！')
    print(f'   📅 {START} 〜 {END}（{nd}日間）')
    print(f'   📋 {total_tasks}タスク / {len(TASKS)}カテゴリ')
    print(f'   🔗 https://docs.google.com/spreadsheets/d/{SSID}/edit')

if __name__ == '__main__':
    main()
