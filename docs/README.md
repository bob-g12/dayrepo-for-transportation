## 概要
この README は、主に開発をする上で別途残しておきたいものを記載していきます。
ルートディレクトリにある README はサービス説明です。

## ページリンク
よく使用するコマンドをまとめたドキュメントです。
- [command.md](./command.md)

独自にカスタマイズしたコマンドをまとめたドキュメントです。
- [add_customcommand.md](./add_customcommand.md)

開発する際におすすめの拡張機能などをまとめたドキュメントです。
- [my_favorite.md](./my_favorite.md)

# 環境構築
Python をインストール
参考記事; [PythonをWindows、macOS、Linuxにインストールする方法](https://kinsta.com/jp/knowledgebase/install-python/)

Django をインストール
``` sh
python -m pip install Django
```

openpyxl をインストール
``` sh
pip install openpyxl
```
[openpyxl で Excel を操作する【 Python 入門】](https://tech-blog.rakus.co.jp/entry/20210729/openpyxl#:~:text=openpyxl%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%AF%E7%B0%A1%E5%8D%98,%E3%81%A6%E3%82%A8%E3%83%B3%E3%82%BF%E3%83%BC%203%20)%20%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E5%AE%8C%E4%BA%86%EF%BC%81)

### アプリを起動する手順
マイグレーションファイルを作成
``` sh
python manage.py makemigrations
```

マイグレーションファイルをデータベースに適用
``` sh
python manage.py migrate
```

サーバー起動
``` sh
python manage.py runserver
```
