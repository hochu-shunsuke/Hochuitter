from django.shortcuts import render,redirect
from .models import Post,Comment
from django.urls import reverse_lazy #処理成功後の遷移先urlを引数に持つ,『urlの遅延評価』というらしい．
from .form import PostForm,CommentForm
from django.contrib.auth.decorators import login_required #ログイン状態でない場合はログインページにリダイレクトされる


#url.pyでurl作成したあとで，views.pyに該当の関数を作成しreturn renderでhtmlなり関数の戻り値なりを返すかな

"""
parent_posts:親ポスト
child_posts:返信
nested_replies:返信に対する返信
"""
def index(request):
    #親ポストを全て表示．
    user=request.user #Django標準の認証システムによりログインユーザを取得
    user_id=request.user.id
    parent_posts=Post.objects.all()[:50] #最大数は開発段階ではとりあえず50
    return render(request,'post/index.html',{
        'parent_posts':parent_posts,#key:parent_postに対してvalue:parent_postを持つ辞書を返し，index.htmlにkeyを渡す．
        'username':user.username,
        'user_id':user_id
        })

@login_required #Djangoのデコレータ.ログアウト時はログインページにリダイレクトされる!!!!!
def create_post(request):
    user=request.user
    if request.method=='POST': #HTTPリクエストの種類を確認し適切に処理
        form=PostForm(request.POST)
        if form.is_valid(): #フォームが有効であるか確認
            post=form.save(commit=False) #一時的に保存
            post.user=request.user #現在のユーザ
            post.save() #データベースに保存
            return redirect('post:index') #投稿後にリダイレクト
    else:
        form=PostForm() #GETリクエストの場合は空のフォームを作成
    return render(request,'post/create.html',
                  {'form':form,
                   'user':user,
                   'user_id':user.id} #実際にはcreate.htmlでextendしているbase.htmlの中で使用している
    ) #フォームをテンプレートに渡す

@login_required
def create_comment(request,post_id): #post_idを必ず受け取ることを忘れずに
    user=request.user
    if request.method=='POST': #HTTPリクエストの種類を確認し適切に処理
        form=CommentForm(request.Comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.user=request.user #現在のユーザ
            comment.save()
            return redirect('post:index') #投稿後にリダイレクト
    else:
        form=CommentForm() #GETリクエストの場合は空のフォームを作成
    return render(request,'post/create_comment.html',
                    {'form':form,
                    'user':user,
                    } #o親ポストを表示した上でコメントのフォームをcreate_html（作成済み)に設ける．
    ) #フォームをテンプレートに返す