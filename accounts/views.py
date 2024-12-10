from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorSignupForm
from django.contrib.auth import login, logout
from blog.models import Blog
from .models import Author
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def custom_login_view(request):

  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
      user = form.get_user()
      login(request, user)
      messages.success(request, 'You have successfully logged in!')
      return redirect('home') 

  else:
    form = AuthenticationForm()

  return render(request, 'registration/login.html', {'form': form})


def signup(request):
  
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    form = AuthorSignupForm(request.POST)
  
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, 'You have successfully signed up and are now logged in!')
      return redirect('home')

  else:
    form = AuthorSignupForm()

  return render(request, 'accounts/signup.html', {'form': form})


def custom_logout_view(request):
  logout(request)
  messages.info(request, 'You have successfully logged out.')
  return redirect('login')


@login_required
def profile(request):
  author = request.user
  blogs = Blog.objects.filter(author=author).order_by('-created_at')

  return render(request, 'accounts/my_profile.html', {'author': author, 'blogs': blogs})