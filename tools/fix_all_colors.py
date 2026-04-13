#!/usr/bin/env python3
"""
全シートの文字色を完全修正
- 濃い背景色 → 白文字
- 薄い背景色・入力セル → 黒文字
"""
import json
import requests

with open('/Users/kyouyuu/.google-mcp/tokens/main.json') as f:
    creds = json.load(f)

def get_access_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

token = get_access_token()
SPREADSHEET_ID = '1lHM_lbS02XWzW8_S3sTP56YmF_fOP4GOgnpFYRrZjlM'
h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def batch_update(reqs):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate'
    r = requests.post(url, headers=h, json={'requests': reqs})
    if r.status_code != 200:
        raise Exception(f'batchUpdate error: {r.status_code} {r.text[:500]}')
    return r.json()

def rgb(c):
    c = c.lstrip('#')
    return {'red': int(c[0:2],16)/255, 'green': int(c[2:4],16)/255, 'blue': int(c[4:6],16)/255}

def fmt(sid, r0, r1, c0, c1, bg=None, color=None, bold=None, italic=None,
        fs=None, halign=None, nfmt=None):
    uf, fields = {}, []
    if bg    is not None: uf['backgroundColor'] = rgb(bg); fields.append('userEnteredFormat.backgroundColor')
    tf = {}
    if bold   is not None: tf['bold'] = bold
    if italic is not None: tf['italic'] = italic
    if color  is not None: tf['foregroundColor'] = rgb(color)
    if fs     is not None: tf['fontSize'] = fs
    if tf: uf['textFormat'] = tf; fields.append('userEnteredFormat.textFormat')
    if halign is not None: uf['horizontalAlignment'] = halign; fields.append('userEnteredFormat.horizontalAlignment')
    if nfmt   is not None: uf['numberFormat'] = nfmt; fields.append('userEnteredFormat.numberFormat')
    return {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'cell': {'userEnteredFormat': uf}, 'fields': ','.join(fields)
    }}

# 通貨フォーマット
YEN  = {'type': 'NUMBER', 'pattern': '¥#,##0'}
PCT  = {'type': 'NUMBER', 'pattern': '0.0%'}

# シート情報取得
info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
print('シート一覧:', sheets)

PL_ID   = sheets['PL_月次']
COST_ID = sheets['コスト明細']
SALE_ID = sheets['売上明細']
CASE_ID = sheets.get('案件別P/L')

reqs = []

# =================================================================
# PL_月次
# =================================================================
# 行構成（1-indexed）:
# 1:タイトル 2:月ヘッダー 3:実績/見込
# 4:【売上】 5-8:各売上 9:売上合計
# 10:空白
# 11:【売上原価】 12-14:各原価 15:原価合計
# 16:空白
# 17:粗利 18:粗利率
# 19:空白
# 20:【販管費】 21-27:各販管費 28:販管費合計
# 29:空白
# 30:営業利益 31:営業利益率

