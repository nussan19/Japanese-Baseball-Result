import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1371893412944547900/h2jzSEK-yv-x99fZjguFJ25YDO2es3LuvWPnTXDWsDmwZp_qMg3CzK24ZaJE1Rfb3a_m"

message = {
    "content": "✅ 通知テスト：これはDiscordへの初めての通知です！"
}

response = requests.post(WEBHOOK_URL, json=message)

if response.status_code == 204:
    print("✅ Discordに通知を送信しました。")
else:
    print(f"⚠️ 送信失敗: {response.status_code} - {response.text}")