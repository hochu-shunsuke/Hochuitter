from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Follow

def get_follow_stats(request, username):
    """
    ユーザーのフォロー関連の統計情報を取得するビュー
    """
    user = get_object_or_404(User, username=username)
    
    # フォロワー数を取得
    followers_count = Follow.objects.filter(followed=user).count()
    
    # フォロー中のユーザー数を取得
    following_count = Follow.objects.filter(follower=user).count()
    
    # 相互フォロー（フレンド）数を取得
    friends_count = Follow.objects.filter(
        follower=user,
        ff_is_active=True
    ).count()
    
    stats = {
        'followers_count': followers_count,
        'following_count': following_count,
        'friends_count': friends_count
    }
    
    return JsonResponse(stats)

@login_required
def follow_user(request, username):
    """
    ユーザーをフォローするビュー
    """
    target_user = get_object_or_404(User, username=username)
    
    # 自分自身をフォローできないようにする
    if request.user == target_user:
        return JsonResponse({'error': '自分自身をフォローすることはできません'}, status=400)
    
    # すでにフォローしている場合は解除
    if Follow.objects.filter(follower=request.user, followed=target_user).exists():
        Follow.objects.filter(follower=request.user, followed=target_user).delete()
        return JsonResponse({'status': 'unfollowed'})
    
    # フォローする
    follow = Follow.objects.create(
        follower=request.user,
        followed=target_user
    )
    
    return JsonResponse({'status': 'followed'})
