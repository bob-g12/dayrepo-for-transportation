from django import forms
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process
from django.core.exceptions import NON_FIELD_ERRORS


class CustomChecklistCarsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):  # label_from_instance 関数をオーバーライド
        return obj.place_name +" "+ str(obj.class_number) +" "+ obj.kana +" "+ str(obj.serial_number) # 表示したいカラム名を return
class CustomChecklistAccountsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + " " + obj.first_name
    
class SnippetForm(forms.ModelForm):
    class Meta:
        # モデルを指定
        model = Snippet

        # フォームとして表示したいカラムを指定
        fields = (
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
        queryset=Car.objects.all().filter(is_display_check=True),
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
            "working_day",
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

class CarForm(forms.ModelForm):
    class Meta:
        model = Car

        fields = (
            'place_name',
            'class_number',
            'kana',
            'serial_number',
            'now_mileage',
        )