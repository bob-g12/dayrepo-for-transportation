# 独自に追加したコマンドをまとめるページ

## カスタムコマンドの作り方
参考URL: https://zenn.dev/wtkn25/articles/django-custom-command

### 例
```sh
python manage.py mycommand
```
![mycommandの実行結果](exec_mycommand.png)

## baccount
accountテーブルを操作するコマンド

### account テーブルのデータを全件表示
```sh
python manage.py baccount --get all
```

### account テーブルにテストデータを新規作成
```sh
python manage.py baccount --create f
```

### account テーブルのデータを全件削除
```sh
python manage.py baccount --del all
```
