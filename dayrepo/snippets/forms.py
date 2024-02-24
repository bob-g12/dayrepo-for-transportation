from django import forms
from .models import Snippet
from django.core.exceptions import NON_FIELD_ERRORS



class SnippetForm(forms.ModelForm):
    class Meta:
        #モデルを指定
        model = Snippet
        #フォームとして表示したいカラムを指定
        fields = (
            'account_id',
            'car_id',
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
            'account_id':forms.Select(
                choices=(
                ('','アカウントを選択'),
                ('0','gokki'),
                ('1','やんけ'),
                ('2','とっしー'),
                ),
                attrs={
                'required' : 'アカウントを選択'
            }),
            'account_id':forms.Select(
                choices=(
                ('','車両を選択'),
                ('0','札幌 ひ 20-20'),
                ('1','船橋 ふ 19-19'),
                ('2','八雲 や 89-89'),
                ),
                attrs={
                'required' : '車両を選択'
            }),
        }