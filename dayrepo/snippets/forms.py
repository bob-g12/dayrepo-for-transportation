from django import forms
from .models import Snippet, Car
from django.core.exceptions import NON_FIELD_ERRORS


class CustomSnippetModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.vehicle_number # 表示したいカラム名を return

class SnippetForm(forms.ModelForm):
    car_id = CustomSnippetModelChoiceField(queryset=Car.objects.all(), empty_label="車両番号を選択してください",label="車両番号")
    class Meta:
        #モデルを指定
        model = Snippet
        
        #フォームとして表示したいカラムを指定
        fields = (
            'account_id',
            'car_id',
            'duties_trouble_id',
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