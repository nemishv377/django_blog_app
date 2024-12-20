from django.urls import include, path 
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter() 

router.register(r'blog/bloggers', AuthorsViewSet) 
router.register(r'blog/blogs', BlogsViewSet) 
  
# specify URL Path for rest_framework 
urlpatterns = [ 
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('accounts/profile/', profile),
    # path('accounts/register/', register),
    path('accounts/register/', RegisterView.as_view()),
    path('accounts/signup/', signup),
    path('blog/blogger/<int:id>/', delete_author),
    path('blog/blogger/<int:id>/edit/', edit_author),
    path('blog/new/', new_blog),
    path('blog/<int:id>/edit/', edit_blog),
    path('blog/<int:id>/create/', create_comment),
    path('accounts/login/', MyTokenObtainPairView.as_view()),
    path('accounts/token/refresh/', TokenRefreshView.as_view()),
    path('accounts/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]