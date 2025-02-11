from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('settings/', views.settings, name='settings'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
