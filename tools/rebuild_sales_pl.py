#!/usr/bin/env python3
"""
PLスプレッドシートを売上管理特化の2シート構成に再構築
- 月次サマリー（髙橋COO確認用）
- 売上明細（入力シート：売上・原価・契約書/請求書リンク）
"""
import json
import requests

# =========================================================
# 認証・共通関数
# =========================================================
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

def clear_range(range_):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_}:clear'
    requests.post(url, headers=h, json={})

def get_values(range_):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_}'
    r = requests.get(url, headers=h, params={'valueRenderOption': 'FORMATTED_VALUE'})
    return r.json().get('values', [])

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
    if 'wrap' in kw: uf['wrapStrategy'] = kw['wrap']; fields.append('userEnteredFormat.wrapStrategy')
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

def dropdown(sid, r0, r1, c0, c1, vals, strict=True):
    return {'setDataValidation': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'rule': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': [{'userEnteredValue': v} for v in vals]
            },
            'showCustomUi': True,
            'strict': strict
        }
    }}

# =========================================================
# 定数
# =========================================================
MONTHS = ['25年10月','25年11月','25年12月','26年1月','26年2月','26年3月',
          '26年4月','26年5月','26年6月','26年7月','26年8月','26年9月']

SERVICES = ['Kawaru Team', 'Kawaru BPO', 'Kawaru Coach', 'Kawaru']

CLIENTS = [
    'FROUR株式会社',
    '株式会社オンシナジー',
    '株式会社バチャ・スタ',
    '中部キリンビバレッジサービス株式会社',
    '株式会社NTTネクシア',
    'StockSun株式会社（ビバリーグレン分）',
    '株式会社中西製作所',
]

YEN = {'type': 'NUMBER', 'pattern': '¥#,##0'}
PCT = {'type': 'NUMBER', 'pattern': '0.0%'}

# =========================================================
# Step 1: 既存データ（ハードコード — 前回実行で読み取り済み）
# =========================================================
print('[1] データ準備中...')

info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
print(f'   現在のシート: {sheets}')

# 前回の実行で読み取った既存データを直接使用（旧シートは削除済みのため）
# New layout: A=月, B=クライアント, C=サービス, D=売上金額, E=売上原価, F=実績/見込, G=契約書, H=請求書, I=備考
migrated = [
    ['25年10月', 'FROUR株式会社', 'Kawaru Team', 200000, '', '実績', '', '', ''],
    ['25年10月', '株式会社オンシナジー', 'Kawaru Coach', 100000, '', '実績', '', '', ''],
    ['25年12月', '株式会社バチャ・スタ', 'Kawaru Team', 45455, '', '実績', '', '', ''],
    ['26年2月', '中部キリンビバレッジサービス株式会社', 'Kawaru Team', 450000, 100000, '実績', '', '7,001', '生成AI基礎研修 / 2026年2月5日実施'],
    ['26年3月', '株式会社NTTネクシア', 'Kawaru Team', 5000000, '', '実績', '', '8,001', 'AI活用推進支援・研修コンテンツ作成'],
    ['26年3月', 'StockSun株式会社（ビバリーグレン分）', 'Kawaru BPO', 240000, '', '実績', '', '9,001', '2026年1〜3月分まとめ'],
    ['26年4月', '株式会社中西製作所', 'Kawaru BPO', 1000000, '', '見込', '', '', ''],
]

print(f'   移行データ: {len(migrated)}行')
for r in migrated:
    print(f'      {r[0]} | {r[1]} | {r[2]} | {r[3]}')

# =========================================================
# Step 2: 月次サマリーシートを作成（既存なら再利用）
# =========================================================
print('\n[2] 月次サマリーシート準備中...')

if '月次サマリー' in sheets:
    SUMMARY_ID = sheets['月次サマリー']
    clear_range('月次サマリー!A1:O50')
    print(f'   既存シートをクリア (sheetId={SUMMARY_ID})')
else:
    add_resp = batch_update([{
        'addSheet': {
            'properties': {
                'title': '月次サマリー',
                'index': 0,
                'gridProperties': {'rowCount': 50, 'columnCount': 15}
            }
        }
    }])
    SUMMARY_ID = add_resp['replies'][0]['addSheet']['properties']['sheetId']
    print(f'   新規作成 (sheetId={SUMMARY_ID})')

# =========================================================
# Step 3: 不要シートを削除
# =========================================================
print('\n[3] 不要シートを削除中...')