print('\n[PL_月次] 修正中...')
reqs += [
    # ベースリセット: 白背景・黒文字
    fmt(PL_ID, 0, 35, 0, 14, bg='FFFFFF', color='1A1A1A'),

    # --- タイトル（行1）濃紺・白文字 ---
    fmt(PL_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=12, halign='CENTER'),

    # --- 月ヘッダー（行2）ネイビー・白文字 ---
    fmt(PL_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),

    # --- 実績/見込行（行3）薄青・グレー文字 ---
    fmt(PL_ID, 2, 3, 0, 14, bg='EBF5FB', color='5D6D7E', italic=True, halign='CENTER'),

    # --- 【売上】セクション（行4）濃い青・白文字 ---
    fmt(PL_ID, 3, 4, 0, 14, bg='1A5276', color='FFFFFF', bold=True),

    # --- 売上各行（行5-8）薄青・黒文字 ---
    fmt(PL_ID, 4, 8, 0, 1,  bg='F4F9FF', color='1A1A1A'),
    fmt(PL_ID, 4, 8, 1, 14, bg='F4F9FF', color='1A1A1A', nfmt=YEN, halign='RIGHT'),

    # --- 売上合計（行9）濃い青・白文字 ---
    fmt(PL_ID, 8, 9, 0, 14, bg='1A5276', color='FFFFFF', bold=True),
    fmt(PL_ID, 8, 9, 1, 14, bg='1A5276', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),

    # --- 空白（行10）---
    fmt(PL_ID, 9, 10, 0, 14, bg='F8F9FA', color='1A1A1A'),

    # --- 【売上原価】セクション（行11）濃い茶・白文字 ---
    fmt(PL_ID, 10, 11, 0, 14, bg='6E2F00', color='FFFFFF', bold=True),

    # --- 原価各行（行12-14）薄オレンジ・黒文字 ---
    fmt(PL_ID, 11, 14, 0, 1,  bg='FFF3E0', color='1A1A1A'),
    fmt(PL_ID, 11, 14, 1, 14, bg='FFF3E0', color='1A1A1A', nfmt=YEN, halign='RIGHT'),

    # --- 売上原価合計（行15）茶・白文字 ---
    fmt(PL_ID, 14, 15, 0, 14, bg='A04000', color='FFFFFF', bold=True),
    fmt(PL_ID, 14, 15, 1, 14, bg='A04000', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),

    # --- 空白（行16）---
    fmt(PL_ID, 15, 16, 0, 14, bg='F8F9FA'),

    # --- 粗利（行17）深緑・白文字 ---
    fmt(PL_ID, 16, 17, 0, 14, bg='1E8449', color='FFFFFF', bold=True),
    fmt(PL_ID, 16, 17, 1, 14, bg='1E8449', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),

    # --- 粗利率（行18）薄緑・黒文字 ---
    fmt(PL_ID, 17, 18, 0, 1,  bg='EAFAF1', color='1A1A1A'),
    fmt(PL_ID, 17, 18, 1, 14, bg='EAFAF1', color='1A1A1A', nfmt=PCT, halign='RIGHT'),

    # --- 空白（行19）---
    fmt(PL_ID, 18, 19, 0, 14, bg='F8F9FA'),

    # --- 【販管費】セクション（行20）濃い紫・白文字 ---
    fmt(PL_ID, 19, 20, 0, 14, bg='4A235A', color='FFFFFF', bold=True),

    # --- 販管費各行（行21-27）薄紫・黒文字 ---
    fmt(PL_ID, 20, 27, 0, 1,  bg='F9F2FF', color='1A1A1A'),
    fmt(PL_ID, 20, 27, 1, 14, bg='F9F2FF', color='1A1A1A', nfmt=YEN, halign='RIGHT'),

    # --- 販管費合計（行28）紫・白文字 ---
    fmt(PL_ID, 27, 28, 0, 14, bg='7D3C98', color='FFFFFF', bold=True),
    fmt(PL_ID, 27, 28, 1, 14, bg='7D3C98', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),

    # --- 空白（行29）---
    fmt(PL_ID, 28, 29, 0, 14, bg='F8F9FA'),

    # --- 営業利益（行30）ダーク・白文字 ---
    fmt(PL_ID, 29, 30, 0, 14, bg='212F3D', color='FFFFFF', bold=True, fs=11),
    fmt(PL_ID, 29, 30, 1, 14, bg='212F3D', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),

    # --- 営業利益率（行31）薄グレー・黒文字 ---
    fmt(PL_ID, 30, 31, 0, 1,  bg='ECEFF1', color='1A1A1A'),
    fmt(PL_ID, 30, 31, 1, 14, bg='ECEFF1', color='1A1A1A', nfmt=PCT, halign='RIGHT'),

    # 年間合計列（N列=13）: やや強調
    fmt(PL_ID, 1, 31, 13, 14, bold=True),
]
print('   PL_月次: リクエスト追加完了')

# =================================================================
# コスト明細
# =================================================================
print('[コスト明細] 修正中...')

ROWS_DEF = [
    ('title',    'タイトル'),
    ('header',   'ヘッダー'),
    ('section',  '【A】売上原価（COGS）'),
    ('item',     '研修講師費'),
    ('item',     '外注開発費'),
    ('item',     'コーチ人件費'),
    ('subtotal', '売上原価合計'),
    ('blank',    ''),
    ('section',  '【B】人件費'),
    ('item',     '人件費（給与）'),
    ('item',     '業務委託費'),
    ('subtotal', '人件費合計'),
    ('blank',    ''),
    ('section',  '【C】ツール・インフラ費'),
    ('item',     'AI APIコスト'),
    ('item',     'SaaSサブスク'),
    ('item',     'システム開発・保守'),
    ('subtotal', 'ツール合計'),
    ('blank',    ''),
    ('section',  '【D】マーケティング・営業費'),
    ('item',     '広告費'),
    ('item',     '展示会・イベント費'),
    ('item',     '資料作成費'),
    ('item',     '交通費・出張費'),
    ('item',     '接待交際費'),
    ('subtotal', 'マーケ合計'),
    ('blank',    ''),
    ('section',  '【E】管理費'),
    ('item',     '事務所費（按分）'),
    ('item',     '通信費'),
    ('item',     '備品・消耗品費'),
    ('item',     '外部顧問・士業費'),
    ('subtotal', '管理費合計'),
    ('blank',    ''),
    ('grand',    '★販管費合計'),
    ('grand2',   '★コスト合計'),
]

