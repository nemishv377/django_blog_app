from django.urls import path
from .views import signup
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', signup, name='signup'),
]