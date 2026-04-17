"""KPI試算シート全体のセル幅・高さを修正。フローチャートとKPIテーブルの両立"""
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

def cr(r1, r2, c1, c2):
    return {"sheetId": SHEET_ID, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}

def col_w(c, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "COLUMNS", "startIndex": c, "endIndex": c + 1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

def row_h(r1, r2, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": r1, "endIndex": r2},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}

NONE_BORDER = {"style": "NONE", "width": 0}
W = {"red": 1, "green": 1, "blue": 1}

# === Step 1: フローチャート(Row 1-12)のマージ解除・クリア ===
pre_reqs = [
    {"unmergeCells": {"range": cr(0, 20, 0, 14)}},
    {"repeatCell": {
        "range": cr(0, 14, 0, 14),
        "cell": {"userEnteredFormat": {
            "backgroundColor": W,
            "textFormat": {"bold": False, "fontSize": 10, "fontFamily": "Noto Sans JP",
                           "foregroundColor": {"red": 0, "green": 0, "blue": 0}},
            "horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE",
        }},
        "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
    }},
    {"updateBorders": {"range": cr(0, 14, 0, 14),
                       "top": NONE_BORDER, "bottom": NONE_BORDER,
                       "left": NONE_BORDER, "right": NONE_BORDER,
                       "innerHorizontal": NONE_BORDER, "innerVertical": NONE_BORDER}},
]
service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={"requests": pre_reqs}).execute()
service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range="Kawaru KPI試算!A1:N14").execute()
print("Cleared flowchart area")

# === Step 2: 列幅をKPIテーブル優先で設定 ===
# KPIテーブル: A=ラベル B-E=データ F=区切 G-H=YouTube I=区切 J-K=Instagram L=区切 M-N=X
col_widths = {
    0: 200,   # A: ラベル
    1: 95,    # B
    2: 95,    # C
    3: 95,    # D
    4: 105,   # E
    5: 25,    # F: 区切
    6: 95,    # G
    7: 105,   # H
    8: 25,    # I: 区切
    9: 95,    # J
    10: 105,  # K
    11: 25,   # L: 区切
    12: 95,   # M
    13: 105,  # N
}
reqs = [col_w(c, px) for c, px in col_widths.items()]

# === Step 3: フローチャートを新しい列幅に合わせて書き直し ===
# 列マッピング:
#   A=流入元 B=→ C=LINE登録 D=→ E=LP送付 F=→ G+H=Kawaru LP I=→ J+K=登録
flow_data = [
    # Row 1: タイトル
    ["■ ファネル全体図", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 2: blank (thin)
    [""],
    # Row 3: 導線A ラベル
    ["導線A：SNS経由", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 4: YouTube
    ["YouTube", "→", "LINE登録", "→", "LP送付", "→", "Kawaru LP", "", "→", "登録", "", "", "", ""],
    # Row 5: Instagram
    ["Instagram", "→", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 6: X
    ["X", "→", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 7: blank (thin)
    [""],
    # Row 8: 導線B ラベル
    ["導線B：セミナー経由", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 9: セミナー ルート1 (LP直接)
    ["セミナー", "→", "LP直接訴求", "─", "─", "→", "Kawaru LP", "", "→", "登録", "", "", "", ""],
    # Row 10: セミナー ルート2 (LINE経由)
    ["", "→", "LINE登録", "→", "LP送付", "→", "", "", "", "", "", "", "", ""],
    # Row 11: blank (thin)
    [""],
    # Row 12: UTM注記
    ["", "", "", "", "", "", "登録時 utm_source で媒体別に計測", "", "", "", "", "", "", ""],
    # Row 13-14: blank separator
    [""], [""],
]

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range="Kawaru KPI試算!A1:N14",
    valueInputOption="USER_ENTERED",
    body={"values": flow_data},
).execute()
print("Flowchart rewritten")

# === Step 4: フローチャートのフォーマット ===
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

WH = {"red": 1, "green": 1, "blue": 1}
TITLE_BG = {"red": 0.15, "green": 0.15, "blue": 0.15}
SECTION_SNS = {"red": 0.22, "green": 0.46, "blue": 0.78}
SECTION_SEM = {"red": 0.85, "green": 0.52, "blue": 0.15}
C_YT = {"red": 0.92, "green": 0.26, "blue": 0.21}
C_IG = {"red": 0.76, "green": 0.18, "blue": 0.56}
C_X = {"red": 0.12, "green": 0.12, "blue": 0.12}
C_SEM = {"red": 0.85, "green": 0.52, "blue": 0.15}
C_LINE = {"red": 0.0, "green": 0.72, "blue": 0.35}
C_LP = {"red": 0.25, "green": 0.52, "blue": 0.85}
C_KAWARU = {"red": 0.12, "green": 0.33, "blue": 0.65}
C_REG = {"red": 0.13, "green": 0.59, "blue": 0.33}
ARROW_FG = {"red": 0.6, "green": 0.6, "blue": 0.6}
NOTE_BG = {"red": 0.97, "green": 0.95, "blue": 0.85}

# 行高さ（フローチャート部分）
reqs.append(row_h(0, 1, 30))    # タイトル
reqs.append(row_h(1, 2, 5))     # blank
reqs.append(row_h(2, 3, 22))    # 導線Aラベル
reqs.append(row_h(3, 4, 36))    # YouTube
reqs.append(row_h(4, 5, 36))    # Instagram
reqs.append(row_h(5, 6, 36))    # X
reqs.append(row_h(6, 7, 8))     # blank
reqs.append(row_h(7, 8, 22))    # 導線Bラベル
reqs.append(row_h(8, 9, 36))    # ルート1
reqs.append(row_h(9, 10, 36))   # ルート2
reqs.append(row_h(10, 11, 5))   # blank
reqs.append(row_h(11, 12, 20))  # 注記
reqs.append(row_h(12, 14, 5))   # separator

# 行高さ（KPIテーブル部分 Row 20以降 = index 19+）
# 入力値セクション
for r in range(19, 38):
    reqs.append(row_h(r, r+1, 24))
# セクションヘッダー行は少し高く
for r in [19, 22, 27, 32, 38, 44, 50, 56]:
    if r < 70:
        reqs.append(row_h(r, r+1, 28))
# シナリオテーブルヘッダー
reqs.append(row_h(39, 40, 50))  # ヘッダー行（改行テキストあり）
# シナリオデータ行
for r in range(40, 50):
    reqs.append(row_h(r, r+1, 26))

# === フローチャートフォーマット ===

# Row 1: タイトル
reqs.append(bg(cr(0, 1, 0, 14), TITLE_BG, bold=True, fg=WH, size=12))

# Row 3: 導線Aラベル
reqs.append(bg(cr(2, 3, 0, 14), SECTION_SNS, bold=True, fg=WH, size=10))

# Row 8: 導線Bラベル
reqs.append(bg(cr(7, 8, 0, 14), SECTION_SEM, bold=True, fg=WH, size=10))

# 流入元ボックス
reqs.append(bg(cr(3, 4, 0, 1), C_YT, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 4, 0, 1), C_YT))
reqs.append(bg(cr(4, 5, 0, 1), C_IG, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(4, 5, 0, 1), C_IG))
reqs.append(bg(cr(5, 6, 0, 1), C_X, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(5, 6, 0, 1), C_X))

# セミナーボックス（2行結合）
reqs.append(bg(cr(8, 10, 0, 1), C_SEM, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 0, 1), C_SEM))
reqs.append({"mergeCells": {"range": cr(8, 10, 0, 1), "mergeType": "MERGE_ALL"}})

# 矢印列：全て中央揃え・グレー
for r in [3, 4, 5, 8, 9]:
    for c in [1, 3, 5, 8]:  # B, D, F, I列
        reqs.append(bg(cr(r, r+1, c, c+1), W, bold=True, fg=ARROW_FG, size=13, halign="CENTER", valign="MIDDLE"))

# LINE登録ボックス（C列 = col2, SNS: 3行結合）
reqs.append(bg(cr(3, 6, 2, 3), C_LINE, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 2, 3), C_LINE))
reqs.append({"mergeCells": {"range": cr(3, 6, 2, 3), "mergeType": "MERGE_ALL"}})

# LINE登録ボックス（セミナー ルート2 Row 10）
reqs.append(bg(cr(9, 10, 2, 3), C_LINE, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(9, 10, 2, 3), C_LINE))

# LP送付ボックス（E列 = col4, SNS: 3行結合）
reqs.append(bg(cr(3, 6, 4, 5), C_LP, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 4, 5), C_LP))
reqs.append({"mergeCells": {"range": cr(3, 6, 4, 5), "mergeType": "MERGE_ALL"}})