SEC_BG = {
    '【A】売上原価（COGS）':       '1A5276',
    '【B】人件費':                 '1E8449',
    '【C】ツール・インフラ費':     '6E2F00',
    '【D】マーケティング・営業費': '4A235A',
    '【E】管理費':                 '212F3D',
}
SUB_BG = {
    '売上原価合計': '2471A3',
    '人件費合計':   '239B56',
    'ツール合計':   'A04000',
    'マーケ合計':   '7D3C98',
    '管理費合計':   '2C3E50',
}
ITEM_BG = {
    '【A】売上原価（COGS）':       'D6EAF8',
    '【B】人件費':                 'D5F5E3',
    '【C】ツール・インフラ費':     'FAE5D3',
    '【D】マーケティング・営業費': 'E8DAEF',
    '【E】管理費':                 'D5D8DC',
}

# ベースリセット
reqs.append(fmt(COST_ID, 0, 40, 0, 14, bg='FFFFFF', color='1A1A1A'))

cur_sec = None
for row_idx, (type_, label) in enumerate(ROWS_DEF):
    ri = row_idx  # 0-indexed

    if type_ == 'title':
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14,
                        bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'))

    elif type_ == 'header':
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14,
                        bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'))

    elif type_ == 'section':
        cur_sec = label
        bg = SEC_BG.get(label, '333333')
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14,
                        bg=bg, color='FFFFFF', bold=True))

    elif type_ == 'item':
        item_bg = ITEM_BG.get(cur_sec, 'F5F5F5')
        reqs += [
            # ラベル列: 薄い系統色・黒文字
            fmt(COST_ID, ri, ri+1, 0, 1,  bg=item_bg, color='1A1A1A'),
            # 入力列（月）: 黄色・黒文字
            fmt(COST_ID, ri, ri+1, 1, 13, bg='FFFDE7', color='1A1A1A',
                nfmt=YEN, halign='RIGHT'),
            # 年間合計列: 薄グレー・黒文字
            fmt(COST_ID, ri, ri+1, 13, 14, bg='ECF0F1', color='1A1A1A',
                bold=True, nfmt=YEN, halign='RIGHT'),
        ]

    elif type_ == 'subtotal':
        bg = SUB_BG.get(label, '555555')
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14,
                        bg=bg, color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'))
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 1,
                        bg=bg, color='FFFFFF', bold=True, halign='LEFT'))

    elif type_ in ('grand', 'grand2'):
        bg = '1C2833' if type_ == 'grand' else '0B0C10'
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14,
                        bg=bg, color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'))
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 1,
                        bg=bg, color='FFFFFF', bold=True, halign='LEFT'))

    elif type_ == 'blank':
        reqs.append(fmt(COST_ID, ri, ri+1, 0, 14, bg='F8F9FA', color='1A1A1A'))

print('   コスト明細: リクエスト追加完了')

