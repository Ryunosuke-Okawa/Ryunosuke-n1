#!/usr/bin/env python3
"""
PL改修スクリプト v2
- コスト明細: 仕訳帳型に変更（クライアント・サービス・カテゴリ・金額 1行1明細）
- PL_月次: SUMIFS式に更新
- 案件別P/L: 新規作成
- 全シート書式設定（ネイビー＋交互カラー）
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

def clear(range_):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_}:clear'
    requests.post(url, headers=h, json={})

def rgb(hex_color):
    c = hex_color.lstrip('#')
    return {'red': int(c[0:2],16)/255, 'green': int(c[2:4],16)/255, 'blue': int(c[4:6],16)/255}

def cell_fmt(sid, r0, r1, c0, c1, **kw):
    uf = {}
    fields = []
    if 'bg' in kw:
        uf['backgroundColor'] = rgb(kw['bg'])
        fields.append('userEnteredFormat.backgroundColor')
    tf = {}
    if 'bold' in kw:
        tf['bold'] = kw['bold']
    if 'italic' in kw:
        tf['italic'] = kw['italic']
    if 'color' in kw:
        tf['foregroundColor'] = rgb(kw['color'])
    if 'fs' in kw:
        tf['fontSize'] = kw['fs']
    if tf:
        uf['textFormat'] = tf
        fields.append('userEnteredFormat.textFormat')
    if 'halign' in kw:
        uf['horizontalAlignment'] = kw['halign']
        fields.append('userEnteredFormat.horizontalAlignment')
    if 'valign' in kw:
        uf['verticalAlignment'] = kw['valign']
        fields.append('userEnteredFormat.verticalAlignment')
    if 'nfmt' in kw:
        uf['numberFormat'] = kw['nfmt']
        fields.append('userEnteredFormat.numberFormat')
    if 'wrap' in kw:
        uf['wrapStrategy'] = kw['wrap']
        fields.append('userEnteredFormat.wrapStrategy')
    return {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'cell': {'userEnteredFormat': uf},
        'fields': ','.join(fields)
    }}

def border(sid, r0, r1, c0, c1, color='CCCCCC', style='SOLID'):
    b = {'style': style, 'color': rgb(color)}
    return {'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'top': b, 'bottom': b, 'left': b, 'right': b,
        'innerHorizontal': b, 'innerVertical': b
    }}

def border_bottom(sid, r0, r1, c0, c1, color='CCCCCC', style='SOLID'):
    b = {'style': style, 'color': rgb(color)}
    return {'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'bottom': b
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

def dropdown(sid, r0, r1, c0, c1, vals):
    return {'setDataValidation': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'rule': {
            'condition': {'type': 'ONE_OF_LIST',
                          'values': [{'userEnteredValue': v} for v in vals]},
            'showCustomUi': True, 'strict': False
        }
    }}

# =========================================================
# シート情報取得
# =========================================================
info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
print('シート一覧:', sheets)

PL_ID   = sheets['PL_月次']
COST_ID = sheets['コスト明細']
SALE_ID = sheets['売上明細']

# 案件別P/Lシートを追加
if '案件別P/L' not in sheets:
    result = batch_update([{'addSheet': {'properties': {'title': '案件別P/L'}}}])
    CASE_ID = result['replies'][0]['addSheet']['properties']['sheetId']
    print(f'案件別P/L作成: sheetId={CASE_ID}')
else:
    CASE_ID = sheets['案件別P/L']
    print(f'案件別P/L既存: sheetId={CASE_ID}')

# =========================================================
# Step 1: コスト明細 → 仕訳帳型に変更
# =========================================================
print('\n[1] コスト明細を仕訳帳型に変更中...')
clear('コスト明細!A1:Z200')

months_dd = ['25年10月','25年11月','25年12月','26年1月','26年2月','26年3月',
             '26年4月','26年5月','26年6月','26年7月','26年8月','26年9月']
services_dd = ['Kawaru','Kawaru Team','Kawaru BPO','Kawaru Coach','共通']
categories_dd = [
    '研修講師費','外注開発費','コーチ人件費',
    '人件費（給与）','業務委託費',
    'ツール・インフラ費','マーケティング費',
    '交通費・出張費','接待交際費','その他管理費'
]
clients_dd = [
    'FROUR株式会社',
    '株式会社オンシナジー',
    '中部キリンビバレッジサービス株式会社',
    '株式会社NTTネクシア',
    'StockSun株式会社（ビバリーグレン分）',
    '（要確認）',
    '共通'
]

cost_data = [
    ['コスト明細（クライアント別）　★各列をプルダウンから選択して入力してください'],
    ['日付', '月', 'クライアント', 'サービス', 'コストカテゴリ', '内容・備考', '金額（税抜）'],
    ['★入力例', '25年10月', 'FROUR株式会社', 'Kawaru Team', '研修講師費', '研修講師（外部）費', 50000],
    ['★入力例', '25年10月', '共通', '共通', 'ツール・インフラ費', 'Claude API利用料', 15000],
] + [[''] * 7 for _ in range(100)]

values_batch([{'range': 'コスト明細!A1', 'values': cost_data}])
print('   コスト明細データ書き込み完了')

# =========================================================
# Step 2: PL_月次 → SUMIFS式に更新
# =========================================================
print('\n[2] PL_月次の数式をSUMIFSに更新中...')
cols = ['B','C','D','E','F','G','H','I','J','K','L','M']

# コスト行とカテゴリのマッピング
pl_cost = {
    12: '研修講師費',
    13: '外注開発費',
    14: 'コーチ人件費',
    21: '人件費（給与）',
    22: '業務委託費',
    23: 'ツール・インフラ費',
    24: 'マーケティング費',
    25: '交通費・出張費',
    26: '接待交際費',
    27: 'その他管理費',
}

vdata = []
for rn, cat in pl_cost.items():
    for col in cols:
        vdata.append({
            'range': f'PL_月次!{col}{rn}',
            'values': [[f'=IFERROR(SUMIFS(コスト明細!$G$3:$G$1000,コスト明細!$B$3:$B$1000,{col}$2,コスト明細!$E$3:$E$1000,"{cat}"),0)']]
        })
    vdata.append({'range': f'PL_月次!N{rn}', 'values': [[f'=SUM(B{rn}:M{rn})']]})

# 合計・集計行を再設定
for col in cols + ['N']:
    vdata += [
        {'range': f'PL_月次!{col}15', 'values': [[f'=SUM({col}12:{col}14)']]},
        {'range': f'PL_月次!{col}17', 'values': [[f'={col}9-{col}15']]},
        {'range': f'PL_月次!{col}28', 'values': [[f'=SUM({col}21:{col}27)']]},
        {'range': f'PL_月次!{col}30', 'values': [[f'={col}17-{col}28']]},
    ]
    if col != 'N':
        vdata += [
            {'range': f'PL_月次!{col}18',
             'values': [[f'=IFERROR(IF({col}9=0,"—",{col}17/{col}9),"—")']]},
            {'range': f'PL_月次!{col}31',
             'values': [[f'=IFERROR(IF({col}9=0,"—",{col}30/{col}9),"—")']]},
        ]

values_batch(vdata)
print('   PL_月次 数式更新完了')

# =========================================================
# Step 3: 案件別P/L シート作成
# =========================================================
print('\n[3] 案件別P/Lシートを作成中...')
clear('案件別P/L!A1:Z100')

clients_pl = [
    'FROUR株式会社',
    '株式会社オンシナジー',
    '中部キリンビバレッジサービス株式会社',
    '株式会社NTTネクシア',
    'StockSun株式会社（ビバリーグレン分）',
    '（要確認）',
]

case_data = [
    ['案件別P/L（クライアント別 売上・コスト・粗利）'],
    ['クライアント名', '売上合計', '直接コスト', '粗利', '粗利率'],
]
for i, client in enumerate(clients_pl):
    r = i + 3
    case_data.append([
        client,
        f'=IFERROR(SUMIF(売上明細!$B:$B,A{r},売上明細!$D:$D),0)',
        f'=IFERROR(SUMIF(コスト明細!$C:$C,A{r},コスト明細!$G:$G),0)',
        f'=B{r}-C{r}',
        f'=IFERROR(IF(B{r}=0,"—",D{r}/B{r}),"—")',
    ])

last_r = 2 + len(clients_pl)
tot_r  = last_r + 1
case_data.append([
    '合計',
    f'=SUM(B3:B{last_r})',
    f'=SUM(C3:C{last_r})',
    f'=SUM(D3:D{last_r})',
    f'=IFERROR(IF(B{tot_r}=0,"—",D{tot_r}/B{tot_r}),"—")',
])
case_data.append([])
case_data.append(['共通コスト（クライアント紐付けなし）', '',
                  '=IFERROR(SUMIF(コスト明細!$C:$C,"共通",コスト明細!$G:$G),0)', '', ''])

values_batch([{'range': '案件別P/L!A1', 'values': case_data}])
print('   案件別P/Lデータ書き込み完了')

# =========================================================
# Step 4: 書式設定（全3シート）
# =========================================================
print('\n[4] 書式設定を適用中...')
fmt = []

# -------------------- コスト明細 --------------------
NUM_COST_ROWS = 104
# タイトル
fmt += [
    merge(COST_ID, 0, 1, 0, 7),
    cell_fmt(COST_ID, 0, 1, 0, 7, bg='1F3864', color='FFFFFF', bold=True, fs=12, halign='CENTER', valign='MIDDLE'),
    row_h(COST_ID, 0, 1, 36),
    # ヘッダー
    cell_fmt(COST_ID, 1, 2, 0, 7, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER', valign='MIDDLE'),
    row_h(COST_ID, 1, 2, 28),
    # サンプル行（入力例）
    cell_fmt(COST_ID, 2, 4, 0, 7, bg='EBF5FB', color='808B96', italic=True),
    # 入力行（偶数行薄グレー、奇数行白）
    cell_fmt(COST_ID, 4, NUM_COST_ROWS, 0, 7, bg='FFFFFF'),
]
# ゼブラストライプ（5行目以降：6, 8, 10... → インデックス5, 7, 9...）
for i in range(4, NUM_COST_ROWS, 2):
    fmt.append(cell_fmt(COST_ID, i, i+1, 0, 7, bg='F2F3F4'))

fmt += [
    # 金額列: 通貨フォーマット・右揃え
    cell_fmt(COST_ID, 2, NUM_COST_ROWS, 6, 7,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    # 日付列: 日付フォーマット
    cell_fmt(COST_ID, 2, NUM_COST_ROWS, 0, 1,
             nfmt={'type': 'DATE', 'pattern': 'yyyy/m/d'}),
    # 罫線
    border(COST_ID, 1, NUM_COST_ROWS, 0, 7),
    # 列幅
    col_w(COST_ID, 0, 90),   # 日付
    col_w(COST_ID, 1, 100),  # 月
    col_w(COST_ID, 2, 210),  # クライアント
    col_w(COST_ID, 3, 130),  # サービス
    col_w(COST_ID, 4, 155),  # カテゴリ
    col_w(COST_ID, 5, 210),  # 内容・備考
    col_w(COST_ID, 6, 120),  # 金額
    # フリーズ（ヘッダー2行）
    freeze(COST_ID, rows=2, cols=0),
    # プルダウン
    dropdown(COST_ID, 2, 102, 1, 2, months_dd),       # B: 月
    dropdown(COST_ID, 2, 102, 2, 3, clients_dd),      # C: クライアント
    dropdown(COST_ID, 2, 102, 3, 4, services_dd),     # D: サービス
    dropdown(COST_ID, 2, 102, 4, 5, categories_dd),   # E: カテゴリ
]

# -------------------- 案件別P/L --------------------
nc = len(clients_pl)
fmt += [
    # タイトル
    merge(CASE_ID, 0, 1, 0, 5),
    cell_fmt(CASE_ID, 0, 1, 0, 5, bg='1F3864', color='FFFFFF', bold=True, fs=12, halign='CENTER', valign='MIDDLE'),
    row_h(CASE_ID, 0, 1, 40),
    # ヘッダー
    cell_fmt(CASE_ID, 1, 2, 0, 5, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(CASE_ID, 1, 2, 28),
    # 合計行
    cell_fmt(CASE_ID, 2 + nc, 3 + nc, 0, 5, bg='1A252F', color='FFFFFF', bold=True),
    # 共通コスト行
    cell_fmt(CASE_ID, 4 + nc, 5 + nc, 0, 5, bg='EAECEE', color='5D6D7E', italic=True),
    # 金額列: 通貨フォーマット
    cell_fmt(CASE_ID, 2, 3 + nc, 1, 4,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    cell_fmt(CASE_ID, 4 + nc, 5 + nc, 2, 3,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    # 粗利率列
    cell_fmt(CASE_ID, 2, 3 + nc, 4, 5, halign='RIGHT'),
    # 罫線
    border(CASE_ID, 1, 3 + nc, 0, 5),
    # 列幅
    col_w(CASE_ID, 0, 290),  # クライアント名
    col_w(CASE_ID, 1, 140),  # 売上
    col_w(CASE_ID, 2, 140),  # コスト
    col_w(CASE_ID, 3, 140),  # 粗利
    col_w(CASE_ID, 4, 100),  # 粗利率
    # フリーズ
    freeze(CASE_ID, rows=2),
]
# クライアント行: ゼブラストライプ
for i in range(nc):
    bg = 'EBF5FB' if i % 2 == 0 else 'FDFEFE'
    fmt.append(cell_fmt(CASE_ID, 2 + i, 3 + i, 0, 5, bg=bg))

batch_update(fmt)
print('   書式設定完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
