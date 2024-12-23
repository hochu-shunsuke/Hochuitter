from django.shortcuts import render
from .models import Post
from django.urls import reverse_lazy #処理成功後の遷移先urlを引数に持つ,『urlの遅延評価』というらしい．
from django.views.generic import CreateView
from .form import PostForm
from django.contrib.auth.models import User


#url.pyでurl作成したあとで，views.pyに該当の関数を作成しreturn renderでhtmlなり関数の戻り値なりを返すかな

"""
parent_posts:親ポスト
child_posts:返信
nested_replies:返信に対する返信
"""
def index(request):
    #親ポストを全て表示．
    parent_posts=Post.objects.all()[:20] #最大数は開発段階ではとりあえず20
    return render(request,'post/index.html',{'parent_posts':parent_posts}) #key:parent_postに対してvalue:parent_postを持つ辞書を返し，index.htmlにkeyを渡す．

class PostCreateView(CreateView):
    template_name='post/create.html' #TODO:後ほど作成
    form_class=PostForm #Post_create.htmlに渡すモデル．
    success_url=reverse_lazy('post/index.html/<int:user_id>') #成功時にindex.htmlへ移動
    """
    Djangoプロジェクト起動の際にはurls.pyの評価よりもビュークラスの評価が先に行われる。
    reverse_lazyでurlの遅延評価を行わなければurlの解決ができずプロジェクトの起動ができない!!!"""
    def form_valid(self, form):
        form.instance.user=self.request.user # ログイン中のユーザーを設定
        return super().form_valid(form)