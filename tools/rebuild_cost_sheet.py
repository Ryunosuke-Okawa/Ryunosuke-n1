#!/usr/bin/env python3
"""
コスト明細を「合計行＋内訳行」マトリクス形式に再設計
PL_月次の参照式も合計行の直接セル参照に更新
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
    if 'indent' in kw: uf['textFormat'] = uf.get('textFormat', {}); fields.append('userEnteredFormat.textFormat')
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

def border_bottom(sid, r0, r1, c0, c1, style='SOLID_MEDIUM', color='888888'):
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

# =========================================================
# シート情報取得
# =========================================================
info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
print('シート一覧:', sheets)

PL_ID   = sheets['PL_月次']
COST_ID = sheets['コスト明細']

# =========================================================
# シート構造定義
# =========================================================
# 各セクションのカテゴリと初期内訳ラベル
STRUCTURE = [
    {
        'section': '【A】売上原価（COGS）',
        'key': 'cogs',
        'categories': [
            {'label': '研修講師費',   'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
            {'label': '外注開発費',   'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
            {'label': 'コーチ人件費', 'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
        ],
        'subtotal': '売上原価合計',
    },
    {
        'section': '【B】人件費',
        'key': 'hr',
        'categories': [
            {'label': '人件費（給与）', 'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
            {'label': '業務委託費',     'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
        ],
        'subtotal': '人件費合計',
    },
    {
        'section': '【C】ツール・インフラ費',
        'key': 'tools',
        'categories': [
            {'label': 'ツール・インフラ費',
             'details': ['Claude API', 'Notion / Slack等', 'システム開発・保守',
                         '（内訳を入力）', '（内訳を入力）']},
        ],
        'subtotal': 'ツール合計',
    },
    {
        'section': '【D】マーケティング・営業費',
        'key': 'mktg',
        'categories': [
            {'label': 'マーケティング費', 'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
            {'label': '交通費・出張費',   'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
            {'label': '接待交際費',       'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
        ],
        'subtotal': 'マーケ合計',
    },
    {
        'section': '【E】管理費',
        'key': 'mgmt',
        'categories': [
            {'label': 'その他管理費', 'details': ['（内訳を入力）', '（内訳を入力）', '（内訳を入力）']},
        ],
        'subtotal': '管理費合計',
    },
]

months    = ['25年10月','25年11月','25年12月','26年1月','26年2月','26年3月',
             '26年4月','26年5月','26年6月','26年7月','26年8月','26年9月']
NUM_COLS  = 14  # A + 12ヶ月 + 年間合計

# =========================================================
# 行レイアウトを動的に計算
# =========================================================
layout = []  # {'row': 1-indexed, 'type': ..., 'label': ..., 'meta': ...}

cur = 1  # 1-indexed

def add(type_, label, meta=None):
    global cur
    layout.append({'row': cur, 'type': type_, 'label': label, 'meta': meta or {}})
    cur += 1

# 行1: タイトル
add('title',   'コスト明細（月別）　★インデント行（水色セル）に金額を入力してください')
# 行2: ヘッダー
add('header',  '')

category_rows = {}   # label -> row番号（PL参照用）
subtotal_rows = {}   # key   -> row番号

for sec in STRUCTURE:
    add('section', sec['section'], {'key': sec['key']})

    cat_total_rows_in_sec = []
    for cat in sec['categories']:
        total_row = cur
        category_rows[cat['label']] = total_row
        cat_total_rows_in_sec.append(total_row)

        item_start = cur + 1
        item_end   = cur + len(cat['details'])
        add('total', cat['label'], {'item_start': item_start, 'item_end': item_end})

        for d in cat['details']:
            add('item', d)

    sub_row = cur
    subtotal_rows[sec['key']] = sub_row
    add('subtotal', sec['subtotal'], {'cat_rows': cat_total_rows_in_sec})

    add('blank', '')

# 販管費・コスト合計
sga_row = cur
add('sga', '★販管費合計（B+C+D+E）', {
    'sub_keys': ['hr', 'tools', 'mktg', 'mgmt']
})
grand_row = cur
add('grand', '★コスト合計（A+販管費）', {
    'cogs_key': 'cogs', 'sga_row': sga_row
})

print(f'総行数: {cur - 1}')
print('カテゴリ行マップ:', {k: v for k, v in category_rows.items()})

# =========================================================
# データ行を構築
# =========================================================
COLS = ['B','C','D','E','F','G','H','I','J','K','L','M']

all_rows = []
for entry in layout:
    r    = entry['row']
    t    = entry['type']
    lbl  = entry['label']
    meta = entry['meta']

    if t == 'title':
        row_data = [lbl] + [''] * (NUM_COLS - 1)

    elif t == 'header':
        row_data = ['コストカテゴリ / 内訳'] + months + ['年間合計']

    elif t == 'section':
        row_data = [lbl] + [''] * (NUM_COLS - 1)

    elif t == 'total':
        is_ = meta['item_start']
        ie_ = meta['item_end']
        row_data = [lbl]
        for col in COLS:
            row_data.append(f'=SUM({col}{is_}:{col}{ie_})')
        row_data.append(f'=SUM(B{r}:M{r})')

    elif t == 'item':
        row_data = [f'   └ {lbl}'] + [''] * 12 + [f'=SUM(B{r}:M{r})']

    elif t == 'subtotal':
        cat_rows = meta['cat_rows']
        row_data = [lbl]
        for col in COLS:
            row_data.append('+'.join([f'{col}{cr}' for cr in cat_rows]))
            row_data[-1] = f'={row_data[-1]}'
        row_data.append(f'=SUM(B{r}:M{r})')

    elif t == 'sga':
        sub_keys = meta['sub_keys']
        row_data = [lbl]
        for col in COLS:
            row_data.append(f'={"+".join([f"{col}{subtotal_rows[k]}" for k in sub_keys])}')
        row_data.append(f'=SUM(B{r}:M{r})')

    elif t == 'grand':
        row_data = [lbl]
        for col in COLS:
            row_data.append(f'={col}{subtotal_rows[meta["cogs_key"]]}+{col}{meta["sga_row"]}')
        row_data.append(f'=SUM(B{r}:M{r})')

    elif t == 'blank':
        row_data = [''] * NUM_COLS

    else:
        row_data = [''] * NUM_COLS

    all_rows.append(row_data)

# =========================================================
# コスト明細シートに書き込み
# =========================================================
print('\n[1] コスト明細データ書き込み中...')
clear_range('コスト明細!A1:N300')
values_batch([{'range': 'コスト明細!A1', 'values': all_rows}])
print('   完了')

# =========================================================
# PL_月次の参照式を更新（直接行参照）
# =========================================================
print('\n[2] PL_月次の参照式を更新中...')

# PL_月次のコスト行とカテゴリのマッピング
PL_COST_MAP = {
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

pl_vdata = []
for pl_row, cat_label in PL_COST_MAP.items():
    cost_row = category_rows.get(cat_label)
    if not cost_row:
        print(f'   WARNING: {cat_label} の行番号が見つかりません')
        continue
    for i, col in enumerate(COLS):
        pl_vdata.append({
            'range': f'PL_月次!{col}{pl_row}',
            'values': [[f'=コスト明細!{col}{cost_row}']]
        })
    pl_vdata.append({'range': f'PL_月次!N{pl_row}', 'values': [[f'=SUM(B{pl_row}:M{pl_row})']]})

values_batch(pl_vdata)
print('   完了')

# =========================================================
# 書式設定
# =========================================================
print('\n[3] 書式設定を適用中...')

# セクションのカラーテーマ
SECTION_COLORS = {
    'cogs':  {'header': '1A5276', 'total': '2471A3', 'item': 'D6EAF8', 'sub': '1A5276'},
    'hr':    {'header': '1E8449', 'total': '239B56', 'item': 'D5F5E3', 'sub': '1E8449'},
    'tools': {'header': '6E2F00', 'total': 'A04000', 'item': 'FAE5D3', 'sub': '6E2F00'},
    'mktg':  {'header': '4A235A', 'total': '7D3C98', 'item': 'E8DAEF', 'sub': '4A235A'},
    'mgmt':  {'header': '212F3D', 'total': '2C3E50', 'item': 'D5D8DC', 'sub': '212F3D'},
}

TOTAL_DATA_ROWS = cur  # 最終行+1

fmt = []

# --- 列幅 ---
fmt += [
    col_w(COST_ID, 0, 200),   # カテゴリ/内訳
]
for i in range(1, 13):
    fmt.append(col_w(COST_ID, i, 82))
fmt.append(col_w(COST_ID, 13, 95))  # 年間合計

# --- タイトル行 ---
fmt += [
    merge(COST_ID, 0, 1, 0, 14),
    cell_fmt(COST_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=11,
             halign='CENTER', valign='MIDDLE'),
    row_h(COST_ID, 0, 1, 36),
    # ヘッダー行
    cell_fmt(COST_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(COST_ID, 1, 2, 26),
    # 全体ベース（白）
    cell_fmt(COST_ID, 2, TOTAL_DATA_ROWS, 0, 14, bg='FFFFFF'),
    # 数値列（B〜N）: 通貨フォーマット・右揃え
    cell_fmt(COST_ID, 2, TOTAL_DATA_ROWS, 1, 14,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    # 年間合計列を少し目立たせる（薄グレー背景）
    cell_fmt(COST_ID, 1, TOTAL_DATA_ROWS, 13, 14, bg='ECF0F1', bold=True),
    # フリーズ（2行）
    freeze(COST_ID, rows=2, cols=0),
]

# --- 行別スタイル適用 ---
cur_section_key = None
for entry in layout:
    ri  = entry['row'] - 1   # 0-indexed
    t   = entry['type']
    meta = entry['meta']

    if t == 'section':
        cur_section_key = meta.get('key')
        c = SECTION_COLORS.get(cur_section_key, {})
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg=c.get('header','333333'), color='FFFFFF', bold=True),
            row_h(COST_ID, ri, ri+1, 24),
        ]

    elif t == 'total':
        c = SECTION_COLORS.get(cur_section_key, {})
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg=c.get('total','555555'), color='FFFFFF', bold=True),
            row_h(COST_ID, ri, ri+1, 24),
        ]

    elif t == 'item':
        c = SECTION_COLORS.get(cur_section_key, {})
        fmt += [
            # 入力セル（月列のみ水色）
            cell_fmt(COST_ID, ri, ri+1, 0, 1, bg='FDFEFE', color='555555', italic=True),
            cell_fmt(COST_ID, ri, ri+1, 1, 13, bg='EBF5FB'),  # 月列: 水色（入力エリア）
            cell_fmt(COST_ID, ri, ri+1, 13, 14, bg='ECF0F1'),  # 年間合計列
            row_h(COST_ID, ri, ri+1, 22),
        ]

    elif t == 'subtotal':
        c = SECTION_COLORS.get(cur_section_key, {})
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14,
                     bg=c.get('sub','333333'), color='FFFFFF', bold=True),
            border_bottom(COST_ID, ri, ri+1, 0, 14),
            row_h(COST_ID, ri, ri+1, 26),
        ]

    elif t == 'sga':
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14, bg='1C2833', color='FFFFFF', bold=True, fs=10),
            row_h(COST_ID, ri, ri+1, 28),
        ]

    elif t == 'grand':
        fmt += [
            cell_fmt(COST_ID, ri, ri+1, 0, 14, bg='0B0C10', color='FFFFFF', bold=True, fs=10),
            row_h(COST_ID, ri, ri+1, 30),
        ]

# --- 全体罫線 ---
fmt.append(border_all(COST_ID, 1, TOTAL_DATA_ROWS, 0, 14))

batch_update(fmt)
print('   完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
print('\n【PL_月次 参照マップ】')
for pl_row, cat in PL_COST_MAP.items():
    cost_r = category_rows.get(cat, '?')
    print(f'  PL行{pl_row} {cat} → コスト明細 行{cost_r}')
