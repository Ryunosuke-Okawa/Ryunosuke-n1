#!/usr/bin/env python3
"""
案件別P/Lシートを半自動形式に更新
- 売上: 売上明細から自動参照
- 直接コスト: 手動入力（黄色セル）
- 粗利: 自動計算
- 共通コスト: コスト明細から自動参照（下部に別枠）
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

def values_batch(data):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values:batchUpdate'
    r = requests.post(url, headers=h, json={'valueInputOption': 'USER_ENTERED', 'data': data})
    if r.status_code != 200:
        raise Exception(f'values batchUpdate error: {r.status_code} {r.text[:500]}')
    return r.json()

def clear_range(r):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{r}:clear'
    requests.post(url, headers=h, json={})

def rgb(c):
    c = c.lstrip('#')
    return {'red': int(c[0:2],16)/255, 'green': int(c[2:4],16)/255, 'blue': int(c[4:6],16)/255}

def cell_fmt(sid, r0, r1, c0, c1, **kw):
    uf, fields = {}, []
    if 'bg' in kw:
        uf['backgroundColor'] = rgb(kw['bg']); fields.append('userEnteredFormat.backgroundColor')
    tf = {}
    if 'bold' in kw: tf['bold'] = kw['bold']
    if 'italic' in kw: tf['italic'] = kw['italic']
    if 'color' in kw: tf['foregroundColor'] = rgb(kw['color'])
    if 'fs' in kw: tf['fontSize'] = kw['fs']
    if tf: uf['textFormat'] = tf; fields.append('userEnteredFormat.textFormat')
    if 'halign' in kw: uf['horizontalAlignment'] = kw['halign']; fields.append('userEnteredFormat.horizontalAlignment')
    if 'valign' in kw: uf['verticalAlignment'] = kw['valign']; fields.append('userEnteredFormat.verticalAlignment')
    if 'nfmt' in kw: uf['numberFormat'] = kw['nfmt']; fields.append('userEnteredFormat.numberFormat')
    return {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'cell': {'userEnteredFormat': uf}, 'fields': ','.join(fields)
    }}

def border_all(sid, r0, r1, c0, c1, color='CCCCCC', style='SOLID'):
    b = {'style': style, 'color': rgb(color)}
    return {'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'top': b, 'bottom': b, 'left': b, 'right': b,
        'innerHorizontal': b, 'innerVertical': b
    }}

def col_w(sid, col, px):
    return {'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col+1},
        'properties': {'pixelSize': px}, 'fields': 'pixelSize'
    }}

def row_h(sid, r0, r1, px):
    return {'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': r0, 'endIndex': r1},
        'properties': {'pixelSize': px}, 'fields': 'pixelSize'
    }}

def merge(sid, r0, r1, c0, c1):
    return {'mergeCells': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'mergeType': 'MERGE_ALL'
    }}

def freeze(sid, rows=0, cols=0):
    return {'updateSheetProperties': {
        'properties': {'sheetId': sid, 'gridProperties': {
            'frozenRowCount': rows, 'frozenColumnCount': cols}},
        'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
    }}

# =========================================================
# シート情報取得
# =========================================================
info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
CASE_ID = sheets['案件別P/L']
print('案件別P/L sheetId:', CASE_ID)

# コスト明細の行番号（restore_cost_simple.py の構造に基づく）
COST_ROW = {
    '人件費合計':   12,
    'ツール合計':   18,
    'マーケ合計':   26,
    '管理費合計':   33,
    '販管費合計':   35,
    'コスト合計':   36,
}

CLIENTS = [
    'FROUR株式会社',
    '株式会社オンシナジー',
    '中部キリンビバレッジサービス株式会社',
    '株式会社NTTネクシア',
    'StockSun株式会社（ビバリーグレン分）',
    '（要確認・4月BPO）',
]
NC = len(CLIENTS)

# =========================================================
# データ構築
# =========================================================
# 列構成: A=クライアント名, B=売上, C=直接コスト（入力）, D=粗利, E=粗利率
# 行構成:
#   1: タイトル
#   2: ヘッダー（説明）
#   3: サブヘッダー（列名）
#   4〜4+NC-1: クライアント行
#   4+NC: 合計行
#   (空白)
#   (空白)
#   共通コストセクションヘッダー
#   人件費合計
#   ツール合計
#   マーケ合計
#   管理費合計
#   販管費合計

DATA_START = 4       # クライアントデータ開始行（1-indexed）
TOTAL_ROW  = DATA_START + NC        # 合計行
BLANK1     = TOTAL_ROW + 1
BLANK2     = TOTAL_ROW + 2
SEC_HDR    = TOTAL_ROW + 3          # 共通コストセクションヘッダー
COM_ROWS_START = SEC_HDR + 1        # 共通コスト明細開始

com_items = [
    ('人件費合計',   COST_ROW['人件費合計']),
    ('ツール・インフラ費合計', COST_ROW['ツール合計']),
    ('マーケ・営業費合計',     COST_ROW['マーケ合計']),
    ('管理費合計',   COST_ROW['管理費合計']),
]
COM_TOTAL_ROW = COM_ROWS_START + len(com_items)

all_rows = []

# 行1: タイトル
all_rows.append(['案件別P/L（クライアント別 売上・直接コスト・粗利）', '', '', '', ''])

# 行2: 説明
all_rows.append(['※ 直接コスト欄（黄色）に、その案件に直接かかったコスト（研修講師費等）を入力してください', '', '', '', ''])

# 行3: ヘッダー
all_rows.append(['クライアント名', '売上合計', '直接コスト', '粗利', '粗利率'])

# 行4〜: クライアント行
for i, client in enumerate(CLIENTS):
    r = DATA_START + i
    all_rows.append([
        client,
        f'=IFERROR(SUMIF(売上明細!$B:$B,A{r},売上明細!$D:$D),0)',
        '',   # 直接コスト: 手動入力
        f'=B{r}-C{r}',
        f'=IFERROR(IF(B{r}=0,"—",D{r}/B{r}),"—")',
    ])

# 合計行
all_rows.append([
    '合計',
    f'=SUM(B{DATA_START}:B{DATA_START+NC-1})',
    f'=SUM(C{DATA_START}:C{DATA_START+NC-1})',
    f'=SUM(D{DATA_START}:D{DATA_START+NC-1})',
    f'=IFERROR(IF(B{TOTAL_ROW}=0,"—",D{TOTAL_ROW}/B{TOTAL_ROW}),"—")',
])

# 空白2行
all_rows.append([''] * 5)
all_rows.append([''] * 5)

# 共通コストセクションヘッダー
all_rows.append(['【共通コスト】　クライアントに紐付かないコスト（コスト明細から自動参照）', '', '', '', ''])

# 共通コスト明細
for label, cost_row in com_items:
    r = COM_ROWS_START + com_items.index((label, cost_row))
    # コスト明細のN列（年間合計）を参照することもできるが、月別は難しいので年間合計を表示
    all_rows.append([
        label,
        '',
        f'=コスト明細!N{cost_row}',  # 年間合計
        '',
        '',
    ])

# 共通コスト合計
all_rows.append([
    '共通コスト合計（年間）',
    '',
    f'=コスト明細!N{COST_ROW["販管費合計"]}',
    '',
    '',
])

# =========================================================
# 書き込み
# =========================================================
clear_range('案件別P/L!A1:Z50')
values_batch([{'range': '案件別P/L!A1', 'values': all_rows}])
print('データ書き込み完了')

# =========================================================
# 書式設定
# =========================================================
fmt = []
NFMT_YEN  = {'type': 'NUMBER', 'pattern': '¥#,##0'}
NFMT_PCT  = {'type': 'NUMBER', 'pattern': '0.0%'}
LAST_ROW  = len(all_rows) + 1

# タイトル
fmt += [
    merge(CASE_ID, 0, 1, 0, 5),
    cell_fmt(CASE_ID, 0, 1, 0, 5, bg='1F3864', color='FFFFFF', bold=True, fs=11,
             halign='CENTER', valign='MIDDLE'),
    row_h(CASE_ID, 0, 1, 38),
]

# 説明行
fmt += [
    merge(CASE_ID, 1, 2, 0, 5),
    cell_fmt(CASE_ID, 1, 2, 0, 5, bg='EBF5FB', color='1A5276', italic=True),
    row_h(CASE_ID, 1, 2, 22),
]

# ヘッダー行
fmt += [
    cell_fmt(CASE_ID, 2, 3, 0, 5, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(CASE_ID, 2, 3, 26),
]

# クライアント行: 交互カラー
for i in range(NC):
    ri = DATA_START - 1 + i   # 0-indexed
    bg = 'F8FBFF' if i % 2 == 0 else 'FFFFFF'
    fmt += [
        cell_fmt(CASE_ID, ri, ri+1, 0, 5, bg=bg, color='1A1A1A'),
        # 直接コスト列（C列=index 2）: 黄色入力セル
        cell_fmt(CASE_ID, ri, ri+1, 2, 3, bg='FFFDE7', color='1A1A1A'),
        row_h(CASE_ID, ri, ri+1, 24),
    ]

# 合計行
fmt += [
    cell_fmt(CASE_ID, TOTAL_ROW-1, TOTAL_ROW, 0, 5,
             bg='1A252F', color='FFFFFF', bold=True),
    row_h(CASE_ID, TOTAL_ROW-1, TOTAL_ROW, 26),
]

# 共通コストセクションヘッダー
fmt += [
    merge(CASE_ID, SEC_HDR-1, SEC_HDR, 0, 5),
    cell_fmt(CASE_ID, SEC_HDR-1, SEC_HDR, 0, 5,
             bg='4A235A', color='FFFFFF', bold=True),
    row_h(CASE_ID, SEC_HDR-1, SEC_HDR, 24),
]

# 共通コスト明細行
for i in range(len(com_items)):
    ri = COM_ROWS_START - 1 + i
    bg = 'F5EEF8' if i % 2 == 0 else 'FFFFFF'
    fmt.append(cell_fmt(CASE_ID, ri, ri+1, 0, 5, bg=bg, color='1A1A1A'))

# 共通コスト合計行
fmt += [
    cell_fmt(CASE_ID, COM_TOTAL_ROW-1, COM_TOTAL_ROW, 0, 5,
             bg='7D3C98', color='FFFFFF', bold=True),
]

# 数値フォーマット
fmt += [
    # B列（売上）, C列（直接コスト）, D列（粗利）: 通貨
    cell_fmt(CASE_ID, 2, COM_TOTAL_ROW, 1, 4, nfmt=NFMT_YEN, halign='RIGHT'),
    # E列（粗利率）: パーセント
    cell_fmt(CASE_ID, 2, TOTAL_ROW, 4, 5, nfmt=NFMT_PCT, halign='RIGHT'),
    # 共通コストのC列（コスト金額）
    cell_fmt(CASE_ID, COM_ROWS_START-1, COM_TOTAL_ROW, 2, 3, nfmt=NFMT_YEN, halign='RIGHT'),
]

# 罫線
fmt += [
    border_all(CASE_ID, 2, TOTAL_ROW, 0, 5),
    border_all(CASE_ID, SEC_HDR-1, COM_TOTAL_ROW, 0, 5),
]

# 列幅
fmt += [
    col_w(CASE_ID, 0, 285),  # クライアント名
    col_w(CASE_ID, 1, 130),  # 売上
    col_w(CASE_ID, 2, 130),  # 直接コスト
    col_w(CASE_ID, 3, 130),  # 粗利
    col_w(CASE_ID, 4, 100),  # 粗利率
    freeze(CASE_ID, rows=3, cols=0),
]

batch_update(fmt)
print('書式設定完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
print('\n【使い方】')
print('  黄色セル（直接コスト列）に、その案件に直接かかったコストを入力してください')
print('  例: FROUR向け研修講師費を50,000円払った場合 → FROUR行のC列に50000と入力')
print('  共通コスト（ツール費・人件費等）は下部に自動表示されます')