# LP直接訴求ボックス（セミナー ルート1 Row 9 C列）
reqs.append(bg(cr(8, 9, 2, 3), C_LP, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 9, 2, 3), C_LP))

# LP送付ボックス（セミナー ルート2 Row 10 E列）
reqs.append(bg(cr(9, 10, 4, 5), C_LP, bold=True, fg=WH, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(9, 10, 4, 5), C_LP))

# Kawaru LPボックス（G+H = col6-7, SNS: 3行結合）
reqs.append(bg(cr(3, 6, 6, 8), C_KAWARU, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 6, 8), C_KAWARU))
reqs.append({"mergeCells": {"range": cr(3, 6, 6, 8), "mergeType": "MERGE_ALL"}})

# Kawaru LPボックス（セミナー: 2行結合）
reqs.append(bg(cr(8, 10, 6, 8), C_KAWARU, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 6, 8), C_KAWARU))
reqs.append({"mergeCells": {"range": cr(8, 10, 6, 8), "mergeType": "MERGE_ALL"}})

# 登録ボックス（J+K = col9-10, SNS: 3行結合）
reqs.append(bg(cr(3, 6, 9, 11), C_REG, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(3, 6, 9, 11), C_REG))
reqs.append({"mergeCells": {"range": cr(3, 6, 9, 11), "mergeType": "MERGE_ALL"}})

# 登録ボックス（セミナー: 2行結合）
reqs.append(bg(cr(8, 10, 9, 11), C_REG, bold=True, fg=WH, size=11, halign="CENTER", valign="MIDDLE"))
reqs.append(border_outer(cr(8, 10, 9, 11), C_REG))
reqs.append({"mergeCells": {"range": cr(8, 10, 9, 11), "mergeType": "MERGE_ALL"}})

# セミナー ルート1 の ─ ─（Row 9 D-F列）矢印表現
reqs.append(bg(cr(8, 9, 3, 6), W, bold=True, fg=ARROW_FG, size=13, halign="CENTER"))

# UTM注記（Row 12）
reqs.append(bg(cr(11, 12, 6, 11), NOTE_BG, size=9, halign="CENTER", valign="MIDDLE"))
reqs.append({"mergeCells": {"range": cr(11, 12, 6, 11), "mergeType": "MERGE_ALL"}})

# === 実行 ===
body = {"requests": reqs}
resp = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
print(f"Done: {len(resp.get('replies', []))} updates")
