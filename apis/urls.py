from django.urls import include, path
from . import views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
  path('accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('accounts/signup/', views.signup, name='signup'),
  # Blogger CRUD
  path('blog/bloggers/', views.BloggerViewSet.as_view({'get': 'list'}), name='bloggers-list'),
  path('accounts/register/', views.BloggerViewSet.as_view({'post': 'create'}), name='register'),
  path('blog/blogger/<int:pk>/', views.BloggerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='blogger-detail'),
  path('blog/blogger/<int:pk>/edit/', views.BloggerViewSet.as_view({'put': 'update'}), name='update-blogger'),
  path('blog/blogs/', views.BlogViewSet.as_view({'get': 'list'}), name='blogs-list'),
  path('blog/<int:pk>/', views.BlogViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),
  # Reset Password
  path('accounts/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
  path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
  # OTP verificaton via email
  path('accounts/forgot-password/', views.ForgetPasswordView.as_view(), name='forgot-password'),
  path('accounts/check-otp/', views.CheckOTPView.as_view(), name='check-otp'),
]