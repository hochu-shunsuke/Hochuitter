from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('stats/<str:username>/', views.get_follow_stats, name='follow_stats'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