delete_reqs = []
for name in ['PL_月次', 'コスト明細', '案件別P/L']:
    if name in sheets:
        delete_reqs.append({'deleteSheet': {'sheetId': sheets[name]}})
        print(f'   削除: {name} (id={sheets[name]})')
if delete_reqs:
    batch_update(delete_reqs)
else:
    print('   削除対象なし')

SALES_ID = sheets['売上明細']

# =========================================================
# Step 4: 売上明細を再構築
# =========================================================
print('\n[4] 売上明細を再構築中...')

clear_range('売上明細!A1:Z200')

# タイトル + ヘッダー + データ + 空行
DETAIL_HEADERS = ['月', 'クライアント名', 'サービス', '売上金額（税抜）', '売上原価（税抜）',
                  '実績/見込', '契約書リンク', '請求書リンク', '備考']

detail_rows = [
    ['売上明細（クライアント別）'] + [''] * 8,  # Row 1: title
    DETAIL_HEADERS,                               # Row 2: headers
]

# データ行
for r in migrated:
    detail_rows.append(r)

# 空の入力行を追加（100行分）
data_start = 3  # Row 3 from 1-indexed
data_end = data_start + len(migrated) + 100
for _ in range(100):
    detail_rows.append([''] * 9)

values_batch([{'range': '売上明細!A1', 'values': detail_rows}])
print(f'   書き込み完了 ({len(migrated)}行データ + 100空行)')

# =========================================================
# Step 5: 月次サマリーにデータ・数式を書き込み
# =========================================================
print('\n[5] 月次サマリーに数式を書き込み中...')

# SUMIFS用のデータ範囲（売上明細の200行分をカバー）
DR = 200  # data range rows

# --- セクションA: 月別/サービス別 売上 ---
summary_rows = []

# Row 1: タイトル
summary_rows.append(['月次サマリー（髙橋COO確認用）'] + [''] * 13)

# Row 2: ヘッダー
summary_rows.append([''] + MONTHS + ['年間合計'])

# Row 3: セクションヘッダー
summary_rows.append(['【売上】'] + [''] * 13)

# Row 4-7: サービス別売上 (SUMIFS)
for si, svc in enumerate(SERVICES):
    row = [svc]
    for mi, month in enumerate(MONTHS):
        col = chr(66 + mi)  # B, C, D, ... M
        row.append(f'=IFERROR(SUMIFS(売上明細!$D$3:$D${DR},売上明細!$A$3:$A${DR},{col}$2,売上明細!$C$3:$C${DR},$A{4+si}),0)')
    row.append(f'=SUM(B{4+si}:M{4+si})')
    summary_rows.append(row)

# Row 8: 売上合計
r_sales_total = 8
summary_rows.append(['売上合計'] + [f'=SUM({chr(66+mi)}4:{chr(66+mi)}7)' for mi in range(12)] + [f'=SUM(B8:M8)'])

# Row 9: 空行
summary_rows.append([''] * 14)

# --- セクションB: 月別/サービス別 売上原価 ---
# Row 10: セクションヘッダー
summary_rows.append(['【売上原価】'] + [''] * 13)

# Row 11-14: サービス別原価 (SUMIFS)
for si, svc in enumerate(SERVICES):
    row = [svc]
    for mi, month in enumerate(MONTHS):
        col = chr(66 + mi)  # B, C, D, ... M
        row.append(f'=IFERROR(SUMIFS(売上明細!$E$3:$E${DR},売上明細!$A$3:$A${DR},{col}$2,売上明細!$C$3:$C${DR},$A{11+si}),0)')
    row.append(f'=SUM(B{11+si}:M{11+si})')
    summary_rows.append(row)

# Row 15: 売上原価合計
r_cogs_total = 15
summary_rows.append(['売上原価合計'] + [f'=SUM({chr(66+mi)}11:{chr(66+mi)}14)' for mi in range(12)] + [f'=SUM(B15:M15)'])

# Row 16: 空行
summary_rows.append([''] * 14)

# --- セクションC: 売上総利益・粗利率 ---
# Row 17: セクションヘッダー
summary_rows.append(['【売上総利益】'] + [''] * 13)

# Row 18: 売上総利益
summary_rows.append(['売上総利益'] + [f'={chr(66+mi)}8-{chr(66+mi)}15' for mi in range(12)] + ['=SUM(B18:M18)'])

