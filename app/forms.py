from django import forms
from .models import Schedule


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_date', 'end_date', 'start_time', 'end_time')

        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'readonly': 'readonly',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # start_dateをreadonlyに設定して変更不可にする
        if self.instance and self.instance.start_date:
            self.fields['start_date'].widget.attrs['readonly'] = 'readonly'
            self.fields['start_date'].widget.attrs['class'] = 'form-control'
            self.fields['start_date'].disabled = True  # disabledでフォーム送信時に値を送信しないようにする

    # 各フィールドに対してのバリデーション確認
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # どれかの日時が未入力の場合
        if None in (start_date, end_date, start_time, end_time):
            raise forms.ValidationError('すべての日時を入力してください。')

        # 終了日より開始日の方が後の日付に設定されていた場合
        if end_date < start_date:
            self.add_error('end_date','終了日が開始日より前に設定されています')
        
        if start_date == end_date:
            # 終了時間と開始時間が同じまたは、開始時間のほうが後に設定されている場合
            if end_time <= start_time:
                self.add_error('end_time', '終了時間が開始時間よりも前に設定されています')
        
        return cleaned_data



class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('summary', 'date',)
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.HiddenInput,
        }