# =================================================================
# 売上明細
# =================================================================
print('[売上明細] 修正中...')
reqs += [
    # ベースリセット
    fmt(SALE_ID, 0, 25, 0, 7, bg='FFFFFF', color='1A1A1A'),
    # タイトル（行1）
    fmt(SALE_ID, 0, 1, 0, 7, bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'),
    # ヘッダー（行2）
    fmt(SALE_ID, 1, 2, 0, 7, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    # 実績データ行（行3-10）白背景・黒文字
    fmt(SALE_ID, 2, 11, 0, 7, bg='FFFFFF', color='1A1A1A'),
    # 金額列（D列=3）: 通貨・右揃え
    fmt(SALE_ID, 2, 11, 3, 4, bg='FFFFFF', color='1A1A1A', nfmt=YEN, halign='RIGHT'),
    # 見込み行（行12-16）薄黄・黒文字
    fmt(SALE_ID, 11, 17, 0, 7, bg='FFFDE7', color='1A1A1A', italic=True),
    fmt(SALE_ID, 11, 17, 3, 4, bg='FFFDE7', color='1A1A1A', nfmt=YEN, halign='RIGHT'),
    # 空白行（行17）
    fmt(SALE_ID, 16, 17, 0, 7, bg='F8F9FA'),
    # サービス別集計ヘッダー（行18）
    fmt(SALE_ID, 17, 18, 0, 7, bg='2E5090', color='FFFFFF', bold=True),
    # 集計データ行（行19-23）
    fmt(SALE_ID, 18, 23, 0, 2, bg='EBF5FB', color='1A1A1A'),
    fmt(SALE_ID, 18, 22, 1, 2, bg='EBF5FB', color='1A1A1A', nfmt=YEN, halign='RIGHT'),
    # 合計行（行23）
    fmt(SALE_ID, 22, 23, 0, 2, bg='1A5276', color='FFFFFF', bold=True),
    fmt(SALE_ID, 22, 23, 1, 2, bg='1A5276', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'),
]
print('   売上明細: リクエスト追加完了')

# =================================================================
# 案件別P/L
# =================================================================
if CASE_ID:
    print('[案件別P/L] 修正中...')
    NC = 6  # クライアント数
    DATA_START_RI = 3   # 0-indexed（行4から）
    TOTAL_RI      = DATA_START_RI + NC
    SEC_HDR_RI    = TOTAL_RI + 3
    COM_ITEM_COUNT = 4
    COM_TOTAL_RI   = SEC_HDR_RI + 1 + COM_ITEM_COUNT

    reqs += [
        # ベースリセット
        fmt(CASE_ID, 0, 25, 0, 5, bg='FFFFFF', color='1A1A1A'),
        # タイトル（行1）
        fmt(CASE_ID, 0, 1, 0, 5, bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'),
        # 説明（行2）
        fmt(CASE_ID, 1, 2, 0, 5, bg='EBF5FB', color='1A5276', italic=True),
        # ヘッダー（行3）
        fmt(CASE_ID, 2, 3, 0, 5, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
        # 数値フォーマット（B/C/D列）
        fmt(CASE_ID, DATA_START_RI, TOTAL_RI+1, 1, 4,
            color='1A1A1A', nfmt=YEN, halign='RIGHT'),
    ]

    # クライアント行: 交互カラー
    for i in range(NC):
        ri = DATA_START_RI + i
        bg = 'F4F9FF' if i % 2 == 0 else 'FFFFFF'
        reqs += [
            fmt(CASE_ID, ri, ri+1, 0, 5, bg=bg, color='1A1A1A'),
            # 直接コスト列（C=2）: 黄色入力セル・黒文字
            fmt(CASE_ID, ri, ri+1, 2, 3, bg='FFFDE7', color='1A1A1A'),
        ]

    # 合計行
    reqs.append(fmt(CASE_ID, TOTAL_RI, TOTAL_RI+1, 0, 5,
                    bg='1A252F', color='FFFFFF', bold=True))
    reqs.append(fmt(CASE_ID, TOTAL_RI, TOTAL_RI+1, 1, 4,
                    bg='1A252F', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'))

    # 共通コストセクションヘッダー
    reqs.append(fmt(CASE_ID, SEC_HDR_RI, SEC_HDR_RI+1, 0, 5,
                    bg='4A235A', color='FFFFFF', bold=True))

    # 共通コスト明細
    for i in range(COM_ITEM_COUNT):
        ri = SEC_HDR_RI + 1 + i
        bg = 'F5EEF8' if i % 2 == 0 else 'FFFFFF'
        reqs += [
            fmt(CASE_ID, ri, ri+1, 0, 5, bg=bg, color='1A1A1A'),
            fmt(CASE_ID, ri, ri+1, 2, 3, bg=bg, color='1A1A1A', nfmt=YEN, halign='RIGHT'),
        ]

    # 共通コスト合計
    reqs.append(fmt(CASE_ID, COM_TOTAL_RI, COM_TOTAL_RI+1, 0, 5,
                    bg='7D3C98', color='FFFFFF', bold=True))
    reqs.append(fmt(CASE_ID, COM_TOTAL_RI, COM_TOTAL_RI+1, 2, 3,
                    bg='7D3C98', color='FFFFFF', bold=True, nfmt=YEN, halign='RIGHT'))

    print('   案件別P/L: リクエスト追加完了')

# =================================================================
# 一括送信（50件ずつ分割）
# =================================================================
print(f'\n合計リクエスト数: {len(reqs)}件')
CHUNK = 50
for i in range(0, len(reqs), CHUNK):
    batch_update(reqs[i:i+CHUNK])
    print(f'   {min(i+CHUNK, len(reqs))}/{len(reqs)} 完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
