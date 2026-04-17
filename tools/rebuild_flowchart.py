"""KPI試算シート上部のフローチャートを横フロー形式に作り直す"""
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

# --- Step 1: 既存のフローチャート行(1-20)をクリア＆アンマージ ---
# まずマージ解除
unmerge_req = {"requests": [{"unmergeCells": {"range": {
    "sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 20,
    "startColumnIndex": 0, "endColumnIndex": 14
}}}]}
service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=unmerge_req).execute()

# クリア
service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID, range="Kawaru KPI試算!A1:N20"
).execute()

# 背景を白にリセット
WHITE = {"red": 1, "green": 1, "blue": 1}
reset_req = {"requests": [{"repeatCell": {
    "range": {"sheetId": SHEET_ID, "startRowIndex": 0, "endRowIndex": 20,
              "startColumnIndex": 0, "endColumnIndex": 14},
    "cell": {"userEnteredFormat": {
        "backgroundColor": WHITE,
        "textFormat": {"bold": False, "fontSize": 10,
                       "foregroundColor": {"red": 0, "green": 0, "blue": 0}},
        "horizontalAlignment": "LEFT"
    }},
    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
}}]}
service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=reset_req).execute()
print("Cleared old flowchart")

# --- Step 2: 横フロー形式で書き込み ---
# レイアウト（左→右に流れる）
# 列: A=流入元, B=矢印, C=LINE登録, D=矢印, E=LP, F=矢印, G=登録
#
# 導線A（SNS）: Row 3-7
#   YouTube  → LINE登録 → LP送付 → Kawaru LP → 登録
#   Instagram →    ↑         ↑
#   X        →    ↑         ↑
#
# 導線B（セミナー）: Row 9-11
#   セミナー → LP直接訴求  ───────→ Kawaru LP → 登録
#            → LINE登録訴求 → LP送付 → ↑

data = [
    # Row 1: タイトル
    ["■ ファネル全体図", "", "", "", "", "", "", "", "", ""],
    # Row 2: blank
    [""],
    # Row 3: 導線A ヘッダー
    ["導線A：SNS経由", "", "", "", "", "", "", "", "", ""],
    # Row 4: blank
    [""],
    # Row 5: YouTube行
    ["YouTube", "→", "LINE登録", "→", "LP送付", "→", "Kawaru LP", "→", "登録", ""],
    # Row 6: Instagram行
    ["Instagram", "→", "（Lステップ", "", "（utm_source", "", "", "", "（カード登録", ""],
    # Row 7: X行
    ["X", "→", "  タグ付与）", "", "  別URL）", "", "", "", "＝アカウント付与）", ""],
    # Row 8: blank
    [""],
    # Row 9: 導線B ヘッダー
    ["導線B：セミナー経由", "", "", "", "", "", "", "", "", ""],
    # Row 10: blank
    [""],
    # Row 11: セミナー ルート1
    ["セミナー", "→", "LP直接訴求", "→", "", "", "Kawaru LP", "→", "登録", ""],
    # Row 12: セミナー ルート2
    ["", "→", "LINE登録訴求", "→", "LP送付", "→", "↑", "", "", ""],
    # Row 13: blank
    [""],
    # Row 14: 計測注釈
    ["", "", "", "", "", "", "utm_sourceで媒体別の登録数を計測", "", "", ""],
    # Row 15-20: blank
    [""], [""], [""], [""], [""], [""],
]

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range="Kawaru KPI試算!A1:J20",
    valueInputOption="USER_ENTERED",
    body={"values": data},
).execute()
print("Flowchart content written")

# --- Step 3: フォーマット ---
def cr(r1, r2, c1, c2):
    return {"sheetId": SHEET_ID, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}

def bg(rng, color, bold=False, fg=None, size=None, halign=None):
    fmt = {"backgroundColor": color}
    txt = {}
    if bold: txt["bold"] = True
    if fg: txt["foregroundColor"] = fg
    if size: txt["fontSize"] = size
    if txt: fmt["textFormat"] = txt
    if halign: fmt["horizontalAlignment"] = halign
    parts = ["backgroundColor"]
    if txt: parts.append("textFormat")
    if halign: parts.append("horizontalAlignment")
    return {"repeatCell": {"range": rng, "cell": {"userEnteredFormat": fmt},
                           "fields": f"userEnteredFormat({','.join(parts)})"}}

