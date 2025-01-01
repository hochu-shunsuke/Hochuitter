from django.urls import path
from .views import create_post, index ,toggle_like

app_name='post'

urlpatterns=[
    path('',index,name='index'),
    path('create/',create_post,name='create_post'), #投稿作成用のURL
    path('<int:post_id>/toggle/like/',toggle_like,name='toggle_like'), #いいね切り替え用のURL
]