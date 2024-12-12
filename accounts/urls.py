from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('register/', views.register, name='register'),
]