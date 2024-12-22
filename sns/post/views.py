from django.shortcuts import render
from .models import Post
#url.pyでurl作成したあとで，views.pyに該当の関数を作成しreturn renderでhtmlなり関数の戻り値なりを返すかな

"""
parent_posts:親ポスト
child_posts:返信
nested_replies:返信に対する返信
"""
def index(request):
    #親ポストを全て表示．
    parent_posts=Post.objects.all()
    return render(request,'post/index.html',{'parent_posts':parent_posts}) #key:parent_postに対してvalue:parent_postを持つ辞書を返し，index.htmlにkeyを渡す．