# Row 19: 粗利率
summary_rows.append(['粗利率'] + [f'=IFERROR({chr(66+mi)}18/{chr(66+mi)}8,"—")' for mi in range(12)] + [f'=IFERROR(N18/N8,"—")'])

# Row 20-21: 空行
summary_rows.append([''] * 14)
summary_rows.append([''] * 14)

# --- セクションD: クライアント別売上 ---
# Row 22: セクションヘッダー
summary_rows.append(['【クライアント別 売上】'] + [''] * 13)

# Row 23: クライアント別ヘッダー（A-F列を使用）
summary_rows.append(['クライアント名', '売上合計', '原価合計', '粗利', '粗利率', '契約書'] + [''] * 8)

# Row 24+: クライアント行
for ci, client in enumerate(CLIENTS):
    r = 24 + ci
    summary_rows.append([
        client,
        f'=IFERROR(SUMIF(売上明細!$B$3:$B${DR},$A{r},売上明細!$D$3:$D${DR}),0)',  # 売上合計
        f'=IFERROR(SUMIF(売上明細!$B$3:$B${DR},$A{r},売上明細!$E$3:$E${DR}),0)',  # 原価合計
        f'=B{r}-C{r}',           # 粗利
        f'=IFERROR(D{r}/B{r},"—")',  # 粗利率
        f'=IFERROR(INDEX(売上明細!$G$3:$G${DR},MATCH($A{r},売上明細!$B$3:$B${DR},0)),"")',  # 契約書リンク
    ] + [''] * 8)

# 合計行
r_client_total = 24 + len(CLIENTS)
summary_rows.append([
    '合計',
    f'=SUM(B24:B{r_client_total-1})',
    f'=SUM(C24:C{r_client_total-1})',
    f'=B{r_client_total}-C{r_client_total}',
    f'=IFERROR(D{r_client_total}/B{r_client_total},"—")',
    '',
] + [''] * 8)

values_batch([{'range': '月次サマリー!A1', 'values': summary_rows}])
print(f'   書き込み完了 ({len(summary_rows)}行)')

# =========================================================
# Step 6: 書式設定 — 売上明細
# =========================================================
print('\n[6] 売上明細の書式設定中...')

DETAIL_DATA_END = 3 + len(migrated) + 100  # タイトル(1) + ヘッダー(1) + データ + 空行

fmt_detail = []

# タイトル
fmt_detail += [
    merge(SALES_ID, 0, 1, 0, 9),
    cell_fmt(SALES_ID, 0, 1, 0, 9, bg='1F3864', color='FFFFFF', bold=True, fs=12,
             halign='CENTER', valign='MIDDLE'),
    row_h(SALES_ID, 0, 1, 36),
]

# ヘッダー
fmt_detail += [
    cell_fmt(SALES_ID, 1, 2, 0, 9, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(SALES_ID, 1, 2, 28),
]

# データ領域ベース
fmt_detail += [
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 0, 9, bg='FFFFFF', color='333333'),
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 0, 1, halign='CENTER'),  # 月: CENTER
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 2, 3, halign='CENTER'),  # サービス: CENTER
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 5, 6, halign='CENTER'),  # 実績/見込: CENTER
]

# 金額列（D, E）: 通貨
fmt_detail += [
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 3, 5, nfmt=YEN, halign='RIGHT'),
]

# リンク列（G, H）: WRAP
fmt_detail += [
    cell_fmt(SALES_ID, 2, DETAIL_DATA_END, 6, 8, wrap='WRAP'),
]

# ゼブラストライプ（データ行のみ）
for i in range(len(migrated)):
    ri = 2 + i  # 0-indexed
    if i % 2 == 1:
        fmt_detail.append(cell_fmt(SALES_ID, ri, ri+1, 0, 9, bg='F4F9FF'))

# 列幅
detail_col_widths = [90, 220, 130, 130, 130, 80, 200, 200, 180]
for ci, w in enumerate(detail_col_widths):
    fmt_detail.append(col_w(SALES_ID, ci, w))

# フリーズ
fmt_detail.append(freeze(SALES_ID, rows=2, cols=0))

# 罫線（ヘッダー+データ行）
fmt_detail.append(border_all(SALES_ID, 1, 2 + len(migrated), 0, 9))

# ドロップダウン
DATA_ROW_START = 2  # 0-indexed (row 3 in 1-indexed)
DATA_ROW_END = DETAIL_DATA_END

