## 概要
よく使用するコマンドまとめ

## Django
#### 開発用サーバー立ち上げ
``` sh
python manage.py runserver
```

#### Django テストの実行
``` sh
python manage.py test
```

#### Django アプリケーションの作成
``` sh
python manage.py startapp snippets
```

#### 管理ユーザーの作成
``` sh
python manage.py createsuperuser
```

### マイグレーション系
マイグレーション系は以下の記事もご参考にどうぞ
- 参考記事1: [Django マイグレーション まとめ](https://qiita.com/okoppe8/items/c9f8372d5ac9a9679396)
  - 以下に記載がない、「マイグレーションの適用計画順（後述）に表示」「対象のマイグレーションID適用時のSQLを表示」 その他特殊操作などのコマンド例もあります。

#### マイグレーションファイルを作成
``` sh
python manage.py makemigrations
```

#### マイグレーションファイルをデータベースに適用
``` sh
python manage.py migrate
```

#### マイグレーションの一覧を表示（アプリ・名前順）
``` sh
python manage.py showmigrations
```

## DB
#### DB 起動
``` sh
sqlite3 db.sqlite3
```
> [!CAUTION]
> リリース時 DB ファイル名は変更します。