import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1371893412944547900/h2jzSEK-yv-x99fZjguFJ25YDO2es3LuvWPnTXDWsDmwZp_qMg3CzK24ZaJE1Rfb3a_m"
SAVE_PATH = "last_data/standings.json"
URL = "https://baseball.yahoo.co.jp/npb/standings/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

res = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(res.text, "html.parser")

today = datetime.now().strftime("%Y年%m月%d日")
sections = soup.select("section.bb-modCommon01")

standings_data = {}

for section in sections:
    league_tag = section.select_one("h2.bb-rankHead__title")
    table = section.select_one("table.bb-rankTable")

    if not league_tag or not table:
        continue

    league_name = league_tag.text.strip()

    # セ・リーグ／パ・リーグ だけを対象にする
    if not ("セ" in league_name or "パ" in league_name):
        continue

    rows = table.select("tbody tr")
    league_data = []

    for row in rows:
        cols = row.select("td")
        if len(cols) < 8:
            continue

        team = cols[1].text.strip()
        game = cols[2].text.strip()
        win = cols[3].text.strip()
        lose = cols[4].text.strip()
        draw = cols[5].text.strip()
        win_rate = cols[6].text.strip()
        game_diff = cols[7].text.strip()

        line = f"{team} {game}試合{win}勝{lose}敗{draw}分 勝率{win_rate} ゲーム差{game_diff}"
        league_data.append(line)

    standings_data[league_name] = league_data

# 差分チェック
if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        last_data = json.load(f)
else:
    last_data = {}

if standings_data != last_data:
    message = f"📊 {today} の順位表が更新されました！\n"
    for league, lines in standings_data.items():
        message += f"\n【{league}】\n" + "\n".join(lines)

    requests.post(WEBHOOK_URL, json={"content": message})

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(standings_data, f, ensure_ascii=False, indent=2)
else:
    print("順位表に更新はありませんでした。")