from django import forms
from .models import Profile

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['like_emoji', 'comment_emoji', 'bookmark_emoji', 'theme', 'post_spacing', 'content_spacing']
        labels = {
            'like_emoji': 'いいねの絵文字',
            'comment_emoji': 'コメントの絵文字',
            'bookmark_emoji': 'ブックマークの絵文字',
            'theme': 'テーマ',
            'post_spacing': '投稿の余白',
            'content_spacing': '投稿内容の行間'
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
            'post_spacing': forms.Select(attrs={
                'class': 'spacing-select'
            }),
            'content_spacing': forms.Select(attrs={
                'class': 'spacing-select'
            })
        }
        help_texts = {
            'like_emoji': '投稿へのいいねボタンに使用される絵文字',
            'comment_emoji': 'コメントボタンに使用される絵文字',
            'bookmark_emoji': 'ブックマークボタンに使用される絵文字',
            'theme': 'サイト全体の配色テーマ',
            'post_spacing': '投稿の余白の大きさを選択',
            'content_spacing': '投稿内容の行間の大きさを選択'
        }
