#!/usr/bin/env python3
"""商談お礼メール下書き作成スクリプト（Gmail API直接呼び出し）"""

import json
import base64
from email.mime.text import MIMEText
from email.header import Header
import requests

# === 認証情報の読み込み ===
with open("/Users/kyouyuu/.google-mcp/tokens/main.json") as f:
    tokens = json.load(f)

def get_access_token():
    """refresh_tokenからaccess_tokenを取得"""
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": tokens["client_id"],
        "client_secret": tokens["client_secret"],
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_message_header(access_token, message_id, header_name):
    """メッセージから特定のヘッダーを取得"""
    resp = requests.get(
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"format": "metadata", "metadataHeaders": header_name},
    )
    resp.raise_for_status()
    for h in resp.json().get("payload", {}).get("headers", []):
        if h["name"].lower() == header_name.lower():
            return h["value"]
    return None

def create_draft_reply(access_token, to, cc, subject, body, thread_id, reply_to_msg_id):
    """スレッドへの返信ドラフトを作成"""
    # 元メッセージのMessage-IDヘッダーを取得
    original_message_id = get_message_header(access_token, reply_to_msg_id, "Message-ID")

    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    msg["From"] = "大川龍之介 <r.okawa@n1-inc.co.jp>"
    msg["Subject"] = Header(subject, "utf-8").encode()

    if original_message_id:
        msg["In-Reply-To"] = original_message_id
        msg["References"] = original_message_id

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

    draft_body = {
        "message": {
            "raw": raw,
            "threadId": thread_id,
        }
    }

    resp = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/drafts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=draft_body,
    )
    resp.raise_for_status()
    return resp.json()


# === メイン処理 ===
access_token = get_access_token()
print("✅ アクセストークン取得成功")

# ============================
# 1. リードインクス お礼メール
# ============================
leadinx_body = """\
リードインクス株式会社
呉様

お世話になっております。
株式会社エヌイチの大川です。

本日はお忙しい中、貴重なお時間をいただき誠にありがとうございました。
柏岡社長にもご同席いただき、大変有意義なお話ができたかと思います。

改めて本日のお打ち合わせ内容を整理させていただきます。

■ ご要望・課題
・エンジニア向けのAIエージェント構築に関する研修
・セキュリティ（リージョン含む）面の深いカバー
・現場のAI活用レベルの底上げ（現状Lv.2〜3）
・業務の棚卸しから要件定義までのプロセスにおけるAI活用

■ 次のステップ
上記の内容をもとに、貴社のエンジニア組織に最適な研修カリキュラム・ご提案書を作成させていただきます。
準備ができ次第、改めてご連絡差し上げますので、少々お待ちいただけますと幸いです。

ご不明な点やご要望がございましたら、お気軽にお申し付けください。
引き続き、どうぞよろしくお願いいたします。


―――――――――――――――――――――――――――――――
株式会社エヌイチ
法人事業部 セールスマネージャー
大川 龍之介（Okawa Ryunosuke）

TEL：080-2646-2420
Mail：r.okawa@n1-inc.co.jp
Website：https://n1-inc.co.jp/

「AI（アイ）ある社会に 」
―――――――――――――――――――――――――――――――"""

result1 = create_draft_reply(
    access_token=access_token,
    to="zhenyu.wu@leadinx.co.jp",
    cc="y.takahashi@n1-inc.co.jp",
    subject="Re: 【Eight EXPO】本日はありがとうございました 2月 27日 (金曜日)⋅11:30～12:30 商談のご案内",
    body=leadinx_body,
    thread_id="19c70ad2dae26416",
    reply_to_msg_id="19cd55f9be99340c",
)
print(f"✅ リードインクス下書き作成完了 (Draft ID: {result1['id']})")

# ============================
# 2. マミーズエンジェル お礼メール
# ============================
mammys_body = """\
株式会社マミーズエンジェル
小川 奈於人 様
小川 泰輝 様

お世話になっております。
株式会社エヌイチの大川です。

本日はお忙しい中、貴重なお時間をいただき誠にありがとうございました。
保育業界特有の課題やAI活用の状況について詳しくお伺いでき、大変有意義なお打ち合わせとなりました。

改めて本日のお打ち合わせ内容を整理させていただきます。

■ ご要望・課題
・一人あたりの業務負荷の軽減をAI活用で実現したい
・本部職の事務業務（人事・コア業務）の効率化
・シフト管理の自動化・最適化
・保育現場のITリテラシーを踏まえた導入設計

■ 次のステップ
上記の内容を踏まえ、本部職・保育職それぞれに最適なAI活用のご提案書を作成させていただきます。
準備ができ次第、改めてご連絡差し上げますので、少々お待ちいただけますと幸いです。

ご不明な点やご要望がございましたら、お気軽にお申し付けください。
引き続き、どうぞよろしくお願いいたします。


―――――――――――――――――――――――――――――――
株式会社エヌイチ
法人事業部 セールスマネージャー
大川 龍之介（Okawa Ryunosuke）

TEL：080-2646-2420
Mail：r.okawa@n1-inc.co.jp
Website：https://n1-inc.co.jp/

「AI（アイ）ある社会に 」
―――――――――――――――――――――――――――――――"""

result2 = create_draft_reply(
    access_token=access_token,
    to="n-ogawa@mammys-angel.co.jp, ti-ogawa@mammys-angel.co.jp",
    cc="y.takahashi@n1-inc.co.jp",
    subject="Re: 再送【会話で作れるAIワークフロー「Kawaru」】お打合せ日時のご連絡 3月17日(火)15:00（株式会社エヌイチ）",
    body=mammys_body,
    thread_id="19c93425e7efc3f9",
    reply_to_msg_id="19cf9b5afe0185c9",
)
print(f"✅ マミーズエンジェル下書き作成完了 (Draft ID: {result2['id']})")

print("\n🎉 2件の下書き作成が完了しました（送信はしていません）")
