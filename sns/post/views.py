from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.urls import reverse_lazy, reverse
from .form import PostForm, CommentForm
from django.contrib.auth.models import User
from social.models import Follow, Profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    # ログインユーザーの情報を取得
    current_user = request.user
    current_user_id = current_user.id if current_user.is_authenticated else None
    
    # 通常のインデックスページの場合は全投稿を表示
    posts = Post.objects.all()[:50]
    page_title = "投稿一覧"

    # 各投稿のコメント数とブックマーク状態を計算
    for post in posts:
        post.comments_count = Comment.objects.filter(post=post, parent_comment=None).count()
        if current_user.is_authenticated:
            post.is_bookmarked = post.bookmarked_users.filter(id=current_user.id).exists()
        else:
            post.is_bookmarked = False

    # ユーザープロフィールの取得
    profile = None
    if current_user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=current_user)

    context = {
        'username': current_user.username if current_user.is_authenticated else None,
        'posts': posts,
        'user_id': current_user_id,
        'page_title': page_title,
        'profile': profile
    }

    return render(request, 'post/index.html', context)

@login_required
def create_post(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)[0]
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post:index')
    else:
        form = PostForm()
    
    return render(request, 'post/create.html', {
        'form': form,
        'user': user,
        'user_id': user.id,
        'username': user.username,
        'profile': profile
    })

@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.liked_users.all():
        post.liked_users.remove(request.user)
        post.like_count -= 1
        is_liked = False
    else:
        post.liked_users.add(request.user)
        post.like_count += 1
        is_liked = True
    post.save()
    return JsonResponse({'like_count': post.like_count, 'is_liked': is_liked})

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

@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.bookmarked_users.all():
        post.bookmarked_users.remove(request.user)
        is_bookmarked = False
    else:
        post.bookmarked_users.add(request.user)
        is_bookmarked = True
    post.save()
    return JsonResponse({'is_bookmarked': is_bookmarked})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, parent_comment=None)
    comment_form = CommentForm()
    profile = None
    
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        post.is_bookmarked = post.bookmarked_users.filter(id=request.user.id).exists()
    else:
        post.is_bookmarked = False

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
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
        'profile': profile
    })
