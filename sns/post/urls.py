from django.urls import path
from post import views
from .views import PostCreateView

app_name='post'

main_urlpatterns=[
    path('',views.index,name='index'),
    #nameを用いるとurlが変更されても動的にnameの値で対応できる!!
    path('create/<int:user_id>',PostCreateView.as_view(),name='post_create'),
]

api_urlpatterns=[
    #APIって何に使う？システム構成ちゃんと考えてから作成しよう
]

urlpatterns=main_urlpatterns+api_urlpatterns