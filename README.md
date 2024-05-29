## 説明
OBSでTwitch配信をミラーするためのコントローラー。

## 使い方
1. OBSで、`player N`という名前の、ブラウザソースを作成
2. OBSのスクリプトに、`obs_controller.py`を追加
3. `\data\allnames.txt`に、Twitch IDを行ごとに追加
4. `main_controller.pyw`を起動
5. プレイヤーのコンボボックスから、Twitch IDを選択
6. `Refresh`をクリック

### エラーが起きた場合
`Clear`をクリックし、再度`Refresh`をクリックする。

## 設定
必要に応じて、コントローラーをテキストエディタで開き、設定を変更する。

## デバッグ
問題がある場合は、`main_controller`の拡張子を、`.py`に変える。
