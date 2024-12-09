from django.urls import path
from .views import signup, profile
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile')
]