from django import forms
from .models import Snippet, Car
from django.core.exceptions import NON_FIELD_ERRORS


class CustomSnippetModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj): # label_from_instance 関数をオーバーライド
         return obj.vehicle_number # 表示したいカラム名を return

class SnippetForm(forms.ModelForm):
    car_id = CustomSnippetModelChoiceField(queryset=Car.objects.all())
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
        widgets = {
            # 'account_id':forms.Select(
            #     choices=(
            #     ('','アカウントを選択'),
            #     ('0','gokki'),
            #     ('1','やんけ'),
            #     ('2','とっしー'),
            #     ),
            #     attrs={
            #     'required' : 'アカウントを選択'
            # }),
            # 'account_id':forms.Select(
            #     choices=(
            #     ('','車両を選択'),
            #     ('札幌 ひ 20-20','0'),
            #     ('1','船橋 ふ 19-19'),
            #     ('2','八雲 や 89-89'),
            #     ),
            #     attrs={
            #     'required' : '車両を選択'
            # }),
        }