## 説明
OBSでTwitch配信をミラーするためのコントローラー。

## 使い方
1. autoswitchを有効にする場合は、OBSで`Normal`と、`Focus`という名前のシーンを作成
2. 作成したシーンに、`Player N`という名前のブラウザソースを作成（`N`は、1から順に必要数作成）
3. OBSのスクリプトに、`obs_controller.py`を追加
4. `\data\allnames.txt`に、Twitch IDを行ごとに追加
5. `main_controller.pyw`を起動
6. プレイヤーのコンボボックスから、Twitch IDを選択
7. `Refresh`をクリック

### フォーカス
プレイヤーの右にある、ラジオボタンでフォーカスを有効にできる。有効にしたプレイヤーは、`Player 1`に表示される。  
一番下のラジオボタンで無効化。

### allnames.txtを起動中に編集した場合
`Refresh`をクリックすることで、コンボボックスが更新される。

### エラーが起きた場合
`Clear`をクリックし、再度`Refresh`をクリックする。

## 設定
各ファイルをテキストエディタで開いて編集する。

### main_controller
- `view` 表示する配信の最大数
- `autoswitch` 自動的にシーンを切り替える
- `pacecatcher` [PaceCatcherBot](https://github.com/mebuki117/PaceCatcherBot)と併用する

### obs_controller
- `browser_format` ブラウザソースの識別子
- `normal_scene_name` ノーマルシーン名
- `focus_scene_name` フォーカスシーン名
 
## デバッグ
問題がある場合は、`main_controller`の拡張子を、`.py`に変える。
