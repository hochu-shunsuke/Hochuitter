from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DirectMessage(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:50] + ('...' if len(self.content) > 50 else '')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def cleanup_old_messages(cls):
        # 30日以上前のメッセージを削除（定期実行用）
        cls.objects.filter(
            created_at__lt=timezone.now() - timezone.timedelta(days=30)
        ).delete()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_message = models.ForeignKey(DirectMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_message_conversation')
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Conversation between {", ".join([user.username for user in self.participants.all()])}'
