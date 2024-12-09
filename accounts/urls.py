from django.urls import path
from .views import signup, my_profile
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('my_profile', my_profile, name='my_profile')
]