#!/usr/bin/env python3
"""
全シートの修正:
1. 残存プルダウン（データ検証）を全削除
2. 文字色が白で見えないセルを修正（入力行は黒文字に統一）
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
    if 'nfmt' in kw: uf['numberFormat'] = kw['nfmt']; fields.append('userEnteredFormat.numberFormat')
    return {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                  'startColumnIndex': c0, 'endColumnIndex': c1},
        'cell': {'userEnteredFormat': uf}, 'fields': ','.join(fields)
    }}

def clear_validation(sid, r0=0, r1=1000, c0=0, c1=26):
    """プルダウン（データ検証）を削除"""
    return {
        'setDataValidation': {
            'range': {
                'sheetId': sid,
                'startRowIndex': r0, 'endRowIndex': r1,
                'startColumnIndex': c0, 'endColumnIndex': c1,
            }
            # rule を省略 = 検証ルール削除
        }
    }

# =========================================================
# シート情報取得
# =========================================================
info = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}', headers=h).json()
sheets = {s['properties']['title']: s['properties']['sheetId'] for s in info['sheets']}
print('シート一覧:', sheets)

PL_ID   = sheets['PL_月次']
COST_ID = sheets['コスト明細']
SALE_ID = sheets['売上明細']
CASE_ID = sheets.get('案件別P/L')

reqs = []

# =========================================================
# Step 1: 全シートのプルダウンをまとめて削除
# =========================================================
print('\n[1] 全シートのプルダウンを削除...')
for sid in [PL_ID, COST_ID, SALE_ID] + ([CASE_ID] if CASE_ID else []):
    reqs.append(clear_validation(sid))

# =========================================================
# Step 2: コスト明細 — 入力行の文字色を黒に修正
# =========================================================
print('[2] コスト明細の文字色修正...')

# 行定義（restore_cost_simple.py と同じ構造）
ROWS_DEF = [
    ('title',    'コスト入力シート（月別）　※黄色セルに数値を入力してください'),
    ('header',   ''),
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
    ('item',     'SaaSサブスク（Slack/Notion等）'),
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
    ('grand',    '★販管費合計（B+C+D+E）'),
    ('grand2',   '★コスト合計（A+販管費）'),
]

# 全行に「文字色リセット（黒）」を適用してから、種別ごとに上書き
# まず全行を黒文字にリセット
reqs.append(cell_fmt(COST_ID, 0, 40, 0, 14, color='1A1A1A'))

row_idx = 1
for type_, label in ROWS_DEF:
    ri = row_idx - 1  # 0-indexed

    if type_ == 'title':
        # タイトル: 濃紺背景+白文字（そのまま）
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14,
                             bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'))

    elif type_ == 'header':
        # ヘッダー: ネイビー背景+白文字
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14,
                             bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'))

    elif type_ == 'section':
        # セクション色マップ
        sec_bg = {
            '【A】売上原価（COGS）': '1A5276',
            '【B】人件費': '1E8449',
            '【C】ツール・インフラ費': '6E2F00',
            '【D】マーケティング・営業費': '4A235A',
            '【E】管理費': '212F3D',
        }.get(label, '333333')
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14,
                             bg=sec_bg, color='FFFFFF', bold=True))

    elif type_ == 'item':
        # 入力行: A列はグレー文字、月列（B〜M）は黄色背景＋黒文字
        reqs += [
            cell_fmt(COST_ID, ri, ri+1, 0, 1,
                     bg='FAFAFA', color='444444', bold=False),
            cell_fmt(COST_ID, ri, ri+1, 1, 13,
                     bg='FFFDE7', color='1A1A1A', bold=False,
                     nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}),
            cell_fmt(COST_ID, ri, ri+1, 13, 14,
                     bg='ECF0F1', color='1A1A1A', bold=True,
                     nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}),
        ]

    elif type_ == 'subtotal':
        sub_bg = {
            '売上原価合計': '2471A3',
            '人件費合計':   '239B56',
            'ツール合計':   'A04000',
            'マーケ合計':   '7D3C98',
            '管理費合計':   '2C3E50',
        }.get(label, '555555')
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14,
                             bg=sub_bg, color='FFFFFF', bold=True,
                             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}))

    elif type_ in ('grand', 'grand2'):
        bg = '1C2833' if type_ == 'grand' else '0B0C10'
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14,
                             bg=bg, color='FFFFFF', bold=True, fs=10,
                             nfmt={'type': 'NUMBER', 'pattern': '¥#,##0'}))

    elif type_ == 'blank':
        reqs.append(cell_fmt(COST_ID, ri, ri+1, 0, 14, bg='FFFFFF', color='1A1A1A'))

    row_idx += 1

# =========================================================
# Step 3: 売上明細 — 文字色を黒に統一
# =========================================================
print('[3] 売上明細の文字色修正...')
reqs += [
    # 全体リセット（黒文字）
    cell_fmt(SALE_ID, 0, 30, 0, 7, color='1A1A1A'),
    # タイトル行: 白文字は維持
    cell_fmt(SALE_ID, 0, 1, 0, 7, bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'),
    # ヘッダー行: 白文字維持
    cell_fmt(SALE_ID, 1, 2, 0, 7, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    # データ行（実績）: 黒文字
    cell_fmt(SALE_ID, 2, 12, 0, 7, color='1A1A1A'),
    # 見込み行: 少し薄い色
    cell_fmt(SALE_ID, 11, 17, 0, 7, bg='FFF9C4', color='555555', italic=True),
    # サービス別集計ヘッダー
    cell_fmt(SALE_ID, 17, 18, 0, 2, bg='2E5090', color='FFFFFF', bold=True),
    # 集計値: 黒文字
    cell_fmt(SALE_ID, 18, 24, 0, 2, color='1A1A1A'),
]

# =========================================================
# Step 4: 案件別P/L — 文字色を黒に統一
# =========================================================
if CASE_ID:
    print('[4] 案件別P/Lの文字色修正...')
    reqs += [
        cell_fmt(CASE_ID, 0, 15, 0, 5, color='1A1A1A'),
        # タイトル・ヘッダーは白文字維持
        cell_fmt(CASE_ID, 0, 1, 0, 5, bg='1F3864', color='FFFFFF', bold=True, fs=11, halign='CENTER'),
        cell_fmt(CASE_ID, 1, 2, 0, 5, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
        # データ行: 黒文字
        cell_fmt(CASE_ID, 2, 10, 0, 5, color='1A1A1A'),
        # 合計行: 白文字維持
        cell_fmt(CASE_ID, 8, 9, 0, 5, bg='1A252F', color='FFFFFF', bold=True),
    ]

# =========================================================
# Step 5: PL_月次 — 文字色確認・修正
# =========================================================
print('[5] PL_月次の文字色修正...')
reqs += [
    # 全体リセット（黒文字）
    cell_fmt(PL_ID, 0, 35, 0, 14, color='1A1A1A'),
    # タイトル: 白文字維持
    cell_fmt(PL_ID, 0, 1, 0, 14, bg='1F3864', color='FFFFFF', bold=True, fs=12, halign='CENTER'),
    # ヘッダー行: 白文字維持
    cell_fmt(PL_ID, 1, 2, 0, 14, bg='2E5090', color='FFFFFF', bold=True, halign='CENTER'),
    # 実績/見込行: 文字色
    cell_fmt(PL_ID, 2, 3, 0, 14, color='666666', italic=True, halign='CENTER'),
    # 売上行: 黒文字
    cell_fmt(PL_ID, 3, 10, 0, 14, color='1A1A1A'),
    # 売上合計: 白文字
    cell_fmt(PL_ID, 8, 9, 0, 14, bg='1A5276', color='FFFFFF', bold=True),
    # 売上原価: 黒文字
    cell_fmt(PL_ID, 10, 17, 0, 14, color='1A1A1A'),
    # 粗利行: 白文字
    cell_fmt(PL_ID, 16, 17, 0, 14, bg='1E8449', color='FFFFFF', bold=True),
    cell_fmt(PL_ID, 17, 18, 0, 14, color='1A1A1A'),
    # 販管費: 黒文字
    cell_fmt(PL_ID, 19, 29, 0, 14, color='1A1A1A'),
    # 販管費合計: 白文字
    cell_fmt(PL_ID, 27, 28, 0, 14, bg='7D3C98', color='FFFFFF', bold=True),
    # 営業利益: 白文字
    cell_fmt(PL_ID, 29, 30, 0, 14, bg='212F3D', color='FFFFFF', bold=True, fs=11),
    cell_fmt(PL_ID, 30, 31, 0, 14, color='1A1A1A'),
]

# =========================================================
# 一括適用
# =========================================================
print('\n書式を一括適用中...')
# リクエストが多い場合は分割して送る
CHUNK = 50
for i in range(0, len(reqs), CHUNK):
    chunk = reqs[i:i+CHUNK]
    batch_update(chunk)
    print(f'   {i+len(chunk)}/{len(reqs)} 完了')

print(f'\n✓ 完了: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit')
