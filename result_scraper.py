# result_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "last_data/result.json"

def fetch_today_results():
    now = datetime.now()
    if now.hour < 5:
        target_date = now - timedelta(days=1)
    else:
        target_date = now

    date_str = target_date.strftime("%Y-%m-%d")
    url = f"https://baseball.yahoo.co.jp/npb/schedule/?date={date_str}"

    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    cards = soup.select("li.bb-score__item")
    for card in cards:
        teams = card.select("div.bb-score__team p")
        scores = card.select("p.bb-score__status span")

        if len(teams) >= 2 and len(scores) == 3:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            score = f"{scores[0].text}-{scores[2].text}"
            results.append(f"{team1} {score} {team2}")

    return results, target_date.strftime("%Y年%m月%d日")


def load_last_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_current_data(data):
    os.makedirs("last_data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_result_update():
    current_results, date_str = fetch_today_results()
    last_results = load_last_data()

    if current_results != last_results and current_results:
        save_current_data(current_results)
        message = f"📢 {date_str} の試合結果が更新されました！\n" + "\n".join(current_results)
        return message
    return None

if __name__ == "__main__":
    message = check_result_update()
    if message:
        print(message)
    else:
        print("試合結果に更新はありませんでした。")