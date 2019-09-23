# 概要
通信対戦できるオセロプログラムです。次の手を選択するアルゴリズムを実装することで強いオセロAIをつくることができます。
__なお、現在実装中なので、動作の保証はできません。ご了承ください。__

## 対戦方法
まず端末を1つ起動し、次のようにしてオセロサーバを立てます。

```
python othello_server.py <ポート番号>
```

次に端末をもう2つ用意し、次のようにしてオセロクライアントを起動します。なお、ホスト名はサーバを立てたPCのIPアドレスを指定します。(同じPC上で動かしていれば "localhost" としても動作します。)ポート番号はサーバをたてるときに指定したものとします。

```
python othello_client.py <ホスト名> <ポート番号>
```

クライアントが2つ接続されると対戦が始まります。現在の実装では接続したクライアントどうしが対戦を終了するとサーバも終了するようになっています。

## 設定変更の方法
設定ファイル othello_configuration_editable.py の変数の値を書き換えることで対戦設定を変更することができます。現在の実装では以下のオプションをサポートしています。

- PLAYERNAME_EDITABLE 各プレイヤーの名前
- MATCHNUMBER_EDITABLE 対戦数


## 手の選択アルゴリズムの実装
アルゴリズムの実装はothello_ai_editable.py の内部で行うことができます。同じファイルで定義されている変数 AI_EDITABLE にそのアルゴリズムの関数名を文字列で格納しておくことで反映させることができます。

