from django import forms
from .models import Profile

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['like_emoji', 'comment_emoji', 'bookmark_emoji', 'theme']
        widgets = {
            'like_emoji': forms.TextInput(attrs={
                'maxlength': 1,
                'class': 'emoji-input',
                'placeholder': '絵文字を入力',
                'style': 'height: 3rem;'
            }),
            'comment_emoji': forms.TextInput(attrs={
                'maxlength': 1,
                'class': 'emoji-input',
                'placeholder': '絵文字を入力',
                'style': 'height: 3rem;'
            }),
            'bookmark_emoji': forms.TextInput(attrs={
                'maxlength': 1,
                'class': 'emoji-input',
                'placeholder': '絵文字を入力',
                'style': 'height: 3rem;'
            }),
            'theme': forms.Select(attrs={
                'class': 'theme-select',
                'style': 'height: 3rem;'
            })
        }
        labels = {
            'like_emoji': 'いいねの絵文字',
            'comment_emoji': 'コメントの絵文字',
            'bookmark_emoji': 'ブックマークの絵文字',
            'theme': 'テーマ'
        }
        help_texts = {
            'like_emoji': '1文字の絵文字を入力してください',
            'comment_emoji': '1文字の絵文字を入力してください',
            'bookmark_emoji': '1文字の絵文字を入力してください'
        }
