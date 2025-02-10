from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.urls import reverse_lazy, reverse
from .form import PostForm, CommentForm
from django.contrib.auth.models import User
from social.models import Follow
from django.contrib.auth.decorators import login_required #ログイン状態でない場合はログインページにリダイレクトされる
from django.http import JsonResponse #Ajax用のレスポンス(非同期処理)を返すために必要


#url.pyでurl作成したあとで，views.pyに該当の関数を作成しreturn renderでhtmlなり関数の戻り値なりを返すかな

"""
parent_posts:親ポスト
child_posts:返信
nested_replies:返信に対する返信
"""
def index(request, user_id=None):
    # ログインユーザーの情報を取得
    current_user = request.user
    current_user_id = current_user.id if current_user.is_authenticated else None
    
    if user_id:
        # ユーザーページの場合は特定ユーザーの投稿のみ表示
        target_user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=target_user)[:50]
        page_title = f"{target_user.username}のページ"
    else:
        # 通常のインデックスページの場合は全投稿を表示
        posts = Post.objects.all()[:50]
        page_title = "投稿一覧"

    # 各投稿のコメント数とフォロー状態を計算
    for post in posts:
        post.comments_count = Comment.objects.filter(post=post, parent_comment=None).count()
        if current_user.is_authenticated and current_user.id != post.user.id:
            post.user.is_followed = Follow.objects.filter(
                follower=current_user,
                followed=post.user
            ).exists()
        else:
            post.user.is_followed = False

    comment_form = CommentForm()

    context = {
        'username': current_user.username if current_user.is_authenticated else None,
        'parent_posts': posts,
        'user_id': current_user_id,
        'page_title': page_title,
        'comment_form': comment_form,
        'is_user_page': bool(user_id)
    }

    # ユーザーページの場合はフォロー状態を追加
    if user_id and current_user.is_authenticated and current_user.id != user_id:
        context['target_user'] = target_user
        context['is_following'] = Follow.objects.filter(
            follower=current_user,
            followed=target_user
        ).exists()
        # フォロワー数とフォロー数を追加
        context['followers_count'] = Follow.objects.filter(followed=target_user).count()
        context['following_count'] = Follow.objects.filter(follower=target_user).count()

    return render(request, 'post/index.html', context)

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
def toggle_like(request,post_id): #ここではユーザ一人単位のいいね数を更新する
    post=Post.objects.get(id=post_id)
    if request.user in post.liked_users.all(): #postのliked_usersリストにある場合
        post.liked_users.remove(request.user) #いいねを削除
        post.like_count-=1 #いいね数を-1
    else:
        post.liked_users.add(request.user) #いいねを追加
        post.like_count+=1
    post.save()
    return JsonResponse({'like_count':post.like_count}) #Ajax用のレスポンスを返す

@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.liked_users.all():
        comment.liked_users.remove(request.user)
        comment.like_count -= 1
    else:
        comment.liked_users.add(request.user)
        comment.like_count += 1
    comment.save()
    return JsonResponse({'like_count': comment.like_count})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, parent_comment=None)
    comment_form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            # 投稿のコメント数を更新
            post.comment_count = Comment.objects.filter(post=post, parent_comment=None).count()
            post.save()
            
            return redirect('post:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'username': request.user.username if request.user.is_authenticated else None,
    })
