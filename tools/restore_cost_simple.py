#!/usr/bin/env python3
"""
コスト明細を最初のシンプルなマトリクス形式に戻す
コスト一覧シートを削除
PL_月次の参照式を更新
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

def clear_range(range_):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_}:clear'
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
print('シート一覧:', sheets)

PL_ID   = sheets['PL_月次']
COST_ID = sheets['コスト明細']

# =========================================================
# Step 1: コスト一覧シートを削除
# =========================================================
if 'コスト一覧' in sheets:
    batch_update([{'deleteSheet': {'sheetId': sheets['コスト一覧']}}])
    print('コスト一覧シート削除完了')

# =========================================================
# Step 2: コスト明細をシンプルなマトリクス形式に再構築
# =========================================================
print('\n[1] コスト明細データ構築中...')

months = ['25年10月','25年11月','25年12月','26年1月','26年2月','26年3月',
          '26年4月','26年5月','26年6月','26年7月','26年8月','26年9月']
COLS = ['B','C','D','E','F','G','H','I','J','K','L','M']
NUM_COLS = 14  # A + 12ヶ月 + 年間合計

# 行定義: (type, label)
# type: title/header/section/item/subtotal/grand/blank
ROWS_DEF = [
    ('title',    'コスト入力シート（月別）　※黄色セルに数値を入力してください'),
    ('header',   ''),
    ('section',  '【A】売上原価（COGS）'),
    ('item',     '研修講師費'),       # 行4
    ('item',     '外注開発費'),       # 行5
    ('item',     'コーチ人件費'),     # 行6
    ('subtotal', '売上原価合計'),     # 行7
    ('blank',    ''),
    ('section',  '【B】人件費'),
    ('item',     '人件費（給与）'),   # 行10
    ('item',     '業務委託費'),       # 行11
    ('subtotal', '人件費合計'),       # 行12
    ('blank',    ''),
    ('section',  '【C】ツール・インフラ費'),
    ('item',     'AI APIコスト'),     # 行15
    ('item',     'SaaSサブスク（Slack/Notion等）'), # 行16
    ('item',     'システム開発・保守'),# 行17
    ('subtotal', 'ツール合計'),        # 行18
    ('blank',    ''),
    ('section',  '【D】マーケティング・営業費'),
    ('item',     '広告費'),            # 行21
    ('item',     '展示会・イベント費'),# 行22
    ('item',     '資料作成費'),        # 行23
    ('item',     '交通費・出張費'),    # 行24
    ('item',     '接待交際費'),        # 行25
    ('subtotal', 'マーケ合計'),        # 行26
    ('blank',    ''),
    ('section',  '【E】管理費'),
    ('item',     '事務所費（按分）'),  # 行29
    ('item',     '通信費'),            # 行30
    ('item',     '備品・消耗品費'),    # 行31
    ('item',     '外部顧問・士業費'),  # 行32
    ('subtotal', '管理費合計'),        # 行33
    ('blank',    ''),
    ('grand',    '★販管費合計（B+C+D+E）'), # 行35
    ('grand2',   '★コスト合計（A+販管費）'),# 行36
]

# 行番号マップ構築
row_map = {}  # label -> 1-indexed行番号
subtotal_map = {}  # section_key -> subtotal行番号
cur = 1
sections_items = {}  # subtotal_label -> [item rows]
current_sec_items = []
current_subtotal = None

for type_, label in ROWS_DEF:
    row_map[label] = cur
    if type_ == 'item':
        current_sec_items.append(cur)
    elif type_ == 'subtotal':
        subtotal_map[label] = {'row': cur, 'items': list(current_sec_items)}
        current_sec_items = []
    cur += 1

# データ行構築
all_rows = []
for type_, label in ROWS_DEF:
    r = row_map[label]

    if type_ == 'title':
        all_rows.append([label] + [''] * (NUM_COLS - 1))

    elif type_ == 'header':
        all_rows.append(['コストカテゴリ'] + months + ['年間合計'])

    elif type_ in ('section', 'blank'):
        all_rows.append([label] + [''] * (NUM_COLS - 1))

    elif type_ == 'item':
        row_data = [label] + [''] * 12 + [f'=SUM(B{r}:M{r})']
        all_rows.append(row_data)

    elif type_ == 'subtotal':
        items = subtotal_map[label]['items']
        row_data = [label]
        for col in COLS:
            row_data.append(f'=SUM({col}{min(items)}:{col}{max(items)})')
        row_data.append(f'=SUM(B{r}:M{r})')
        all_rows.append(row_data)

    elif type_ == 'grand':
        # 販管費 = 人件費合計+ツール合計+マーケ合計+管理費合計
        sub_rows = [
            subtotal_map['人件費合計']['row'],
            subtotal_map['ツール合計']['row'],
            subtotal_map['マーケ合計']['row'],
            subtotal_map['管理費合計']['row'],
        ]
        row_data = [label]
        for col in COLS:
            row_data.append(f'={"+".join([f"{col}{sr}" for sr in sub_rows])}')
        row_data.append(f'=SUM(B{r}:M{r})')
        all_rows.append(row_data)

    elif type_ == 'grand2':
        cogs_row = subtotal_map['売上原価合計']['row']
        sga_row  = row_map['★販管費合計（B+C+D+E）']
        row_data = [label]
        for col in COLS:
            row_data.append(f'={col}{cogs_row}+{col}{sga_row}')
        row_data.append(f'=SUM(B{r}:M{r})')
        all_rows.append(row_data)

print(f'   行数: {len(all_rows)}')
print(f'   行マップ（主要）:')
key_labels = ['研修講師費','外注開発費','コーチ人件費','人件費（給与）','業務委託費',
              'ツール合計','広告費','展示会・イベント費','資料作成費','交通費・出張費',
              '接待交際費','管理費合計']
for lbl in key_labels:
    if lbl in row_map:
        print(f'      {lbl}: 行{row_map[lbl]}')

clear_range('コスト明細!A1:N100')
values_batch([{'range': 'コスト明細!A1', 'values': all_rows}])
print('   書き込み完了')

# =========================================================
# Step 3: PL_月次の参照式を更新
# =========================================================
print('\n[2] PL_月次の参照式を更新中...')

# PL行 → コスト明細の参照先
# マーケティング費は広告費+展示会+資料作成費の合計
mktg_rows = [row_map['広告費'], row_map['展示会・イベント費'], row_map['資料作成費']]

def direct_ref(cost_row, col):
    return f'=コスト明細!{col}{cost_row}'

def multi_ref(cost_rows, col):
    return f'={"+".join([f"コスト明細!{col}{r}" for r in cost_rows])}'

pl_vdata = []
for col in COLS:
    pl_vdata += [
        # 売上原価
        {'range': f'PL_月次!{col}12', 'values': [[direct_ref(row_map['研修講師費'], col)]]},
        {'range': f'PL_月次!{col}13', 'values': [[direct_ref(row_map['外注開発費'], col)]]},
        {'range': f'PL_月次!{col}14', 'values': [[direct_ref(row_map['コーチ人件費'], col)]]},
        # 販管費
        {'range': f'PL_月次!{col}21', 'values': [[direct_ref(row_map['人件費（給与）'], col)]]},
        {'range': f'PL_月次!{col}22', 'values': [[direct_ref(row_map['業務委託費'], col)]]},
        {'range': f'PL_月次!{col}23', 'values': [[direct_ref(subtotal_map['ツール合計']['row'], col)]]},
        {'range': f'PL_月次!{col}24', 'values': [[multi_ref(mktg_rows, col)]]},
        {'range': f'PL_月次!{col}25', 'values': [[direct_ref(row_map['交通費・出張費'], col)]]},
        {'range': f'PL_月次!{col}26', 'values': [[direct_ref(row_map['接待交際費'], col)]]},
        {'range': f'PL_月次!{col}27', 'values': [[direct_ref(subtotal_map['管理費合計']['row'], col)]]},
    ]
# 年間合計列（N列）
for pl_row in [12,13,14,21,22,23,24,25,26,27]:
    pl_vdata.append({'range': f'PL_月次!N{pl_row}', 'values': [[f'=SUM(B{pl_row}:M{pl_row})']]})

values_batch(pl_vdata)
print('   完了')

# =========================================================
# Step 4: 書式設定
# =========================================================
print('\n[3] 書式設定を適用中...')

TOTAL_ROWS = len(all_rows) + 1  # 0-indexed終端

# セクションカラー
SEC_COLORS = {
    '【A】売上原価（COGS）':          ('1A5276', 'D6EAF8'),
    '【B】人件費':                    ('1E8449', 'D5F5E3'),
    '【C】ツール・インフラ費':        ('6E2F00', 'FAE5D3'),
    '【D】マーケティング・営業費':    ('4A235A', 'E8DAEF'),
    '【E】管理費':                    ('212F3D', 'D5D8DC'),
}
SUBTOTAL_BG = {
    '売上原価合計': '2471A3',
    '人件費合計':   '239B56',
    'ツール合計':   'A04000',
    'マーケ合計':   '7D3C98',
    '管理費合計':   '2C3E50',
}

fmt = []

# タイトル
fmt += [
    merge(COST_ID, 0, 1, 0, 14),
    cell_fmt(COST_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=11,
             halign='CENTER', valign='MIDDLE'),
    row_h(COST_ID, 0, 1, 36),
    # ヘッダー
    cell_fmt(COST_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(COST_ID, 1, 2, 26),
    # 全体ベース
    cell_fmt(COST_ID, 2, TOTAL_ROWS, 0, 14, bg='FFFFFF'),
    # 数値列: 通貨・右揃え
    cell_fmt(COST_ID, 2, TOTAL_ROWS, 1, 14,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    # 年間合計列
    cell_fmt(COST_ID, 1, TOTAL_ROWS, 13, 14, bg='ECF0F1', bold=True),
    # フリーズ
    freeze(COST_ID, rows=2, cols=0),
    # 列幅
    col_w(COST_ID, 0, 195),
]
for i in range(1, 13):
    fmt.append(col_w(COST_ID, i, 82))
fmt.append(col_w(COST_ID, 13, 95))

# 各行スタイル
cur_sec_dark = None
cur_sec_light = None
for type_, label in ROWS_DEF:
    ri = row_map[label] - 1  # 0-indexed

    if type_ == 'section':
        colors = SEC_COLORS.get(label, ('333333', 'EEEEEE'))
        cur_sec_dark, cur_sec_light = colors
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg=cur_sec_dark, color='FFFFFF', bold=True),
            row_h(COST_ID, ri, ri+1, 24),
        ]
    elif type_ == 'item':
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 1,
                     bg='FAFAFA', color='333333'),
            # 入力セル（月列）: 黄色
            cell_fmt(COST_ID, ri, ri+1, 1, 13,
                     bg='FFFDE7'),
            row_h(COST_ID, ri, ri+1, 22),
        ]
    elif type_ == 'subtotal':
        sub_bg = SUBTOTAL_BG.get(label, '555555')
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg=sub_bg, color='FFFFFF', bold=True),
            row_h(COST_ID, ri, ri+1, 24),
        ]
    elif type_ == 'grand':
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg='1C2833', color='FFFFFF', bold=True, fs=10),
            row_h(COST_ID, ri, ri+1, 28),
        ]
    elif type_ == 'grand2':
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg='0B0C10', color='FFFFFF', bold=True, fs=10),
            row_h(COST_ID, ri, ri+1, 30),
        ]

# 全体罫線
fmt.append(border_all(COST_ID, 1, TOTAL_ROWS, 0, 14))

batch_update(fmt)
print('   完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
