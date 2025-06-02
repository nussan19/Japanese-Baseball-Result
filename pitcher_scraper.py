import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1371893412944547900/h2jzSEK-yv-x99fZjguFJ25YDO2es3LuvWPnTXDWsDmwZp_qMg3CzK24ZaJE1Rfb3a_m"
SAVE_PATH = "last_data/next_pitchers.json"

today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
url = f"https://baseball.yahoo.co.jp/npb/schedule/?date={date_str}"

headers = {"User-Agent": "Mozilla/5.0"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

matches = soup.select("li.bb-score__item")
print(f"取得した試合数: {len(matches)}")

pitchers_data = []
for match in matches:
    teams = match.select("div.bb-score__team p")
    home_pitcher_tag = match.select_one("ul.bb-score__home li.bb-score__player--probable")
    away_pitcher_tag = match.select_one("ul.bb-score__away li.bb-score__player--probable")

    if len(teams) >= 2:
        away_team = teams[0].text.strip()
        home_team = teams[1].text.strip()
        home_pitcher = home_pitcher_tag.text.strip() if home_pitcher_tag else "（未発表）"
        away_pitcher = away_pitcher_tag.text.strip() if away_pitcher_tag else "（未発表）"
        line = f"{home_team}（先発: {home_pitcher}） vs {away_team}（先発: {away_pitcher}）"
        pitchers_data.append(line)

# デバッグ出力
print("📋 取得した予告先発一覧:")
for p in pitchers_data:
    print(p)

# 差分チェック
if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        last_data = json.load(f)
else:
    last_data = []

if pitchers_data != last_data:
    message = f"📢 **{today.strftime('%Y年%m月%d日')} の予告先発が更新されました！**\n```" + "\n".join(pitchers_data) + "```"
    requests.post(WEBHOOK_URL, json={"content": message})

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(pitchers_data, f, ensure_ascii=False, indent=2)
else:
    print("予告先発に更新はありませんでした。")