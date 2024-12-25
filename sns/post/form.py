from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post #使用するモデル
        fields=['content'] #フォームに含めるフィールド
        #'content'フィールドのみを使用するため、他のフィールドは除外

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment #使用するモデル
        fields=['content'] #フォームに含めるフィールド