# A列: 月
fmt_detail.append(dropdown(SALES_ID, DATA_ROW_START, DATA_ROW_END, 0, 1, MONTHS, strict=False))
# B列: クライアント（自由入力OK）
fmt_detail.append(dropdown(SALES_ID, DATA_ROW_START, DATA_ROW_END, 1, 2, CLIENTS, strict=False))
# C列: サービス
fmt_detail.append(dropdown(SALES_ID, DATA_ROW_START, DATA_ROW_END, 2, 3, SERVICES, strict=False))
# F列: 実績/見込
fmt_detail.append(dropdown(SALES_ID, DATA_ROW_START, DATA_ROW_END, 5, 6, ['実績', '見込'], strict=True))

batch_update(fmt_detail)
print('   完了')

# =========================================================
# Step 7: 書式設定 — 月次サマリー
# =========================================================
print('\n[7] 月次サマリーの書式設定中...')

fmt_summary = []

# --- タイトル ---
fmt_summary += [
    merge(SUMMARY_ID, 0, 1, 0, 14),
    cell_fmt(SUMMARY_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=12,
             halign='CENTER', valign='MIDDLE'),
    row_h(SUMMARY_ID, 0, 1, 40),
]

# --- ヘッダー行（月） ---
fmt_summary += [
    cell_fmt(SUMMARY_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(SUMMARY_ID, 1, 2, 26),
]

# --- セクションA: 売上 ---
# Row 3 (idx=2): セクションヘッダー
fmt_summary += [
    cell_fmt(SUMMARY_ID, 2, 3, 0, 14, bg='1A5276', color='FFFFFF', bold=True),
    row_h(SUMMARY_ID, 2, 3, 24),
]
# Row 4-7 (idx=3-6): サービス行
fmt_summary += [
    cell_fmt(SUMMARY_ID, 3, 7, 0, 14, bg='FFFFFF', color='333333'),
    cell_fmt(SUMMARY_ID, 3, 7, 1, 14, nfmt=YEN, halign='RIGHT'),
]
# ゼブラ
fmt_summary.append(cell_fmt(SUMMARY_ID, 4, 5, 0, 14, bg='F4F9FF'))
fmt_summary.append(cell_fmt(SUMMARY_ID, 6, 7, 0, 14, bg='F4F9FF'))
# Row 8 (idx=7): 売上合計
fmt_summary += [
    cell_fmt(SUMMARY_ID, 7, 8, 0, 14, bg='1A5276', color='FFFFFF', bold=True),
    cell_fmt(SUMMARY_ID, 7, 8, 1, 14, nfmt=YEN, halign='RIGHT'),
    row_h(SUMMARY_ID, 7, 8, 26),
]

# --- セクションB: 売上原価 ---
# Row 10 (idx=9): セクションヘッダー
fmt_summary += [
    cell_fmt(SUMMARY_ID, 9, 10, 0, 14, bg='6E2F00', color='FFFFFF', bold=True),
    row_h(SUMMARY_ID, 9, 10, 24),
]
# Row 11-14 (idx=10-13): サービス行
fmt_summary += [
    cell_fmt(SUMMARY_ID, 10, 14, 0, 14, bg='FFFFFF', color='333333'),
    cell_fmt(SUMMARY_ID, 10, 14, 1, 14, nfmt=YEN, halign='RIGHT'),
]
fmt_summary.append(cell_fmt(SUMMARY_ID, 11, 12, 0, 14, bg='FFF8F0'))
fmt_summary.append(cell_fmt(SUMMARY_ID, 13, 14, 0, 14, bg='FFF8F0'))
# Row 15 (idx=14): 売上原価合計
fmt_summary += [
    cell_fmt(SUMMARY_ID, 14, 15, 0, 14, bg='A04000', color='FFFFFF', bold=True),
    cell_fmt(SUMMARY_ID, 14, 15, 1, 14, nfmt=YEN, halign='RIGHT'),
    row_h(SUMMARY_ID, 14, 15, 26),
]

# --- セクションC: 売上総利益 ---
# Row 17 (idx=16): セクションヘッダー
fmt_summary += [
    cell_fmt(SUMMARY_ID, 16, 17, 0, 14, bg='1E8449', color='FFFFFF', bold=True),
    row_h(SUMMARY_ID, 16, 17, 24),
]
# Row 18 (idx=17): 売上総利益
fmt_summary += [
    cell_fmt(SUMMARY_ID, 17, 18, 0, 14, bg='D5F5E3', color='1E8449', bold=True),
    cell_fmt(SUMMARY_ID, 17, 18, 1, 14, nfmt=YEN, halign='RIGHT'),
    row_h(SUMMARY_ID, 17, 18, 26),
]
# Row 19 (idx=18): 粗利率
fmt_summary += [
    cell_fmt(SUMMARY_ID, 18, 19, 0, 14, bg='EAFAF1', color='1E8449', bold=True),
    cell_fmt(SUMMARY_ID, 18, 19, 1, 14, nfmt=PCT, halign='RIGHT'),
    row_h(SUMMARY_ID, 18, 19, 24),
]

# --- セクションD: クライアント別売上 ---
# Row 22 (idx=21): セクションヘッダー
fmt_summary += [
    cell_fmt(SUMMARY_ID, 21, 22, 0, 14, bg='2E5090', color='FFFFFF', bold=True),
    row_h(SUMMARY_ID, 21, 22, 24),
]
# Row 23 (idx=22): クライアント別ヘッダー
fmt_summary += [
    cell_fmt(SUMMARY_ID, 22, 23, 0, 6, bg='34495E', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(SUMMARY_ID, 22, 23, 26),
]
# Row 24-30 (idx=23-29): クライアント行
client_end_idx = 23 + len(CLIENTS)
fmt_summary += [
    cell_fmt(SUMMARY_ID, 23, client_end_idx, 0, 6, bg='FFFFFF', color='333333'),
    cell_fmt(SUMMARY_ID, 23, client_end_idx, 1, 4, nfmt=YEN, halign='RIGHT'),
    cell_fmt(SUMMARY_ID, 23, client_end_idx, 4, 5, nfmt=PCT, halign='RIGHT'),
]
# ゼブラ
for i in range(len(CLIENTS)):
    if i % 2 == 1:
        fmt_summary.append(cell_fmt(SUMMARY_ID, 23+i, 24+i, 0, 6, bg='F4F9FF'))
# 合計行
fmt_summary += [
    cell_fmt(SUMMARY_ID, client_end_idx, client_end_idx+1, 0, 6,
             bg='1A252F', color='FFFFFF', bold=True),
    cell_fmt(SUMMARY_ID, client_end_idx, client_end_idx+1, 1, 4, nfmt=YEN, halign='RIGHT'),
    cell_fmt(SUMMARY_ID, client_end_idx, client_end_idx+1, 4, 5, nfmt=PCT, halign='RIGHT'),
    row_h(SUMMARY_ID, client_end_idx, client_end_idx+1, 26),
]

# --- 年間合計列の強調 ---
fmt_summary.append(cell_fmt(SUMMARY_ID, 1, 19, 13, 14, bold=True, bg='ECF0F1'))

# --- 列幅 ---
fmt_summary.append(col_w(SUMMARY_ID, 0, 170))
for i in range(1, 13):
    fmt_summary.append(col_w(SUMMARY_ID, i, 85))
fmt_summary.append(col_w(SUMMARY_ID, 13, 100))

# --- フリーズ（タイトル行がマージされているのでcols=0） ---
fmt_summary.append(freeze(SUMMARY_ID, rows=2, cols=0))

# --- 罫線 ---
# 売上セクション
fmt_summary.append(border_all(SUMMARY_ID, 1, 8, 0, 14))
# 売上原価セクション
fmt_summary.append(border_all(SUMMARY_ID, 9, 15, 0, 14))
# 売上総利益セクション
fmt_summary.append(border_all(SUMMARY_ID, 16, 19, 0, 14))
# クライアント別セクション
fmt_summary.append(border_all(SUMMARY_ID, 22, client_end_idx+1, 0, 6))

batch_update(fmt_summary)
print('   完了')

# =========================================================
# Step 8: シート順序確定（月次サマリーが先頭）
# =========================================================
print('\n[8] シート順序を確定中...')
batch_update([
    {'updateSheetProperties': {
        'properties': {'sheetId': SUMMARY_ID, 'index': 0},
        'fields': 'index'
    }},
    {'updateSheetProperties': {
        'properties': {'sheetId': SALES_ID, 'index': 1},
        'fields': 'index'
    }},
])
print('   完了')

print(f'\n✅ 再構築完了!')
print(f'   月次サマリー (sheetId={SUMMARY_ID})')
print(f'   売上明細 (sheetId={SALES_ID})')
print(f'   URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
