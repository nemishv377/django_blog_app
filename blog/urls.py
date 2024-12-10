from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blogs_list, name='blogs_list'),
    path('<int:id>/', views.blog_detail, name='blog_detail'),
    path('bloggers/', views.bloggers_list, name='bloggers_list'),
    path('bloggers/<int:id>/', views.blogger_detail, name='blogger_detail'),
    path('new/', views.new_blog, name='new_blog'),
    path('<int:blog_id>/create/', views.create_comment, name='create_comment'),
]