def border(rng, style="SOLID", color=None):
    if not color:
        color = {"red": 0.5, "green": 0.5, "blue": 0.5}
    b = {"style": style, "width": 1, "color": color}
    return {"updateBorders": {"range": rng, "top": b, "bottom": b, "left": b, "right": b}}

def col_w(c, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": c, "endIndex": c+1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

def row_h(r1, r2, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": r1, "endIndex": r2},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

# Colors
DARK = {"red": 0.2, "green": 0.2, "blue": 0.2}
W = {"red": 1, "green": 1, "blue": 1}
YT_RED = {"red": 0.92, "green": 0.27, "blue": 0.27}
IG_PURPLE = {"red": 0.76, "green": 0.22, "blue": 0.63}
X_BLACK = {"red": 0.15, "green": 0.15, "blue": 0.15}
LINE_GREEN = {"red": 0.35, "green": 0.75, "blue": 0.35}
LP_BLUE = {"red": 0.25, "green": 0.52, "blue": 0.85}
REG_GREEN = {"red": 0.18, "green": 0.62, "blue": 0.35}
SEM_ORANGE = {"red": 0.91, "green": 0.58, "blue": 0.15}
ARROW_GRAY = {"red": 0.75, "green": 0.75, "blue": 0.75}
LIGHT_GRAY = {"red": 0.95, "green": 0.95, "blue": 0.95}
NOTE_YELLOW = {"red": 1, "green": 0.97, "blue": 0.88}

reqs = []

# 列幅
reqs.append(col_w(0, 150))  # A: 流入元
reqs.append(col_w(1, 40))   # B: 矢印
reqs.append(col_w(2, 150))  # C: LINE/LP直接
reqs.append(col_w(3, 40))   # D: 矢印
reqs.append(col_w(4, 150))  # E: LP送付
reqs.append(col_w(5, 40))   # F: 矢印
reqs.append(col_w(6, 180))  # G: Kawaru LP
reqs.append(col_w(7, 40))   # H: 矢印
reqs.append(col_w(8, 180))  # I: 登録
reqs.append(col_w(9, 20))   # J: spacer

# 行高
reqs.append(row_h(0, 1, 32))   # タイトル
reqs.append(row_h(1, 2, 10))   # blank
reqs.append(row_h(2, 3, 28))   # 導線Aヘッダー
reqs.append(row_h(3, 4, 8))    # blank
reqs.append(row_h(4, 5, 36))   # YouTube
reqs.append(row_h(5, 6, 24))   # Instagram
reqs.append(row_h(6, 7, 24))   # X
reqs.append(row_h(7, 8, 12))   # blank
reqs.append(row_h(8, 9, 28))   # 導線Bヘッダー
reqs.append(row_h(9, 10, 8))   # blank
reqs.append(row_h(10, 11, 36)) # セミナールート1
reqs.append(row_h(11, 12, 36)) # セミナールート2
reqs.append(row_h(12, 13, 8))  # blank
reqs.append(row_h(13, 14, 24)) # 注釈
reqs.append(row_h(14, 20, 6))  # blank rows

# === Row 1: タイトル ===
reqs.append(bg(cr(0, 1, 0, 10), DARK, bold=True, fg=W, size=12))

# === Row 3: 導線Aヘッダー ===
reqs.append(bg(cr(2, 3, 0, 10), {"red": 0.22, "green": 0.46, "blue": 0.78}, bold=True, fg=W, size=10))

# === Row 5: YouTube ===
reqs.append(bg(cr(4, 5, 0, 1), YT_RED, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(4, 5, 0, 1)))
# === Row 6: Instagram ===
reqs.append(bg(cr(5, 6, 0, 1), IG_PURPLE, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(5, 6, 0, 1)))
# === Row 7: X ===
reqs.append(bg(cr(6, 7, 0, 1), X_BLACK, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(6, 7, 0, 1)))

# 矢印列（B, D, F, H）をセンター＋グレーテキスト
for r in [4, 5, 6, 10, 11]:
    for c in [1, 3, 5, 7]:
        reqs.append(bg(cr(r, r+1, c, c+1), W, bold=True, fg=ARROW_GRAY, halign="CENTER"))

# === LINE登録ボックス（C列 Row 5-7） ===
reqs.append(bg(cr(4, 5, 2, 3), LINE_GREEN, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(4, 7, 2, 3), style="SOLID_MEDIUM", color={"red": 0.2, "green": 0.55, "blue": 0.2}))
reqs.append(bg(cr(5, 7, 2, 3), {"red": 0.88, "green": 0.95, "blue": 0.88}, halign="CENTER"))

# === LP送付ボックス（E列 Row 5-7） ===
reqs.append(bg(cr(4, 5, 4, 5), LP_BLUE, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(4, 7, 4, 5), style="SOLID_MEDIUM", color={"red": 0.15, "green": 0.35, "blue": 0.65}))
reqs.append(bg(cr(5, 7, 4, 5), {"red": 0.87, "green": 0.91, "blue": 0.97}, halign="CENTER"))

# === Kawaru LP ボックス（G列 Row 5） ===
reqs.append(bg(cr(4, 5, 6, 7), {"red": 0.16, "green": 0.38, "blue": 0.7}, bold=True, fg=W, size=11, halign="CENTER"))
reqs.append(border(cr(4, 5, 6, 7), style="SOLID_MEDIUM", color={"red": 0.1, "green": 0.25, "blue": 0.55}))

# === 登録ボックス（I列 Row 5） ===
reqs.append(bg(cr(4, 5, 8, 9), REG_GREEN, bold=True, fg=W, size=11, halign="CENTER"))
reqs.append(border(cr(4, 5, 8, 9), style="SOLID_MEDIUM", color={"red": 0.1, "green": 0.45, "blue": 0.2}))
reqs.append(bg(cr(5, 7, 8, 9), {"red": 0.87, "green": 0.95, "blue": 0.9}, halign="CENTER"))

# === Row 9: 導線Bヘッダー ===
reqs.append(bg(cr(8, 9, 0, 10), SEM_ORANGE, bold=True, fg=W, size=10))

# === Row 11: セミナーボックス ===
reqs.append(bg(cr(10, 11, 0, 1), SEM_ORANGE, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(10, 12, 0, 1)))
reqs.append(bg(cr(11, 12, 0, 1), {"red": 0.98, "green": 0.93, "blue": 0.86}))

# === LP直接訴求（C列 Row 11） ===
reqs.append(bg(cr(10, 11, 2, 3), {"red": 0.95, "green": 0.65, "blue": 0.2}, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(10, 11, 2, 3)))

# === LINE登録訴求（C列 Row 12） ===
reqs.append(bg(cr(11, 12, 2, 3), LINE_GREEN, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(11, 12, 2, 3)))

# === LP送付（E列 Row 12） ===
reqs.append(bg(cr(11, 12, 4, 5), LP_BLUE, bold=True, fg=W, halign="CENTER"))
reqs.append(border(cr(11, 12, 4, 5)))

# === Kawaru LP（G列 Row 11） ===
reqs.append(bg(cr(10, 11, 6, 7), {"red": 0.16, "green": 0.38, "blue": 0.7}, bold=True, fg=W, size=11, halign="CENTER"))
reqs.append(border(cr(10, 11, 6, 7), style="SOLID_MEDIUM", color={"red": 0.1, "green": 0.25, "blue": 0.55}))

# === 登録（I列 Row 11） ===
reqs.append(bg(cr(10, 11, 8, 9), REG_GREEN, bold=True, fg=W, size=11, halign="CENTER"))
reqs.append(border(cr(10, 11, 8, 9), style="SOLID_MEDIUM", color={"red": 0.1, "green": 0.45, "blue": 0.2}))

# ↑ マーク（G列 Row 12）
reqs.append(bg(cr(11, 12, 6, 7), LIGHT_GRAY, bold=True, halign="CENTER"))

# Row 14: 注釈
reqs.append(bg(cr(13, 14, 6, 9), NOTE_YELLOW, halign="CENTER"))
reqs.append(border(cr(13, 14, 6, 9)))

# Merge: 注釈
reqs.append({"mergeCells": {"range": cr(13, 14, 6, 9), "mergeType": "MERGE_ALL"}})

body = {"requests": reqs}
resp = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
print(f"Done: {len(resp.get('replies', []))} updates")
