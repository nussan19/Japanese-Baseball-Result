import requests
from bs4 import BeautifulSoup

url = "https://baseball.yahoo.co.jp/npb/standings/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# セ・リーグとパ・リーグそれぞれのタイトルを取得
sections = soup.select("section.bb-modCommon03")

def parse_standings(section, league_name):
    print(f"\n=== {league_name} 順位表 ===\n")
    rows = section.select("table.bb-rankTable tbody tr")

    for row in rows:
        cols = row.select("td")
        if len(cols) >= 8:
            rank = cols[0].text.strip()
            team = cols[1].text.strip()
            win = cols[3].text.strip()
            lose = cols[4].text.strip()
            draw = cols[5].text.strip()
            win_rate = cols[6].text.strip()
            game_behind = cols[7].text.strip()

            print(f"{rank}位 {team}：{win}勝{lose}敗{draw}分 勝率{win_rate} ゲーム差 {game_behind}")

# セ・リーグ（1番目）、パ・リーグ（2番目）
if len(sections) >= 2:
    parse_standings(sections[0], "セ・リーグ")
    parse_standings(sections[1], "パ・リーグ")
else:
    print("順位表の取得に失敗しました。")