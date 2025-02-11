from django import forms
from .models import Profile

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['like_emoji', 'comment_emoji', 'bookmark_emoji', 'theme', 'post_vertical_padding', 'post_content_line_height']
        labels = {
            'like_emoji': 'いいねの絵文字',
            'comment_emoji': 'コメントの絵文字',
            'bookmark_emoji': 'ブックマークの絵文字',
            'theme': 'テーマ',
            'post_vertical_padding': '投稿の上下の余白',
            'post_content_line_height': '投稿内容の行間'
        }
        widgets = {
            'like_emoji': forms.TextInput(attrs={
                'class': 'emoji-input',
                'maxlength': '2',
                'placeholder': '❤️'
            }),
            'comment_emoji': forms.TextInput(attrs={
                'class': 'emoji-input',
                'maxlength': '2',
                'placeholder': '💭'
            }),
            'bookmark_emoji': forms.TextInput(attrs={
                'class': 'emoji-input',
                'maxlength': '2',
                'placeholder': '🔖'
            }),
            'theme': forms.Select(attrs={
                'class': 'theme-select'
            }),
            'post_vertical_padding': forms.NumberInput(attrs={
                'class': 'number-input',
                'step': '0.1',
                'min': '0.25',
                'max': '2.0'
            }),
            'post_content_line_height': forms.NumberInput(attrs={
                'class': 'number-input',
                'step': '0.1',
                'min': '1.0',
                'max': '2.0'
            })
        }
        help_texts = {
            'like_emoji': '投稿へのいいねボタンに使用される絵文字',
            'comment_emoji': 'コメントボタンに使用される絵文字',
            'bookmark_emoji': 'ブックマークボタンに使用される絵文字',
            'theme': 'サイト全体の配色テーマ',
            'post_vertical_padding': '投稿の上下の余白をremで指定（0.25～2.0）',
            'post_content_line_height': '投稿内容の行間を指定（1.0～2.0）'
        }
