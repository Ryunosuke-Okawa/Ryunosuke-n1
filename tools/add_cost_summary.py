#!/usr/bin/env python3
"""
コスト一覧シートを追加
カテゴリ×月のマトリクス集計表（コスト明細からSUMIFSで自動集計）
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
    uf, fields = {}, []
    if 'bg' in kw:
        uf['backgroundColor'] = rgb(kw['bg'])
        fields.append('userEnteredFormat.backgroundColor')
    tf = {}
    if 'bold' in kw: tf['bold'] = kw['bold']
    if 'italic' in kw: tf['italic'] = kw['italic']
    if 'color' in kw: tf['foregroundColor'] = rgb(kw['color'])
    if 'fs' in kw: tf['fontSize'] = kw['fs']
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

def thick_border_bottom(sid, r0, r1, c0, c1):
    b = {'style': 'SOLID_MEDIUM', 'color': rgb('888888')}
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

# コスト一覧シートを追加（なければ）
if 'コスト一覧' not in sheets:
    # PL_月次(0), 売上明細(1), コスト明細(2), 案件別P/L(3) の後ろに追加
    result = batch_update([{'addSheet': {'properties': {'title': 'コスト一覧', 'index': 3}}}])
    SUM_ID = result['replies'][0]['addSheet']['properties']['sheetId']
    print(f'コスト一覧作成: sheetId={SUM_ID}')
else:
    SUM_ID = sheets['コスト一覧']
    print(f'コスト一覧既存: sheetId={SUM_ID}')

# =========================================================
# データ書き込み
# =========================================================
clear('コスト一覧!A1:O50')

months = ['25年10月','25年11月','25年12月','26年1月','26年2月','26年3月',
          '26年4月','26年5月','26年6月','26年7月','26年8月','26年9月']
cols_letters = ['B','C','D','E','F','G','H','I','J','K','L','M']

# セクション定義: (表示名, カテゴリキー, セクション種別)
sections = [
    # セクションヘッダー
    ('【A】売上原価（COGS）', None, 'header_a'),
    ('研修講師費',      '研修講師費',      'item'),
    ('外注開発費',      '外注開発費',      'item'),
    ('コーチ人件費',    'コーチ人件費',    'item'),
    ('売上原価合計',    None,              'subtotal_a'),
    # 空行
    (None, None, 'blank'),
    # セクションヘッダー
    ('【B】人件費',     None,              'header_b'),
    ('人件費（給与）',  '人件費（給与）',  'item'),
    ('業務委託費',      '業務委託費',      'item'),
    ('人件費合計',      None,              'subtotal_b'),
    (None, None, 'blank'),
    ('【C】ツール・インフラ費', None,      'header_c'),
    ('ツール・インフラ費','ツール・インフラ費','item'),
    ('ツール合計',      None,              'subtotal_c'),
    (None, None, 'blank'),
    ('【D】マーケティング・営業費', None,  'header_d'),
    ('マーケティング費','マーケティング費','item'),
    ('交通費・出張費',  '交通費・出張費',  'item'),
    ('接待交際費',      '接待交際費',      'item'),
    ('マーケ合計',      None,              'subtotal_d'),
    (None, None, 'blank'),
    ('【E】管理費',     None,              'header_e'),
    ('その他管理費',    'その他管理費',    'item'),
    ('管理費合計',      None,              'subtotal_e'),
    (None, None, 'blank'),
    ('★販管費合計（B+C+D+E）', None,     'total_sga'),
    ('★コスト合計（A+販管費）', None,    'grand_total'),
]

# 行番号を確定させる（1-indexed）
row_map = {}  # キー → 行番号(1-indexed)
rows_data = []
current_row = 3  # 1行目タイトル、2行目ヘッダー

# 各セクションの行番号を記録
subtotal_a_row = None
item_a_rows = []
subtotal_b_row = None; item_b_rows = []
subtotal_c_row = None; item_c_rows = []
subtotal_d_row = None; item_d_rows = []
subtotal_e_row = None; item_e_rows = []
total_sga_row = None
grand_total_row = None

for label, key, kind in sections:
    if kind == 'blank':
        current_row += 1
        continue
    r = current_row
    if kind == 'item' and key:
        if key in ['研修講師費','外注開発費','コーチ人件費']:
            item_a_rows.append(r)
        elif key in ['人件費（給与）','業務委託費']:
            item_b_rows.append(r)
        elif key == 'ツール・インフラ費':
            item_c_rows.append(r)
        elif key in ['マーケティング費','交通費・出張費','接待交際費']:
            item_d_rows.append(r)
        elif key == 'その他管理費':
            item_e_rows.append(r)
    elif kind == 'subtotal_a': subtotal_a_row = r
    elif kind == 'subtotal_b': subtotal_b_row = r
    elif kind == 'subtotal_c': subtotal_c_row = r
    elif kind == 'subtotal_d': subtotal_d_row = r
    elif kind == 'subtotal_e': subtotal_e_row = r
    elif kind == 'total_sga':  total_sga_row = r
    elif kind == 'grand_total': grand_total_row = r
    row_map[label] = r
    current_row += 1

# データ行を構築
def sumifs_formula(cat, col):
    return f'=IFERROR(SUMIFS(コスト明細!$G$3:$G$1000,コスト明細!$B$3:$B$1000,{col}$2,コスト明細!$E$3:$E$1000,"{cat}"),0)'

def sum_rows_formula(row_list, col):
    refs = '+'.join([f'{col}{r}' for r in row_list])
    return f'={refs}'

# ヘッダー行（1行目: タイトル）
title_row = ['コスト一覧（月別サマリー）'] + [''] * 13
header_row = ['コストカテゴリ'] + months + ['年間合計']

# 全データ行を組み立て
all_rows = [title_row, header_row]

for label, key, kind in sections:
    if kind == 'blank':
        all_rows.append([''] * 14)
        continue

    row = [label if label else '']
    if kind in ('header_a','header_b','header_c','header_d','header_e'):
        row += [''] * 13

    elif kind == 'item' and key:
        for col in cols_letters:
            row.append(sumifs_formula(key, col))
        row.append(f'=SUM(B{row_map[label]}:M{row_map[label]})')

    elif kind == 'subtotal_a':
        items = item_a_rows
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in items])}')
        row.append(f'=SUM(B{subtotal_a_row}:M{subtotal_a_row})')

    elif kind == 'subtotal_b':
        items = item_b_rows
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in items])}')
        row.append(f'=SUM(B{subtotal_b_row}:M{subtotal_b_row})')

    elif kind == 'subtotal_c':
        items = item_c_rows
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in items])}')
        row.append(f'=SUM(B{subtotal_c_row}:M{subtotal_c_row})')

    elif kind == 'subtotal_d':
        items = item_d_rows
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in items])}')
        row.append(f'=SUM(B{subtotal_d_row}:M{subtotal_d_row})')

    elif kind == 'subtotal_e':
        items = item_e_rows
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in items])}')
        row.append(f'=SUM(B{subtotal_e_row}:M{subtotal_e_row})')

    elif kind == 'total_sga':
        subs = [subtotal_b_row, subtotal_c_row, subtotal_d_row, subtotal_e_row]
        for col in cols_letters:
            row.append(f'={"+".join([f"{col}{r}" for r in subs])}')
        row.append(f'=SUM(B{total_sga_row}:M{total_sga_row})')

    elif kind == 'grand_total':
        for col in cols_letters:
            row.append(f'={col}{subtotal_a_row}+{col}{total_sga_row}')
        row.append(f'=SUM(B{grand_total_row}:M{grand_total_row})')

    all_rows.append(row)

values_batch([{'range': 'コスト一覧!A1', 'values': all_rows}])
print('コスト一覧データ書き込み完了')
print(f'  小計行: A={subtotal_a_row}, B={subtotal_b_row}, C={subtotal_c_row}, D={subtotal_d_row}, E={subtotal_e_row}')
print(f'  販管費合計: {total_sga_row}, コスト合計: {grand_total_row}')

# =========================================================
# 書式設定
# =========================================================
print('書式設定を適用中...')
fmt = []

TOTAL_ROWS = grand_total_row + 1  # データの最終行+1

# タイトル行
fmt += [
    merge(SUM_ID, 0, 1, 0, 14),
    cell_fmt(SUM_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=12,
             halign='CENTER', valign='MIDDLE'),
    row_h(SUM_ID, 0, 1, 38),
    # ヘッダー行（月名）
    cell_fmt(SUM_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    row_h(SUM_ID, 1, 2, 26),
    # 全体白ベース
    cell_fmt(SUM_ID, 2, TOTAL_ROWS, 0, 14, bg='FFFFFF'),
    # 金額列（B〜N）: 数値フォーマット・右揃え
    cell_fmt(SUM_ID, 2, TOTAL_ROWS, 1, 14,
             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}, halign='RIGHT'),
    # A列（ラベル）左揃え
    cell_fmt(SUM_ID, 2, TOTAL_ROWS, 0, 1, halign='LEFT'),
    # 列幅
    col_w(SUM_ID, 0, 200),  # カテゴリ名
]
for i in range(1, 13):
    fmt.append(col_w(SUM_ID, i, 85))
fmt.append(col_w(SUM_ID, 13, 95))  # 年間合計

# セクションヘッダー行の色分け
section_header_style = {
    'header_a': ('1A5276', 'FFFFFF'),  # 売上原価: ダークブルー
    'header_b': ('1E8449', 'FFFFFF'),  # 人件費: ダークグリーン
    'header_c': ('784212', 'FFFFFF'),  # ツール: ダークブラウン
    'header_d': ('6C3483', 'FFFFFF'),  # マーケ: ダークパープル
    'header_e': ('1A252F', 'FFFFFF'),  # 管理費: ダークチャコール
}
item_style = {
    'header_a': ('D6EAF8', '1B4F72'),  # 売上原価: 薄青
    'header_b': ('D5F5E3', '145A32'),  # 人件費: 薄グリーン
    'header_c': ('FAD7A0', '784212'),  # ツール: 薄オレンジ
    'header_d': ('E8DAEF', '4A235A'),  # マーケ: 薄パープル
    'header_e': ('D5D8DC', '1C2833'),  # 管理費: 薄グレー
}
subtotal_style = {
    'subtotal_a': ('2471A3', 'FFFFFF'),
    'subtotal_b': ('239B56', 'FFFFFF'),
    'subtotal_c': ('A04000', 'FFFFFF'),
    'subtotal_d': ('7D3C98', 'FFFFFF'),
    'subtotal_e': ('2C3E50', 'FFFFFF'),
}

current_section = None
row_index = 2  # 0-indexed（all_rowsの0=title, 1=header, 2以降=data）
for label, key, kind in sections:
    ri = row_index
    if kind == 'blank':
        row_index += 1
        continue
    if kind in section_header_style:
        current_section = kind
        bg, fg = section_header_style[kind]
        fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 14, bg=bg, color=fg, bold=True))
        fmt.append(row_h(SUM_ID, ri, ri+1, 24))
    elif kind == 'item':
        # 現在のセクションの色を適用
        sec_key = current_section
        if sec_key and sec_key in item_style:
            bg, fg = item_style[sec_key]
            # 偶数項目は少し薄くする
            fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 14, bg=bg, color=fg))
        fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 1,
                            bold=False, halign='LEFT'))
        fmt.append(row_h(SUM_ID, ri, ri+1, 22))
    elif kind in subtotal_style:
        bg, fg = subtotal_style[kind]
        fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 14, bg=bg, color=fg, bold=True))
        fmt.append(thick_border_bottom(SUM_ID, ri-1, ri+1, 0, 14))
        fmt.append(row_h(SUM_ID, ri, ri+1, 24))
    elif kind == 'total_sga':
        fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 14, bg='1C2833', color='FFFFFF', bold=True, fs=11))
        fmt.append(row_h(SUM_ID, ri, ri+1, 28))
    elif kind == 'grand_total':
        fmt.append(cell_fmt(SUM_ID, ri, ri+1, 0, 14, bg='0B0B0B', color='FFFFFF', bold=True, fs=11))
        fmt.append(row_h(SUM_ID, ri, ri+1, 30))

    row_index += 1

# 年間合計列（N列）を少し目立たせる
fmt += [
    cell_fmt(SUM_ID, 1, TOTAL_ROWS, 13, 14, bg='17202A', color='FFFFFF', bold=True),
    # 罫線（データ全体）
    border(SUM_ID, 1, TOTAL_ROWS, 0, 14),
    # フリーズ（上2行）
    freeze(SUM_ID, rows=2, cols=0),
]

batch_update(fmt)
print('書式設定完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
