from django.urls import path
from .views import create_post, index

app_name='post'

urlpatterns=[
    path('',index,name='index'),
    path('create/',create_post,name='create_post'), #投稿作成用のURL
]