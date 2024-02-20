from django.db import models


# Create your models here.
class Account(models.Model):

    class Meta(object):

        # 作成されるテーブル名を指定
        db_table = "accounts"
        # 管理画面でのモデルの名称
        verbose_name = "アカウント"

    # 項目作成

    id = models.AutoField(
        verbose_name="アカウントID",
        primary_key=True,
        editable=False,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name="姓", max_length=25, blank=False, null=False
    )
    first_name = models.CharField(
        verbose_name="名", max_length=25, blank=False, null=False
    )
    password = models.SlugField(
        verbose_name="パスワード", max_length=20, blank=False, null=False
    )
    is_administrator = models.BooleanField(
        verbose_name="管理権限", default=False, blank=False, null=False
    )
    is_approval = models.BooleanField(
        verbose_name="承認", default=False, blank=False, null=False
    )
    create_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):

        return str(self.id)


class Car(models.Model):

    class Meta(object):

        # 作成されるテーブル名を指定
        db_table = "cars"
        # 管理画面でのモデルの名称
        verbose_name = "車両"

    # 項目作成

    id = models.AutoField(
        verbose_name="車両ID", primary_key=True, editable=False, blank=False, null=False
    )
    vehicle_number = models.CharField(
        verbose_name="車両番号", max_length=15, blank=False, null=False
    )
    now_mileage = models.IntegerField(verbose_name="走行距離", blank=False, null=False)

    def __str__(self):

        return str(self.id)


class Checklist(models.Model):

    class Meta(object):

        # 作成されるテーブル名を指定
        db_table = "checklists"
        # 管理画面でのモデルの名称
        verbose_name = "点検項目"

    # 項目作成

    # snippet_id = models.ForeignKey(.id, on_delete=models.CASCADE, null=False)
    is_tire_damage = models.BooleanField(
        verbose_name="タイヤの損傷(空気圧/摩耗/亀裂/損傷)",
        default=False,
        blank=True,
        null=False,
    )
    is_tire_groove = models.BooleanField(
        verbose_name="タイヤの溝の深さ", default=False, blank=True, null=False
    )
    is_tire_parts = models.BooleanField(
        verbose_name="タイヤのナット・ボルト(緩み/脱落)",
        default=False,
        blank=True,
        null=False,
    )
    is_radiator = models.BooleanField(
        verbose_name="ラジエータの冷却水(液量)", default=False, blank=True, null=False
    )
    is_brake_oil = models.BooleanField(
        verbose_name="ブレーキオイル(液量)", default=False, blank=True, null=False
    )
    is_air_tank = models.BooleanField(
        verbose_name="エアタンク(凝水)", default=False, blank=True, null=False
    )
    is_air_brake = models.BooleanField(
        verbose_name="エアブレーキ(空気圧/排気音)",
        default=False,
        blank=True,
        null=False,
    )
    is_brake_pedal = models.BooleanField(
        verbose_name="ブレーキペダルの踏みしろ", default=False, blank=True, null=False
    )
    is_parking_brake = models.BooleanField(
        verbose_name="駐車ブレーキ(かかり具合/引きしろ)",
        default=False,
        blank=True,
        null=False,
    )
    is_engine_oil = models.BooleanField(
        verbose_name="エンジンオイル(液量)", default=False, blank=True, null=False
    )
    is_battery = models.BooleanField(
        verbose_name="バッテリー(液量)", default=False, blank=True, null=False
    )
    is_belt = models.BooleanField(
        verbose_name="ファン・ベルトの異常(張り/損傷)",
        default=False,
        blank=True,
        null=False,
    )
    is_washer_fluid = models.BooleanField(
        verbose_name="ウォッシャー液/ワイパー(液量/噴射状態/払拭状態)",
        default=False,
        blank=True,
        null=False,
    )
    is_engine = models.BooleanField(
        verbose_name="エンジン(かかり具合/異音/状態)",
        default=False,
        blank=True,
        null=False,
    )
    is_light = models.BooleanField(
        verbose_name="ライト(ヘッドライト/ウインカー/車内灯/ハザード/速度表示)",
        default=False,
        blank=True,
        null=False,
    )
    is_brake_details = models.BooleanField(
        verbose_name="ブレーキチャンバロッド/ブレーキペダルのライニング",
        default=False,
        blank=True,
        null=False,
    )
    is_before_trouble = models.BooleanField(
        verbose_name="前日の異常", default=False, blank=False, null=False
    )
    is_today_trouble = models.BooleanField(
        verbose_name="本日の異常", default=False, blank=False, null=False
    )

    def __str__(self):

        return str(self.snippet_id)


class Snippet(models.Model):

    class Meta(object):

        # 作成されるテーブル名を指定
        db_table = "snippets"
        # 管理画面でのモデルの名称
        verbose_name = "日報"

    # 項目作成

    id = models.AutoField(
        verbose_name="日報ID", primary_key=True, editable=False, blank=False, null=False
    )
    # account_id = models.ForeignKey(Account.id,verbose_name='アカウントID', on_delete=models.SET_NULL, null=False)
    # start_mileage = models.ForeignKey(Car.now_mileage,verbose_name='出発時メーター', on_delete=models.SET_NULL, null=False)
    end_mileage = models.IntegerField(
        verbose_name="到着時メーター", blank=False, null=False
    )
    start_time = models.TimeField(
        verbose_name="始業時間", blank=False, null=False, max_length=10
    )
    end_time = models.TimeField(
        verbose_name="終業時間", blank=False, null=False, max_length=10
    )
    start_point = models.CharField(
        verbose_name="出発地点", blank=False, null=False, max_length=10
    )
    end_point = models.CharField(
        verbose_name="最終到着地点", blank=False, null=False, max_length=10
    )
    break_spot = models.CharField(
        verbose_name="休憩地点", blank=False, null=False, max_length=10
    )
    weather = models.CharField(
        verbose_name="天気", max_length=5, blank=False, null=False
    )
    gasoline_amount = models.FloatField(
        verbose_name="給油", max_length=4, blank=True, null=True
    )
    oil = models.FloatField(verbose_name="オイル", max_length=4, blank=True, null=True)
    is_trouble_situation = models.BooleanField(
        verbose_name="事故/遅延等異常_状況", default=False, blank=True, null=False
    )
    is_trouble_cause = models.BooleanField(
        verbose_name="事故/遅延等異常_原因", default=False, blank=True, null=False
    )
    is_trouble_support = models.BooleanField(
        verbose_name="事故/遅延等異常_処置", default=False, blank=True, null=False
    )
    create_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):

        return str(self.id)
