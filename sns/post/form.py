from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm): #ModelFormは元のモデルを再利用してどのカラムをフォーム値として定義するかを定義．Formモデルを作成するよりコード量が減る!
    class Meta:
        model=Post #Postモデルを参照し，この中で何をフォームに使用するか以降で決定
        user=User
        fields=('content',)
        #content以外に作成時必要なidはUserから取れるし,post_dateは作成時auto_now_addだしいらないかな．
        #使用しないカラムの方が少ない時は，exclude=('')と書いていくとfieldsの逆に参照されないカラムを設定可能らしい
        