from django.contrib import admin
from .models import Post, Comment

# Postモデル用のAdminクラス
class PostAdmin(admin.ModelAdmin):
    # 管理画面の一覧で表示するフィールドを指定
    list_display = (
        'content',          # 投稿内容
        'like_count',       # いいね数
        'comment_count',    # 返信数
        'post_date',        # 投稿日時
        'user',             # 投稿者
    )
    
    # 検索機能を追加（投稿内容と投稿者のユーザー名で検索可能）
    search_fields = ('content', 'user__username')
    
    # フィルター機能を追加（いいね数、投稿日時、投稿者でフィルタリング可能）
    list_filter = ('like_count', 'post_date', 'user')
    
    # 日付階層ナビゲーションを追加（投稿日時で階層的に絞り込み可能）
    date_hierarchy = 'post_date'
    
    # 詳細ページで編集可能な関連オブジェクトをインライン表示
    filter_horizontal = ('liked_users', 'bookmarked_users')  # いいね・ブックマークしたユーザの選択を分かりやすく

# Commentモデル用のAdminクラス
class CommentAdmin(admin.ModelAdmin):
    # 管理画面の一覧で表示するフィールドを指定
    list_display = (
        'content',          # コメント内容
        'like_count',       # いいね数
        'comment_count',    # 返信数
        'post_date',        # 投稿日時
        'user',             # 投稿者
        'post',             # 親となるPost
        'parent_comment',   # 親となるComment（返信の場合）
    )
    
    # 検索機能を追加（コメント内容、投稿者、親Postで検索可能）
    search_fields = ('content', 'user__username', 'post__content')
    
    # フィルター機能を追加（いいね数、投稿日時、投稿者、親Postでフィルタリング可能）
    list_filter = ('like_count', 'post_date', 'user', 'post')
    
    # 日付階層ナビゲーションを追加（投稿日時で階層的に絞り込み可能）
    date_hierarchy = 'post_date'
    
    # 詳細ページで編集可能な関連オブジェクトをインライン表示
    filter_horizontal = ('liked_users',)  # いいねしたユーザの選択を分かりやすく

# 管理サイトにモデルを登録
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)