from django import forms
from .models import Snippet, Car, Account, DutiesTrouble, Process
from django.core.exceptions import NON_FIELD_ERRORS


class CustomSnippet_carsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
        return obj.vehicle_number # 表示したいカラム名を return
class CustomSnippet_accountsModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
        return obj.last_name +" "+ obj.first_name # 表示したいカラム名を return

class SnippetForm(forms.ModelForm):
    car_id = CustomSnippet_carsModelChoiceField(queryset=Car.objects.all(), empty_label="車両番号を選択してください", label="車両番号")
    account_id = CustomSnippet_accountsModelChoiceField(queryset=Account.objects.all(), empty_label="運転者を選択してください",label="運転者")
    class Meta:
        #モデルを指定
        model = Snippet
        
        #フォームとして表示したいカラムを指定
        fields = (
            'account_id',
            'car_id',
            'dutiestrouble_id',
            'create_day',
            'start_mileage',
            'end_mileage',
            'start_time',
            'end_time',
            'start_point',
            'end_point',
            'break_spot',
            'weather',
            'gasoline_amount',
            'oil',
            'driving_time',
            'non_driving_time',
            'break_time',
            'free_space',
            )
        widgets = {}

class DutiesTroubleForm(forms.ModelForm):
    class Meta:
        #モデルを指定
        model = DutiesTrouble

        fields = (
            'trouble_situation',
            'trouble_cause',
            'trouble_support',
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
            'load_situation',
        )