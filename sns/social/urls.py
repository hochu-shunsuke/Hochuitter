from django.urls import path
from social import views

app_name='social'

"""
sns/urls.pyにて
path('social/',include('social.urls'))
と設定したため,socialアプリのurlの先頭には social/ がつくよ!!!
"""
main_urlpatterns=[
    path('userpage/<int:user_id>/',views.userpage,name='userpage')
    #nameを用いるとurlが変更されても動的にnameの値で対応できる!!
]

api_urlpatterns=[
    #APIって何に使う？システム構成ちゃんと考えてから作成しよう
]

urlpatterns=main_urlpatterns+api_urlpatterns
