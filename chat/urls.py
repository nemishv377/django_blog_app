from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
  path('', views.index_view, name='chat-index'),
  path('<str:room_name>/', views.room_view, name='chat-room'),
  path('<str:room_name>/join', views.join_room, name='join-chat-room'),
  path('<str:room_name>/leave', views.leave_room, name='leave-chat-room'),
]