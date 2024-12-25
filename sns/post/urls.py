from django.urls import path
from .views import index,create_post,create_comment

app_name='post'

urlpatterns=[
    path('',index,name='index'),
    path('create/',create_post,name='create_post'), #投稿作成用のURL
    path('create/comment/<int:post_id>',create_comment,name='create_comment')
]