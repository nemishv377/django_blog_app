from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blogs_list, name='blogs_list'),
    path('<int:id>/', views.blog_detail, name='blog_detail'),
]
