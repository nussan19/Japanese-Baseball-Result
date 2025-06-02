# Japanese-Baseball-Result

このリポジトリは、プロ野球の試合結果・予告先発・順位表を取得し、Discordに自動通知するツールです。  
主にPythonで開発しており、スクレイピングとWebhook通知を組み合わせて構成されています。

## 主な機能

- スポナビ（Yahoo!スポーツ）からの試合結果データ取得
- 予告先発の取得と保存
- プロ野球の順位表の取得と比較
- 変更があった場合のみDiscordに通知
- 定期実行に対応（crontabなどで運用可能）

## 使用技術

- Python（requests, BeautifulSoup, json など）
- Discord Webhook
- Git / GitHub

## 使用例

- 毎日10分おきにスクリプトを実行し、変更があった場合のみ通知
- スポーツファン向けの速報通知ボットのベースとして活用可能
