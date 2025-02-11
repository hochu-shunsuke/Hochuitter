from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Follow, Profile
from .forms import ProfileSettingsForm
from post.models import Comment, Post

def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=target_user)
    
    # フォロワー数とフォロー数を取得
    followers_count = Follow.objects.filter(followed=target_user).count()
    following_count = Follow.objects.filter(follower=target_user).count()
    
    # ログインユーザーがこのユーザーをフォローしているかチェック
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            followed=target_user
        ).exists()
    
    # ユーザーの投稿を取得
    posts = target_user.posts.all()[:50]
    for post in posts:
        post.comments_count = Comment.objects.filter(post=post, parent_comment=None).count()
        if request.user.is_authenticated:
            post.is_bookmarked = post.bookmarked_users.filter(id=request.user.id).exists()
        else:
            post.is_bookmarked = False
    
    return render(request, 'social/profile.html', {
        'target_user': target_user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'posts': posts,
        'username': request.user.username if request.user.is_authenticated else None,
        'viewer_profile': Profile.objects.get_or_create(user=request.user)[0] if request.user.is_authenticated else None
    })

@login_required
def settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('post:index')
    else:
        form = ProfileSettingsForm(instance=profile)
    
    return render(request, 'social/settings.html', {
        'form': form,
        'user_id': request.user.id,
        'username': request.user.username,
        'profile': profile
    })

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    
    # 自分自身をフォローできないようにする
    if request.user == target_user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
        
    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=target_user
    )
    
    if not created:  # すでにフォローしている場合は解除
        follow_obj.delete()
        return JsonResponse({'status': 'unfollowed'})
        
    return JsonResponse({'status': 'followed'})
