import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 日付を決定（深夜0〜4時は前日を対象にする）
now = datetime.now()
if now.hour < 5:
    target_date = now - timedelta(days=1)
else:
    target_date = now

date_str = target_date.strftime("%Y-%m-%d")  # スポナビのURLは YYYY-MM-DD 形式

# URLを組み立て
url = f"https://baseball.yahoo.co.jp/npb/schedule/?date={date_str}"
headers = {"User-Agent": "Mozilla/5.0"}

# ページ取得
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 試合行（1試合につき1つ）を抽出
matches = soup.select('tr.bb-scheduleTable__row')

print(f"=== {target_date.strftime('%Y年%m月%d日')} の試合結果 ===\n")

found = False  # 試合が1つもなかった場合の判定用

for match in matches:
    home_tag = match.select_one('.bb-scheduleTable__homeName a')
    away_tag = match.select_one('.bb-scheduleTable__awayName a')
    score_tag = match.select_one('.bb-scheduleTable__score')
    stadium_tag = match.select_one('.bb-scheduleTable__data--stadium')

    if home_tag and away_tag and score_tag:
        home = home_tag.text.strip()
        away = away_tag.text.strip()
        score = score_tag.text.strip().replace('\n', '').replace(' ', '')
        stadium = stadium_tag.text.strip() if stadium_tag else "不明"

        print(f"{home} {score} {away}（{stadium}）")
        found = True

if not found:
    print("試合データが見つかりませんでした。")
    
