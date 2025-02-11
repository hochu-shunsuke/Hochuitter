from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    create_post, index, toggle_like, toggle_comment_like, 
    post_detail, toggle_bookmark, bookmarks,
    threads, create_thread, thread_detail
)

app_name = 'post'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_post, name='create_post'),  # 投稿作成用のURL
    path('<int:post_id>/toggle/like/', toggle_like, name='toggle_like'),  # いいね切り替え用のURL
    path('comment/<int:comment_id>/toggle/like/', toggle_comment_like, name='toggle_comment_like'),  # コメントのいいね切り替え用のURL
    path('<int:post_id>/', post_detail, name='post_detail'),  # 投稿詳細表示用のURL（コメント作成も含む）
    path('<int:post_id>/toggle/bookmark/', toggle_bookmark, name='toggle_bookmark'),  # ブックマーク切り替え用のURL
    path('bookmarks/', login_required(bookmarks), name='bookmarks'),  # ブックマーク一覧表示用のURL
    
    # スレッド関連のURL
    path('threads/', login_required(threads), name='threads'),  # スレッド一覧
    path('threads/create/', login_required(create_thread), name='create_thread'),  # スレッド作成
    path('threads/<int:thread_id>/', login_required(thread_detail), name='thread_detail'),  # スレッド詳細
]
