from django.urls import include, path
from rest_framework import routers, status
from . import views
from rest_framework.views import APIView
from rest_framework.response import Response


router = routers.DefaultRouter()
router.register(r'blog/bloggers', views.BloggerViewSet, basename='bloggers')

urlpatterns = [
  path('', include(router.urls)),
  path('blog/blogger/<int:pk>/', views.BloggerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='blogger-detail'),
  path('accounts/', include('rest_framework.urls')),
]