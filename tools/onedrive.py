#!/usr/bin/env python3
"""
OneDrive操作ツール — トークン自動更新対応

使い方:
  python3 tools/onedrive.py upload <ローカルファイルパス> [OneDrive上のファイル名]
  python3 tools/onedrive.py list [フォルダパス]
  python3 tools/onedrive.py download <OneDriveファイル名> <保存先パス>
"""

import sys
import json
import os
import msal
import requests

# === 設定 ===
CLIENT_ID = "2afbad9b-1557-4bec-a1a5-0cf8a0436193"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Files.ReadWrite", "User.Read"]
TOKEN_CACHE_PATH = os.path.expanduser("~/.ms365-mcp-token-cache.json")
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# ms-365-mcp-server のキャッシュからもフォールバック
MCP_CACHE_PATHS = [
    os.path.expanduser("~/.npm/_npx/813b81b976932cb5/node_modules/@softeria/ms-365-mcp-server/.token-cache.json"),
]


def get_msal_app():
    """MSALアプリケーションを作成（キャッシュ付き）"""
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH) as f:
            cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache,
    )
    return app, cache


def save_cache(cache):
    """トークンキャッシュを保存"""
    if cache.has_state_changed:
        with open(TOKEN_CACHE_PATH, "w") as f:
            f.write(cache.serialize())
        os.chmod(TOKEN_CACHE_PATH, 0o600)


def get_token():
    """アクセストークンを取得（自動リフレッシュ対応）"""
    app, cache = get_msal_app()

    # 1. キャッシュからサイレント取得を試みる
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            save_cache(cache)
            return result["access_token"]

    # 2. MCP serverのキャッシュからリフレッシュトークンを取得して移行
    for mcp_path in MCP_CACHE_PATHS:
        if os.path.exists(mcp_path):
            try:
                with open(mcp_path) as f:
                    envelope = json.load(f)
                mcp_data = json.loads(envelope["data"]) if isinstance(envelope.get("data"), str) else envelope
                if "RefreshToken" in mcp_data:
                    for rt_key, rt_val in mcp_data["RefreshToken"].items():
                        refresh_token = rt_val.get("secret")
                        if refresh_token:
                            result = app.acquire_token_by_refresh_token(refresh_token, SCOPES)
                            if result and "access_token" in result:
                                save_cache(cache)
                                return result["access_token"]
            except Exception:
                continue

    # 3. デバイスコードフローでログイン
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(f"エラー: デバイスコードフローの開始に失敗: {flow}")
        sys.exit(1)

    print(f"\n{flow['message']}\n")
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        save_cache(cache)
        return result["access_token"]
    else:
        print(f"認証エラー: {result.get('error_description', result)}")
        sys.exit(1)


def get_drive_id(token):
    """デフォルトドライブIDを取得"""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{GRAPH_BASE}/me/drives", headers=headers)
    if resp.status_code == 200:
        drives = resp.json().get("value", [])
        if drives:
            return drives[0]["id"]
    # フォールバック: 既知のドライブID
    return "b!6_l5e5vsHE2MgfPgoFp89u-LJAtTwypBp8_MFlEdqClq02yIECYqRaOfvCsmZ7UR"


def upload(local_path, remote_name=None):
    """ファイルをOneDriveにアップロード"""
    if not os.path.exists(local_path):
        print(f"エラー: ファイルが見つかりません: {local_path}")
        sys.exit(1)

    if remote_name is None:
        remote_name = os.path.basename(local_path)

    token = get_token()
    drive_id = get_drive_id(token)

    file_size = os.path.getsize(local_path)

    if file_size <= 4 * 1024 * 1024:  # 4MB以下
        url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{remote_name}:/content"
        with open(local_path, "rb") as f:
            data = f.read()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
        }
        resp = requests.put(url, headers=headers, data=data)
    else:
        # 4MB超はアップロードセッション使用
        url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{remote_name}:/createUploadSession"
        headers = {"Authorization": f"Bearer {token}"}
        session = requests.post(url, headers=headers, json={}).json()
        upload_url = session["uploadUrl"]

        chunk_size = 10 * 1024 * 1024  # 10MB chunks
        with open(local_path, "rb") as f:
            offset = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                end = offset + len(chunk) - 1
                headers = {
                    "Content-Range": f"bytes {offset}-{end}/{file_size}",
                    "Content-Length": str(len(chunk)),
                }
                resp = requests.put(upload_url, headers=headers, data=chunk)
                offset += len(chunk)

    if resp.status_code in (200, 201):
        result = resp.json()
        print(f"✅ アップロード完了: {remote_name}")
        print(f"   URL: {result.get('webUrl', 'N/A')}")
        return result
    else:
        print(f"❌ エラー ({resp.status_code}): {resp.text[:300]}")
        sys.exit(1)


def list_files(folder_path="root"):
    """OneDriveのファイル一覧を表示"""
    token = get_token()
    drive_id = get_drive_id(token)

    if folder_path == "root":
        url = f"{GRAPH_BASE}/drives/{drive_id}/root/children"
    else:
        url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{folder_path}:/children"

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params={"$top": 50, "$select": "name,size,lastModifiedDateTime,webUrl"})

    if resp.status_code == 200:
        items = resp.json().get("value", [])
        for item in items:
            size = item.get("size", 0)
            name = item["name"]
            modified = item.get("lastModifiedDateTime", "")[:10]
            print(f"  {modified}  {size:>10,}  {name}")
    else:
        print(f"エラー: {resp.status_code}")


def download(remote_name, local_path):
    """OneDriveからファイルをダウンロード"""
    token = get_token()
    drive_id = get_drive_id(token)

    url = f"{GRAPH_BASE}/drives/{drive_id}/root:/{remote_name}:/content"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, allow_redirects=True)

    if resp.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(resp.content)
        print(f"✅ ダウンロード完了: {local_path}")
    else:
        print(f"❌ エラー ({resp.status_code})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "upload":
        local_path = sys.argv[2]
        remote_name = sys.argv[3] if len(sys.argv) > 3 else None
        upload(local_path, remote_name)

    elif cmd == "list":
        folder = sys.argv[2] if len(sys.argv) > 2 else "root"
        list_files(folder)

    elif cmd == "download":
        remote_name = sys.argv[2]
        local_path = sys.argv[3]
        download(remote_name, local_path)

    else:
        print(f"不明なコマンド: {cmd}")
        print(__doc__)
