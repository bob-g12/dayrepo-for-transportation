from django import forms
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process
from django.core.exceptions import NON_FIELD_ERRORS


class CustomChecklistCarsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):  # label_from_instance 関数をオーバーライド
        return obj.vehicle_number  # 表示したいカラム名を return
class CustomChecklistAccountsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + " " + obj.first_name

class CustomSnippetChecklistsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # checklistテーブルから稼働日と、FK先から苗字、名前、車両番号を取得して選択肢に表示
            # 参照テーブルのFK先から同じデータ帯のカラム情報を取得する方法
            # 直下の参照元テーブル(obj).外部キーカラム(account_id).欲しいカラム(first_name)
        return str(obj.create_day) + " " + obj.account_id.first_name + " " + obj.account_id.last_name + " " + obj.car_id.vehicle_number
    
class SnippetForm(forms.ModelForm):
    checklist_id = CustomSnippetChecklistsModelChoiceField(
        queryset= Checklist.objects.all().filter(is_snippet_make=0),
        empty_label="今回使用する点検データを選択してください",
        label="点検データ",
    )
    class Meta:
        # モデルを指定
        model = Snippet

        # フォームとして表示したいカラムを指定
        fields = (
            "checklist_id",
            "start_mileage",
            "end_mileage",
            "start_time",
            "end_time",
            "start_point",
            "end_point",
            "break_spot",
            "weather",
            "gasoline_amount",
            "oil",
            "driving_time",
            "non_driving_time",
            "break_time",
            'is_today_trouble',
            "free_space",
        )
        widgets = {}  # 今後のフォーム編集で使用


class DutiesTroubleForm(forms.ModelForm):
    class Meta:
        # モデルを指定
        model = DutiesTrouble

        fields = (
            "trouble_situation",
            "trouble_cause",
            "trouble_support",
        )

class ProcessForm(forms.ModelForm):
    class Meta:
        #モデルを指定
        model = Process

        fields = (
            'start_time',
            'end_time',
            'start_point',
            'end_point',
            'via_point',
            'client',
            'goods',
            'load_situation',
            'is_load_situation',
            'load_mileage',
            'hollow_mileage',
        )

class ChecklistForm(forms.ModelForm):
    car_id = CustomChecklistCarsModelChoiceField(
        queryset=Car.objects.all(),
        empty_label="車両番号を選択してください",
        label="車両番号",
    )
    account_id = CustomChecklistAccountsModelChoiceField(
        queryset=Account.objects.all(),
        empty_label="運転者を選択してください",
        label="運転者",
    )
    class Meta:
        #モデルを指定
        model = Checklist

        fields = (
            "account_id",
            "car_id",
            "create_day",
            'is_tire_damage',
            'is_tire_groove',
            'is_tire_parts',
            'is_radiator',
            'is_brake_oil',
            'is_air_tank',
            'is_air_brake',
            'is_brake_pedal',
            'is_parking_brake',
            'is_engine_oil',
            'is_battery',
            'is_belt',
            'is_washer_fluid',
            'is_engine',
            'is_light',
            'is_brake_details',
            'is_before_trouble',
        )