from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Thread(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        related_name='threads',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

class Post(models.Model):
    content = models.CharField(max_length=280)  # 投稿内容
    like_count = models.PositiveIntegerField(default=0)  # いいね数
    comment_count = models.PositiveIntegerField(default=0)  # 返信数(階層が1つ下の返信のみをカウント)
    post_date = models.DateTimeField(auto_now_add=True)  # 投稿日時
    user = models.ForeignKey(
        User,  # 一人のユーザが複数のpostを持つため，ForeignKeyを使用
        related_name='posts',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        Thread,
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    liked_users = models.ManyToManyField(
        User,
        related_name='liked_post',
        blank=True
    )  # いいねしたユーザ
    bookmarked_users = models.ManyToManyField(
        User,
        related_name='bookmarked_posts',
        blank=True
    )  # ブックマークしたユーザ
    
    def __str__(self):
        return self.content
            
    class Meta:
        ordering = ['-post_date']  # postを投稿順に並び替え
        indexes = [
            models.Index(fields=['like_count']),
            models.Index(fields=['post_date']),
        ]

class Comment(models.Model):
    content = models.CharField(max_length=280)
    like_count = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )  # いいねしたユーザ
    comment_count = models.PositiveIntegerField(default=0)  # 返信数(階層が1つ下の返信のみをカウント)
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    parent_comment = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.content if self.content else "No content"
    
    class Meta:
        ordering = ['-like_count', '-post_date']
        indexes = [
            models.Index(fields=['like_count']),
            models.Index(fields=['post_date']),
        ]
