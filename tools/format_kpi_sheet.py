"""Kawaru KPI試算シートのフォーマット設定"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1mTOjgxfJV-zruETo7Yl04NP1SvzYTN5CXdAIiay_zm4"
SHEET_ID = 1271589038  # Kawaru KPI試算

# 認証
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

# カラー定義
BLUE = {"red": 0.267, "green": 0.447, "blue": 0.769}
DARK = {"red": 0.2, "green": 0.2, "blue": 0.2}
WHITE = {"red": 1, "green": 1, "blue": 1}
YELLOW = {"red": 1, "green": 0.949, "blue": 0.8}
LIGHT_BLUE = {"red": 0.835, "green": 0.894, "blue": 0.941}
LIGHT_GREEN = {"red": 0.886, "green": 0.937, "blue": 0.855}
LIGHT_RED = {"red": 0.988, "green": 0.894, "blue": 0.894}
LIGHT_YELLOW = {"red": 1, "green": 0.976, "blue": 0.886}
LIGHT_PURPLE = {"red": 0.914, "green": 0.871, "blue": 0.973}
LIGHT_GRAY = {"red": 0.949, "green": 0.949, "blue": 0.949}
GREEN_TEXT = {"red": 0.133, "green": 0.545, "blue": 0.133}
RED_TEXT = {"red": 0.8, "green": 0.133, "blue": 0.133}


def cell_range(r1, r2, c1, c2):
    return {"sheetId": SHEET_ID, "startRowIndex": r1, "endRowIndex": r2,
            "startColumnIndex": c1, "endColumnIndex": c2}


def bg_format(rng, bg, bold=False, fg=None, size=None):
    fmt = {"backgroundColor": bg}
    txt = {}
    if bold: txt["bold"] = True
    if fg: txt["foregroundColor"] = fg
    if size: txt["fontSize"] = size
    if txt: fmt["textFormat"] = txt
    fields = "userEnteredFormat(backgroundColor"
    if txt: fields += ",textFormat"
    fields += ")"
    return {"repeatCell": {"range": rng, "cell": {"userEnteredFormat": fmt}, "fields": fields}}


def border_req(rng, style="SOLID", color=None):
    if color is None:
        color = {"red": 0.7, "green": 0.7, "blue": 0.7}
    b = {"style": style, "width": 1, "color": color}
    return {"updateBorders": {"range": rng,
                              "top": b, "bottom": b, "left": b, "right": b,
                              "innerHorizontal": b, "innerVertical": b}}


def col_width(col, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "COLUMNS",
                  "startIndex": col, "endIndex": col + 1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}


def row_height(r1, r2, px):
    return {"updateDimensionProperties": {
        "range": {"sheetId": SHEET_ID, "dimension": "ROWS",
                  "startIndex": r1, "endIndex": r2},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}}


requests = []

# === 列幅設定 ===
requests.append(col_width(0, 280))  # A列
for c in range(1, 14):
    requests.append(col_width(c, 120))
# F, I, L列（スペーサー）は細く
for c in [5, 8, 11]:
    requests.append(col_width(c, 20))

# === Row 1: タイトル ===
requests.append(bg_format(cell_range(0, 1, 0, 14), BLUE, bold=True, fg=WHITE, size=14))
requests.append(row_height(0, 1, 40))

# === Row 2: サブタイトル ===
requests.append(bg_format(cell_range(1, 2, 0, 14), {"red": 0.933, "green": 0.933, "blue": 0.933}))

# === Row 4 (idx 3): ■ 入力値 ===
requests.append(bg_format(cell_range(3, 4, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 5-7 (idx 4-6): 入力値エリア ===
requests.append(bg_format(cell_range(4, 7, 0, 1), LIGHT_GRAY, bold=True))  # ラベル
requests.append(bg_format(cell_range(4, 7, 1, 4), YELLOW))  # 入力セル
requests.append(border_req(cell_range(4, 7, 0, 4)))

# === Row 9 (idx 8): ■ SNS内 媒体配分 ===
requests.append(bg_format(cell_range(8, 9, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 10-12 (idx 9-11): 媒体配分 ===
requests.append(bg_format(cell_range(9, 12, 0, 1), LIGHT_GRAY, bold=True))
requests.append(bg_format(cell_range(9, 12, 1, 3), YELLOW))
requests.append(border_req(cell_range(9, 12, 0, 3)))

# === Row 14 (idx 13): ■ ファネル転換率 ===
requests.append(bg_format(cell_range(13, 14, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 15-17 (idx 14-16): 転換率テーブル ===
requests.append(bg_format(cell_range(14, 15, 1, 4), LIGHT_BLUE, bold=True))  # ヘッダー
requests.append(bg_format(cell_range(15, 17, 0, 1), LIGHT_GRAY, bold=True))  # ラベル
requests.append(bg_format(cell_range(15, 17, 1, 4), YELLOW))  # 入力セル
requests.append(border_req(cell_range(14, 17, 0, 4)))

# === Row 19 (idx 18): ■ 必要LINE登録数マトリクス ===
requests.append(bg_format(cell_range(18, 19, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 20-23 (idx 19-22): マトリクス ===
requests.append(bg_format(cell_range(19, 20, 0, 4), LIGHT_BLUE, bold=True))  # ヘッダー
requests.append(bg_format(cell_range(20, 21, 0, 1), LIGHT_GREEN, bold=True))  # 良い行ラベル
requests.append(bg_format(cell_range(20, 21, 1, 4), LIGHT_GREEN))            # 良い行データ
requests.append(bg_format(cell_range(21, 22, 0, 1), LIGHT_YELLOW, bold=True))  # 普通行ラベル
requests.append(bg_format(cell_range(21, 22, 1, 4), LIGHT_YELLOW))
requests.append(bg_format(cell_range(22, 23, 0, 1), LIGHT_RED, bold=True))   # 悪い行ラベル
requests.append(bg_format(cell_range(22, 23, 1, 4), LIGHT_RED))
requests.append(border_req(cell_range(19, 23, 0, 4),
                           style="SOLID_MEDIUM",
                           color={"red": 0.4, "green": 0.4, "blue": 0.4}))

# === Row 25 (idx 24): ■ 全9シナリオ ===
requests.append(bg_format(cell_range(24, 25, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 26 (idx 25): シナリオヘッダー ===
requests.append(bg_format(cell_range(25, 26, 0, 14), LIGHT_BLUE, bold=True))

# === Row 27-35 (idx 26-34): シナリオデータ ===
# 良い×良い〜良い×悪い (idx 26-28)
for r in range(26, 29):
    requests.append(bg_format(cell_range(r, r + 1, 0, 14), {"red": 0.953, "green": 0.973, "blue": 0.945}))
# 普通×良い〜普通×悪い (idx 29-31)
# 普通×普通★ (idx 30) を強調
requests.append(bg_format(cell_range(30, 31, 0, 14), LIGHT_GREEN, bold=True))
# 悪い×良い〜悪い×悪い (idx 32-34)
for r in range(32, 35):
    requests.append(bg_format(cell_range(r, r + 1, 0, 14), {"red": 0.992, "green": 0.953, "blue": 0.953}))

requests.append(border_req(cell_range(25, 35, 0, 14)))

# スペーサー列を白に
for r in range(26, 35):
    for c in [5, 8, 11]:
        requests.append(bg_format(cell_range(r, r + 1, c, c + 1), WHITE))

# === Row 37 (idx 36): ■ 参考 ===
requests.append(bg_format(cell_range(36, 37, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 38-42 (idx 37-41): 実績比較 ===
requests.append(bg_format(cell_range(37, 38, 0, 4), LIGHT_BLUE, bold=True))
requests.append(bg_format(cell_range(38, 41, 0, 4), LIGHT_GRAY))
requests.append(border_req(cell_range(37, 41, 0, 4)))

# === Row 44 (idx 43): ■ セミナー ===
requests.append(bg_format(cell_range(43, 44, 0, 14), DARK, bold=True, fg=WHITE, size=11))

# === Row 45-50 (idx 44-49): セミナー詳細 ===
requests.append(bg_format(cell_range(44, 50, 0, 1), LIGHT_PURPLE, bold=True))
requests.append(bg_format(cell_range(44, 50, 1, 4), {"red": 0.957, "green": 0.933, "blue": 0.988}))
requests.append(border_req(cell_range(44, 50, 0, 4)))

# === 数値フォーマット（カンマ区切り） ===
num_fmt = {"repeatCell": {
    "range": cell_range(20, 23, 1, 4),
    "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}}},
    "fields": "userEnteredFormat.numberFormat"
}}
requests.append(num_fmt)

# シナリオ詳細の数値列にカンマ区切り
for col_range in [(4, 5), (6, 8), (9, 11), (12, 14)]:
    requests.append({"repeatCell": {
        "range": cell_range(26, 35, col_range[0], col_range[1]),
        "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}}},
        "fields": "userEnteredFormat.numberFormat"
    }})

# === シート全体のフォントをNoto Sans JPに ===
requests.append({"repeatCell": {
    "range": cell_range(0, 50, 0, 14),
    "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Noto Sans JP"}}},
    "fields": "userEnteredFormat.textFormat.fontFamily"
}})

# === フリーズ（先頭行固定） ===
requests.append({"updateSheetProperties": {
    "properties": {"sheetId": SHEET_ID, "gridProperties": {"frozenRowCount": 1}},
    "fields": "gridProperties.frozenRowCount"
}})

# 実行
body = {"requests": requests}
resp = service.spreadsheets().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=body
).execute()
print(f"Done: {len(resp.get('replies', []))} updates applied")
