import os
import time
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1371893412944547900/h2jzSEK-yv-x99fZjguFJ25YDO2es3LuvWPnTXDWsDmwZp_qMg3CzK24ZaJE1Rfb3a_m"

# 監視するファイルと通知メッセージ
files_to_watch = {
    "result.py": "📢 試合結果が更新されました！",
    "next_pitchers.py": "📢 新しい予告先発が発表されました！",
    "standings.py": "📢 順位表が更新されました！"
}

# ファイルの更新時刻を記録
last_modified = {file: os.path.getmtime(file) for file in files_to_watch}

def send_discord_notification(message):
    requests.post(WEBHOOK_URL, json={"content": message})

print("🟢 自動通知監視を開始します...")

while True:
    for file, message in files_to_watch.items():
        try:
            current_mtime = os.path.getmtime(file)
            if current_mtime != last_modified[file]:
                send_discord_notification(f"{message}（{time.strftime('%Y-%m-%d %H:%M:%S')}）")
                last_modified[file] = current_mtime
        except FileNotFoundError:
            continue
    time.sleep(10)  # 10秒ごとにチェック（必要なら短くしてOK）