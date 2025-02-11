from django.contrib import admin
from .models import Profile, Follow

# Profileモデル用のAdminクラス
class ProfileAdmin(admin.ModelAdmin):
    # 管理画面の一覧で表示するフィールドを指定
    list_display = (
        'user',             # ユーザー名（Profileに関連付けられたUser）
        'date_joined',      # 登録日時
        'bio',              # プロフィール文
        'icon_picture',     # アイコン画像
        'like_emoji',       # いいねの絵文字
        'comment_emoji',    # コメントの絵文字
        'bookmark_emoji',   # ブックマークの絵文字
        'theme',            # テーマ（ライトモード/ダークモード）
    )
    
    # 検索機能を追加（ユーザー名とプロフィール文で検索可能）
    search_fields = ('user__username', 'bio')
    
    # フィルター機能を追加（テーマや登録日時でフィルタリング可能）
    list_filter = ('theme', 'date_joined')
    
    # 日付階層ナビゲーションを追加（登録日時で階層的に絞り込み可能）
    date_hierarchy = 'date_joined'
    
    # 詳細ページで編集可能なフィールドを指定
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'date_joined', 'bio', 'icon_picture'),
        }),
        ('UI設定', {
            'fields': ('like_emoji', 'comment_emoji', 'bookmark_emoji', 'theme'),
        }),
    )

# Followモデル用のAdminクラス
class FollowAdmin(admin.ModelAdmin):
    # 管理画面の一覧で表示するフィールドを指定
    list_display = (
        'follower',         # フォロワー（フォローしている側）
        'followed',         # フォローされている側
        'ff_date',          # 相互フォローが完了した日
        'ff_is_active',     # 相互フォロー状態かどうか
    )
    
    # 検索機能を追加（フォロワーとフォローされている側のユーザー名で検索可能）
    search_fields = ('follower__username', 'followed__username')
    
    # フィルター機能を追加（相互フォロー状態や日付でフィルタリング可能）
    list_filter = ('ff_is_active', 'ff_date')
    
    # 日付階層ナビゲーションを追加（相互フォローが完了した日で階層的に絞り込み可能）
    date_hierarchy = 'ff_date'
    
    # 詳細ページで編集可能なフィールドを指定
    fieldsets = (
        ('フォローデータ', {
            'fields': ('follower', 'followed'),
        }),
        ('相互フォロー情報', {
            'fields': ('ff_date', 'ff_is_active'),
        }),
    )

# 管理サイトにモデルを登録
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)