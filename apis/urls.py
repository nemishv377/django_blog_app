from django.urls import include, path
from rest_framework import routers, status
from . import views
from rest_framework.views import APIView
from rest_framework.response import Response


router = routers.DefaultRouter()
router.register(r'blog/bloggers', views.BloggerViewSet, basename='bloggers')
router.register(r'blog/blogs', views.BlogViewSet, basename='blogs') 

urlpatterns = [
  path('', include(router.urls)),
  path('accounts/signup/', views.signup, name='signup'),
  path('accounts/', include('rest_framework.urls')),
  path('blog/blogger/<int:pk>/', views.BloggerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='blogger-detail'),
  path('blog/<int:pk>/', views.BlogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='blog-detail'),
]