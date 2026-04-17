"""KPI試算シートの上部にファネル全体図を挿入"""
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

ROWS_TO_INSERT = 20

# --- Step 1: 上部に行を挿入（既存コンテンツは自動で下にずれる） ---
insert_req = {
    "requests": [{
        "insertDimension": {
            "range": {
                "sheetId": SHEET_ID,
                "dimension": "ROWS",
                "startIndex": 0,
                "endIndex": ROWS_TO_INSERT,
            },
            "inheritFromBefore": False,
        }
    }]
}
service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=insert_req
).execute()
print(f"Inserted {ROWS_TO_INSERT} rows")

# --- Step 2: フローチャートのコンテンツを書き込み ---
flowchart_data = [
    # Row 1: タイトル
    ["■ Kawaruローンチ ファネル全体図", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 2: blank
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 3: 二つの導線ヘッダー
    ["【導線A】SNS経由（90%＝450名）", "", "", "", "", "", "", "【導線B】セミナー経由（10%＝50名）", "", "", "", "", "", ""],
    # Row 4: SNS媒体 / セミナー
    ["YouTube", "", "Instagram", "", "X", "", "", "取りこぼしセミナー（12回）", "", "", "", "", "", ""],
    # Row 5: 配分 / セミナー説明
    ["40%（180名）", "", "40%（180名）", "", "20%（90名）", "", "", "AIエージェント道場 + Kawaru 併催", "", "", "", "", "", ""],
    # Row 6: 矢印
    ["↓", "", "↓", "", "↓", "", "", "↓", "", "", "↓", "", "", ""],
    # Row 7: LINE登録 / セミナー分岐
    ["LINE登録（エヌイチ法人LINE）", "", "", "", "", "", "", "セミナー内LP直接訴求", "", "", "LINE登録訴求", "", "", ""],
    # Row 8: Lステップ説明 / 矢印
    ["Lステップでタグ付与（流入元別）", "", "", "", "", "", "", "↓", "", "", "↓", "", "", ""],
    # Row 9: 矢印
    ["↓", "", "", "", "", "", "", "↓", "", "", "LINE登録", "", "", ""],
    # Row 10: LP送付
    ["LP送付（utm_source別URL）", "", "", "", "", "", "", "↓", "", "", "↓", "", "", ""],
    # Row 11: 矢印
    ["↓", "", "", "", "", "", "", "↓", "", "", "LP送付", "", "", ""],
    # Row 12: blank
    ["", "", "", "", "", "", "", "", "", "", "↓", "", "", ""],
    # Row 13: LP（中央合流）
    ["", "", "", "▼ Kawaru LP ▼", "", "", "", "", "", "", "", "", "", ""],
    # Row 14: 登録
    ["", "", "", "無料トライアル登録（カード登録＝アカウント付与）", "", "", "", "", "", "", "", "", "", ""],
    # Row 15: UTM計測
    ["", "", "", "utm_source で媒体別の登録数を計測", "", "", "", "", "", "", "", "", "", ""],
    # Row 16: blank
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 17: 凡例
    ["※ 導線AのLINE→LP間の転換率と、LP→登録の転換率がKPI試算の核（下記参照）", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 18: blank separator
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 19: blank separator
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    # Row 20: blank
    ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
]

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range="Kawaru KPI試算!A1:N20",
    valueInputOption="USER_ENTERED",
    body={"values": flowchart_data},
).execute()
print("Flowchart content written")

# --- Step 3: フォーマット ---
def cell_range(r1, r2, c1, c2):
    return {"sheetId": SHEET_ID, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}

def bg_format(rng, bg, bold=False, fg=None, size=None, halign=None):
    fmt = {"backgroundColor": bg}
    txt = {}
    if bold: txt["bold"] = True
    if fg: txt["foregroundColor"] = fg
    if size: txt["fontSize"] = size
    if txt: fmt["textFormat"] = txt
    if halign: fmt["horizontalAlignment"] = halign
    fields_parts = ["backgroundColor"]
    if txt: fields_parts.append("textFormat")
    if halign: fields_parts.append("horizontalAlignment")
    return {"repeatCell": {"range": rng,
                           "cell": {"userEnteredFormat": fmt},
                           "fields": f"userEnteredFormat({','.join(fields_parts)})"}}

def border_req(rng, style="SOLID", color=None):
    if color is None:
        color = {"red": 0.6, "green": 0.6, "blue": 0.6}
    b = {"style": style, "width": 1, "color": color}
    return {"updateBorders": {"range": rng,
                              "top": b, "bottom": b, "left": b, "right": b}}

BLUE = {"red": 0.267, "green": 0.447, "blue": 0.769}
DARK = {"red": 0.2, "green": 0.2, "blue": 0.2}
WHITE = {"red": 1, "green": 1, "blue": 1}
LIGHT_BLUE = {"red": 0.835, "green": 0.894, "blue": 0.941}
LIGHT_GREEN = {"red": 0.886, "green": 0.937, "blue": 0.855}
LIGHT_PURPLE = {"red": 0.914, "green": 0.871, "blue": 0.973}
LIGHT_GRAY = {"red": 0.949, "green": 0.949, "blue": 0.949}
YT_RED = {"red": 1, "green": 0.85, "blue": 0.85}
IG_PINK = {"red": 0.98, "green": 0.85, "blue": 0.95}
X_BLUE = {"red": 0.85, "green": 0.9, "blue": 1}
ORANGE = {"red": 1, "green": 0.929, "blue": 0.831}
GREEN_BOX = {"red": 0.788, "green": 0.918, "blue": 0.788}
DARK_GREEN = {"red": 0.133, "green": 0.4, "blue": 0.133}

fmt_requests = []

# Row 1: タイトルバー
fmt_requests.append(bg_format(cell_range(0, 1, 0, 14), DARK, bold=True, fg=WHITE, size=12))

# Row 3: 導線ヘッダー
fmt_requests.append(bg_format(cell_range(2, 3, 0, 6), BLUE, bold=True, fg=WHITE, size=11))
fmt_requests.append(bg_format(cell_range(2, 3, 7, 14), LIGHT_PURPLE, bold=True, size=11))

# Row 4-5: SNS媒体ボックス
fmt_requests.append(bg_format(cell_range(3, 4, 0, 2), YT_RED, bold=True, halign="CENTER"))
fmt_requests.append(bg_format(cell_range(3, 4, 2, 4), IG_PINK, bold=True, halign="CENTER"))
fmt_requests.append(bg_format(cell_range(3, 4, 4, 6), X_BLUE, bold=True, halign="CENTER"))
fmt_requests.append(bg_format(cell_range(4, 5, 0, 2), YT_RED, halign="CENTER"))
fmt_requests.append(bg_format(cell_range(4, 5, 2, 4), IG_PINK, halign="CENTER"))
fmt_requests.append(bg_format(cell_range(4, 5, 4, 6), X_BLUE, halign="CENTER"))
fmt_requests.append(border_req(cell_range(3, 5, 0, 2)))
fmt_requests.append(border_req(cell_range(3, 5, 2, 4)))
fmt_requests.append(border_req(cell_range(3, 5, 4, 6)))

# Row 4-5: セミナーボックス
fmt_requests.append(bg_format(cell_range(3, 5, 7, 11), LIGHT_PURPLE, bold=True))
fmt_requests.append(border_req(cell_range(3, 5, 7, 11)))

# Row 6: 矢印
fmt_requests.append(bg_format(cell_range(5, 6, 0, 14), WHITE, halign="CENTER"))

# Row 7: LINE登録ボックス
fmt_requests.append(bg_format(cell_range(6, 7, 0, 6), LIGHT_GREEN, bold=True))
fmt_requests.append(border_req(cell_range(6, 7, 0, 6)))

# Row 7: セミナー分岐
fmt_requests.append(bg_format(cell_range(6, 7, 7, 10), ORANGE, bold=True))
fmt_requests.append(border_req(cell_range(6, 7, 7, 10)))
fmt_requests.append(bg_format(cell_range(6, 7, 10, 13), LIGHT_GREEN, bold=True))
fmt_requests.append(border_req(cell_range(6, 7, 10, 13)))

# Row 8: Lステップ説明
fmt_requests.append(bg_format(cell_range(7, 8, 0, 6), {"red": 0.93, "green": 0.96, "blue": 0.93}))

# Row 9: LINE登録(セミナー側)
fmt_requests.append(bg_format(cell_range(8, 9, 10, 13), LIGHT_GREEN))
fmt_requests.append(border_req(cell_range(8, 9, 10, 13)))

# Row 10: LP送付ボックス
fmt_requests.append(bg_format(cell_range(9, 10, 0, 6), LIGHT_BLUE, bold=True))
fmt_requests.append(border_req(cell_range(9, 10, 0, 6)))

# Row 10-11: セミナー→LP送付
fmt_requests.append(bg_format(cell_range(10, 11, 10, 13), LIGHT_BLUE))
fmt_requests.append(border_req(cell_range(10, 11, 10, 13)))

# Row 13-14: Kawaru LP（中央）
fmt_requests.append(bg_format(cell_range(12, 13, 2, 12), BLUE, bold=True, fg=WHITE, size=12, halign="CENTER"))
fmt_requests.append(border_req(cell_range(12, 13, 2, 12), style="SOLID_MEDIUM", color={"red": 0.2, "green": 0.3, "blue": 0.6}))

# Row 14: 登録
fmt_requests.append(bg_format(cell_range(13, 14, 2, 12), GREEN_BOX, bold=True, fg=DARK_GREEN, size=11, halign="CENTER"))
fmt_requests.append(border_req(cell_range(13, 14, 2, 12), style="SOLID_MEDIUM", color={"red": 0.2, "green": 0.5, "blue": 0.2}))

# Row 15: UTM計測
fmt_requests.append(bg_format(cell_range(14, 15, 2, 12), LIGHT_GRAY, halign="CENTER"))
fmt_requests.append(border_req(cell_range(14, 15, 2, 12)))

# Row 17: 凡例
fmt_requests.append(bg_format(cell_range(16, 17, 0, 14), {"red": 1, "green": 1, "blue": 0.878}))

# 矢印セルを中央揃え
for r in [5, 7, 8, 10, 11]:
    fmt_requests.append(bg_format(cell_range(r, r+1, 0, 14), WHITE, halign="CENTER"))
    # Re-apply specific formatting that was overridden

# Row heights
fmt_requests.append({"updateDimensionProperties": {
    "range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
    "properties": {"pixelSize": 35}, "fields": "pixelSize"}})
fmt_requests.append({"updateDimensionProperties": {
    "range": {"sheetId": SHEET_ID, "dimension": "ROWS", "startIndex": 12, "endIndex": 14},
    "properties": {"pixelSize": 35}, "fields": "pixelSize"}})

# Merge cells for key boxes
merges = [
    # SNS LINE登録
    cell_range(6, 7, 0, 6),
    # Lステップ説明
    cell_range(7, 8, 0, 6),
    # LP送付
    cell_range(9, 10, 0, 6),
    # セミナー
    cell_range(3, 4, 7, 11),
    cell_range(4, 5, 7, 11),
    # セミナー分岐左
    cell_range(6, 7, 7, 10),
    # セミナー分岐右
    cell_range(6, 7, 10, 13),
    # Kawaru LP
    cell_range(12, 13, 2, 12),
    # 登録
    cell_range(13, 14, 2, 12),
    # UTM計測
    cell_range(14, 15, 2, 12),
    # 凡例
    cell_range(16, 17, 0, 14),
]
for m in merges:
    fmt_requests.append({"mergeCells": {"range": m, "mergeType": "MERGE_ALL"}})

body = {"requests": fmt_requests}
resp = service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=body
).execute()
print(f"Formatting done: {len(resp.get('replies', []))} updates")
