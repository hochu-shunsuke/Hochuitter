from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Follow, Profile
from .forms import ProfileSettingsForm

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
