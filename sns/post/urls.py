from django.urls import path
from post import views

app_name='post'

main_urlpatterns=[
    path('',views.index,name='index')
    #nameを用いるとurlが変更されても動的にnameの値で対応できる!!
]

api_urlpatterns=[
    #APIって何に使う？システム構成ちゃんと考えてから作成しよう
]

urlpatterns=main_urlpatterns+api_urlpatterns