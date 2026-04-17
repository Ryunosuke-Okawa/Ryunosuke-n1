"""フローチャートをクリーンアップ：不要枠線削除、色統一、視認性向上"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1mTOjgxfJV-zruETo7Yl04NP1SvzYTN5CXdAIiay_zm4"
SHEET_ID = 1271589038

with open("/Users/kyouyuu/.google-mcp/tokens/main.json") as f:
    token_data = json.load(f)
with open("/Users/kyouyuu/.google-mcp/credentials.json") as f:
    cred_data = json.load(f)["installed"]

creds = Credentials(
    token=None,
    refresh_token=token_data["refresh_token"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=token_data.get("client_id") or cred_data["client_id"],
    client_secret=token_data.get("client_secret") or cred_data["client_secret"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
service = build("sheets", "v4", credentials=creds)

# --- Step 1: 全体リセット（Row 1-20） ---
def cr(r1, r2, c1, c2):
    return {"sheetId": SHEET_ID, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}

W = {"red": 1, "green": 1, "blue": 1}
NONE_BORDER = {"style": "NONE", "width": 0}

reset_reqs = [
    # アンマージ
    {"unmergeCells": {"range": cr(0, 20, 0, 14)}},
    # 背景白・テキストリセット
    {"repeatCell": {
        "range": cr(0, 20, 0, 14),
        "cell": {"userEnteredFormat": {
            "backgroundColor": W,
            "textFormat": {"bold": False, "fontSize": 10, "fontFamily": "Noto Sans JP",
                           "foregroundColor": {"red": 0, "green": 0, "blue": 0}},
            "horizontalAlignment": "LEFT",
            "verticalAlignment": "MIDDLE",
            "wrapStrategy": "CLIP",
        }},
        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
    }},
    # 全枠線削除
    {"updateBorders": {"range": cr(0, 20, 0, 14),
                       "top": NONE_BORDER, "bottom": NONE_BORDER,
                       "left": NONE_BORDER, "right": NONE_BORDER,
                       "innerHorizontal": NONE_BORDER, "innerVertical": NONE_BORDER}},
]
service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={"requests": reset_reqs}).execute()

# クリア
service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID, range="Kawaru KPI試算!A1:N20"
).execute()
print("Reset complete")

# --- Step 2: コンテンツ書き込み ---
# 横フロー: 流入元 → LINE登録 → LP → 登録
# 列: A=流入元  B=→  C=ステップ2  D=→  E=ステップ3  F=→  G=ステップ4  H=→  I=ステップ5
data = [
    # Row 1: タイトル
    ["■ ファネル全体図"],
    # Row 2: blank
    [""],
    # Row 3: 導線A ラベル
    ["導線A：SNS経由"],
    # Row 4: YouTube
    ["YouTube", "→", "LINE登録", "→", "LP送付", "→", "Kawaru LP", "→", "登録"],
    # Row 5: Instagram
    ["Instagram", "→", "", "", "", "", "", "", ""],
    # Row 6: X
    ["X", "→", "", "", "", "", "", "", ""],
    # Row 7: blank
    [""],
    # Row 8: 導線B ラベル
    ["導線B：セミナー経由"],
    # Row 9: セミナー ルート1（LP直接）
    ["セミナー", "→", "LP直接訴求", "─", "─", "→", "Kawaru LP", "→", "登録"],
    # Row 10: セミナー ルート2（LINE経由）
    ["", "→", "LINE登録", "→", "LP送付", "→", "", "", ""],
    # Row 11: blank
    [""],
    # Row 12: 注記
    ["", "", "", "", "", "", "登録時 utm_source で媒体別に計測"],
    # Row 13-20: blank
    [""], [""], [""], [""], [""], [""], [""],
]

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range="Kawaru KPI試算!A1:I20",
    valueInputOption="USER_ENTERED",
    body={"values": data},
).execute()
print("Content written")

# --- Step 3: フォーマット ---
def bg(rng, color, bold=False, fg=None, size=None, halign=None, valign=None):
    fmt = {"backgroundColor": color}
    txt = {}
    if bold: txt["bold"] = True
    if fg: txt["foregroundColor"] = fg
    if size: txt["fontSize"] = size
    if txt: fmt["textFormat"] = txt
    if halign: fmt["horizontalAlignment"] = halign
    if valign: fmt["verticalAlignment"] = valign
    parts = ["backgroundColor"]
    if txt: parts.append("textFormat")
    if halign: parts.append("horizontalAlignment")
    if valign: parts.append("verticalAlignment")
    return {"repeatCell": {"range": rng, "cell": {"userEnteredFormat": fmt},
                           "fields": f"userEnteredFormat({','.join(parts)})"}}

def border_outer(rng, color):
    b = {"style": "SOLID_MEDIUM", "width": 2, "color": color}
    return {"updateBorders": {"range": rng, "top": b, "bottom": b, "left": b, "right": b}}

def col_w(c, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": c, "endIndex": c+1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

def row_h(r, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": r, "endIndex": r+1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

# === カラーパレット（役割ごとに統一） ===
TITLE_BG = {"red": 0.15, "green": 0.15, "blue": 0.15}
SECTION_SNS = {"red": 0.22, "green": 0.46, "blue": 0.78}
SECTION_SEM = {"red": 0.85, "green": 0.52, "blue": 0.15}

# 流入元
C_YT = {"red": 0.92, "green": 0.26, "blue": 0.21}
C_IG = {"red": 0.76, "green": 0.18, "blue": 0.56}
C_X = {"red": 0.12, "green": 0.12, "blue": 0.12}
C_SEM = {"red": 0.85, "green": 0.52, "blue": 0.15}

# ファネルステップ（同じ役割＝同じ色）
C_LINE = {"red": 0.0, "green": 0.72, "blue": 0.35}       # LINE登録 = 緑
C_LP_SEND = {"red": 0.25, "green": 0.52, "blue": 0.85}    # LP送付 = 青
C_LP_DIRECT = {"red": 0.25, "green": 0.52, "blue": 0.85}  # LP直接訴求 = 同じ青
C_KAWARU = {"red": 0.12, "green": 0.33, "blue": 0.65}     # Kawaru LP = 濃い青
C_REG = {"red": 0.13, "green": 0.59, "blue": 0.33}        # 登録 = 濃い緑
C_NOTE = {"red": 0.97, "green": 0.95, "blue": 0.85}       # 注記 = 薄黄

ARROW_FG = {"red": 0.65, "green": 0.65, "blue": 0.65}
WH = {"red": 1, "green": 1, "blue": 1}

reqs = []

# 列幅
reqs.append(col_w(0, 130))  # A: 流入元
reqs.append(col_w(1, 30))   # B: →
reqs.append(col_w(2, 130))  # C: LINE/LP直接
reqs.append(col_w(3, 30))   # D: →
reqs.append(col_w(4, 130))  # E: LP送付
reqs.append(col_w(5, 30))   # F: →
reqs.append(col_w(6, 150))  # G: Kawaru LP
reqs.append(col_w(7, 30))   # H: →
reqs.append(col_w(8, 150))  # I: 登録

# 行高
reqs.append(row_h(0, 32))   # タイトル
reqs.append(row_h(1, 6))    # blank
reqs.append(row_h(2, 24))   # 導線Aラベル
reqs.append(row_h(3, 38))   # YouTube
reqs.append(row_h(4, 38))   # Instagram
reqs.append(row_h(5, 38))   # X
reqs.append(row_h(6, 10))   # blank
reqs.append(row_h(7, 24))   # 導線Bラベル
reqs.append(row_h(8, 38))   # セミナールート1
reqs.append(row_h(9, 38))   # セミナールート2
reqs.append(row_h(10, 8))   # blank
reqs.append(row_h(11, 22))  # 注記
for r in range(12, 20):
    reqs.append(row_h(r, 4))

# === タイトル ===
reqs.append(bg(cr(0, 1, 0, 9), TITLE_BG, bold=True, fg=WH, size=12))

# === 導線A ラベル ===
reqs.append(bg(cr(2, 3, 0, 9), SECTION_SNS, bold=True, fg=WH, size=10))

# === 導線B ラベル ===
reqs.append(bg(cr(7, 8, 0, 9), SECTION_SEM, bold=True, fg=WH, size=10))

# === 流入元ボックス ===
for r, color in [(3, C_YT), (4, C_IG), (5, C_X)]:
    reqs.append(bg(cr(r, r+1, 0, 1), color, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
    reqs.append(border_outer(cr(r, r+1, 0, 1), color))

# セミナーボックス（2行結合）
reqs.append(bg(cr(8, 10, 0, 1), C_SEM, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 0, 1), C_SEM))
reqs.append({"mergeCells": {"range": cr(8, 10, 0, 1), "mergeType": "MERGE_ALL"}})

# === 矢印列（B, D, F, H）===
for r in [3, 4, 5, 8, 9]:
    for c in [1, 3, 5, 7]:
        reqs.append(bg(cr(r, r+1, c, c+1), W, bold=True, fg=ARROW_FG, size=14, halign="CENTER", valign="MIDDLE"))

# === LINE登録ボックス（C列）=== 同じ緑
# SNS側（Row 4, 3行結合）
reqs.append(bg(cr(3, 6, 2, 3), C_LINE, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 2, 3), C_LINE))
reqs.append({"mergeCells": {"range": cr(3, 6, 2, 3), "mergeType": "MERGE_ALL"}})

# セミナー側 ルート2（Row 10）
reqs.append(bg(cr(9, 10, 2, 3), C_LINE, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(9, 10, 2, 3), C_LINE))

# === LP訴求ボックス（C列 Row 9）=== LP系は同じ青
reqs.append(bg(cr(8, 9, 2, 3), C_LP_DIRECT, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 9, 2, 3), C_LP_DIRECT))

# === LP送付ボックス（E列）=== 同じ青
# SNS側（Row 4, 3行結合）
reqs.append(bg(cr(3, 6, 4, 5), C_LP_SEND, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 4, 5), C_LP_SEND))
reqs.append({"mergeCells": {"range": cr(3, 6, 4, 5), "mergeType": "MERGE_ALL"}})

# セミナー側 ルート2（Row 10）
reqs.append(bg(cr(9, 10, 4, 5), C_LP_SEND, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(9, 10, 4, 5), C_LP_SEND))

# セミナールート1 の ─ ─（Row 9, D-E列）= 点線表現
reqs.append(bg(cr(8, 9, 3, 6), W, bold=True, fg=ARROW_FG, size=14, halign="CENTER"))

# === Kawaru LP ボックス（G列）=== 濃い青
# SNS側（Row 4, 3行結合）
reqs.append(bg(cr(3, 6, 6, 7), C_KAWARU, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 6, 7), C_KAWARU))
reqs.append({"mergeCells": {"range": cr(3, 6, 6, 7), "mergeType": "MERGE_ALL"}})

# セミナー側（Row 9, 2行結合）
reqs.append(bg(cr(8, 10, 6, 7), C_KAWARU, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 6, 7), C_KAWARU))
reqs.append({"mergeCells": {"range": cr(8, 10, 6, 7), "mergeType": "MERGE_ALL"}})

# === 登録ボックス（I列）=== 濃い緑
# SNS側（Row 4, 3行結合）
reqs.append(bg(cr(3, 6, 8, 9), C_REG, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 8, 9), C_REG))
reqs.append({"mergeCells": {"range": cr(3, 6, 8, 9), "mergeType": "MERGE_ALL"}})

# セミナー側（Row 9, 2行結合）
reqs.append(bg(cr(8, 10, 8, 9), C_REG, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 8, 9), C_REG))
reqs.append({"mergeCells": {"range": cr(8, 10, 8, 9), "mergeType": "MERGE_ALL"}})

# === 注記 ===
reqs.append(bg(cr(11, 12, 6, 9), C_NOTE, size=9, halign="CENTER", valign="MIDDLE"))
reqs.append({"mergeCells": {"range": cr(11, 12, 6, 9), "mergeType": "MERGE_ALL"}})

# フォント統一
reqs.append({"repeatCell": {
    "range": cr(0, 20, 0, 14),
    "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Noto Sans JP"}}},
    "fields": "userEnteredFormat.textFormat.fontFamily"
}})

body = {"requests": reqs}
resp = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
print(f"Done: {len(resp.get('replies', []))} updates")
