import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 今日の日付を日本語形式に整形（例: 5月14日）
today = datetime.now()
target_date_str = today.strftime("%-m月%-d日")

print(f"=== {today.strftime('%Y年%m月%d日')} の予告先発 ===\n")

# スポナビのスケジュールページ
date_param = today.strftime("%Y-%m-%d")
url = f"https://baseball.yahoo.co.jp/npb/schedule/?date={date_param}"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 試合カード（liタグ）をすべて取得
cards = soup.select("li.bb-score__item")
found = False

for card in cards:
    # チーム名の取得
    home_team = card.select_one("p.bb-score__homeLogo")
    away_team = card.select_one("p.bb-score__awayLogo")

    # 予告先発の取得
    home_pitcher = card.select_one("ul.bb-score__home li.bb-score__player--probable")
    away_pitcher = card.select_one("ul.bb-score__away li.bb-score__player--probable")

    if home_team and away_team:
        team1 = home_team.text.strip()
        team2 = away_team.text.strip()
        pitcher1 = home_pitcher.text.strip() if home_pitcher else "（未発表）"
        pitcher2 = away_pitcher.text.strip() if away_pitcher else "（未発表）"

        print(f"{team1}（先発: {pitcher1}） vs {team2}（先発: {pitcher2}）")
        found = True

if not found:
    print("予告先発はまだ発表されていません。")