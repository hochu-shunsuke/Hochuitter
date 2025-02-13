from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:user_id>/', views.conversation_detail, name='conversation_detail'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
]
