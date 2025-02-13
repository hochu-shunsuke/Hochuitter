from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import DirectMessage, Conversation
from django.utils import timezone

def conversation_list(request):
    if not request.user.is_authenticated:
        return render(request, 'message/conversation_list.html', {
            'user': request.user,
            'user_id': None,
            'profile': None
        })

    profile = request.user.profile
    conversations = request.user.conversations.all().order_by('-last_message__created_at')
    conversation_data = []
    
    for conversation in conversations:
        other_user = conversation.participants.exclude(id=request.user.id).first()
        if other_user:
            conversation_data.append({
                'conversation': conversation,
                'other_user': other_user
            })
    
    return render(request, 'message/conversation_list.html', {
        'user': request.user,
        'user_id': request.user.id,
        'profile': profile,
        'viewer_profile': profile,  # ダークモード対応用
        'conversation_data': sorted(conversation_data, key=lambda x: x['conversation'].last_message.created_at if x['conversation'].last_message else x['conversation'].updated_at, reverse=True)
    })

def conversation_detail(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    other_user = get_object_or_404(User, id=user_id)
    
    # 会話を取得または作成
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
    
    # メッセージを取得（30日以内のもののみ）
    messages = DirectMessage.objects.filter(
        Q(from_user=request.user, to_user=other_user) |
        Q(from_user=other_user, to_user=request.user),
        created_at__gte=timezone.now() - timezone.timedelta(days=30)
    ).order_by('created_at')
    
    return render(request, 'message/conversation_detail.html', {
        'user': request.user,
        'user_id': request.user.id,
        'profile': request.user.profile,
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
        'viewer_profile': request.user.profile  # ダークモード対応用
    })

@login_required
def send_message(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    content = request.POST.get('content', '').strip()
    
    # メッセージを作成
    message = DirectMessage.objects.create(
        from_user=request.user,
        to_user=to_user,
        content=content
    )
    
    # 会話を更新
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=to_user).first()
    if conversation:
        conversation.last_message = message
        conversation.save()
    
    return JsonResponse({
        'message': {
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%i')
        }
    })
