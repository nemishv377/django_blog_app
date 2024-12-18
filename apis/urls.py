from django.urls import include, path 
from rest_framework import routers
  
from .views import *

router = routers.DefaultRouter() 

router.register(r'blog/bloggers', AuthorsViewSet) 
router.register(r'blog/blogs', BlogsViewSet) 
  
# specify URL Path for rest_framework 
urlpatterns = [ 
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')) 
]