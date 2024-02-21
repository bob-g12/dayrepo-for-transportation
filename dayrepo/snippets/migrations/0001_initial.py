# Generated by Django 4.2.2 on 2024-02-21 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='アカウントid')),
                ('last_name', models.CharField(max_length=25, verbose_name='姓')),
                ('first_name', models.CharField(max_length=25, verbose_name='名')),
                ('password', models.CharField(max_length=20, verbose_name='パスワード')),
                ('is_administrator', models.BooleanField(default=False, verbose_name='管理権限')),
                ('is_approval', models.BooleanField(default=False, verbose_name='承認')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': 'アカウント',
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='車両id')),
                ('vehicle_number', models.CharField(max_length=15, verbose_name='車両番号')),
                ('now_mileage', models.IntegerField(verbose_name='走行距離')),
            ],
            options={
                'verbose_name': '車両',
                'db_table': 'cars',
            },
        ),
        migrations.CreateModel(
            name='process',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='工程id')),
                ('start_time', models.TimeField(max_length=10, verbose_name='出発時間')),
                ('end_time', models.TimeField(max_length=10, verbose_name='到着時間')),
                ('start_point', models.CharField(max_length=20, verbose_name='出発地点')),
                ('end_point', models.CharField(max_length=20, verbose_name='到着地点')),
                ('via_point', models.CharField(max_length=20, verbose_name='経由地')),
                ('client', models.CharField(max_length=20, verbose_name='荷主')),
                ('goods', models.CharField(max_length=20, verbose_name='品名')),
                ('is_load_situation', models.IntegerField(verbose_name='積載状況')),
                ('load_mileage', models.IntegerField(blank=True, null=True, verbose_name='積載走行距離')),
                ('load_situation', models.IntegerField(blank=True, null=True, verbose_name='空走行距離')),
            ],
            options={
                'verbose_name': '工程',
                'db_table': 'processsss',
            },
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='日報ID')),
                ('start_mileage', models.IntegerField(verbose_name='出発時メーター')),
                ('end_mileage', models.IntegerField(verbose_name='到着時メーター')),
                ('start_time', models.TimeField(max_length=10, verbose_name='始業時間')),
                ('end_time', models.TimeField(max_length=10, verbose_name='終業時間')),
                ('start_point', models.CharField(max_length=20, verbose_name='出発地点')),
                ('end_point', models.CharField(max_length=20, verbose_name='最終到着地点')),
                ('break_spot', models.CharField(max_length=20, verbose_name='休憩地点')),
                ('weather', models.CharField(max_length=5, verbose_name='天気')),
                ('gasoline_amount', models.FloatField(blank=True, max_length=4, null=True, verbose_name='給油')),
                ('oil', models.FloatField(blank=True, max_length=4, null=True, verbose_name='オイル')),
                ('is_trouble_situation', models.BooleanField(blank=True, default=False, verbose_name='事故/遅延等異常_状況')),
                ('is_trouble_cause', models.BooleanField(blank=True, default=False, verbose_name='事故/遅延等異常_原因')),
                ('is_trouble_support', models.BooleanField(blank=True, default=False, verbose_name='事故/遅延等異常_処置')),
                ('driving_time', models.TimeField(max_length=10, verbose_name='運転時間')),
                ('non_driving_time', models.TimeField(max_length=10, verbose_name='運転以外の業務時間')),
                ('break_time', models.TimeField(max_length=10, verbose_name='休憩時間')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('account_id', models.ForeignKey(default=False, on_delete=django.db.models.deletion.DO_NOTHING, to='snippets.account', verbose_name='アカウントID')),
            ],
            options={
                'verbose_name': '日報',
                'db_table': 'snippets',
            },
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_tire_damage', models.BooleanField(blank=True, default=False, verbose_name='タイヤの損傷(空気圧/摩耗/亀裂/損傷)')),
                ('is_tire_groove', models.BooleanField(blank=True, default=False, verbose_name='タイヤの溝の深さ')),
                ('is_tire_parts', models.BooleanField(blank=True, default=False, verbose_name='タイヤのナット・ボルト(緩み/脱落)')),
                ('is_radiator', models.BooleanField(blank=True, default=False, verbose_name='ラジエータの冷却水(液量)')),
                ('is_brake_oil', models.BooleanField(blank=True, default=False, verbose_name='ブレーキオイル(液量)')),
                ('is_air_tank', models.BooleanField(blank=True, default=False, verbose_name='エアタンク(凝水)')),
                ('is_air_brake', models.BooleanField(blank=True, default=False, verbose_name='エアブレーキ(空気圧/排気音)')),
                ('is_brake_pedal', models.BooleanField(blank=True, default=False, verbose_name='ブレーキペダルの踏みしろ')),
                ('is_parking_brake', models.BooleanField(blank=True, default=False, verbose_name='駐車ブレーキ(かかり具合/引きしろ)')),
                ('is_engine_oil', models.BooleanField(blank=True, default=False, verbose_name='エンジンオイル(液量)')),
                ('is_battery', models.BooleanField(blank=True, default=False, verbose_name='バッテリー(液量)')),
                ('is_belt', models.BooleanField(blank=True, default=False, verbose_name='ファン・ベルトの異常(張り/損傷)')),
                ('is_washer_fluid', models.BooleanField(blank=True, default=False, verbose_name='ウォッシャー液/ワイパー(液量/噴射状態/払拭状態)')),
                ('is_engine', models.BooleanField(blank=True, default=False, verbose_name='エンジン(かかり具合/異音/状態)')),
                ('is_light', models.BooleanField(blank=True, default=False, verbose_name='ライト(ヘッドライト/ウインカー/車内灯/ハザード/速度表示)')),
                ('is_brake_details', models.BooleanField(blank=True, default=False, verbose_name='ブレーキチャンバロッド/ブレーキペダルのライニング')),
                ('is_before_trouble', models.BooleanField(default=False, verbose_name='前日の異常')),
                ('is_today_trouble', models.BooleanField(default=False, verbose_name='本日の異常')),
                ('snippet_id', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='snippets.snippet')),
            ],
            options={
                'verbose_name': '点検項目',
                'db_table': 'checklists',
            },
        ),
    ]
